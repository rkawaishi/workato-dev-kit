# JIRA Service Desk recipes

Provider value to use in every step: `jira_service_desk`

This skill extends the base `workato-recipes` skill. Read that first for recipe JSON structure, datapill syntax, and control flow; this document only covers what is specific to this connector.

## Before you generate

- Set `"provider": "jira_service_desk"` on every step that uses this connector.
- Use only the internal names listed below. They are the same list `lint-rules.json` enforces, so anything else fails `wk lint`.
- Reach for `__adhoc_http_action` only when no native operation covers the call.

## Triggers (1)

| Internal name | Title | Batch |
|---|---|---|
| `new_customer_request` | New customer request | - |


## Actions (8)

| Internal name | Title | Batch |
|---|---|---|
| `__adhoc_http_action` | Custom action | - |
| `create_comment` | Create comment | - |
| `create_customer` | Create customer | - |
| `create_customer_request` | Create customer request | - |
| `get_comment_by_ID` | Get comment by ID | - |
| `get_issue_in_queue_v2` | Get issue in queue | yes |
| `get_queues` | Get queues | yes |
| `list_comments` | List comments | yes |


## Deprecated -- do not generate

Workato still executes these in existing recipes, but new recipes must not use them. They are excluded from `valid_action_names`.


### Actions

| Internal name | Title | Batch |
|---|---|---|
| `get_issue_in_queue` | Get issue in queue | yes |


## Validation

```bash
wk lint <recipe>.recipe.json --skills-path <path-to>/skills
```
