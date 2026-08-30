# Capsule CRM recipes

Provider value to use in every step: `capsulecrm`

This skill extends the base `workato-recipes` skill. Read that first for recipe JSON structure, datapill syntax, and control flow; this document only covers what is specific to this connector.

## Before you generate

- Set `"provider": "capsulecrm"` on every step that uses this connector.
- Use only the internal names listed below. They are the same list `lint-rules.json` enforces, so anything else fails `wk lint`.
- This connector has no custom-action escape hatch; if no native operation fits, use the HTTP connector instead.

## Triggers (4)

| Internal name | Title | Batch |
|---|---|---|
| `new_opportunity` | New opportunity | - |
| `new_organisation` | New organization | - |
| `new_party_opportunity` | New opportunity from a specific party | - |
| `new_person` | New person | - |


## Actions (8)

| Internal name | Title | Batch |
|---|---|---|
| `add_opportunity` | Add opportunity | - |
| `add_organisation` | Add organization | - |
| `add_person` | Add person | - |
| `search_organisations` | Search organizations | yes |
| `search_people` | Search people | yes |
| `update_opportunity` | Update opportunity | - |
| `update_organisation` | Update organization | - |
| `update_person` | Update person | - |


## Validation

```bash
wk lint <recipe>.recipe.json --skills-path <path-to>/skills
```
