# Raiser's Edge NXT recipes

Provider value to use in every step: `raisers_edge`

This skill extends the base `workato-recipes` skill. Read that first for recipe JSON structure, datapill syntax, and control flow; this document only covers what is specific to this connector.

## Before you generate

- Set `"provider": "raisers_edge"` on every step that uses this connector.
- Use only the internal names listed below. They are the same list `lint-rules.json` enforces, so anything else fails `wk lint`.
- Reach for `__adhoc_http_action` only when no native operation covers the call.

## Triggers (15)

| Internal name | Title | Batch |
|---|---|---|
| `new_address` | New address | - |
| `new_appeal` | New appeal | - |
| `new_campaign` | New campaign | - |
| `new_constituent` | New constituent | - |
| `new_email` | New email | - |
| `new_fund` | New fund | - |
| `new_gift` | New gift | - |
| `new_online_presence` | New online presence | - |
| `new_or_updated_address` | New or updated address | - |
| `new_or_updated_appeal` | New or updated appeal | - |
| `new_or_updated_campaign` | New or updated campaign | - |
| `new_or_updated_constituent` | New or updated constituent | - |
| `new_or_updated_fund` | New or updated fund | - |
| `new_or_updated_gift` | New or updated gift | - |
| `new_phone` | New phone | - |


## Actions (37)

| Internal name | Title | Batch |
|---|---|---|
| `__adhoc_http_action` | Custom action | - |
| `add_custom_field_to_constituent` | Add custom field to constituent | - |
| `create_address` | Create address | - |
| `create_communication_preferences` | Create communication preferences | - |
| `create_constituent` | Create constituent | - |
| `create_constituent_code` | Create constituent code | - |
| `create_email` | Create email | - |
| `create_online_presence` | Create online presence | - |
| `create_phone` | Create phone | - |
| `delete_address` | Delete address | - |
| `delete_email` | Delete email | - |
| `delete_online_presence` | Delete online presence | - |
| `delete_phone` | Delete phone | - |
| `get_addresses` | Get addresses | yes |
| `get_appeal_details` | Get appeal details | - |
| `get_campaign_details` | Get campaign details | - |
| `get_constituent_details` | Get constituent details | - |
| `get_custom_fields_by_appeal_id` | Get custom fields by appeal ID | yes |
| `get_custom_fields_by_campaign_id` | Get custom fields by campaign ID | yes |
| `get_custom_fields_by_constituent_id` | Get custom fields by constituent ID | yes |
| `get_custom_fields_by_fund_id` | Get custom fields by fund ID | yes |
| `get_custom_fields_by_gift_id` | Get custom fields by gift ID | yes |
| `get_email_addresses` | Get email addresses | yes |
| `get_fund_details` | Get fund details | - |
| `get_gift_details` | Get gift details | - |
| `get_phones` | Get phones | yes |
| `search_constituent` | Search constituent | yes |
| `search_constituent_code` | Search constituent code | yes |
| `search_online_presence` | Search online presence | yes |
| `update_address` | Update address | - |
| `update_communication_preferences` | Update communication preferences | - |
| `update_constituent` | Update constituent | - |
| `update_constituent_code` | Update constituent code | - |
| `update_custom_field_in_constituent` | Update custom field in constituent | - |
| `update_email` | Update email | - |
| `update_online_presence` | Update online presence | - |
| `update_phone` | Update phone | - |


## Validation

```bash
wk lint <recipe>.recipe.json --skills-path <path-to>/skills
```
