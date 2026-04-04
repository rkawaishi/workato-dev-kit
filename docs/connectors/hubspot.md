# HubSpot コネクタ

公式: https://docs.workato.com/en/connectors/hubspot.html
Provider: `hubspot`

## Triggers (6種)
| 名前 | 説明 |
|---|---|
| New record | 新規レコード作成時 |
| New records (batch) | 新規レコードのバッチ取得 |
| New/updated record | 新規/更新レコード |
| New/updated records (batch) | 新規/更新レコードのバッチ取得 |
| New contact in list | リストにコンタクト追加時 |
| New form submission | フォーム送信時 |

## Actions (22種)

### Universal Actions
| 名前 | 説明 |
|---|---|
| Get record | ID でレコード取得 |
| Search record (batch) | 条件に合うレコード検索 |
| Create record | レコード作成 |
| Create records (batch) | 複数レコード一括作成 |
| Update record | レコード更新 |
| Update records (batch) | 複数レコード一括更新 |

### Association Actions
| 名前 | 説明 |
|---|---|
| Get associations (batch) | 関連レコード一括取得 |
| Get contacts associated with a company (batch) | 企業に紐づくコンタクト取得 |
| List associations (batch) | 関連一覧取得 |
| Associate records | レコード間の関連付け |
| Associate records (batch) | 複数レコード一括関連付け |
| Delete associations (batch) | 関連の一括削除 |

### Export/Import Actions
| 名前 | 説明 |
|---|---|
| Export object data (file) | データをファイルでエクスポート |
| Import CRM data (file) | ファイルからデータインポート |

### Contact Actions
| 名前 | 説明 |
|---|---|
| Get contacts in list (batch) | リスト内コンタクト取得 |
| Add contact to list (batch) | コンタクトをリストに一括追加 |
| Add contact to workflow | ワークフローにコンタクト登録 |
| Remove contact from list (batch) | リストからコンタクト一括削除 |
| Delete contact | コンタクト削除 |

### Other Actions
| 名前 | 説明 |
|---|---|
| Create engagement | エンゲージメント（活動）記録 |
| Get owner details | メールでオーナー情報取得 |
| Get owner details by ID | ID でオーナー情報取得 |
| Search pipeline stages (batch) | パイプラインステージ検索 |

## 備考
- 旧トリガー（contacts, companies, deals 個別）は非推奨。Universal record triggers を使用
