# JIRA Service Desk コネクタ

Provider: `jira_service_desk`

## Triggers

| 名前 | provider 内名称 | Batch | 説明 |
|---|---|---|---|
| New customer request | `new_customer_request` | - |  |

## Actions

| 名前 | provider 内名称 | Batch | 説明 |
|---|---|---|---|
| Custom action | `__adhoc_http_action` | - |  |
| Create comment | `create_comment` | - |  |
| Create customer | `create_customer` | - |  |
| Create customer request | `create_customer_request` | - |  |
| Get comment by ID | `get_comment_by_ID` | - |  |
| Get issue in queue | `get_issue_in_queue` | Yes |  [deprecated] |
| Get issue in queue | `get_issue_in_queue_v2` | Yes |  |
| Get queues | `get_queues` | Yes |  |
| List comments | `list_comments` | Yes |  |
