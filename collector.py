from prometheus_client.core import GaugeMetricFamily, REGISTRY, CounterMetricFamily
from prometheus_client import start_http_server
from jira import JIRA, JIRAError
from config import *
import time

jira = JIRA(basic_auth=(user, apikey), options={"server": instance})


class IssueCollector:

    block_num = 0
    promOutput = {}

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

            promLabels = []
            result = IssueCollector.search(jql)

            # Loop over the JQL results
            while bool(result):

                for issue in result:

                    # Assign Jira attributes to variables
                    project = str(issue.fields.project)
                    assignee = str(issue.fields.assignee)
                    issueType = str(issue.fields.issuetype)
                    status = str(issue.fields.status)
                    resolution = str(issue.fields.resolution)
                    reporter = str(issue.fields.reporter)
                    components = issue.fields.components
                    labels = issue.fields.labels

                    # Construct the list of labels from attributes
                    promLabel = [
                        project,
                        assignee,
                        issueType,
                        status,
                        resolution,
                        reporter,
                    ]

                    if components:
                        for component in components:
                            promLabel.append(str(component))
                    else:
                        promLabel.append("None")
                    if labels:
                        for label in labels:
                            promLabel.append(str(label))
                    else:
                        promLabel.append("None")
                    promLabels.append(promLabel)
                # Increment the results via pagination
                self.block_num += 1
                time.sleep(2)
                result = IssueCollector.search(jql)
            jira.close()

            # Convert nested lists into a list of tuples, so that we may hash and count duplicates
            for l in promLabels:
                self.promOutput.setdefault(tuple(l), list()).append(1)
            for k, v in self.promOutput.items():
                self.promOutput[k] = sum(v)
            return self.promOutput
        except (JIRAError, AttributeError):

            jira.close()

    def collect(self):

        # Set up the Issues Prometheus gauge
        issuesGauge = GaugeMetricFamily(
            "jira_issues",
            "Jira issues",
            labels=[
                "project",
                "assignee",
                "issueType",
                "status",
                "resolution",
                "reporter",
                "component",
                "label",
            ],
        )

        for labels, value in self.promOutput.items():
            issuesGauge.add_metric(labels, value)
        yield issuesGauge


if __name__ == "__main__":

    # Start the webserver, search Jira, and register the issue collector
    start_http_server(8000)
    IssueCollector.construct(str(jql))
    REGISTRY.register(IssueCollector())
    while True:
        time.sleep(int(interval))
