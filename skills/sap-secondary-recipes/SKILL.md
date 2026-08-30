# SAP RFC secondary recipes

Provider value to use in every step: `sap_secondary`

This skill extends the base `workato-recipes` skill. Read that first for recipe JSON structure, datapill syntax, and control flow; this document only covers what is specific to this connector.

## Before you generate

- Set `"provider": "sap_secondary"` on every step that uses this connector.
- Use only the internal names listed below. They are the same list `lint-rules.json` enforces, so anything else fails `wk lint`.
- This connector has no custom-action escape hatch; if no native operation fits, use the HTTP connector instead.

## Triggers (2)

| Internal name | Title | Batch |
|---|---|---|
| `new_idocs_batch` | New IDocs | yes |
| `new_updated_idoc` | New IDoc | - |


## Actions (7)

| Internal name | Title | Batch |
|---|---|---|
| `call_bapi` | Call BAPI | - |
| `idoc_status` | Check IDoc status | - |
| `idoc_upload_new` | Send IDoc | - |
| `idoc_upload_v3` | Send IDoc (Advanced) | - |
| `run_rfm` | Call remote function module | - |
| `trfc_begin` | Begin transaction | - |
| `trfc_end` | End transaction | - |


## Deprecated -- do not generate

Workato still executes these in existing recipes, but new recipes must not use them. They are excluded from `valid_action_names`.


### Actions

| Internal name | Title | Batch |
|---|---|---|
| `idoc_upload` | Send IDoc (Legacy) | - |


## Validation

```bash
wk lint <recipe>.recipe.json --skills-path <path-to>/skills
```
