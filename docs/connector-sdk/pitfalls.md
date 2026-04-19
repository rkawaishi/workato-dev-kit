# Connector SDK ハマりどころ集

Workato Connector SDK 実装時に繰り返し踏みやすい落とし穴をまとめる。新しい `connector.rb` を書く前に一読しておくと時間を節約できる。

参考: `@docs/connector-sdk/connector-rb.md`, `@docs/connector-sdk/overview.md`

## 実装時

### 1. `get/post/...` の戻り値は `SimpleDelegator` でラップされる

`get`, `post`, `put`, `patch`, `delete` の戻り値は `Workato::Connector::Sdk::Request < SimpleDelegator`。Array や Hash を返す API でも、直接の型チェックは通らない。

```ruby
response = get('/items')
response.is_a?(Array)  # => false（Delegator 自身を見ている）
response.class         # => Workato::Connector::Sdk::Request
```

中身を取り出すには、まず `method_missing` を何か呼んで実体の遅延評価を走らせたうえで `__getobj__` を使う。

```ruby
response.length rescue nil   # Delegator に任意メソッドを委譲させる
body = response.__getobj__   # 実体（Array / Hash）を取り出す
```

実用上は `methods` ブロックに正規化ヘルパーを持たせて一箇所に閉じ込めるのが定石。

```ruby
methods: {
  normalize_list_response: lambda do |response|
    response.length rescue nil
    body = response.__getobj__ rescue response

    case body
    when Array then body
    when Hash  then body['result'] || body['data'] || body['items'] || []
    else []
    end
  end
}
```

### 2. `base_uri` の末尾スラッシュと path の先頭スラッシュは共存させない

RestClient は path が `/` で始まるとホスト直下にリセットする。`base_uri` 側に `/api/` などのプレフィックスを置いている場合、path を絶対パスで書くと **プレフィックスが落ちる**。

```ruby
# connection
base_uri: lambda { |_c| 'https://example.com/api/' }

# アクション内
get('/users/me')   # => https://example.com/users/me   ← /api/ が消える
get('users/me')    # => https://example.com/api/users/me ← 正しい
```

**ルール**: `base_uri` は末尾スラッシュあり、`get` 等に渡す path は先頭スラッシュなしの相対パスで統一する。

### 3. レスポンス包装パターンはエンドポイントごとに異なる

同じ API プロダクト内でも次のような混在はよくある（Workato Developer API 自体で観測済み）:

| パターン | 例 |
|---|---|
| 配列直接 | `[item1, item2, ...]` |
| `result` 包装 | `{ "result": [...], "next_page": N }` |
| `data/total` 包装 | `{ "data": [...], "total": N }` |
| `items` 包装 | `{ "items": [...], "cursor": "..." }` |

アクションごとに条件分岐を書くと DRY が壊れる。`methods` ブロックに `normalize_list_response` のような共通ヘルパーを 1 本置き、`execute` からは必ずそれを通す。

### 4. ページネーションは最初のレスポンスで形を確定させる

包装パターンが違うと「次ページの取り方」も違う（`next_page`, `cursor`, `offset` など）。ヘルパーの戻り値を `{ items:, next_cursor: }` のような固定形に揃えておくと、トリガー `poll` の `closure` も素直に書ける。

## 環境構築・実行時

### 5. Ruby 4.0 では default gems が外れている

`workato-connector-sdk` 1.3.19 系を Ruby 4.0 で動かすには、以下を `Gemfile` に明示追加が必要。

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

Ruby 3.x では bundled/default gems 扱いで不要だったため、アップグレード時に `LoadError: cannot load such file -- csv` 等で気付く。

### 6. macOS で `charlock_holmes` のビルドに `icu4c@78` が要る

`bundle install` が `charlock_holmes` でコケたら ICU のバージョン不一致。Homebrew で `icu4c@78` を入れて PKG_CONFIG 系を通す。

```bash
brew install icu4c@78

export PKG_CONFIG_PATH="$(brew --prefix icu4c@78)/lib/pkgconfig:$PKG_CONFIG_PATH"
export LDFLAGS="-L$(brew --prefix icu4c@78)/lib"
export CPPFLAGS="-I$(brew --prefix icu4c@78)/include"

bundle install
```

最新 ICU で通ることを確認できたらバージョンを上げてよいが、SDK gem のビルド対象に合わせるのが無難。

### 7. 日本語コメントを含む `connector.rb` には `LANG/LC_ALL=UTF-8` が要る

`bundle exec workato exec` 実行時、ロケールが C のままだと日本語コメントでパースエラーになる。`.envrc` や実行コマンドの頭に UTF-8 を明示する。

```bash
LANG=en_US.UTF-8 LC_ALL=en_US.UTF-8 bundle exec workato exec test
```

CI/CD でも同じ環境変数を設定しておく。

## 開発フロー

### 8. push 後は `connectors/docs/<name>.md` を更新する

`python3 scripts/workato-api.py sdk push` でアップロードした後、`connectors/docs/<name>.md` を必ず更新する。次回の実装時に doc-first で辿れるようにするためのルール。詳細は `@.claude/rules/workato-connector-sdk.md` の「sdk push 後の docs 自動更新」を参照。

### 9. 新しいハマりどころはこの doc に追記する

本ファイルは「一度踏んだ落とし穴を二度と踏まない」ための蓄積先。実装中に新しい罠に遭遇したら、該当セクション（実装時 / 環境構築 / 開発フロー）に追記して PR を出す。
