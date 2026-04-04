# Connector SDK 概要

公式: https://docs.workato.com/en/developing-connectors/sdk.html

## Custom Connector とは

Workato が標準で提供していないアプリケーションに接続するための自作コネクタ。Ruby DSL で記述し、トリガー・アクション・認証を定義する。

## 開発手段

### 1. Web エディタ（Cloud SDK）
- Workato UI 上の Tools > Connector SDK からブラウザで開発
- CodeMirror エディタ（構文ハイライト、エラー表示）
- Test code タブでインタラクティブテスト

### 2. SDK CLI（ローカル開発）
- `gem install workato-connector-sdk` でインストール
- ローカルで開発・テスト → `workato push` でアップロード
- RSpec + VCR によるユニットテスト
- Git 連携、CI/CD パイプライン対応

## SDK CLI コマンド

### 本家 CLI (`gem install workato-connector-sdk`)

| コマンド | 説明 |
|---|---|
| `workato new <PATH>` | 新規コネクタプロジェクト作成 |
| `workato exec <PATH>` | コネクタの lambda ブロックを実行・テスト |
| `workato push <FOLDER>` | コネクタコードを Workato にアップロード |
| `workato edit <PATH>` | 暗号化ファイルを編集 |
| `workato generate <SUBCOMMAND>` | テンプレートからコード生成 |

### フォーク版 CLI (`rkawaishi/workato-platform-cli`)

SDK コマンドが Platform CLI に統合されており、Ruby gem 不要:

| コマンド | 説明 |
|---|---|
| `workato sdk new <PATH>` | 新規コネクタプロジェクト作成 |
| `workato sdk exec <PATH>` | コネクタの lambda ブロックを実行・テスト |
| `workato sdk push <FOLDER>` | コネクタコードを Workato にアップロード |
| `workato sdk generate schema <PATH>` | コネクタからスキーマ生成 |
| `workato sdk oauth2 <PATH>` | OAuth2 フロー実行 |

フォーク版にはさらに以下の追加機能がある:
- `workato jobs list` / `workato jobs get` — ジョブ一覧・詳細
- `workato oauth-profiles` — Custom OAuth Profile の CRUD
- `workspace_id` による自動プロファイル解決（`.workatoenv` の Git 共有対応）

## プロジェクト構造

`workato new <name>` で生成されるファイル:

```
<name>/
├── connector.rb          # メインのコネクタ定義
├── settings.yaml.enc     # 認証情報（暗号化）
├── settings.yaml         # 認証情報（平文、開発用）
├── master.key            # 暗号化キー（.gitignore 必須）
├── Gemfile               # Ruby 依存関係
├── spec/                 # テストファイル
│   ├── spec_helper.rb    # RSpec + VCR 設定
│   ├── connector_spec.rb # コネクタテスト
│   └── cassettes/        # VCR 録画（HTTP モック）
└── .rspec
```

## 前提条件

- Ruby 2.7.x / 3.0.x / 3.1.x
- `workato push` には API クライアント（"Get details" 権限）が必要
