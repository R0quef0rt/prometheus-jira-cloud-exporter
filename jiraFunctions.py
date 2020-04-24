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
            result = jira.search_issues(jql, startAt=block_num*block_size, maxResults=block_size, 
                                        fields="issuetype, created, resolutiondate, reporter, assignee, status")

            while bool(result):
                for issue in result:
                    issue_key = issue.key
                    print(issue_key)
                    # issue.fields.status.name

                block_num = block_num + 1
                time.sleep(5)
                result = jira.search_issues(jql, startAt=block_num*block_size, maxResults=block_size, 
                                        fields="issuetype, created, resolutiondate, reporter, assignee, status")
            jira.close()
        except (AttributeError):
            jira.close()



Issues.totalIssues()