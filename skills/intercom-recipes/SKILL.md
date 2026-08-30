# Intercom recipes

Provider value to use in every step: `intercom`

This skill extends the base `workato-recipes` skill. Read that first for recipe JSON structure, datapill syntax, and control flow; this document only covers what is specific to this connector.

## Before you generate

- Set `"provider": "intercom"` on every step that uses this connector.
- Use only the internal names listed below. They are the same list `lint-rules.json` enforces, so anything else fails `wk lint`.
- Reach for `__adhoc_http_action` only when no native operation covers the call.

## Triggers (7)

| Internal name | Title | Batch |
|---|---|---|
| `new_company` | New company | - |
| `new_contact` | New contact | - |
| `new_conversation` | New conversation | - |
| `new_user` | New user | - |
| `updated_contact` | Updated contact | - |
| `updated_conversation` | Updated conversation | - |
| `updated_user` | Updated user | - |


## Actions (12)

| Internal name | Title | Batch |
|---|---|---|
| `__adhoc_http_action` | Custom action | - |
| `add_conversation_note` | Add conversation note | - |
| `archive_users` | Archive users | yes |
| `get_conversation_by_id` | Get conversation by ID | - |
| `reply_conversation` | Reply to conversation as user | - |
| `search_conversations_by_user` | Search conversations by user | yes |
| `search_notes_by_user` | Search notes by user | yes |
| `search_segments_by_user` | Search segments by user | yes |
| `search_tags_by_user` | Search tags by user | yes |
| `search_user` | Search user | - |
| `update_user` | Update user | - |
| `upsert_users` | Create/update users | yes |


## Validation

```bash
wk lint <recipe>.recipe.json --skills-path <path-to>/skills
```
