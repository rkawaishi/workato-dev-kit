# Workato Event Streams recipes

Provider value to use in every step: `workato_pub_sub`

This skill extends the base `workato-recipes` skill. Read that first for recipe JSON structure, datapill syntax, and control flow; this document only covers what is specific to this connector.

## Before you generate

- Set `"provider": "workato_pub_sub"` on every step that uses this connector.
- Use only the internal names listed below. They are the same list `lint-rules.json` enforces, so anything else fails `wk lint`.
- This connector has no custom-action escape hatch; if no native operation fits, use the HTTP connector instead.

## Triggers (2)

| Internal name | Title | Batch |
|---|---|---|
| `batch_subscribe_to_topic` | New batch of messages | yes |
| `subscribe_to_topic` | New message | - |


## Actions (2)

| Internal name | Title | Batch |
|---|---|---|
| `publish_to_topic` | Publish message | - |
| `publish_to_topic_batch` | Publish messages (batch) | yes |


## Validation

```bash
wk lint <recipe>.recipe.json --skills-path <path-to>/skills
```
