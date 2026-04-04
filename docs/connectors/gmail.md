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

## 備考
- OAuth 2.0 認証
- provider 名: `gmail`
- スコープ: メールの読み取り、作成、送信
