# Sage Live recipes

Provider value to use in every step: `sagelive`

This skill extends the base `workato-recipes` skill. Read that first for recipe JSON structure, datapill syntax, and control flow; this document only covers what is specific to this connector.

## Before you generate

- Set `"provider": "sagelive"` on every step that uses this connector.
- Use only the internal names listed below. They are the same list `lint-rules.json` enforces, so anything else fails `wk lint`.
- Reach for `__adhoc_http_action` only when no native operation covers the call.

## Triggers (3)

| Internal name | Title | Batch |
|---|---|---|
| `object_created` | Object created | - |
| `object_review` | Daily object review | - |
| `object_updated` | Object created/updated | - |


## Actions (5)

| Internal name | Title | Batch |
|---|---|---|
| `__adhoc_http_action` | Custom action | - |
| `create_object` | Create object | - |
| `get_related` | Get related objects | yes |
| `search_objects` | Search objects | yes |
| `update_object` | Update object | - |


## Validation

```bash
wk lint <recipe>.recipe.json --skills-path <path-to>/skills
```
