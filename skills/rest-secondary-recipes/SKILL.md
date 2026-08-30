# HTTP secondary recipes

Provider value to use in every step: `rest_secondary`

This skill extends the base `workato-recipes` skill. Read that first for recipe JSON structure, datapill syntax, and control flow; this document only covers what is specific to this connector.

## Before you generate

- Set `"provider": "rest_secondary"` on every step that uses this connector.
- Use only the internal names listed below. They are the same list `lint-rules.json` enforces, so anything else fails `wk lint`.
- This connector has no custom-action escape hatch; if no native operation fits, use the HTTP connector instead.

## Triggers (1)

| Internal name | Title | Batch |
|---|---|---|
| `new_poll_event` | New event via polling | - |


## Actions (1)

| Internal name | Title | Batch |
|---|---|---|
| `make_request_v2` | Send request | - |


## Deprecated -- do not generate

Workato still executes these in existing recipes, but new recipes must not use them. They are excluded from `valid_action_names`.


### Triggers

| Internal name | Title | Batch |
|---|---|---|
| `new_event` | New event via webhook | - |


### Actions

| Internal name | Title | Batch |
|---|---|---|
| `make_proxy_request` | Send request and wait for response | - |
| `make_request` | Make REST request | - |


## Validation

```bash
wk lint <recipe>.recipe.json --skills-path <path-to>/skills
```
