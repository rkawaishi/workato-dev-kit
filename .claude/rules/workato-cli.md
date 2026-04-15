---
paths:
  - ".workatoenv"
  - "projects/**"
  - "connectors/**"
---

# Workato CLI ツール

3つのツールを使い分ける:

## 1. Platform CLI（プロジェクト管理）

インストール: `pipx install workato-platform-cli`

主なコマンド:
- Init: `workato init --non-interactive --profile <profile> --project-id <id> --folder-name "projects/<name>"`
- Pull: `workato projects use "<name>" && workato pull`
- Push: `workato push`
- Push (再起動付き): `workato push --restart-recipes`
- Push (削除付き): `workato push --delete`
- レシピ起動: `workato recipes start --id <id>` / `workato recipes start --all`

## 2. API ヘルパー（CLI にない機能の補完）

Platform CLI にないAPI操作を補完するスクリプト。workspace_id ベースでプロファイルを自動解決する。

```bash
python3 scripts/workato-api.py <command>
```

| コマンド | 用途 |
|---|---|
| `jobs list --recipe-id <id> [--status <s>]` | ジョブ一覧 |
| `jobs get --recipe-id <id> --job-id <id>` | ジョブ詳細 |
| `connectors list-platform [--provider <name>]` | Pre-built コネクタ情報 |
| `connectors list-custom` | カスタムコネクタ一覧 |
| `recipes list [--folder-id <id>]` | レシピ一覧（JSON） |
| `profile show` | プロファイル解決結果 |

## 3. Connector SDK CLI（カスタムコネクタ開発）

インストール: `gem install workato-connector-sdk`

**注意:** Platform CLI と同じ `workato` コマンド名を使うため、`bundle exec` でスコープして衝突を避ける。

```bash
cd connectors/<name>
bundle exec workato new <PATH>           # 新規作成
bundle exec workato exec <PATH> test     # テスト
bundle exec workato push <FOLDER>        # push
```

## コネクタの分類

- **Pre-built**: Workato 公式の標準コネクタ（1,000+）
- **Universal**: HTTP, OpenAPI, GraphQL, SOAP — 標準にない API 用
- **Community**: ユーザー共有コネクタ
- **Custom**: Connector SDK で自作 → `connectors/` ディレクトリ
- **Custom Action**: コネクタ内の `__adhoc_http_action` で API 直接呼出し
