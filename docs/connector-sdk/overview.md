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

### SDK CLI (`gem install workato-connector-sdk`)

ローカルでのテスト・開発に使用する。Platform CLI と `workato` コマンド名が競合するため、`bundle exec` で実行する。

| コマンド | 説明 |
|---|---|
| `bundle exec workato new <PATH>` | 新規コネクタプロジェクト作成 |
| `bundle exec workato exec <PATH>` | コネクタの lambda ブロックを実行・テスト |
| `bundle exec workato edit <PATH>` | 暗号化ファイルを編集 |
| `bundle exec workato generate <SUBCOMMAND>` | テンプレートからコード生成 |

### Workato へのアップロード（API ヘルパー推奨）

コネクタの push は API ヘルパーを使う。Platform CLI のプロファイルで認証するため、gem 側の認証設定（API Client トークン）が不要。

```bash
# 新規作成
python3 scripts/workato-api.py sdk push --connector connectors/<name>/connector.rb --title "<Title>"

# 既存コネクタの更新
python3 scripts/workato-api.py sdk push --connector connectors/<name>/connector.rb --connector-id <id>
```

> **Note**: `bundle exec workato push` も引き続き使用可能だが、別途 API Client トークンの設定が必要。

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

- Ruby 2.7.x / 3.0.x / 3.1.x（ローカルテスト用）
- API ヘルパーでの push は Platform CLI のプロファイル認証のみで可能（Ruby 不要）
- `bundle exec workato push` を使う場合は API クライアント（"Get details" 権限）が別途必要

## 環境構築の落とし穴

### Ruby 4.0 では default gems が外れている

`workato-connector-sdk` 1.3.x 系を Ruby 4.0（2026-04 時点では preview 段階）で動かすには、以下を `Gemfile` に明示追加する。Ruby 3.x では bundled/default gems 扱いだったため、アップグレード時に `LoadError: cannot load such file -- csv` 等で気付く。

```ruby
# Gemfile
gem 'csv'
gem 'base64'
gem 'bigdecimal'
gem 'logger'
gem 'drb'
gem 'ostruct'
gem 'mutex_m'
```

### macOS で `charlock_holmes` のビルドに `icu4c@78` が要る

`bundle install` が `charlock_holmes` でコケたら ICU のバージョン不一致。Homebrew で対応バージョンを入れて PKG_CONFIG 系を通す。

```bash
brew install icu4c@78

export PKG_CONFIG_PATH="$(brew --prefix icu4c@78)/lib/pkgconfig:$PKG_CONFIG_PATH"
export LDFLAGS="-L$(brew --prefix icu4c@78)/lib"
export CPPFLAGS="-I$(brew --prefix icu4c@78)/include"

bundle install
```

Homebrew 側の提供バージョンは時期で変わるため、`brew search icu4c` で現行のリストを確認してから入れる。

### 日本語コメントを含む `connector.rb` は `LANG/LC_ALL=UTF-8` が要る

`bundle exec workato exec` 実行時にロケールが C のままだと日本語コメントでパースエラーになる。実行コマンドまたは `.envrc` / CI 設定で UTF-8 を明示する。

```bash
LANG=en_US.UTF-8 LC_ALL=en_US.UTF-8 bundle exec workato exec test
```
