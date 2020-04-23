import requests
from jira import JIRA
from variables import *
from secrets import *

def getIssues():
    jira = JIRA(
        basic_auth=(user, apikey), 
        options={
            'server': instance
        }
    )

    totalIssues = len(jira.search_issues('project=' + project))
    print(totalIssues)
    return totalIssues
getIssues()