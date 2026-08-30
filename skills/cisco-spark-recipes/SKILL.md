# Cisco Webex Teams recipes

Provider value to use in every step: `cisco_spark`

This skill extends the base `workato-recipes` skill. Read that first for recipe JSON structure, datapill syntax, and control flow; this document only covers what is specific to this connector.

## Before you generate

- Set `"provider": "cisco_spark"` on every step that uses this connector.
- Use only the internal names listed below. They are the same list `lint-rules.json` enforces, so anything else fails `wk lint`.
- Reach for `__adhoc_http_action` only when no native operation covers the call.

## Triggers (2)

| Internal name | Title | Batch |
|---|---|---|
| `new_attachment` | New button submission | - |
| `new_message` | New message | - |


## Actions (9)

| Internal name | Title | Batch |
|---|---|---|
| `__adhoc_http_action` | Custom action | - |
| `add_person_to_room` | Add person to room | - |
| `create_room` | Create room | - |
| `get_attachment_details` | Get attachment details | - |
| `get_message_details` | Get message details | - |
| `get_person_details` | Get person details | - |
| `get_room_details` | Get room details | - |
| `post_blocks_message` | Post message | - |
| `update_room` | Update room | - |


## Deprecated -- do not generate

Workato still executes these in existing recipes, but new recipes must not use them. They are excluded from `valid_action_names`.


### Actions

| Internal name | Title | Batch |
|---|---|---|
| `post_message` | Post message | - |


## Validation

```bash
wk lint <recipe>.recipe.json --skills-path <path-to>/skills
```
