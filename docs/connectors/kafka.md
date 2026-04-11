# Apache Kafka コネクタ

Provider: `kafka`

## Triggers

| 名前 | provider 内名称 | Batch | 説明 |
|---|---|---|---|
| New message in topic (Deprecated) | `new_message` | - |  |
| New messages in topic (Deprecated) | `new_message_batch` | Yes |  |
| New messages in topic | `new_message_batch_v2` | Yes |  |
| New message in topic | `new_message_v2` | - |  |

## Actions

| 名前 | provider 内名称 | Batch | 説明 |
|---|---|---|---|
| Publish message | `publish_to_topic` | - |  |
| Publish messages | `publish_to_topic_batch` | Yes |  |
