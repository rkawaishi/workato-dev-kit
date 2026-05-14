# JIRA Service Desk connector

Provider: `jira_service_desk`

## Triggers

| Name | Internal name | Batch | Description |
|---|---|---|---|
| New customer request | `new_customer_request` | - |  |

## Actions

| Name | Internal name | Batch | Description |
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
