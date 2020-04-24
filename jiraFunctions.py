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
            block_size = 100
            block_num = 0
            totalIssues = 0
            projectLabels = []
            result = jira.search_issues(jql, startAt=block_num*block_size, maxResults=block_size,
                                        fields="project, issuetype, created, resolutiondate, reporter, assignee, status")

            while bool(result):
                for issue in result:
                    totalIssues += 1
                    print(issue.fields.project)
                    # projectLabels = list(set(issue.fields.project))
                    # print(projectLabels)
                block_num += 1
                time.sleep(5)
                result = jira.search_issues(jql, startAt=block_num*block_size, maxResults=block_size,
                                        fields="project, issuetype, created, resolutiondate, reporter, assignee, status")
            jira.close()
        except (AttributeError):
            jira.close()



Issues.totalIssues()