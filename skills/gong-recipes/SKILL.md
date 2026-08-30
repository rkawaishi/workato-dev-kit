# Gong.io recipes

Provider value to use in every step: `gong`

This skill extends the base `workato-recipes` skill. Read that first for recipe JSON structure, datapill syntax, and control flow; this document only covers what is specific to this connector.

## Before you generate

- Set `"provider": "gong"` on every step that uses this connector.
- Use only the internal names listed below. They are the same list `lint-rules.json` enforces, so anything else fails `wk lint`.
- Reach for `__adhoc_http_action` only when no native operation covers the call.

## Triggers (1)

| Internal name | Title | Batch |
|---|---|---|
| `new_call` | New call | - |


## Actions (10)

| Internal name | Title | Batch |
|---|---|---|
| `__adhoc_http_action` | Custom action | - |
| `add_call` | Add call | - |
| `add_call_media` | Add call media | - |
| `digital_interaction_action` | Post a digital interaction | - |
| `get_call_by_id` | Get call by ID | - |
| `search_aggregated_user_data` | Search aggregated user data | yes |
| `search_call_scorecards` | Search call scorecards | yes |
| `search_call_transcripts` | Search call transcripts | yes |
| `search_calls` | Search calls | yes |
| `search_users` | Search users | yes |


## Deprecated -- do not generate

Workato still executes these in existing recipes, but new recipes must not use them. They are excluded from `valid_action_names`.


### Actions

| Internal name | Title | Batch |
|---|---|---|
| `report_content_shared` | Create content share engagement event | - |
| `report_content_viewed` | Create content view event | - |
| `report_custom_action` | Create custom action event | - |


## Validation

```bash
wk lint <recipe>.recipe.json --skills-path <path-to>/skills
```
