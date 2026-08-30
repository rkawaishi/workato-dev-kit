# LinkedIn recipes

Provider value to use in every step: `linkedin`

This skill extends the base `workato-recipes` skill. Read that first for recipe JSON structure, datapill syntax, and control flow; this document only covers what is specific to this connector.

## Before you generate

- Set `"provider": "linkedin"` on every step that uses this connector.
- Use only the internal names listed below. They are the same list `lint-rules.json` enforces, so anything else fails `wk lint`.
- Reach for `__adhoc_http_action` only when no native operation covers the call.

## Triggers (1)

| Internal name | Title | Batch |
|---|---|---|
| `new_lead_gen_form_response` | New lead gen form submitted | - |


## Actions (5)

| Internal name | Title | Batch |
|---|---|---|
| `__adhoc_http_action` | Custom action | - |
| `get_campaign_by_id` | Get campaign details by ID | - |
| `get_lead_gen_forms_by_id` | Get lead gen form response by ID | - |
| `get_list_of_campaigns_by_status` | Retrieve a list of campaigns by status | yes |
| `search_lead_gen_form_responses` | Search lead gen form responses | yes |


## Validation

```bash
wk lint <recipe>.recipe.json --skills-path <path-to>/skills
```
