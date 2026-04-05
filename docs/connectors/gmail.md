# Gmail コネクタ

公式: https://docs.workato.com/en/connectors/gmail.html
Provider: `gmail`

## Triggers
| 名前 | 説明 |
|---|---|
| New email | 新着メール受信 |

## Actions
| 名前 | 説明 |
|---|---|
| Download attachment | 添付ファイルダウンロード |
| Send email | メール送信 |

## フィールド詳細

### new_email (Trigger)

レシピ: Upload Gmail attachments to Google Drive

#### Input fields
| フィールド | 型 | 必須 | 説明 |
|---|---|---|---|
| label_ids | string | Yes | Gmail ラベル（例: INBOX） |

#### Output fields
| フィールド | 型 | 説明 |
|---|---|---|
| id | string | メール ID |
| subject | string | メール件名 |
| attachments | array | 添付ファイル一覧 |
| attachments[].filename | string | 添付ファイル名 |
| attachments[].attachmentId | string | 添付ファイル ID |

#### Job Report カラム
| カラム | ラベル | マッピング |
|---|---|---|
| custom_column_3 | Email subject | `data.gmail.new_email.subject` |
| custom_column_1 | Number of files | `data.gmail.new_email.attachments` (リストサイズ) |
| custom_column_2 | File names | `data.gmail.new_email.attachments` の `filename` を結合 |

---

### download_attachment (Action)

レシピ: Upload Gmail attachments to Google Drive

#### Input fields
| フィールド | 型 | 必須 | 説明 |
|---|---|---|---|
| id | string | Yes | メール ID（datapill: new_email.id） |
| attachmentId | string | Yes | 添付ファイル ID（datapill: foreach.attachmentId） |

#### Output fields
| フィールド | 型 | 説明 |
|---|---|---|
| content_bytes | string | 添付ファイルのバイナリコンテンツ |

## Custom Action パターン

Gmail は `gmail` プロバイダーで `__adhoc_http_action` を使用して Gmail API を直接呼び出せる。
- パス例: `me/messages/{messageId}?format=full`
- base URI: `https://gmail.googleapis.com/gmail/v1/users/`

## 備考
- OAuth 2.0 認証
- provider 名: `gmail`
- スコープ: メールの読み取り、作成、送信

---

## MCP Skills (Gmail MCP Server)

プロジェクト `MCP | Gmail` で定義された Genie スキル群。各スキルは `workato_genie` / `start_workflow` トリガーで実装。

---

### search_messages

メッセージを検索する。構造化パラメータ優先、`raw_query` は Gmail 検索構文を直接使う場合のみ。

#### Parameters
| フィールド | 型 | 必須 | 説明 |
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
| フィールド | 型 | 説明 |
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

スレッドを検索する。パラメータは search_messages と同一。

#### Parameters
| フィールド | 型 | 必須 | 説明 |
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
| フィールド | 型 | 説明 |
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

メッセージ ID を指定して単一メッセージの全内容を取得する。

#### Parameters
| フィールド | 型 | 必須 | 説明 |
|---|---|---|---|
| messageId | string | Yes | ID of the message to retrieve. |

#### Result
| フィールド | 型 | 説明 |
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

スレッド ID を指定してスレッド全体を取得する。

#### Parameters
| フィールド | 型 | 必須 | 説明 |
|---|---|---|---|
| threadId | string | Yes | ID of the thread to retrieve. |

#### Result
| フィールド | 型 | 説明 |
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

下書き ID を指定して下書きの詳細を取得する。

#### Parameters
| フィールド | 型 | 必須 | 説明 |
|---|---|---|---|
| draftId | string | Yes | ID of the draft to fetch |

#### Result
| フィールド | 型 | 説明 |
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

下書き一覧を取得する。

#### Parameters
| フィールド | 型 | 必須 | 説明 |
|---|---|---|---|
| query | string | - | Gmail search box と同じクエリ形式でフィルタ |
| pageToken | string | - | Page token to retrieve a specific page of results in the list. |
| maxResults | integer | - | Maximum number of drafts to return. Default 30, max 50. |

#### Result
| フィールド | 型 | 説明 |
|---|---|---|
| error | string | Error message (transient error) |
| drafts[].id | string | Draft ID |
| drafts[].message.id | string | Message ID |
| drafts[].message.threadId | string | Thread ID |
| drafts[].message.snippet | string | Snippet |
| drafts[].message.historyId | number | History ID |
| drafts[].message.internalDate | number | Internal date |
| drafts[].message.sizeEstimate | number | Size estimate |
| drafts[].message.payload | object | Payload (body, headers, parts -- 再帰構造) |
| nextPageToken | string | Next page token |
| has_more | boolean | Has more |

---

### list_labels

認証ユーザーが利用可能なシステム/ユーザー定義ラベル一覧を取得する。

#### Parameters

パラメータなし。

#### Result
| フィールド | 型 | 説明 |
|---|---|---|
| error | string | Error message (transient error) |
| labels[].type | string | Label type (system / user) |
| labels[].name | string | Label name |
| labels[].id | string | Label ID |

---

### list_attachments

メッセージ ID を指定して添付ファイル一覧を取得する。

#### Parameters
| フィールド | 型 | 必須 | 説明 |
|---|---|---|---|
| messageId | string | Yes | ID of the message to retrieve. |

#### Result
| フィールド | 型 | 説明 |
|---|---|---|
| error | string | Error message (transient error) |
| id | string | Message ID |
| threadId | string | Thread ID |
| payload | string | Payload (attachments metadata) |

---

### create_draft

新規下書きを作成する。返信の場合は threadId / inReplyTo / references が必須。

#### Parameters
| フィールド | 型 | 必須 | 説明 |
|---|---|---|---|
| to | array of string | - | 宛先。新規 or reply-to 時に指定。スレッド返信では省略可。 |
| cc | array of string | - | CC recipients。ユーザーが明示した場合のみ。 |
| bcc | array of string | - | BCC recipients。ユーザーが明示した場合のみ。 |
| subject | string | - | 件名。返信時は元メールと同一必須。 |
| body | string | Yes | メール本文。署名・免責・引用は明示指示がない限り不要。 |
| bodyFormat | string | - | plain_text (default) or html。 |
| threadId | string | - | 返信時のみ設定。スレッドとの関連付け。 |
| inReplyTo | string | - | 返信時必須。元メッセージの Message-ID ヘッダ値。 |
| references | string | - | 返信時必須。元の References ヘッダ + Message-ID。 |

#### Result
| フィールド | 型 | 説明 |
|---|---|---|
| error | string | Error message (transient error) |
| id | string | Draft ID |
| message.id | string | Message ID |
| message.threadId | string | Thread ID |
| message.snippet | string | Snippet |
| message.historyId | number | History ID |
| message.internalDate | number | Internal date |
| message.sizeEstimate | number | Size estimate |
| message.payload | object | Payload (body, headers, parts -- 再帰構造) |

---

### update_draft

既存の下書きを編集する。添付の追加/削除は別スキルを使用。

#### Parameters
| フィールド | 型 | 必須 | 説明 |
|---|---|---|---|
| draftId | string | Yes | Draft ID |
| to | array of string | - | 宛先 |
| cc | array of string | - | CC recipients |
| bcc | array of string | - | BCC recipients |
| subject | string | - | 件名 |
| body | string | - | メール本文 |
| bodyFormat | string | - | plain_text (default) or html |

#### Result
| フィールド | 型 | 説明 |
|---|---|---|
| error | string | Error message (transient error) |
| id | string | Draft ID |
| message.id | string | Message ID |
| message.threadId | string | Thread ID |
| message.snippet | string | Snippet |
| message.historyId | number | History ID |
| message.internalDate | number | Internal date |
| message.sizeEstimate | number | Size estimate |
| message.payload | object | Payload (body, headers, parts -- 再帰構造) |

---

### send_draft

下書きを送信する。事前に作成/参照済みの下書きが必要。

#### Parameters
| フィールド | 型 | 必須 | 説明 |
|---|---|---|---|
| draftId | string | Yes | ID of the draft to send |

#### Result
| フィールド | 型 | 説明 |
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

メッセージまたはスレッドにラベルを追加する。事前に list_labels でラベル ID を確認すること。

#### Parameters
| フィールド | 型 | 必須 | 説明 |
|---|---|---|---|
| messages | array of string | - | Gmail message ID のリスト。最大 10 件。messages か threads のどちらか必須。 |
| threads | array of string | - | Gmail thread ID のリスト。最大 10 件。 |
| labels | array of string | Yes | 適用するラベル ID のリスト (例: INBOX, UNREAD, STARRED)。表示名ではなく ID を使用。 |

#### Result
| フィールド | 型 | 説明 |
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

メッセージまたはスレッドからラベルを削除する。事前に list_labels でラベル ID を確認すること。

#### Parameters
| フィールド | 型 | 必須 | 説明 |
|---|---|---|---|
| messages | array of string | - | Gmail message ID のリスト。最大 10 件。messages か threads のどちらか必須。 |
| threads | array of string | - | Gmail thread ID のリスト。最大 10 件。 |
| labels | array of string | Yes | 削除するラベル ID のリスト。表示名ではなく ID を使用。 |

#### Result
| フィールド | 型 | 説明 |
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

既存の下書きに添付ファイルを追加する。Gmail 既存添付 or Google Drive ファイルをソースにできる。

#### Parameters
| フィールド | 型 | 必須 | 説明 |
|---|---|---|---|
| draftId | string | Yes | Draft ID |
| attachments | array of object | Yes | 添付ファイル配列。最低 1 件必須。 |
| attachments[].source | string | Yes | "gmail" or "gdrive" |
| attachments[].filename | string | Yes | ファイル名 (拡張子込み、例: report.csv) |
| attachments[].mimeType | string | Yes | MIME type。Google ネイティブファイルはエクスポート形式を指定。 |
| attachments[].fileId | string | - | source が "gdrive" の場合必須。Google Drive file ID。 |
| attachments[].attachmentId | string | - | source が "gmail" の場合必須。Gmail attachment ID。 |
| attachments[].messageId | string | - | source が "gmail" の場合必須。添付元の message ID。 |

#### Result
| フィールド | 型 | 説明 |
|---|---|---|
| error | string | Error message (transient error) |
| id | string | Draft ID |
| message.id | string | Message ID |
| message.threadId | string | Thread ID |
| message.snippet | string | Snippet |
| message.payload | object | Payload (body, headers, parts -- 再帰構造) |

---

### remove_attachments

既存の下書きから添付ファイルを削除する。

#### Parameters
| フィールド | 型 | 必須 | 説明 |
|---|---|---|---|
| draftId | string | Yes | Draft ID |
| fileNames | array of string | Yes | 削除する添付ファイル名のリスト。下書きに存在するファイル名を指定。 |

#### Result
| フィールド | 型 | 説明 |
|---|---|---|
| error | string | Error message (transient error) |
| id | string | Draft ID |
| message.id | string | Message ID |
| message.threadId | string | Thread ID |
| message.snippet | string | Snippet |
| message.payload | object | Payload (body, headers, parts -- 再帰構造) |

---

### star_messages

メッセージにスターを付ける。

#### Parameters
| フィールド | 型 | 必須 | 説明 |
|---|---|---|---|
| starMessages | array of object | - | スター対象メッセージの配列。最大 10 件。 |
| starMessages[].messageId | string | Yes | Id of the message to be starred |

#### Result
| フィールド | 型 | 説明 |
|---|---|---|
| error | string | Error message (transient error) |
| starMarkedMessages[].labelIds | string | Label IDs |
| starMarkedMessages[].messageId | string | Message ID |
| starMarkedMessages[].id | string | ID |

---

### unstar_messages

メッセージのスターを外す。

#### Parameters
| フィールド | 型 | 必須 | 説明 |
|---|---|---|---|
| unStarMessages | array of object | - | スター解除対象メッセージの配列。最大 10 件。 |
| unStarMessages[].messageId | string | Yes | Id of the message to be unstarred |

#### Result
| フィールド | 型 | 説明 |
|---|---|---|
| error | string | Error message (transient error) |
| unStarMarkedMessages[].labelIds | string | Label IDs |
| unStarMarkedMessages[].messageId | string | Message ID |
| unStarMarkedMessages[].id | string | ID |

---

### archive_threads

スレッドをアーカイブする (INBOX ラベルを除去)。

#### Parameters
| フィールド | 型 | 必須 | 説明 |
|---|---|---|---|
| archiveThreads | array of object | Yes | アーカイブ対象スレッドの配列。最大 10 件。 |
| archiveThreads[].threadId | string | Yes | Id of the thread to be archived |

#### Result
| フィールド | 型 | 説明 |
|---|---|---|
| error | string | Error message (transient error) |
| archivedThreads[].labelIds | string | Label IDs |
| archivedThreads[].threadId | string | Thread ID |
| archivedThreads[].id | string | ID |

---

### unarchive_threads

アーカイブ済みスレッドを受信トレイに戻す。

#### Parameters
| フィールド | 型 | 必須 | 説明 |
|---|---|---|---|
| unArchiveThreads | array of object | Yes | アーカイブ解除対象スレッドの配列。最大 10 件。 |
| unArchiveThreads[].threadId | string | Yes | Id of the thread to be unarchived |

#### Result
| フィールド | 型 | 説明 |
|---|---|---|
| error | string | Error message (transient error) |
| unArchivedThreads[].labelIds | string | Label IDs |
| unArchivedThreads[].threadId | string | Thread ID |
| unArchivedThreads[].id | string | ID |

---

### mark_message_read_state

メッセージを既読/未読に変更する。

#### Parameters
| フィールド | 型 | 必須 | 説明 |
|---|---|---|---|
| readMessageIds | array of object | - | 既読にするメッセージの配列。最大 10 件。 |
| readMessageIds[].messageId | string | Yes | ID of the Gmail message to be marked as read. |
| unreadMessageIds | array of object | - | 未読にするメッセージの配列。最大 10 件。 |
| unreadMessageIds[].messageId | string | Yes | ID of the Gmail message to be marked as unread. |

#### Result
| フィールド | 型 | 説明 |
|---|---|---|
| error | string | Error message (transient error) |
| markedMessagesRead[].labelIds | string | Label IDs |
| markedMessagesRead[].messageId | string | Message ID |
| markedMessagesRead[].id | string | ID |
| markedMessageUnread[].labelIds | string | Label IDs |
| markedMessageUnread[].messageId | string | Message ID |
| markedMessageUnread[].id | string | ID |
