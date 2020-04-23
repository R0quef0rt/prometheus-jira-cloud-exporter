from prometheus_client import start_http_server, Summary, Gauge
import random
import time
import issues
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
    # Set up Jira variables
    issuesGuage = Gauge('total_jira_issues', 'Jira issues')
    # Start up the server to expose the metrics.
    start_http_server(8000)
    # Generate some requests.
    while True:
        # Set up Jira functions
        issuesGuage.set(issues.totalIssues())
        # Wait 
        process_request(60)