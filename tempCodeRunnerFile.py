        jql = ''
        block_size = 2
        block_num = 0
        header = True
        result = jira.search_issues(jql, startAt=block_num*block_size, maxResults=block_size, 
                                    fields="issuetype, created, resolutiondate, reporter, assignee, status")
        print(bool(result))