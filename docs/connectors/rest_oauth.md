# HTTP (OAuth2) connector

Provider: `rest_oauth`

## Triggers

| Name | Internal name | Batch | Description |
|---|---|---|---|
| New event via webhook | `new_event` | - |  [deprecated] |
| New event via polling | `new_poll_event` | - |  |

## Actions

| Name | Internal name | Batch | Description |
|---|---|---|---|
| Send request and wait for response | `make_proxy_request` | - |  [deprecated] |
| Make REST request | `make_request` | - |  [deprecated] |
| Send request | `make_request_v2` | - |  |
