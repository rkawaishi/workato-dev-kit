# Namely コネクタ

Provider: `namely`

## Triggers

| 名前 | provider 内名称 | Batch | 説明 |
|---|---|---|---|
| New event | `new_event` | - |  |
| New employee profile | `new_profile` | - |  |
| New/updated employee profile | `new_updated_profile` | - |  |
| New employee profile | `on_new_profile` | - |  [deprecated] |

## Actions

| 名前 | provider 内名称 | Batch | 説明 |
|---|---|---|---|
| Custom action | `__adhoc_http_action` | - |  |
| Create status post | `create_post` | - |  |
| Get employee profile details by ID | `get_profile` | - |  |
| Post comment | `post_comment` | - |  |
| Search people profiles | `search_profile` | Yes |  |
| Update people profile | `update_profile` | - |  |
