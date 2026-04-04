# Google Drive コネクタ

公式: https://docs.workato.com/en/connectors/google-drive.html
Provider: `google_drive`

## Triggers
| 名前 | 説明 |
|---|---|
| New activity | Google Drive 内の新しいアクティビティ検知 |

## Actions
| 名前 | 説明 |
|---|---|
| Upload file | ファイルアップロード |
| Download file | ファイルダウンロード |
| Create folder | フォルダ作成 |
| Search files | ファイル検索 |

## フィールド詳細

### upload_file (Action)

レシピ: Upload Gmail attachments to Google Drive

#### Input fields
| フィールド | 型 | 必須 | 説明 |
|---|---|---|---|
| fileContent | string | Yes | アップロードするファイルのコンテンツ（バイナリ） |
| name | string | Yes | アップロード先のファイル名 |

## 備考
- OAuth 2.0 またはサービスアカウント認証
- Google Drive API v3 使用
- provider 名: `google_drive`
