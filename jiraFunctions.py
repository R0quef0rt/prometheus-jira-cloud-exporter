from jira import JIRA
from variables import *
from secrets import *
import globals
from globals import *
import time

class Issues:

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
                    promLabel = f"project='{project}', assignee='{assignee}', issueType='{issueType}', status='{status}', resolution='{resolution}', reporter='{reporter}'"

                    if components:
                        for component in components:
                            promLabel += f", component='{component}'"
                    else:
                        promLabel += f", component='None'"

                    if labels:
                        for label in labels:
                            promLabel += f", label='{label}'"
                    else:
                        promLabel += f", label='None'"
                
                    promLabels.append(promLabel)

                block_num += 1
                time.sleep(5)
                result = jira.search_issues(jql, startAt=block_num*block_size, maxResults=block_size,
                                        fields="project, summary, components, labels, status, issuetype, resolution, created, resolutiondate, reporter, assignee, status")

            jira.close()

            return promLabels

        except (AttributeError):

            jira.close()

Issues.search()