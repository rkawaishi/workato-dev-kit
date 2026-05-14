# Apache Kafka connector

Provider: `kafka`

## Triggers

| Name | Internal name | Batch | Description |
|---|---|---|---|
| New message in topic (Deprecated) | `new_message` | - |  |
| New messages in topic (Deprecated) | `new_message_batch` | Yes |  |
| New messages in topic | `new_message_batch_v2` | Yes |  |
| New message in topic | `new_message_v2` | - |  |

## Actions

| Name | Internal name | Batch | Description |
|---|---|---|---|
| Publish message | `publish_to_topic` | - |  |
| Publish messages | `publish_to_topic_batch` | Yes |  |
