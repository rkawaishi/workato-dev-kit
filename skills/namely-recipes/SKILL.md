# Namely recipes

Provider value to use in every step: `namely`

This skill extends the base `workato-recipes` skill. Read that first for recipe JSON structure, datapill syntax, and control flow; this document only covers what is specific to this connector.

## Before you generate

- Set `"provider": "namely"` on every step that uses this connector.
- Use only the internal names listed below. They are the same list `lint-rules.json` enforces, so anything else fails `wk lint`.
- Reach for `__adhoc_http_action` only when no native operation covers the call.

## Triggers (3)

| Internal name | Title | Batch |
|---|---|---|
| `new_event` | New event | - |
| `new_profile` | New employee profile | - |
| `new_updated_profile` | New/updated employee profile | - |


## Actions (6)

| Internal name | Title | Batch |
|---|---|---|
| `__adhoc_http_action` | Custom action | - |
| `create_post` | Create status post | - |
| `get_profile` | Get employee profile details by ID | - |
| `post_comment` | Post comment | - |
| `search_profile` | Search people profiles | yes |
| `update_profile` | Update people profile | - |


## Deprecated -- do not generate

Workato still executes these in existing recipes, but new recipes must not use them. They are excluded from `valid_action_names`.


### Triggers

| Internal name | Title | Batch |
|---|---|---|
| `on_new_profile` | New employee profile | - |


## Validation

```bash
wk lint <recipe>.recipe.json --skills-path <path-to>/skills
```
