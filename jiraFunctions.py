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
            result = jira.search_issues(jql, startAt=block_num*block_size, maxResults=block_size,
                                        fields="project, summary, components, labels, status, issuetype, resolution, created, resolutiondate, reporter, assignee, status")

            # Set up the variables that store Prometheus labels
            global projects
            projects = []
            global assignees
            assignees = []
            global components
            components = []
            global labels
            labels = []
            global issueTypes
            issueTypes = []
            global statuses
            statuses = []
            global resolutions
            resolutions = []
            global reporters
            reporters = []

            while bool(result):

                for issue in result:
                    totalIssues += 1
                    projects.append(str(issue.fields.project))
                    assignees.append(str(issue.fields.assignee))
                    issueTypes.append(str(issue.fields.issuetype))
                    statuses.append(str(issue.fields.status))
                    resolutions.append(str(issue.fields.resolution))
                    reporters.append(str(issue.fields.reporter))

                    for component in issue.fields.components:
                        components.append(str(component))
                    
                    for label in issue.fields.labels:
                        labels.append(str(label))

                block_num += 1
                time.sleep(5)
                result = jira.search_issues(jql, startAt=block_num*block_size, maxResults=block_size,
                                        fields="project, summary, components, labels, status, issuetype, resolution, created, resolutiondate, reporter, assignee, status")

            # Convert list to a set, then back to a list, in order to obtain unique values                            
            projects = list(set(projects))
            assignees = list(set(assignees))
            components = list(set(components))
            labels = list(set(labels))
            issueTypes = list(set(issueTypes))
            statuses = list(set(statuses))
            resolutions = list(set(resolutions))
            reporters = list(set(reporters))

            jira.close()

        except (AttributeError):

            jira.close()

Issues.totalIssues()
print(projects)
print(assignees)
print(components)
print(labels)
print(issueTypes)
print(statuses)
print(resolutions)
print(reporters)
