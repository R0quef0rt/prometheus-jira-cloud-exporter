from prometheus_client import start_http_server, Summary, Gauge, REGISTRY
import random
import time
import jiraFunctions
import globals
from globals import *

# Create a metric to track time spent and requests made.
REQUEST_TIME = Summary('request_processing_seconds', 'Time spent processing request')

# Decorate function with metric.
@REQUEST_TIME.time()
def process_request(t):
    """A dummy function that takes some time."""
    time.sleep(t)

if __name__ == '__main__':
    # Start up the server to expose the metrics.
    start_http_server(8000)
    REGISTRY.register(jiraFunctions.IssueCollector())
    # Generate some requests.
    while True:
        # Set up Jira functions
        # issuesGauge = Gauge('total_jira_issues', 'Jira issues', ['project', 'assignee', 'issueType', 'status', 'resolution', 'reporter', 'component', 'label'])
        # issuesGauge = Gauge('total_jira_issues', 'Jira issues', ['project', 'assignee', 'label'])
        # for promLabel in jiraFunctions.promLabels:
        #     print(promLabel)
            # issuesGauge.set(2.0)
            # issuesGauge.labels(promLabel).set(2.0)
            # issuesGauge.labels(project = '', assignee='', issueType='', status='', resolution='', reporter='', component='', label='').set(2.0)
        # Wait 
        process_request(60)