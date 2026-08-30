# Amazon SQS recipes

Provider value to use in every step: `aws_sqs`

This skill extends the base `workato-recipes` skill. Read that first for recipe JSON structure, datapill syntax, and control flow; this document only covers what is specific to this connector.

## Before you generate

- Set `"provider": "aws_sqs"` on every step that uses this connector.
- Use only the internal names listed below. They are the same list `lint-rules.json` enforces, so anything else fails `wk lint`.
- This connector has no custom-action escape hatch; if no native operation fits, use the HTTP connector instead.

## Triggers (2)

| Internal name | Title | Batch |
|---|---|---|
| `new_message` | New message | - |
| `new_messages_batch` | New messages | yes |


## Actions (5)

| Internal name | Title | Batch |
|---|---|---|
| `delete_message` | Delete message | - |
| `delete_messages_batch` | Delete messages | yes |
| `receive_message` | Receive message | - |
| `send_message` | Send message | - |
| `send_messages_batch` | Send messages | yes |


## Validation

```bash
wk lint <recipe>.recipe.json --skills-path <path-to>/skills
```
