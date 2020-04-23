from jira import JIRA
from variables import *
from secrets import *

global jira
jira = JIRA(
    basic_auth=(user, apikey), 
    options={
        'server': instance
    }
)