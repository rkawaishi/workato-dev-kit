---
paths:
  - "projects/**"
---

# 共有アセットルール

## コネクションの共有

2つ以上のプロジェクトで同じコネクション（Jira, Slack 等）を使う場合は、`Shared` プロジェクトに配置して参照する。

参照方法:
```json
"account_id": {
  "zip_name": "Shared/Connections/shared_jira.connection.json",
  "name": "Shared | Jira",
  "folder": "Shared"
}
```

## Recipe Function の共有

横断的なロジック（マネージャー取得、通知送信等）は `Shared` プロジェクトの Recipe Function として切り出す。

命名: `fnc_<動詞>_<名詞>` (例: `fnc_get_line_manager`, `fnc_send_notification`)

## 共有化の判断

- 2つ以上のプロジェクトで使う → Shared に移動
- HRMS / 通知 / 認証など横断的機能 → 最初から Shared に作成
- 1つのプロジェクトでのみ使用 → プロジェクト内に保持

## 詳細

具体的な実装パターン、インターフェース設計、注意事項は `@docs/patterns/shared-assets.md` を参照。
