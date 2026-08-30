# Workday recipes

Provider value to use in every step: `workday`

This skill extends the base `workato-recipes` skill. Read that first for recipe JSON structure, datapill syntax, and control flow; this document only covers what is specific to this connector.

## Before you generate

- Set `"provider": "workday"` on every step that uses this connector.
- Use only the internal names listed below. They are the same list `lint-rules.json` enforces, so anything else fails `wk lint`.
- Reach for `__adhoc_http_action` only when no native operation covers the call.

## Triggers (4)

| Internal name | Title | Batch |
|---|---|---|
| `new_updated_object` | New/updated business object | - |
| `new_updated_object_batch` | New/updated business object | yes |
| `scheduled_report_batch` | Scheduled report fetch | yes |
| `scheduled_wql_report_batch` | Scheduled report fetch using WQL | yes |


## Actions (10)

| Internal name | Title | Batch |
|---|---|---|
| `Get_business_object_details` | Get business object details | yes |
| `Search_business_object` | Search business object | yes |
| `Update_business_object` | Update business object | - |
| `__adhoc_http_action` | Custom action | - |
| `call_operation` | Call operation | - |
| `get_custom_object` | Get custom objects | - |
| `get_report` | Get report | - |
| `get_wql_report` | Get report using WQL | yes |
| `list_custom_objects` | List custom object definitions | yes |
| `post_custom_object` | Create/update custom object | - |


## Validation

```bash
wk lint <recipe>.recipe.json --skills-path <path-to>/skills
```
