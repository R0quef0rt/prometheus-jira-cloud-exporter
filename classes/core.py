from prometheus_client.core import GaugeMetricFamily, CounterMetricFamily, REGISTRY
from prometheus_client import start_http_server
from jira import JIRA, JIRAError
import config
import time

jira = JIRA(basic_auth=(config.user, config.apikey), options={"server": config.instance})


class IssueCollector:

    block_num = 0
    prom_output = {}

    @classmethod
    def search(self, jql):

        # Search Jira API
        block_size = 100
        result = jira.search_issues(
            jql,
            startAt=self.block_num * block_size,
            maxResults=block_size,
            fields="project, summary, components, labels, status, issuetype, resolution, created, resolutiondate, reporter, assignee, status",
        )

        return result

    @classmethod
    def construct(self, jql):

        try:

            prom_labels = []
            result = IssueCollector.search(config.jql)

            # Loop over the JQL results
            while bool(result):

                for issue in result:

                    # Assign Jira attributes to variables
                    project = str(issue.fields.project)
                    assignee = str(issue.fields.assignee)
                    issue_type = str(issue.fields.issuetype)
                    status = str(issue.fields.status)
                    resolution = str(issue.fields.resolution)
                    reporter = str(issue.fields.reporter)
                    components = issue.fields.components
                    labels = issue.fields.labels

                    # Construct the list of labels from attributes
                    prom_label = [
                        project,
                        assignee,
                        issue_type,
                        status,
                        resolution,
                        reporter,
                    ]

                    if components:
                        for component in components:
                            prom_label.append(str(component))
                    else:
                        prom_label.append("None")
                    if labels:
                        for label in labels:
                            prom_label.append(str(label))
                    else:
                        prom_label.append("None")
                    prom_labels.append(prom_label)
                # Increment the results via pagination
                self.block_num += 1
                time.sleep(2)
                result = IssueCollector.search(config.jql)
            jira.close()

            # Convert nested lists into a list of tuples, so that we may hash and count duplicates
            for li in prom_labels:
                self.prom_output.setdefault(tuple(li), list()).append(1)
            for k, v in self.prom_output.items():
                self.prom_output[k] = sum(v)
            return self.prom_output
        except (JIRAError, AttributeError):

            jira.close()

    def collect(self):

        # Set up the Issues Prometheus gauge
        issues_gauge = GaugeMetricFamily(
            "jira_issues",
            "Jira issues",
            labels=[
                "project",
                "assignee",
                "issue_type",
                "status",
                "resolution",
                "reporter",
                "component",
                "label",
            ],
        )

        for labels, value in self.prom_output.items():
            issues_gauge.add_metric(labels, value)
        yield issues_gauge
