from prometheus_client.core import GaugeMetricFamily, CounterMetricFamily, REGISTRY
from prometheus_client import start_http_server
from classes.core import IssueCollector
import config
import time

if __name__ == "__main__":

    # Start the webserver, search Jira, and register the issue collector
    start_http_server(8000)
    IssueCollector.construct(str(config.jql))
    REGISTRY.register(IssueCollector())
    while True:
        time.sleep(int(config.interval))