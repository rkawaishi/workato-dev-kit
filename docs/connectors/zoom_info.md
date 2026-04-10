# ZoomInfo コネクタ

Provider: `zoom_info`

## Triggers

| 名前 | provider 内名称 | Batch | 説明 |
|---|---|---|---|
| Updated record | `new_event` | - |  |

## Actions

| 名前 | provider 内名称 | Batch | 説明 |
|---|---|---|---|
| Custom action | `__adhoc_http_action` | - |  |
| Enrich companies | `enrich_company` | Yes |  |
| Enrich contacts | `enrich_contact` | Yes |  |
| Enrich company location | `retrieve_comp_location` | Yes |  |
| Enrich compliance data | `retrieve_compliance` | Yes |  |
| Enrich corporate hierarchy | `retrieve_corporate_hierarchy` | Yes |  |
| Enrich hashtags | `retrieve_hashtag` | Yes |  |
| Enrich intent | `retrieve_intent` | Yes |  |
| Enrich news | `retrieve_news` | Yes |  |
| Enrich organizational chart | `retrieve_org_chart` | Yes |  |
| Enrich scoops | `retrieve_scoops` | Yes |  |
| Enrich technology stack information | `retrieve_technology` | Yes |  |
| Search companies | `search_companies` | Yes |  |
| Search contacts | `search_contacts` | Yes |  |
| Search intent | `search_intent` | Yes |  |
| Search news | `search_news` | Yes |  |
| Search scoops | `search_scoops` | Yes |  |
