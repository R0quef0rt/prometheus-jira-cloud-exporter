# prometheus-jira-cloud-exporter
## Overview
---
While there already exist Prometheus exporter plugins for Jira Server, it is not possible to use these plugins on Jira Cloud.

As such, I have created a simple Python app that uses the [Jira library](https://github.com/pycontribs/jira) to scrape metrics from Jira Cloud's API. It uses the [Prometheus library](https://github.com/prometheus/client_python) to expose them in the correct format:

```
jira_issues{assignee="None",component="None",issueType="Bug",label="None",project="TTT",reporter="John Doe",resolution="Done",status="Done"} 1.0
jira_issues{assignee="None",component="None",issueType="Story",label="None",project="TTT",reporter="John Doe",resolution="None",status="To Do"} 2.0
jira_issues{assignee="None",component="None",issueType="Epic",label="None",project="TTT",reporter="John Doe",resolution="None",status="To Do"} 1.0
jira_issues{assignee="None",component="Active Directory",issueType="Service Request",label="Analytics and Reporting Service",project="TEST",reporter="John Doe",resolution="None",status="Waiting for support"} 1.0
jira_issues{assignee="None",component="None",issueType="Service Request",label="None",project="TEST",reporter="John Doe",resolution="None",status="Waiting for support"} 1.0
jira_issues{assignee="None",component="Active Directory",issueType="Service Request",label="HR Services",project="TEST",reporter="Example Customer",resolution="None",status="Waiting for support"} 1.0
jira_issues{assignee="John Doe",component="Active Directory",issueType="Service Request",label="Analytics and Reporting Service",project="TEST",reporter="Example Customer",resolution="Done",status="Resolved"} 1.0
jira_issues{assignee="John Doe",component="None",issueType="Task",label="None",project="GAR",reporter="John Doe",resolution="None",status="To Do"} 1.0
jira_issues{assignee="None",component="None",issueType="Task",label="None",project="GAR",reporter="John Doe",resolution="None",status="To Do"} 1.0
```

## How to use
---
Using this app is simple:

1. Download this project, and extract it to a folder on your computer
2. In this folder, create a "config.py" file containing the following contents:
```
# The URL of your Jira Cloud instance
instance = 'https://myinstance.atlassian.net'
# The username of the user authentication with Jira's API
user = 'ryanjbrooks11@gmail.com'
# The API key associated with your user
apikey = 'nv7w9fpm2AHUBehGytrrDBD9'
# The JQL query you want to use to search Jira. Leave blank to search all issues.
jql = ''
# The interval (in seconds) to search Jira. Do not set this too low, or there is a chance
# of overloading your instance.
interval = '900'
```
3. To run this in Docker, just run the following:
```
docker-compose up
```
4. Navigate to http://localhost:8000. Your metrics should be clearly exposed.

## Note
---
This probably works with Jira Server, too. This is untested.