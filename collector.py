from prometheus_client.core import GaugeMetricFamily, REGISTRY, CounterMetricFamily
from prometheus_client import start_http_server
from jira import JIRA, JIRAError
from config import *
import time

jira = JIRA(
    basic_auth=(user, apikey), 
    options={
        'server': instance
    }
)


class IssueCollector:

    @staticmethod
    def search(jql):

        try:
            
            # Set up the JQL query
            block_size = 100
            block_num = 0
            promLabels = []
            result = jira.search_issues(jql, startAt=block_num*block_size, maxResults=block_size,
                                        fields="project, summary, components, labels, status, issuetype, resolution, created, resolutiondate, reporter, assignee, status")

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
                    promLabel = [f'{project}', f'{assignee}', f'{issueType}', f'{status}', f'{resolution}', f'{reporter}']
                    
                    if components:
                        for component in components:
                            promLabel.append(f'{component}')
                    else:
                        promLabel.append(f'None')

                    if labels:
                        for label in labels:
                            promLabel.append(f'{label}')
                    else:
                        promLabel.append(f'None')
                
                    promLabels.append(promLabel)

                # Increment the results via pagination
                block_num += 1
                time.sleep(2)
                result = jira.search_issues(jql, startAt=block_num*block_size, maxResults=block_size,
                                        fields="project, summary, components, labels, status, issuetype, resolution, created, resolutiondate, reporter, assignee, status")
            jira.close()
            
            # Convert nested lists into a list of tuples, so that we may hash and count duplicates
            global promOutput
            promOutput = {}

            for l in promLabels:
                promOutput.setdefault(tuple(l), list()).append(1)
            for k, v in promOutput.items():
                promOutput[k] = sum(v)

            return promOutput

        except (JIRAError, AttributeError):

            jira.close()

    def collect(self):
        
        # Set up the Issues Prometheus gauge
        issuesGauge = GaugeMetricFamily('jira_issues', 'Jira issues', labels=['project', 'assignee', 'issueType', 'status', 'resolution', 'reporter', 'component', 'label'])

        for labels, value in promOutput.items():
            issuesGauge.add_metric(labels, value)
        yield issuesGauge


if __name__ == '__main__':

    # Start the webserver, search Jira, and register the issue collector
    start_http_server(8000)
    IssueCollector.search(str(jql))
    REGISTRY.register(IssueCollector())
    while True:
        time.sleep(int(interval))