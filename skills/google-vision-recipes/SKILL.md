# Google Vision recipes

Provider value to use in every step: `google_vision`

This skill extends the base `workato-recipes` skill. Read that first for recipe JSON structure, datapill syntax, and control flow; this document only covers what is specific to this connector.

## Before you generate

- Set `"provider": "google_vision"` on every step that uses this connector.
- Use only the internal names listed below. They are the same list `lint-rules.json` enforces, so anything else fails `wk lint`.
- Reach for `__adhoc_http_action` only when no native operation covers the call.

## Triggers (0)

_None._


## Actions (2)

| Internal name | Title | Batch |
|---|---|---|
| `__adhoc_http_action` | Custom action | - |
| `text_from_image` | Read text from image | - |


## Validation

```bash
wk lint <recipe>.recipe.json --skills-path <path-to>/skills
```
