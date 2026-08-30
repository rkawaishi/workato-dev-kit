# JMS tools by Workato recipes

Provider value to use in every step: `jms`

This skill extends the base `workato-recipes` skill. Read that first for recipe JSON structure, datapill syntax, and control flow; this document only covers what is specific to this connector.

## Before you generate

- Set `"provider": "jms"` on every step that uses this connector.
- Use only the internal names listed below. They are the same list `lint-rules.json` enforces, so anything else fails `wk lint`.
- This connector has no custom-action escape hatch; if no native operation fits, use the HTTP connector instead.

## Triggers (2)

| Internal name | Title | Batch |
|---|---|---|
| `new_message_queue` | New message in queue | - |
| `new_message_topic` | New message in topic | - |


## Actions (3)

| Internal name | Title | Batch |
|---|---|---|
| `publish_to_queue` | Publish message to queue | - |
| `publish_to_topic` | Publish message to topic | - |
| `receive_message_from_queue` | Receive message from queue | - |


## Validation

```bash
wk lint <recipe>.recipe.json --skills-path <path-to>/skills
```
