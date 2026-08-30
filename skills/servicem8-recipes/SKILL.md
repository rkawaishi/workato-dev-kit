# ServiceM8 recipes

Provider value to use in every step: `servicem8`

This skill extends the base `workato-recipes` skill. Read that first for recipe JSON structure, datapill syntax, and control flow; this document only covers what is specific to this connector.

## Before you generate

- Set `"provider": "servicem8"` on every step that uses this connector.
- Use only the internal names listed below. They are the same list `lint-rules.json` enforces, so anything else fails `wk lint`.
- This connector has no custom-action escape hatch; if no native operation fits, use the HTTP connector instead.

## Triggers (7)

| Internal name | Title | Batch |
|---|---|---|
| `created_companycontact` | Contact created | - |
| `created_jobactivity` | Job activity created | - |
| `created_material` | Material created | - |
| `created_staff` | Staff created | - |
| `quoted_job` | Job quoted | - |
| `updated_company` | Client updated | - |
| `updated_job` | Job updated | - |


## Actions (19)

| Internal name | Title | Batch |
|---|---|---|
| `add_job` | Add job | - |
| `add_job_material` | Add job material | - |
| `add_material` | Create material | - |
| `add_staff` | Add staff | - |
| `create_client` | Create client | - |
| `create_contact` | Create contact | - |
| `get_client_by_uuid` | Get client details by UUID | - |
| `get_job_by_uuid` | Get job by UUID | - |
| `get_job_material` | Get job materials by job/UUID | yes |
| `get_staff_by_uuid` | Get staff by UUID | - |
| `search_client` | Search client | - |
| `search_contact` | Search contact | yes |
| `search_job_activities` | Search job activities | yes |
| `search_materials` | Search materials | - |
| `search_staff` | Search staff | yes |
| `update_client` | Update client | - |
| `update_contact` | Update contact | - |
| `update_job` | Update job | - |
| `update_material` | Update material | - |


## Validation

```bash
wk lint <recipe>.recipe.json --skills-path <path-to>/skills
```
