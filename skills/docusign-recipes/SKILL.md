# DocuSign recipes

Provider value to use in every step: `docusign`

This skill extends the base `workato-recipes` skill. Read that first for recipe JSON structure, datapill syntax, and control flow; this document only covers what is specific to this connector.

## Before you generate

- Set `"provider": "docusign"` on every step that uses this connector.
- Use only the internal names listed below. They are the same list `lint-rules.json` enforces, so anything else fails `wk lint`.
- Reach for `__adhoc_http_action` only when no native operation covers the call.

## Triggers (3)

| Internal name | Title | Batch |
|---|---|---|
| `new_document_received` | New document received | - |
| `new_event` | New document event | - |
| `new_recipient_event` | New recipient event | - |


## Actions (5)

| Internal name | Title | Batch |
|---|---|---|
| `__adhoc_http_action` | Custom action | - |
| `create_envelope` | Create/send document | - |
| `download_document` | Download document | - |
| `list_documents` | List documents in envelope | yes |
| `send_envelope` | Send document using a template | - |


## Deprecated -- do not generate

Workato still executes these in existing recipes, but new recipes must not use them. They are excluded from `valid_action_names`.


### Triggers

| Internal name | Title | Batch |
|---|---|---|
| `new_signed_document` | New signed document | - |


## Validation

```bash
wk lint <recipe>.recipe.json --skills-path <path-to>/skills
```
