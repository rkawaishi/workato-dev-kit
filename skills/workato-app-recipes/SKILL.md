# RecipeOps by Workato recipes

Provider value to use in every step: `workato_app`

This skill extends the base `workato-recipes` skill. Read that first for recipe JSON structure, datapill syntax, and control flow; this document only covers what is specific to this connector.

## Before you generate

- Set `"provider": "workato_app"` on every step that uses this connector.
- Use only the internal names listed below. They are the same list `lint-rules.json` enforces, so anything else fails `wk lint`.
- This connector has no custom-action escape hatch; if no native operation fits, use the HTTP connector instead.

## Triggers (21)

| Internal name | Title | Batch |
|---|---|---|
| `customer_usage_threshold_reached` | Usage threshold reached | - |
| `deployment_failed` | Deployment failed | - |
| `deployment_finished` | Deployment complete | - |
| `deployment_review_approved` | Deployment approved | - |
| `deployment_review_rejected` | Deployment rejected | - |
| `deployment_review_reset` | Deployment re-opened for review | - |
| `deployment_submitted_for_review` | New deployment submitted for review | - |
| `fanbus_apim_api_request_timeout` | API request timeout | - |
| `fanbus_apim_concurrency_limit_reached` | API concurrency threshold exceeded | - |
| `fanbus_apim_quota_threshold_reached` | API policy quota violations | - |
| `fanbus_apim_rate_limit_reached` | API policy rate limit violations | - |
| `fanbus_opa_disconnected` | On-prem agent disconnected | - |
| `job_error` | Job failed | - |
| `member_invitation_accepted` | Member invitation accepted | - |
| `package_deployed` | Package deployed | - |
| `recipe_started` | Recipe started | - |
| `recipe_stopped` | Recipe stopped by user | - |
| `shared_account_connected` | Account connected | - |
| `shared_account_disconnected` | Account disconnected | - |
| `shared_account_refresh_failed` | Account credentials refresh failed | - |
| `stop_error` | Recipe stopped by Workato | - |


## Actions (9)

| Internal name | Title | Batch |
|---|---|---|
| `get_recipe` | Get recipe details | - |
| `list_jobs` | Search job history | yes |
| `rerun_jobs` | Rerun jobs | yes |
| `search_connections` | List connections | yes |
| `search_recipes` | List recipes | yes |
| `search_recipes_v2` | Search recipes | yes |
| `start_recipe` | Start recipe | - |
| `stop_recipe` | Stop recipe | - |
| `summary_status` | Get account details | - |


## Validation

```bash
wk lint <recipe>.recipe.json --skills-path <path-to>/skills
```
