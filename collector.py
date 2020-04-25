from prometheus_client.core import GaugeMetricFamily, REGISTRY, CounterMetricFamily
from prometheus_client import start_http_server
from jira import JIRA
from variables import *
from secrets import *
import globals
from globals import *
import time

class Issue:

    @staticmethod
    def search():

        try:
            
            jql = ''
            block_size = 100
            block_num = 0
            count = 0
            global promLabels
            promLabels = []
            result = jira.search_issues(jql, startAt=block_num*block_size, maxResults=block_size,
                                        fields="project, summary, components, labels, status, issuetype, resolution, created, resolutiondate, reporter, assignee, status")

            while bool(result):

                for issue in result:
                    count += 1
                    project = str(issue.fields.project)
                    assignee = str(issue.fields.assignee)
                    issueType = str(issue.fields.assignee)
                    status = str(issue.fields.status)
                    resolution = str(issue.fields.resolution)
                    reporter = str(issue.fields.reporter)
                    components = issue.fields.components
                    labels = issue.fields.labels
                    
                    # Construct the PromQL query
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

            return promLabels

        except (AttributeError):

            jira.close()


class IssueCollector(object):
    def __init__(self):
        pass

    def collect(self):
        issuesGauge = GaugeMetricFamily('jira_issues', 'Jira issues', labels=['project', 'assignee', 'issueType', 'status', 'resolution', 'reporter', 'component', 'label'])
        Issue.search()
        for labels in promLabels:
            print(labels)
            issuesGauge.add_metric(labels, 20)
            yield issuesGauge


if __name__ == '__main__':
    start_http_server(8000)
    REGISTRY.register(IssueCollector())
    while True:
        time.sleep(1)