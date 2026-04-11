# Workato Event Streams コネクタ

Provider: `workato_pub_sub`

## Triggers

| 名前 | provider 内名称 | Batch | 説明 |
|---|---|---|---|
| New batch of messages | `batch_subscribe_to_topic` | Yes |  |
| New message | `subscribe_to_topic` | - |  |

## Actions

| 名前 | provider 内名称 | Batch | 説明 |
|---|---|---|---|
| Publish message | `publish_to_topic` | - |  |
| Publish messages (batch) | `publish_to_topic_batch` | Yes |  |
