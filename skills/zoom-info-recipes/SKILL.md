# ZoomInfo recipes

Provider value to use in every step: `zoom_info`

This skill extends the base `workato-recipes` skill. Read that first for recipe JSON structure, datapill syntax, and control flow; this document only covers what is specific to this connector.

## Before you generate

- Set `"provider": "zoom_info"` on every step that uses this connector.
- Use only the internal names listed below. They are the same list `lint-rules.json` enforces, so anything else fails `wk lint`.
- Reach for `__adhoc_http_action` only when no native operation covers the call.

## Triggers (1)

| Internal name | Title | Batch |
|---|---|---|
| `new_event` | Updated record | - |


## Actions (17)

| Internal name | Title | Batch |
|---|---|---|
| `__adhoc_http_action` | Custom action | - |
| `enrich_company` | Enrich companies | yes |
| `enrich_contact` | Enrich contacts | yes |
| `retrieve_comp_location` | Enrich company location | yes |
| `retrieve_compliance` | Enrich compliance data | yes |
| `retrieve_corporate_hierarchy` | Enrich corporate hierarchy | yes |
| `retrieve_hashtag` | Enrich hashtags | yes |
| `retrieve_intent` | Enrich intent | yes |
| `retrieve_news` | Enrich news | yes |
| `retrieve_org_chart` | Enrich organizational chart | yes |
| `retrieve_scoops` | Enrich scoops | yes |
| `retrieve_technology` | Enrich technology stack information | yes |
| `search_companies` | Search companies | yes |
| `search_contacts` | Search contacts | yes |
| `search_intent` | Search intent | yes |
| `search_news` | Search news | yes |
| `search_scoops` | Search scoops | yes |


## Validation

```bash
wk lint <recipe>.recipe.json --skills-path <path-to>/skills
```
