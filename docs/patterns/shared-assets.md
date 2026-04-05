# 共有アセットのデザインパターン

共有化はケースバイケースで判断する。プロジェクトごとに個別で持つ方がシンプルなケースも多く、過度な共有化はかえって管理を複雑にする。

## いつ共有を検討するか

複数のプロジェクトで同じコネクション（例: Jira, Slack）や Recipe Function（例: マネージャー取得）を使い回す場合に、認証情報の一元管理やロジックの重複排除が必要になることがある。

## Workato の参照メカニズム

Workato は `zip_name` と `folder` フィールドで **別プロジェクトのアセットを参照** できる:

```json
"account_id": {
  "zip_name": "Shared/Connections/shared_jira.connection.json",
  "name": "Shared | Jira",
  "folder": "Shared"
}
```

- `folder`: 参照先のプロジェクト名（同一プロジェクト内なら `""`）
- `zip_name`: プロジェクト名を含むパス

## 推奨パターン: Shared プロジェクト

### プロジェクト構成

```
projects/
├── Shared/                          # 共有アセット専用プロジェクト
│   ├── Connections/
│   │   ├── shared_jira.connection.json
│   │   ├── shared_slack.connection.json
│   │   └── shared_gmail.connection.json
│   └── Recipes/
│       ├── fnc_get_line_manager.recipe.json
│       ├── fnc_get_department.recipe.json
│       └── fnc_send_notification.recipe.json
│
├── [App] PC Loan Request/           # 個別プロジェクト
│   └── Recipes/
│       └── main_recipe.recipe.json  # → Shared のコネクション/Function を参照
│
├── [App] Expense Reimbursement/     # 個別プロジェクト
│   └── Recipes/
│       └── main_recipe.recipe.json  # → 同じ Shared を参照
```

### 命名規則

| アセット種別 | 命名 | 例 |
|---|---|---|
| 共有プロジェクト | `Shared` | |
| 共有コネクション | `Shared \| <Provider>` | `Shared \| Jira`, `Shared \| Slack` |
| 共有 Recipe Function | `fnc_<動詞>_<名詞>` | `fnc_get_line_manager`, `fnc_send_notification` |

### コネクションの参照

個別プロジェクトのレシピから共有コネクションを参照:

```json
{
  "keyword": "application",
  "provider": "jira",
  "account_id": {
    "zip_name": "Shared/Connections/shared_jira.connection.json",
    "name": "Shared | Jira",
    "folder": "Shared"
  }
}
```

### Recipe Function の呼び出し

個別プロジェクトのレシピから共有 Function を呼び出す:

```json
{
  "provider": "workato_recipe_function",
  "name": "call_recipe",
  "input": {
    "flow_id": {
      "zip_name": "Shared/Recipes/fnc_get_line_manager.recipe.json",
      "name": "fnc: Get line manager",
      "folder": "Shared"
    },
    "parameters": {
      "requestor_email": "#{_dp('...')}"
    }
  }
}
```

## Recipe Function の設計ガイドライン

### 命名規則

```
fnc_<動詞>_<名詞>.recipe.json
```

| パターン | 例 | 用途 |
|---|---|---|
| `fnc_get_*` | `fnc_get_line_manager` | データ取得 |
| `fnc_send_*` | `fnc_send_slack_notification` | 通知送信 |
| `fnc_validate_*` | `fnc_validate_budget` | 検証 |
| `fnc_create_*` | `fnc_create_jira_ticket` | 外部システムにレコード作成 |
| `fnc_update_*` | `fnc_update_employee_status` | 外部システムのレコード更新 |

### インターフェース設計

共有 Function は明確な入出力を定義する:

```json
{
  "provider": "workato_recipe_function",
  "name": "execute",
  "input": {
    "parameters_schema_json": "[{入力パラメータのスキーマ}]",
    "result_schema_json": "[{出力パラメータのスキーマ}]"
  }
}
```

- **入力は最小限**: 必要なパラメータのみ受け取る（1〜3個が理想）
- **出力は明確**: 呼び出し元が必要とするフィールドを全て返す
- **エラーハンドリング**: Function 内で try/catch し、エラー時は `error` フィールドで報告

### 例: fnc_get_line_manager

```
入力: requestor_email (string)
出力: manager_name (string), manager_email (string)
```

### 例: fnc_send_slack_notification

```
入力: channel (string), message (string), thread_ts (string, optional)
出力: ok (boolean), ts (string)
```

## 共有 vs 個別の判断

共有するか個別に持つかは **アセットの性質と用途** で判断する。利用回数ではない。

### 個別に持つべきケース

| 状況 | 理由 |
|---|---|
| エージェント用コネクション | 専用の権限・スコープが望ましい。他レシピと共有すると権限過多のリスク |
| 特定フローに閉じたロジック | そのプロジェクトの文脈でのみ意味がある |
| 異なるスコープ・認証が必要 | 同じサービスでも用途ごとにコネクションを分ける |

### 共有が適するケース

| 状況 | 理由 |
|---|---|
| 組織横断の共通ロジック | マネージャー検索、部署取得など、どのプロジェクトでも同じ結果を返す |
| インフラ的なコネクション | 全社共通の Slack ワークスペース、共通の Jira プロジェクトなど |

## 注意事項

- Shared プロジェクトのアセットを変更すると、参照している全プロジェクトに影響する
- Shared のコネクション認証を変更した場合、全参照先で再テストが必要
- `workato push --delete` を Shared プロジェクトに対して実行する際は、他プロジェクトからの参照を壊さないよう注意
- Recipe Function の入出力を変更する場合は、全呼び出し元の互換性を確認する
