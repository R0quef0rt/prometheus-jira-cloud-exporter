from jira import JIRA
from variables import *
from secrets import *
import globals
from globals import *
import json
import time

class Issues:

    @staticmethod
    def totalIssues():
        
        try:
            jql = ''
            block_size = 2
            block_num = 0
            totalIssues = 0
            global projectLabels
            projectLabels = []
            result = jira.search_issues(jql, startAt=block_num*block_size, maxResults=block_size,
                                        fields="project, issuetype, created, resolutiondate, reporter, assignee, status")

            while bool(result):
                for issue in result:
                    totalIssues += 1
                    projectLabels.append(str(issue.fields.project))

                block_num += 1
                time.sleep(5)
                result = jira.search_issues(jql, startAt=block_num*block_size, maxResults=block_size,
                                        fields="project, issuetype, created, resolutiondate, reporter, assignee, status")

            # Convert list to a set, then back to a list, in order to obtain unique values                            
            projectLabels = list(set(projectLabels))
            jira.close()

        except (AttributeError):

            jira.close()



Issues.totalIssues()
print(projectLabels)