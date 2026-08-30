# Gmail recipes

Provider value to use in every step: `gmail`

This skill extends the base `workato-recipes` skill. Read that first for recipe JSON structure, datapill syntax, and control flow; this document only covers what is specific to this connector.

## Before you generate

- Set `"provider": "gmail"` on every step that uses this connector.
- Use only the internal names listed below. They are the same list `lint-rules.json` enforces, so anything else fails `wk lint`.
- Reach for `__adhoc_http_action` only when no native operation covers the call.

## Triggers (1)

| Internal name | Title | Batch |
|---|---|---|
| `new_email` | New email | - |


## Actions (3)

| Internal name | Title | Batch |
|---|---|---|
| `__adhoc_http_action` | Custom action | - |
| `download_attachment` | Download attachment | - |
| `send_mail` | Send email | - |


## Field details

Input/output field definitions observed from the Workato UI. The Workato API does not expose these, so treat them as the authoritative source for required fields and types.

### new_email (Trigger)

Recipe: Upload Gmail attachments to Google Drive

#### Input fields
| Field | Type | Required | Description |
|---|---|---|---|
| label_ids | string | Yes | Gmail label (e.g. INBOX) |

#### Output fields
| Field | Type | Description |
|---|---|---|
| id | string | Email ID |
| subject | string | Email subject |
| attachments | array | List of attachments |
| attachments[].filename | string | Attachment filename |
| attachments[].attachmentId | string | Attachment ID |

#### Job Report columns
| Column | Label | Mapping |
|---|---|---|
| custom_column_3 | Email subject | `data.gmail.new_email.subject` |
| custom_column_1 | Number of files | `data.gmail.new_email.attachments` (list size) |
| custom_column_2 | File names | Concatenated `filename` values from `data.gmail.new_email.attachments` |

---

### download_attachment (Action)

Recipe: Upload Gmail attachments to Google Drive

#### Input fields
| Field | Type | Required | Description |
|---|---|---|---|
| id | string | Yes | Email ID (datapill: new_email.id) |
| attachmentId | string | Yes | Attachment ID (datapill: foreach.attachmentId) |

#### Output fields
| Field | Type | Description |
|---|---|---|
| content_bytes | string | Binary content of the attachment |

---

### send_mail (Action)

Kind: Action
Learned from: `/auto-learn` (UI observation) — 2026-04-27

#### Input fields
| Field | Type | Required | Visible by default | Description |
|---|---|---|---|---|
| To | string | Yes | Yes | Provide the recipient email address(es) separated by comma. |
| Subject | string | Yes | Yes | — |
| Email type | select | - | Yes | Select the format of the email message（`Text` / `HTML`） |
| Message | string | - | Yes | Plain text if selected email type is Text, HTML formatted if selected email type is HTML |
| From | string | - | No | — |
| Bcc | string | - | No | — |
| Cc | string | - | No | — |
| Reply to | string | - | No | — |
| Attachments[].File binary content | string | - | No | List-type group field |
| Attachments[].File name | string | - | No | List-type group field |

#### Output fields
| Field | Type | Description |
|---|---|---|
| id | string | ID of the sent email |
| thread_id | string | Thread ID |
| label_ids | string | Applied labels (e.g. `UNREAD`) |


## Validation

```bash
wk lint <recipe>.recipe.json --skills-path <path-to>/skills
```
