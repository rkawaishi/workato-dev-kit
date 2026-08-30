# Zendesk Demo recipes

Provider value to use in every step: `zendesk_demo`

This skill extends the base `workato-recipes` skill. Read that first for recipe JSON structure, datapill syntax, and control flow; this document only covers what is specific to this connector.

## Before you generate

- Set `"provider": "zendesk_demo"` on every step that uses this connector.
- Use only the internal names listed below. They are the same list `lint-rules.json` enforces, so anything else fails `wk lint`.
- This connector has no custom-action escape hatch; if no native operation fits, use the HTTP connector instead.

## Triggers (0)

_None._


## Actions (6)

| Internal name | Title | Batch |
|---|---|---|
| `create_ticket` | Create ticket | - |
| `create_user` | Create user | - |
| `search_ticket` | Search tickets | - |
| `search_user` | Search users | - |
| `update_ticket` | Update ticket | - |
| `update_user` | Update user | - |


## Validation

```bash
wk lint <recipe>.recipe.json --skills-path <path-to>/skills
```
