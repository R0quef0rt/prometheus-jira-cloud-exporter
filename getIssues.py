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
    # issue = jira.issue('TEST-1')
    # print(issue.fields.project.key)            # 'JRA'
    # print(issue.fields.issuetype.name)         # 'New Feature'
    # print(issue.fields.reporter.displayName)   # 'Mike Cannon-Brookes [Atlassian]'
    # url = instance + path + '?jql=project="' + project + '"'
    # print(url)
    # response = requests.get(instance, auth=(user, apikey))
    # print(response)

getIssues()