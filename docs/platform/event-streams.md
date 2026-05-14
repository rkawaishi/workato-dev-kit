# Event Streams

Official: https://docs.workato.com/en/event-streams.html

## Overview

A feature that enables event-driven, message-oriented architecture. Decouples publishers and consumers, enabling asynchronous coordination between recipes.

## Key features

- **Delivery guarantees**: Reliable delivery via message persistence
- **Sequential chaining**: Ordered execution across recipes
- **Zero-downtime updates**: Adding or changing consumers does not affect the publisher
- **Simpler management**: Reduces the complexity of creating, testing, and maintaining recipes

## Architecture

```
Publisher recipe → Topic → Consumer recipe 1
                        → Consumer recipe 2
                        → Consumer recipe 3
```

| Component | Description |
|---|---|
| **Publisher** | A recipe that publishes messages |
| **Consumer** | A recipe that receives and processes messages (multiple allowed) |
| **Topic** | A named channel that holds messages (identified by a unique ID or timestamp) |

## How to use

1. **Workato Event Streams connector**: Publish and consume messages from within recipes
2. **Public API**: Programmatically publish messages and retrieve topic data

## Access

Manage topics from Platform > Event streams.

## Example use cases

- Asynchronous communication between microservices
- Broadcasting events to multiple recipes
- Staged execution of processing pipelines
- Real-time data synchronization across systems
