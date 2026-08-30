# Pipedrive recipes

Provider value to use in every step: `pipedrive`

This skill extends the base `workato-recipes` skill. Read that first for recipe JSON structure, datapill syntax, and control flow; this document only covers what is specific to this connector.

## Before you generate

- Set `"provider": "pipedrive"` on every step that uses this connector.
- Use only the internal names listed below. They are the same list `lint-rules.json` enforces, so anything else fails `wk lint`.
- Reach for `__adhoc_http_action` only when no native operation covers the call.

## Triggers (3)

| Internal name | Title | Batch |
|---|---|---|
| `added_object` | New object | - |
| `updated_object` | New or Updated object | - |
| `updated_object_batch` | New or updated object | yes |


## Actions (10)

| Internal name | Title | Batch |
|---|---|---|
| `__adhoc_http_action` | Custom action | - |
| `create_activity` | Create activity | - |
| `create_deal` | Create deal | - |
| `create_note` | Create note | - |
| `create_organization` | Create organization | - |
| `get_deal_related_products` | Get deal related products | yes |
| `get_object` | Get object | yes |
| `update_deal` | Update deal | - |
| `update_organization` | Update organization | - |
| `update_person` | Update person | - |


## Deprecated -- do not generate

Workato still executes these in existing recipes, but new recipes must not use them. They are excluded from `valid_action_names`.


### Triggers

| Internal name | Title | Batch |
|---|---|---|
| `new_deal` | New deal | - |


## Validation

```bash
wk lint <recipe>.recipe.json --skills-path <path-to>/skills
```
