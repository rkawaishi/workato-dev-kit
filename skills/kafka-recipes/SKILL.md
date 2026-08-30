# Apache Kafka recipes

Provider value to use in every step: `kafka`

This skill extends the base `workato-recipes` skill. Read that first for recipe JSON structure, datapill syntax, and control flow; this document only covers what is specific to this connector.

## Before you generate

- Set `"provider": "kafka"` on every step that uses this connector.
- Use only the internal names listed below. They are the same list `lint-rules.json` enforces, so anything else fails `wk lint`.
- This connector has no custom-action escape hatch; if no native operation fits, use the HTTP connector instead.

## Triggers (4)

| Internal name | Title | Batch |
|---|---|---|
| `new_message` | New message in topic (Deprecated) | - |
| `new_message_batch` | New messages in topic (Deprecated) | yes |
| `new_message_batch_v2` | New messages in topic | yes |
| `new_message_v2` | New message in topic | - |


## Actions (2)

| Internal name | Title | Batch |
|---|---|---|
| `publish_to_topic` | Publish message | - |
| `publish_to_topic_batch` | Publish messages | yes |


## Validation

```bash
wk lint <recipe>.recipe.json --skills-path <path-to>/skills
```
