# Bitbucket recipes

Provider value to use in every step: `bitbucket`

This skill extends the base `workato-recipes` skill. Read that first for recipe JSON structure, datapill syntax, and control flow; this document only covers what is specific to this connector.

## Before you generate

- Set `"provider": "bitbucket"` on every step that uses this connector.
- Use only the internal names listed below. They are the same list `lint-rules.json` enforces, so anything else fails `wk lint`.
- Reach for `__adhoc_http_action` only when no native operation covers the call.

## Triggers (3)

| Internal name | Title | Batch |
|---|---|---|
| `closed_issue` | Closed issue | - |
| `new_issue` | New issue | - |
| `new_or_updated_issue` | New or updated issue | - |


## Actions (8)

| Internal name | Title | Batch |
|---|---|---|
| `__adhoc_http_action` | Custom action | - |
| `create_comment_in_an_issue` | Create comment in an issue | - |
| `create_issue` | Create issue | - |
| `get_events` | Get events | yes |
| `get_issue_by_id` | Get issue by ID | - |
| `list_comments_in_an_issue` | List comments in an issue | yes |
| `search_issues` | Search issues | yes |
| `update_issue_by_id` | Update issue by ID | - |


## Validation

```bash
wk lint <recipe>.recipe.json --skills-path <path-to>/skills
```
