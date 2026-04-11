# SAP RFC secondary コネクタ

Provider: `sap_secondary`

## Triggers

| 名前 | provider 内名称 | Batch | 説明 |
|---|---|---|---|
| New IDocs | `new_idocs_batch` | Yes |  |
| New IDoc | `new_updated_idoc` | - |  |

## Actions

| 名前 | provider 内名称 | Batch | 説明 |
|---|---|---|---|
| Call BAPI | `call_bapi` | - |  |
| Check IDoc status | `idoc_status` | - |  |
| Send IDoc (Legacy) | `idoc_upload` | - |  [deprecated] |
| Send IDoc | `idoc_upload_new` | - |  |
| Send IDoc (Advanced) | `idoc_upload_v3` | - |  |
| Call remote function module | `run_rfm` | - |  |
| Begin transaction | `trfc_begin` | - |  |
| End transaction | `trfc_end` | - |  |
