from jira import JIRA
from variables import *
from secrets import *
import globals
from globals import *

def totalIssues():

    totalIssues = len(jira.search_issues('project=' + project))
    print(totalIssues)
    return totalIssues