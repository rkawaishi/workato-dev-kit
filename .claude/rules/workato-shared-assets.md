---
paths:
  - "projects/**"
---

# 共有アセットガイダンス

複数プロジェクト間でコネクションや Recipe Function を共有する場合の参考パターン。
**共有化は必須ではない。** プロジェクトごとに個別に持つ方がシンプルなケースも多い。

## 共有する場合のパターン

`Shared` プロジェクトに共有アセットを配置し、他プロジェクトから `folder` 参照で利用する:

```json
"account_id": {
  "zip_name": "Shared/Connections/shared_jira.connection.json",
  "name": "Shared | Jira",
  "folder": "Shared"
}
```

## 判断の目安

- 同じコネクションやロジックが複数プロジェクトで重複している → 共有を**検討**
- 1つのプロジェクトでしか使わない → プロジェクト内に保持
- 共有すると変更時の影響範囲が広がる → トレードオフを考慮

## 詳細

命名規則、Recipe Function のインターフェース設計、注意事項は `@docs/patterns/shared-assets.md` を参照。
