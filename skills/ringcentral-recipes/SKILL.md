# RingCentral recipes

Provider value to use in every step: `ringcentral`

This skill extends the base `workato-recipes` skill. Read that first for recipe JSON structure, datapill syntax, and control flow; this document only covers what is specific to this connector.

## Before you generate

- Set `"provider": "ringcentral"` on every step that uses this connector.
- Use only the internal names listed below. They are the same list `lint-rules.json` enforces, so anything else fails `wk lint`.
- Reach for `__adhoc_http_action` only when no native operation covers the call.

## Triggers (6)

| Internal name | Title | Batch |
|---|---|---|
| `call_ended` | Call ended | - |
| `new_call` | New call | - |
| `new_call_recording` | New call recording | - |
| `new_company_level_call` | New company level call | - |
| `new_event` | New event trigger | - |
| `new_sms` | New sms | - |


## Actions (4)

| Internal name | Title | Batch |
|---|---|---|
| `__adhoc_http_action` | Custom action | - |
| `ring_out` | Ring out | - |
| `send_pager_message` | Send pager message | - |
| `send_sms` | Send sms | - |


## Validation

```bash
wk lint <recipe>.recipe.json --skills-path <path-to>/skills
```
