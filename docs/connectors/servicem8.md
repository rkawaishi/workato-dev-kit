# ServiceM8 コネクタ

Provider: `servicem8`

## Triggers

| 名前 | provider 内名称 | Batch | 説明 |
|---|---|---|---|
| Contact created | `created_companycontact` | - |  |
| Job activity created | `created_jobactivity` | - |  |
| Material created | `created_material` | - |  |
| Staff created | `created_staff` | - |  |
| Job quoted | `quoted_job` | - |  |
| Client updated | `updated_company` | - |  |
| Job updated | `updated_job` | - |  |

## Actions

| 名前 | provider 内名称 | Batch | 説明 |
|---|---|---|---|
| Add job | `add_job` | - |  |
| Add job material | `add_job_material` | - |  |
| Create material | `add_material` | - |  |
| Add staff | `add_staff` | - |  |
| Create client | `create_client` | - |  |
| Create contact | `create_contact` | - |  |
| Get client details by UUID | `get_client_by_uuid` | - |  |
| Get job by UUID | `get_job_by_uuid` | - |  |
| Get job materials by job/UUID | `get_job_material` | Yes |  |
| Get staff by UUID | `get_staff_by_uuid` | - |  |
| Search client | `search_client` | - |  |
| Search contact | `search_contact` | Yes |  |
| Search job activities | `search_job_activities` | Yes |  |
| Search materials | `search_materials` | - |  |
| Search staff | `search_staff` | Yes |  |
| Update client | `update_client` | - |  |
| Update contact | `update_contact` | - |  |
| Update job | `update_job` | - |  |
| Update material | `update_material` | - |  |
