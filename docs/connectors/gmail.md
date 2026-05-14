# Gmail connector

Provider: `gmail`

## Triggers

| Name | Internal name | Batch | Description |
|---|---|---|---|
| New email | `new_email` | - |  |

## Actions

| Name | Internal name | Batch | Description |
|---|---|---|---|
| Custom action | `__adhoc_http_action` | - |  |
| Download attachment | `download_attachment` | - |  |
| Send email | `send_mail` | - |  |

## Field details

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

## Custom Action pattern

For Gmail, the `gmail` provider lets you call the Gmail API directly via `__adhoc_http_action`.
- Example path: `me/messages/{messageId}?format=full`
- base URI: `https://gmail.googleapis.com/gmail/v1/users/`

## Notes
- OAuth 2.0 authentication
- provider name: `gmail`
- Scopes: read, compose, and send email

---

## MCP Skills (Gmail MCP Server)

Genie skills defined in the project `MCP | Gmail`. Each skill is implemented with the `workato_genie` / `start_workflow` trigger.

---

### search_messages

Search messages. Prefer structured parameters; use `raw_query` only when you need native Gmail search syntax directly.

#### Parameters
| Field | Type | Required | Description |
|---|---|---|---|
| keywords | string | - | Free-text keywords to search for across subject and message content. |
| from | string | - | Filter messages sent by this email address. |
| to | string | - | Filter messages sent to this email address. |
| participants | array of string | - | Filter messages involving any of the specified email addresses. |
| labels | array of string | - | Restrict results to messages with specific labels. |
| has_attachments | boolean | - | When true, return only messages with attachments. |
| start_time | date_time | - | ISO 8601 timestamp specifying the start of the search window. |
| end_time | date_time | - | ISO 8601 timestamp specifying the end of the search window. |
| limit | string | - | Maximum number of messages to return. Default 20, max 50. |
| raw_query | string | - | Advanced Gmail search query using native Gmail search syntax. Must not be combined with structured search parameters. |
| pageToken | string | - | Page token to retrieve a specific page of results in the list. |
| includeSpamTrash | boolean | - | Include threads from SPAM and TRASH in the results. Default false. |

#### Result
| Field | Type | Description |
|---|---|---|
| error | string | Error message (transient error) |
| messages[].bcc | string | Bcc |
| messages[].cc | string | Cc |
| messages[].timestamp | date_time | Timestamp |
| messages[].sender | string | Sender |
| messages[].subject | string | Subject |
| messages[].threadId | string | Thread ID |
| messages[].messageId | string | Message ID |
| nextPageToken | string | Next page token |
| resultSizeEstimate | string | Result size estimate |
| has_more | boolean | Has more |

---

### search_threads

Search threads. Parameters are identical to search_messages.

#### Parameters
| Field | Type | Required | Description |
|---|---|---|---|
| keywords | string | - | Free-text keywords to search for across subject and message content. |
| from | string | - | Filter messages sent by this email address. |
| to | string | - | Filter messages sent to this email address. |
| participants | array of string | - | Filter messages involving any of the specified email addresses. |
| labels | array of string | - | Restrict results to messages with specific labels. |
| has_attachments | boolean | - | When true, return only messages with attachments. |
| start_time | date_time | - | ISO 8601 timestamp specifying the start of the search window. |
| end_time | date_time | - | ISO 8601 timestamp specifying the end of the search window. |
| limit | string | - | Maximum number of messages to return. Default 20, max 50. |
| raw_query | string | - | Advanced Gmail search query using native Gmail search syntax. Must not be combined with structured search parameters. |
| pageToken | string | - | Page token to retrieve a specific page of results in the list. |
| includeSpamTrash | boolean | - | Include threads from SPAM and TRASH in the results. Default false. |

#### Result
| Field | Type | Description |
|---|---|---|
| error | string | Error message (transient error) |
| threads[].bcc | string | Bcc |
| threads[].cc | string | Cc |
| threads[].timestamp | date_time | Timestamp |
| threads[].sender | string | Sender |
| threads[].subject | string | Subject |
| threads[].threadId | string | Thread ID |
| threads[].messageId | string | Message ID |
| nextPageToken | string | Next page token |
| resultSizeEstimate | string | Result size estimate |
| has_more | boolean | Has more |

---

### get_message

Fetch the full content of a single message by message ID.

#### Parameters
| Field | Type | Required | Description |
|---|---|---|---|
| messageId | string | Yes | ID of the message to retrieve. |

#### Result
| Field | Type | Description |
|---|---|---|
| error | string | Error message (transient error) |
| id | string | Message ID |
| threadId | string | Thread ID |
| labelIds | array of string | Label IDs |
| snippet | string | Snippet |
| payload.partId | string | Part ID |
| payload.mimeType | string | MIME type |
| payload.filename | string | Filename |
| payload.headers[].name | string | Header name |
| payload.headers[].value | string | Header value |
| payload.body.size | number | Body size |
| payload.parts[].partId | string | Part ID |
| payload.parts[].mimeType | string | MIME type |
| payload.parts[].filename | string | Filename |
| payload.parts[].headers[].name | string | Header name |
| payload.parts[].headers[].value | string | Header value |
| payload.parts[].body.size | number | Body size |
| payload.parts[].parts[].body.data | string | Body data (deepest level) |
| sizeEstimate | number | Size estimate |
| historyId | string | History ID |
| internalDate | string | Internal date |

---

### get_thread

Fetch an entire thread by thread ID.

#### Parameters
| Field | Type | Required | Description |
|---|---|---|---|
| threadId | string | Yes | ID of the thread to retrieve. |

#### Result
| Field | Type | Description |
|---|---|---|
| error | string | Error message (transient error) |
| id | string | Thread ID |
| historyId | string | History ID |
| messages[].id | string | Message ID |
| messages[].threadId | string | Thread ID |
| messages[].labelIds | array of string | Label IDs |
| messages[].snippet | string | Snippet |
| messages[].sizeEstimate | number | Size estimate |
| messages[].historyId | string | History ID |
| messages[].internalDate | string | Internal date |

---

### get_draft

Fetch draft details by draft ID.

#### Parameters
| Field | Type | Required | Description |
|---|---|---|---|
| draftId | string | Yes | ID of the draft to fetch |

#### Result
| Field | Type | Description |
|---|---|---|
| error | string | Error message (transient error) |
| id | string | Draft ID |
| message.id | string | Message ID |
| message.threadId | string | Thread ID |
| message.snippet | string | Snippet |
| message.historyId | number | History ID |
| message.internalDate | number | Internal date |
| message.sizeEstimate | number | Size estimate |
| message.payload.body.attachmentId | string | Attachment ID |
| message.payload.body.data | string | Body data |
| message.payload.body.size | number | Body size |
| message.payload.filename | string | Filename |
| message.payload.mimeType | string | MIME type |
| message.payload.partId | string | Part ID |
| message.payload.headers[].name | string | Header name |
| message.payload.headers[].value | string | Header value |
| message.payload.parts[] | array of object | Nested parts (recursive) |

---

### list_drafts

List drafts.

#### Parameters
| Field | Type | Required | Description |
|---|---|---|---|
| query | string | - | Filter using the same query format as the Gmail search box |
| pageToken | string | - | Page token to retrieve a specific page of results in the list. |
| maxResults | integer | - | Maximum number of drafts to return. Default 30, max 50. |

#### Result
| Field | Type | Description |
|---|---|---|
| error | string | Error message (transient error) |
| drafts[].id | string | Draft ID |
| drafts[].message.id | string | Message ID |
| drafts[].message.threadId | string | Thread ID |
| drafts[].message.snippet | string | Snippet |
| drafts[].message.historyId | number | History ID |
| drafts[].message.internalDate | number | Internal date |
| drafts[].message.sizeEstimate | number | Size estimate |
| drafts[].message.payload | object | Payload (body, headers, parts — recursive structure) |
| nextPageToken | string | Next page token |
| has_more | boolean | Has more |

---

### list_labels

List system and user-defined labels available to the authenticated user.

#### Parameters

No parameters.

#### Result
| Field | Type | Description |
|---|---|---|
| error | string | Error message (transient error) |
| labels[].type | string | Label type (system / user) |
| labels[].name | string | Label name |
| labels[].id | string | Label ID |

---

### list_attachments

List attachments by message ID.

#### Parameters
| Field | Type | Required | Description |
|---|---|---|---|
| messageId | string | Yes | ID of the message to retrieve. |

#### Result
| Field | Type | Description |
|---|---|---|
| error | string | Error message (transient error) |
| id | string | Message ID |
| threadId | string | Thread ID |
| payload | string | Payload (attachments metadata) |

---

### create_draft

Create a new draft. For replies, threadId / inReplyTo / references are required.

#### Parameters
| Field | Type | Required | Description |
|---|---|---|---|
| to | array of string | - | Recipients. Specify when creating a new email or a reply-to. Can be omitted for thread replies. |
| cc | array of string | - | CC recipients. Only when explicitly specified by the user. |
| bcc | array of string | - | BCC recipients. Only when explicitly specified by the user. |
| subject | string | - | Subject. Must match the original email when replying. |
| body | string | Yes | Email body. Signature, disclaimers, and quoted content are not added unless explicitly requested. |
| bodyFormat | string | - | plain_text (default) or html. |
| threadId | string | - | Set only when replying. Associates the draft with the thread. |
| inReplyTo | string | - | Required when replying. The Message-ID header value of the original message. |
| references | string | - | Required when replying. The original References header plus Message-ID. |

#### Result
| Field | Type | Description |
|---|---|---|
| error | string | Error message (transient error) |
| id | string | Draft ID |
| message.id | string | Message ID |
| message.threadId | string | Thread ID |
| message.snippet | string | Snippet |
| message.historyId | number | History ID |
| message.internalDate | number | Internal date |
| message.sizeEstimate | number | Size estimate |
| message.payload | object | Payload (body, headers, parts — recursive structure) |

---

### update_draft

Edit an existing draft. Use a separate skill to add or remove attachments.

#### Parameters
| Field | Type | Required | Description |
|---|---|---|---|
| draftId | string | Yes | Draft ID |
| to | array of string | - | Recipients |
| cc | array of string | - | CC recipients |
| bcc | array of string | - | BCC recipients |
| subject | string | - | Subject |
| body | string | - | Email body |
| bodyFormat | string | - | plain_text (default) or html |

#### Result
| Field | Type | Description |
|---|---|---|
| error | string | Error message (transient error) |
| id | string | Draft ID |
| message.id | string | Message ID |
| message.threadId | string | Thread ID |
| message.snippet | string | Snippet |
| message.historyId | number | History ID |
| message.internalDate | number | Internal date |
| message.sizeEstimate | number | Size estimate |
| message.payload | object | Payload (body, headers, parts — recursive structure) |

---

### send_draft

Send a draft. Requires an existing draft that has been created or referenced beforehand.

#### Parameters
| Field | Type | Required | Description |
|---|---|---|---|
| draftId | string | Yes | ID of the draft to send |

#### Result
| Field | Type | Description |
|---|---|---|
| error | string | Error message (transient error) |
| id | string | Message ID |
| threadId | string | Thread ID |
| historyId | number | History ID |
| internalDate | number | Internal date |
| sizeEstimate | number | Size estimate |
| snippet | string | Snippet |
| payload.body | object | Body (attachmentId, data, size) |
| payload.filename | string | Filename |
| payload.mimeType | string | MIME type |
| payload.partId | string | Part ID |
| payload.headers[].name | string | Header name |
| payload.headers[].value | string | Header value |
| payload.parts[] | array of object | Nested parts (recursive) |

---

### add_labels

Add labels to messages or threads. Look up label IDs with list_labels beforehand.

#### Parameters
| Field | Type | Required | Description |
|---|---|---|---|
| messages | array of string | - | List of Gmail message IDs. Max 10 entries. Either messages or threads is required. |
| threads | array of string | - | List of Gmail thread IDs. Max 10 entries. |
| labels | array of string | Yes | List of label IDs to apply (e.g. INBOX, UNREAD, STARRED). Use the ID, not the display name. |

#### Result
| Field | Type | Description |
|---|---|---|
| error | string | Error message (transient error) |
| threads[].labelIds | array of string | Label IDs |
| threads[].threadId | string | Thread ID |
| threads[].id | string | ID |
| messages[].labelIds | array of string | Label IDs |
| messages[].messageId | string | Message ID |
| messages[].id | string | ID |

---

### remove_labels

Remove labels from messages or threads. Look up label IDs with list_labels beforehand.

#### Parameters
| Field | Type | Required | Description |
|---|---|---|---|
| messages | array of string | - | List of Gmail message IDs. Max 10 entries. Either messages or threads is required. |
| threads | array of string | - | List of Gmail thread IDs. Max 10 entries. |
| labels | array of string | Yes | List of label IDs to remove. Use the ID, not the display name. |

#### Result
| Field | Type | Description |
|---|---|---|
| error | string | Error message (transient error) |
| threads[].labelIds | array of string | Label IDs |
| threads[].threadId | string | Thread ID |
| threads[].id | string | ID |
| messages[].labelIds | array of string | Label IDs |
| messages[].messageId | string | Message ID |
| messages[].id | string | ID |

---

### add_attachments

Add attachments to an existing draft. The source can be an existing Gmail attachment or a Google Drive file.

#### Parameters
| Field | Type | Required | Description |
|---|---|---|---|
| draftId | string | Yes | Draft ID |
| attachments | array of object | Yes | Array of attachments. At least 1 entry is required. |
| attachments[].source | string | Yes | "gmail" or "gdrive" |
| attachments[].filename | string | Yes | Filename (with extension, e.g. report.csv) |
| attachments[].mimeType | string | Yes | MIME type. For Google-native files, specify the export format. |
| attachments[].fileId | string | - | Required when source is "gdrive". Google Drive file ID. |
| attachments[].attachmentId | string | - | Required when source is "gmail". Gmail attachment ID. |
| attachments[].messageId | string | - | Required when source is "gmail". Message ID of the source attachment. |

#### Result
| Field | Type | Description |
|---|---|---|
| error | string | Error message (transient error) |
| id | string | Draft ID |
| message.id | string | Message ID |
| message.threadId | string | Thread ID |
| message.snippet | string | Snippet |
| message.payload | object | Payload (body, headers, parts — recursive structure) |

---

### remove_attachments

Remove attachments from an existing draft.

#### Parameters
| Field | Type | Required | Description |
|---|---|---|---|
| draftId | string | Yes | Draft ID |
| fileNames | array of string | Yes | List of attachment filenames to remove. Specify filenames that exist on the draft. |

#### Result
| Field | Type | Description |
|---|---|---|
| error | string | Error message (transient error) |
| id | string | Draft ID |
| message.id | string | Message ID |
| message.threadId | string | Thread ID |
| message.snippet | string | Snippet |
| message.payload | object | Payload (body, headers, parts — recursive structure) |

---

### star_messages

Star messages.

#### Parameters
| Field | Type | Required | Description |
|---|---|---|---|
| starMessages | array of object | - | Array of messages to star. Max 10 entries. |
| starMessages[].messageId | string | Yes | Id of the message to be starred |

#### Result
| Field | Type | Description |
|---|---|---|
| error | string | Error message (transient error) |
| starMarkedMessages[].labelIds | string | Label IDs |
| starMarkedMessages[].messageId | string | Message ID |
| starMarkedMessages[].id | string | ID |

---

### unstar_messages

Remove stars from messages.

#### Parameters
| Field | Type | Required | Description |
|---|---|---|---|
| unStarMessages | array of object | - | Array of messages to unstar. Max 10 entries. |
| unStarMessages[].messageId | string | Yes | Id of the message to be unstarred |

#### Result
| Field | Type | Description |
|---|---|---|
| error | string | Error message (transient error) |
| unStarMarkedMessages[].labelIds | string | Label IDs |
| unStarMarkedMessages[].messageId | string | Message ID |
| unStarMarkedMessages[].id | string | ID |

---

### archive_threads

Archive threads (removes the INBOX label).

#### Parameters
| Field | Type | Required | Description |
|---|---|---|---|
| archiveThreads | array of object | Yes | Array of threads to archive. Max 10 entries. |
| archiveThreads[].threadId | string | Yes | Id of the thread to be archived |

#### Result
| Field | Type | Description |
|---|---|---|
| error | string | Error message (transient error) |
| archivedThreads[].labelIds | string | Label IDs |
| archivedThreads[].threadId | string | Thread ID |
| archivedThreads[].id | string | ID |

---

### unarchive_threads

Move archived threads back to the inbox.

#### Parameters
| Field | Type | Required | Description |
|---|---|---|---|
| unArchiveThreads | array of object | Yes | Array of threads to unarchive. Max 10 entries. |
| unArchiveThreads[].threadId | string | Yes | Id of the thread to be unarchived |

#### Result
| Field | Type | Description |
|---|---|---|
| error | string | Error message (transient error) |
| unArchivedThreads[].labelIds | string | Label IDs |
| unArchivedThreads[].threadId | string | Thread ID |
| unArchivedThreads[].id | string | ID |

---

### mark_message_read_state

Mark messages as read or unread.

#### Parameters
| Field | Type | Required | Description |
|---|---|---|---|
| readMessageIds | array of object | - | Array of messages to mark as read. Max 10 entries. |
| readMessageIds[].messageId | string | Yes | ID of the Gmail message to be marked as read. |
| unreadMessageIds | array of object | - | Array of messages to mark as unread. Max 10 entries. |
| unreadMessageIds[].messageId | string | Yes | ID of the Gmail message to be marked as unread. |

#### Result
| Field | Type | Description |
|---|---|---|
| error | string | Error message (transient error) |
| markedMessagesRead[].labelIds | string | Label IDs |
| markedMessagesRead[].messageId | string | Message ID |
| markedMessagesRead[].id | string | ID |
| markedMessageUnread[].labelIds | string | Label IDs |
| markedMessageUnread[].messageId | string | Message ID |
| markedMessageUnread[].id | string | ID |

---

## Learning summary

Last run: 2026-04-27 by `/auto-learn`
- Attempted: 1 op
- Fully learned: 1
- Partially learned: 0
- Failed: 0
- Skipped:
  - Deprecated: 0
  - adhoc: 1 — `__adhoc_http_action`
  - Already learned: 2 — `new_email`, `download_attachment`

No follow-up needed.
