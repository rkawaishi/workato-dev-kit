# MailChimp コネクタ

Provider: `mailchimp`

## Triggers

| 名前 | provider 内名称 | Batch | 説明 |
|---|---|---|---|
| Campaign created | `campaign_created` | - |  |
| Campaign opened | `campaign_opened` | - |  |
| Campaign sent | `campaign_sent` | - |  |
| New list | `new_list` | - |  |
| New subscriber | `new_subscriber` | - |  |
| New or updated subscriber | `updated_subscriber` | - |  |

## Actions

| 名前 | provider 内名称 | Batch | 説明 |
|---|---|---|---|
| Custom action | `__adhoc_http_action` | - |  |
| Add subscriber | `add_subscriber` | - |  [deprecated] |
| Add subscriber tags | `add_subscriber_tag` | Yes |  |
| Add subscriber | `add_subscriber_v3` | - |  |
| Get subscriber activity | `get_subscriber_activity` | Yes |  |
| Get subscriber tags | `get_subscriber_tags` | Yes |  |
| Remove subscriber | `remove_subscriber_v3` | - |  |
| Remove subscribers | `remove_subscribers` | - |  [deprecated] |
| Search campaigns | `search_campaigns` | Yes |  |
| Search subscribers | `search_subscribers` | Yes |  |
| Search tags | `search_tags` | Yes |  |
| Update subscriber | `update_subscriber` | - |  [deprecated] |
| Update subscriber | `update_subscriber_v3` | - |  |
