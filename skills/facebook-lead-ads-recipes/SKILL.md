# Facebook Lead Ads recipes

Provider value to use in every step: `facebook_lead_ads`

This skill extends the base `workato-recipes` skill. Read that first for recipe JSON structure, datapill syntax, and control flow; this document only covers what is specific to this connector.

## Before you generate

- Set `"provider": "facebook_lead_ads"` on every step that uses this connector.
- Use only the internal names listed below. They are the same list `lint-rules.json` enforces, so anything else fails `wk lint`.
- Reach for `__adhoc_http_action` only when no native operation covers the call.

## Triggers (1)

| Internal name | Title | Batch |
|---|---|---|
| `new_lead` | New lead | - |


## Actions (1)

| Internal name | Title | Batch |
|---|---|---|
| `__adhoc_http_action` | Custom action | - |


## Validation

```bash
wk lint <recipe>.recipe.json --skills-path <path-to>/skills
```
