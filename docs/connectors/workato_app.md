# RecipeOps by Workato コネクタ

Provider: `workato_app`

## Triggers

| 名前 | provider 内名称 | Batch | 説明 |
|---|---|---|---|
| Usage threshold reached | `customer_usage_threshold_reached` | - |  |
| Deployment failed | `deployment_failed` | - |  |
| Deployment complete | `deployment_finished` | - |  |
| Deployment approved | `deployment_review_approved` | - |  |
| Deployment rejected | `deployment_review_rejected` | - |  |
| Deployment re-opened for review | `deployment_review_reset` | - |  |
| New deployment submitted for review | `deployment_submitted_for_review` | - |  |
| API request timeout | `fanbus_apim_api_request_timeout` | - |  |
| API concurrency threshold exceeded | `fanbus_apim_concurrency_limit_reached` | - |  |
| API policy quota violations | `fanbus_apim_quota_threshold_reached` | - |  |
| API policy rate limit violations | `fanbus_apim_rate_limit_reached` | - |  |
| On-prem agent disconnected | `fanbus_opa_disconnected` | - |  |
| Job failed | `job_error` | - |  |
| Member invitation accepted | `member_invitation_accepted` | - |  |
| Package deployed | `package_deployed` | - |  |
| Recipe started | `recipe_started` | - |  |
| Recipe stopped by user | `recipe_stopped` | - |  |
| Account connected | `shared_account_connected` | - |  |
| Account disconnected | `shared_account_disconnected` | - |  |
| Account credentials refresh failed | `shared_account_refresh_failed` | - |  |
| Recipe stopped by Workato | `stop_error` | - |  |

## Actions

| 名前 | provider 内名称 | Batch | 説明 |
|---|---|---|---|
| Get recipe details | `get_recipe` | - |  |
| Search job history | `list_jobs` | Yes |  |
| Rerun jobs | `rerun_jobs` | Yes |  |
| List connections | `search_connections` | Yes |  |
| List recipes | `search_recipes` | Yes |  |
| Search recipes | `search_recipes_v2` | Yes |  |
| Start recipe | `start_recipe` | - |  |
| Stop recipe | `stop_recipe` | - |  |
| Get account details | `summary_status` | - |  |
