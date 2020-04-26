from prometheus_client.core import GaugeMetricFamily, REGISTRY, CounterMetricFamily
from prometheus_client import start_http_server
from jira import JIRA
from variables import *
from secrets import *
import globals
from globals import *
import time

class IssueCollector:

    @staticmethod
    def search(jql):

        try:
            
            block_size = 100
            block_num = 0
            global promLabels
            promLabels = []
            result = jira.search_issues(jql, startAt=block_num*block_size, maxResults=block_size,
                                        fields="project, summary, components, labels, status, issuetype, resolution, created, resolutiondate, reporter, assignee, status")

            while bool(result):

                for issue in result:
                    project = str(issue.fields.project)
                    assignee = str(issue.fields.assignee)
                    issueType = str(issue.fields.issuetype)
                    status = str(issue.fields.status)
                    resolution = str(issue.fields.resolution)
                    reporter = str(issue.fields.reporter)
                    components = issue.fields.components
                    labels = issue.fields.labels
                    
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

                block_num += 1
                time.sleep(5)
                result = jira.search_issues(jql, startAt=block_num*block_size, maxResults=block_size,
                                        fields="project, summary, components, labels, status, issuetype, resolution, created, resolutiondate, reporter, assignee, status")
            jira.close()
            
            global promOutput
            promOutput = {}

            for l in promLabels:
                promOutput.setdefault(tuple(l), list()).append(1)
            for k, v in promOutput.items():
                promOutput[k] = sum(v)

            return promOutput

        except (AttributeError):

            jira.close()

    def collect(self):

        issuesGauge = GaugeMetricFamily('jira_issues', 'Jira issues', labels=['project', 'assignee', 'issueType', 'status', 'resolution', 'reporter', 'component', 'label'])

        for labels, value in promOutput.items():
            issuesGauge.add_metric(labels, value)
        yield issuesGauge


if __name__ == '__main__':

    start_http_server(8000)
    IssueCollector.search(jql)
    REGISTRY.register(IssueCollector())
    while True:
        time.sleep(1)