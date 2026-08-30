# Splunk recipes

Provider value to use in every step: `splunk`

This skill extends the base `workato-recipes` skill. Read that first for recipe JSON structure, datapill syntax, and control flow; this document only covers what is specific to this connector.

## Before you generate

- Set `"provider": "splunk"` on every step that uses this connector.
- Use only the internal names listed below. They are the same list `lint-rules.json` enforces, so anything else fails `wk lint`.
- This connector has no custom-action escape hatch; if no native operation fits, use the HTTP connector instead.

## Triggers (2)

| Internal name | Title | Batch |
|---|---|---|
| `new_generic_alert` | New generic alert | - |
| `new_service_alert` | New service alert | - |


## Actions (3)

| Internal name | Title | Batch |
|---|---|---|
| `execute_saved_search` | Execute saved search | - |
| `search_objects` | Run query | - |
| `send_event_to_splunk` | Send event to splunk | - |


## Validation

```bash
wk lint <recipe>.recipe.json --skills-path <path-to>/skills
```
