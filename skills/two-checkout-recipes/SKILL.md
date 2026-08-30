# 2Checkout recipes

Provider value to use in every step: `two_checkout`

This skill extends the base `workato-recipes` skill. Read that first for recipe JSON structure, datapill syntax, and control flow; this document only covers what is specific to this connector.

## Before you generate

- Set `"provider": "two_checkout"` on every step that uses this connector.
- Use only the internal names listed below. They are the same list `lint-rules.json` enforces, so anything else fails `wk lint`.
- This connector has no custom-action escape hatch; if no native operation fits, use the HTTP connector instead.

## Triggers (3)

| Internal name | Title | Batch |
|---|---|---|
| `ins_webhook` | INS webhooks | - |
| `ipn_webhook` | IPN webhooks | - |
| `lcn_webhook` | LCN webhooks | - |


## Actions (0)

_None._


## Validation

```bash
wk lint <recipe>.recipe.json --skills-path <path-to>/skills
```
