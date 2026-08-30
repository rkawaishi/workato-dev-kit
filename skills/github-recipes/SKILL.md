# GitHub recipes

Provider value to use in every step: `github`

This skill extends the base `workato-recipes` skill. Read that first for recipe JSON structure, datapill syntax, and control flow; this document only covers what is specific to this connector.

## Before you generate

- Set `"provider": "github"` on every step that uses this connector.
- Use only the internal names listed below. They are the same list `lint-rules.json` enforces, so anything else fails `wk lint`.
- Reach for `__adhoc_http_action` only when no native operation covers the call.

## Triggers (7)

| Internal name | Title | Batch |
|---|---|---|
| `new_closed_issue` | Closed issue | - |
| `new_issue` | New issue | - |
| `new_or_updated_issue` | New or updated issue | - |
| `new_or_updated_milestone` | New or updated milestone | - |
| `new_or_updated_pull_request` | New or updated pull request | - |
| `new_pr` | New PR | - |
| `new_updated_issue_comment` | New updated issue comment | - |


## Actions (7)

| Internal name | Title | Batch |
|---|---|---|
| `__adhoc_http_action` | Custom action | - |
| `create_comment_in_an_issue` | Create comment in an issue | - |
| `create_issue` | Create issue | - |
| `get_issue_or_PR_details` | Get issue or PR details | - |
| `list_statuses_for_a_ref` | List statuses for a ref | yes |
| `search_issues` | Search issues/pull requests | yes |
| `update_issue` | Update issue | - |


## Validation

```bash
wk lint <recipe>.recipe.json --skills-path <path-to>/skills
```
