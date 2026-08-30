# Facebook recipes

Provider value to use in every step: `facebook`

This skill extends the base `workato-recipes` skill. Read that first for recipe JSON structure, datapill syntax, and control flow; this document only covers what is specific to this connector.

## Before you generate

- Set `"provider": "facebook"` on every step that uses this connector.
- Use only the internal names listed below. They are the same list `lint-rules.json` enforces, so anything else fails `wk lint`.
- Reach for `__adhoc_http_action` only when no native operation covers the call.

## Triggers (0)

_None._


## Actions (5)

| Internal name | Title | Batch |
|---|---|---|
| `__adhoc_http_action` | Custom action | - |
| `get_adset_insights` | Get Adset Insights | yes |
| `get_campaign_insights` | Get campaign insights | yes |
| `list_adsets` | List Adset | yes |
| `list_campaigns` | List campaigns | yes |


## Deprecated -- do not generate

Workato still executes these in existing recipes, but new recipes must not use them. They are excluded from `valid_action_names`.


### Actions

| Internal name | Title | Batch |
|---|---|---|
| `post_status` | Post new status | - |


## Validation

```bash
wk lint <recipe>.recipe.json --skills-path <path-to>/skills
```
