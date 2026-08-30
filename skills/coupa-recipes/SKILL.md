# Coupa recipes

Provider value to use in every step: `coupa`

This skill extends the base `workato-recipes` skill. Read that first for recipe JSON structure, datapill syntax, and control flow; this document only covers what is specific to this connector.

## Before you generate

- Set `"provider": "coupa"` on every step that uses this connector.
- Use only the internal names listed below. They are the same list `lint-rules.json` enforces, so anything else fails `wk lint`.
- Reach for `__adhoc_http_action` only when no native operation covers the call.

## Triggers (1)

| Internal name | Title | Batch |
|---|---|---|
| `new_or_updated_object` | New or updated object | - |


## Actions (13)

| Internal name | Title | Batch |
|---|---|---|
| `__adhoc_http_action` | Custom action | - |
| `cancel_purchase_order` | Cancel purchase order | - |
| `close_purchase_order` | Close purchase order | - |
| `create_attachment_on_object` | Add file attachment to object | - |
| `create_object` | Create object | - |
| `get_object_by_id` | Get object by ID | - |
| `get_remit_to_addresses_by_object_id` | Get remit to addresses by object ID | - |
| `get_supplier_sites_by_supplier` | Get supplier sites by supplier | - |
| `grant_approval` | Grant approval | - |
| `reject_approval` | Reject approval | - |
| `search_objects` | Search objects | yes |
| `set_integration_run_status` | Set integration run status | - |
| `update_object` | Update object | - |


## Validation

```bash
wk lint <recipe>.recipe.json --skills-path <path-to>/skills
```
