# HTTP コネクタ

Provider: `rest`

## Triggers

| 名前 | provider 内名称 | Batch | 説明 |
|---|---|---|---|
| New event via webhook | `new_event` | - |  [deprecated] |
| New event via polling | `new_poll_event` | - |  |

## Actions

| 名前 | provider 内名称 | Batch | 説明 |
|---|---|---|---|
| Send request and wait for response | `make_proxy_request` | - |  [deprecated] |
| Make REST request | `make_request` | - |  [deprecated] |
| Send request | `make_request_v2` | - |  |
