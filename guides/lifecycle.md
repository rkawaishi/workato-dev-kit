# ライフサイクルと責務マップ

**いつ・誰が・何のために** 各スキルを呼び、各 docs を読み書きするかを一元化したリファレンス。

`@.claude/CLAUDE.md` の「ナレッジの参照優先順位」は **読む順序** を定めるが、本ドキュメントは **書くタイミングと責務** まで含めた全体像を示す。「grep に逃げる前に、本来通るべきスキルを思い出す」ための地図として使う。

## 全体フロー

```
[設計]     /design                 → DESIGN.md に目的・構成を固める
              ↓
[準備]     /catalog                → 既存の再利用資産を把握
           /sync-connectors        → 使用するコネクタのメタデータを取得
              ↓
[構築]     /create-recipe          → docs/connectors/ を読んでレシピを生成
           /create-workflow-app    → Workflow App 一式を生成
           /create-genie           → Genie / MCP を生成
           /create-connector       → カスタムコネクタを生成
              ↓
[検証]     /validate-recipe        → JSON 構造を検証
              ↓
[同期]     /wpush                  → Workato リモートへ push（バリデーション込み）
           (UI で pick_list 等を調整)
           /wpull                  → 調整結果をローカルに取得
              ↓
[学習]     /learn-recipe           → 調整済みレシピから docs/connectors/ を拡充
           /learn-pattern          → 再現性のある組み方を docs/patterns/ に記録
              ↓
[整理]     /catalog                → 新しい共有アセットをカタログに反映
           /design update          → DESIGN.md を実装状況で更新
```

## スキル責務マップ

各スキルが「いつ呼ばれ、何を読み、何を書くか」の一覧。

### 設計フェーズ

| スキル | いつ呼ぶ | 読むもの | 書くもの |
|---|---|---|---|
| `/design new` | プロジェクト開始時 | `projects/CATALOG.md`, `docs/patterns/`, `projects/docs/patterns/` | `projects/<name>/DESIGN.md`（新規） |
| `/design` | セッション開始時、設計確認時 | `projects/<name>/DESIGN.md` | なし（参照のみ） |
| `/design update` | 実装フェーズ完了時、設計判断変更時 | `projects/<name>/` の実装状況 | `projects/<name>/DESIGN.md`（更新） |

### 準備フェーズ

| スキル | いつ呼ぶ | 読むもの | 書くもの |
|---|---|---|---|
| `/catalog` | セッション開始時（再利用確認） | `projects/CATALOG.md` | なし |
| `/catalog scan` | 共有アセット追加・変更後 | `projects/` 全プロジェクト, `projects/CATALOG_CONFIG.yaml` | `projects/CATALOG.md` |
| `/sync-connectors <provider>` | 未知のコネクタを使う直前 | Workato API | `docs/connectors/<provider>.md` |
| `/sync-connectors --custom <name>` | カスタムコネクタ開発後 | `connectors/<name>/connector.rb` | `connectors/docs/<name>.md` |

### 構築フェーズ

| スキル | いつ呼ぶ | 読むもの | 書くもの |
|---|---|---|---|
| `/create-recipe` | レシピ新規作成時 | `docs/connectors/<provider>.md`, `connectors/docs/<name>.md`, `docs/logic/`, `docs/patterns/recipe-patterns/`, `projects/docs/patterns/`, `projects/CATALOG.md`, `.claude/rules/workato-recipe-format.md` | `projects/<name>/Recipes/*.recipe.json`, `*.connection.json` |
| `/create-workflow-app` | 承認ワークフロー等の新規作成時 | `docs/platform/workflow-apps.md`, `docs/patterns/deployment-guide.md`, `.claude/rules/workato-agentic-format.md` | `projects/<name>/Data Tables/*.data_table.json`, `Pages/*.page.json`, `lcap_app.json`, `Recipes/*.recipe.json` |
| `/create-genie` | AI エージェント/MCP サーバー新規作成時 | `docs/platform/agent-studio.md`, `docs/platform/mcp.md`, `.claude/rules/workato-agentic-format.md` | `projects/<name>/Agents/*.agentic_genie.json`, `*.agentic_skill.json`, `*.mcp_server.json` |
| `/create-connector` | カスタム API コネクタ新規作成時 | `docs/connector-sdk/connector-rb.md`, `docs/connector-sdk/overview.md`, `.claude/rules/workato-connector-sdk.md`, API ドキュメント (WebFetch) | `connectors/<name>/connector.rb`, `settings.yaml`, `Gemfile` |

### 検証・同期フェーズ

| スキル | いつ呼ぶ | 読むもの | 書くもの |
|---|---|---|---|
| `/validate-recipe` | push 前、JSON 編集後 | プロジェクトの JSON 群, `.claude/rules/` | なし（検証レポートのみ） |
| `/wpush` | デプロイ前 | プロジェクトのアセット | Workato リモート（ローカルは変更しない） |
| `/wpull` | UI 調整後、引き継ぎ時 | Workato リモート | `projects/<name>/` のアセット（上書き） |

### 学習フェーズ

| スキル | いつ呼ぶ | 読むもの | 書くもの |
|---|---|---|---|
| `/learn-recipe` | `/wpull` 直後、未学習アクション実装後 | `projects/<name>/Recipes/*.recipe.json` | `docs/connectors/<provider>.md`（input/output/snippet 追記）, `docs/logic/data-pills.md`, `.claude/rules/`, `docs/patterns/deployment-guide.md` |
| `/learn-pattern` | 再現性のある組み方に気づいた時 | 参考レシピ（任意）, 既存 `docs/patterns/recipe-patterns/` | `docs/patterns/recipe-patterns/<name>.md`（汎用）または `projects/docs/patterns/<name>.md`（組織固有） |

## docs 責務マップ

各 docs ディレクトリが「誰が書き、誰が読むか」の一覧。

### フレームワーク側（`workato-dev-kit` リポジトリ）

| パス | 書き手 | 読み手 | 内容 |
|---|---|---|---|
| `docs/connectors/<provider>.md` | `/sync-connectors`, `/learn-recipe` | `/create-recipe`, `/create-workflow-app`, `/create-genie` | Pre-built コネクタのトリガー/アクション/フィールド仕様 |
| `docs/connector-sdk/` | 人手 | `/create-connector` | Connector SDK リファレンス |
| `docs/logic/` | 人手, `/learn-recipe` | `/create-recipe`, `/create-workflow-app` | datapill 記法、数式、ループ、エラーハンドリング、トリガー |
| `docs/platform/` | 人手 | `/create-workflow-app`, `/create-genie`, `/design` | Data Table, Lookup Table, Agent Studio, MCP, Workflow App |
| `docs/patterns/recipe-patterns/` | `/learn-pattern` | `/create-recipe`, `/design` | 汎用レシピ構築パターン（Workato 全般に適用可） |
| `docs/patterns/deployment-guide.md` | 人手, `/learn-recipe` | `/wpush`, `/create-workflow-app` | デプロイ手順、よくあるエラー |
| `docs/patterns/shared-assets.md` | 人手 | `/create-recipe`, `/catalog`, `/design` | 共有アセット設計方針 |
| `docs/patterns/workspace-management.md` | 人手 | `/design`, `/catalog` | ワークスペース構成・命名規則 |
| `.claude/rules/` | 人手, `/learn-recipe`（JSON 構造の新発見時） | 全スキル | JSON フォーマット、パス別ルール |
| `docs/learned-patterns.md` | `/learn-recipe`（振り分け先が決まらない時のフォールバックのみ） | 人手（振り分け作業） | 適切な場所が決まるまでの仮置き場 |

### 組織側（`connectors/`, `projects/` は別リポジトリ）

| パス | 書き手 | 読み手 | 内容 |
|---|---|---|---|
| `connectors/docs/<name>.md` | `/sync-connectors --custom` | `/create-recipe`, `/create-workflow-app` | カスタムコネクタのトリガー/アクション/フィールド仕様 |
| `connectors/<name>/connector.rb` | `/create-connector`, 人手 | `/sync-connectors --custom` | カスタムコネクタの実装 |
| `projects/<name>/DESIGN.md` | `/design` | セッション開始時の Claude, `/create-recipe`, `/create-workflow-app` | プロジェクト設計書、Unlearned Actions |
| `projects/<name>/Recipes/*.json` | `/create-recipe`, `/wpull` | `/learn-recipe`, `/validate-recipe`, `/wpush` | レシピ本体 |
| `projects/CATALOG.md` | `/catalog scan` | `/create-recipe`, `/design` | 組織の共有アセット（Recipe Function, コネクション）一覧 |
| `projects/CATALOG_CONFIG.yaml` | 人手 | `/catalog` | スコープ設定（global / team / private） |
| `projects/docs/patterns/` | `/learn-pattern` | `/create-recipe`, `/design` | 組織ドメイン固有の構築パターン |

## ライフサイクルの原則

### 1. docs-first

構築スキル（`/create-recipe` 等）は必ず **先に docs を読む**。

- ドキュメントに情報があれば、そのまま実装
- ドキュメントに情報が無ければ：
  1. ベストエフォートで実装（UI 検証込み）
  2. そのプロジェクトの `DESIGN.md` の **Unlearned Actions** セクション、または当リポジトリの GitHub Issue に記録
  3. 実装後に `/learn-recipe` を回して docs を拡充
  4. 学習完了後に Unlearned Actions エントリから外す

### 2. 既存プロジェクトの grep 禁止

`projects/<other-project>/Recipes/` 配下を grep してサンプル JSON を掘り出すのは **禁止**。
個別プロジェクト固有のロジック・命名・datapill 参照がノイズとして混入し、ナレッジの欠落も可視化されなくなる。

**例外**: パターン学習（`/learn-pattern` で `docs/patterns/recipe-patterns/` や `projects/docs/patterns/` を参照）は可。ただし input/output スキーマを得る目的での grep は不可。

### 3. 学習の責務分離

| 学習内容 | 使うスキル | 書き込み先 |
|---|---|---|
| コネクタのフィールド仕様 | `/sync-connectors`（API/SDK 経由）または `/learn-recipe`（実レシピから） | `docs/connectors/`, `connectors/docs/` |
| 再現性のある組み方 | `/learn-pattern` | `docs/patterns/recipe-patterns/`, `projects/docs/patterns/` |
| JSON 構造の新発見 | `/learn-recipe` | `.claude/rules/` |
| datapill 参照パターン | `/learn-recipe` | `docs/logic/data-pills.md` |

**ポイント**: 学習スキルは中間ファイルを作らず、該当ドキュメントに直接追記する。`docs/learned-patterns.md` だけは仮置き場として許容されるが、早めに振り分けること。

### 4. 構築スキルは docs を書かない

`/create-recipe` 等の構築スキルは `projects/` のアセットを生成するだけで、`docs/connectors/` や `docs/patterns/` には書かない。
ナレッジの書き込みは **学習スキル**（`/learn-recipe`, `/learn-pattern`, `/sync-connectors`）の責務。この分離により、構築の副作用で誤った情報が docs に混入することを防ぐ。

## 典型シナリオ

### シナリオ A: 新規プロジェクト（初めて触るコネクタを使う）

```
/design new <project>          # 設計書を作成
/catalog                       # 再利用できる共有アセットを確認
/sync-connectors <provider>    # コネクタのメタデータを取得
/create-recipe                 # docs/connectors/ を読んでレシピ生成
/validate-recipe <project>     # JSON 構造を検証
/wpush --start                 # デプロイ + 起動
(UI で pick_list 等を調整)
/wpull                         # 調整結果を取得
/learn-recipe <project>        # 調整内容を docs に反映
/design update                 # 実装状況を DESIGN.md に反映
```

### シナリオ B: 既知のコネクタで新規プロジェクト

```
/design new <project>
/catalog
/create-recipe                 # 既に docs/connectors/ にある前提
/validate-recipe <project>
/wpush --start
/design update
```

コネクタ情報が既に揃っていれば `/sync-connectors` と `/learn-recipe` は不要。

### シナリオ C: カスタムコネクタを作る

```
/create-connector <api-name>   # connector.rb を生成
(Workato SDK で実装・テスト)
/sync-connectors --custom <name>  # connectors/docs/<name>.md を更新
/create-recipe                 # カスタムコネクタを使うレシピを生成
```

### シナリオ D: 引き継ぎ（既存プロジェクトを理解する）

```
/wpull --all                   # 全プロジェクトをローカルに取得
/design <project>              # 設計書を読む
/learn-recipe <project>        # 実装から docs を拡充
/catalog scan                  # 共有アセットを棚卸し
```

## このマップに沿わない動きをしそうになったら

- 「projects/<他プロジェクト>/Recipes/ を grep して input/output を調べよう」→ **止まる**。`docs/connectors/<provider>.md` を読むか、無ければ `/sync-connectors` を回す
- 「構築しながら docs/connectors/ を書き足そう」→ **止まる**。構築スキルは docs を書かない。`/learn-recipe` に任せる
- 「DESIGN.md は後で書けばいい」→ **止まる**。セッション開始時の `/design` と終了時の `/design update` はライフサイクルの一部
- 「新しいコネクタだけどとりあえず実装してみよう」→ OK、ただし **Unlearned Actions に記録** し、実装後に `/learn-recipe` を必ず回す
