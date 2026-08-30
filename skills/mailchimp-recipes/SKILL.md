# MailChimp recipes

Provider value to use in every step: `mailchimp`

This skill extends the base `workato-recipes` skill. Read that first for recipe JSON structure, datapill syntax, and control flow; this document only covers what is specific to this connector.

## Before you generate

- Set `"provider": "mailchimp"` on every step that uses this connector.
- Use only the internal names listed below. They are the same list `lint-rules.json` enforces, so anything else fails `wk lint`.
- Reach for `__adhoc_http_action` only when no native operation covers the call.

## Triggers (6)

| Internal name | Title | Batch |
|---|---|---|
| `campaign_created` | Campaign created | - |
| `campaign_opened` | Campaign opened | - |
| `campaign_sent` | Campaign sent | - |
| `new_list` | New list | - |
| `new_subscriber` | New subscriber | - |
| `updated_subscriber` | New or updated subscriber | - |


## Actions (10)

| Internal name | Title | Batch |
|---|---|---|
| `__adhoc_http_action` | Custom action | - |
| `add_subscriber_tag` | Add subscriber tags | yes |
| `add_subscriber_v3` | Add subscriber | - |
| `get_subscriber_activity` | Get subscriber activity | yes |
| `get_subscriber_tags` | Get subscriber tags | yes |
| `remove_subscriber_v3` | Remove subscriber | - |
| `search_campaigns` | Search campaigns | yes |
| `search_subscribers` | Search subscribers | yes |
| `search_tags` | Search tags | yes |
| `update_subscriber_v3` | Update subscriber | - |


## Deprecated -- do not generate

Workato still executes these in existing recipes, but new recipes must not use them. They are excluded from `valid_action_names`.


### Actions

| Internal name | Title | Batch |
|---|---|---|
| `add_subscriber` | Add subscriber | - |
| `remove_subscribers` | Remove subscribers | - |
| `update_subscriber` | Update subscriber | - |


## Validation

```bash
wk lint <recipe>.recipe.json --skills-path <path-to>/skills
```
