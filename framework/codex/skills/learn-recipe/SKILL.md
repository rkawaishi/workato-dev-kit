---
name: learn-recipe
description: レシピ JSON を分析してフィールド情報やパターン知識を組織ナレッジ層 (org/docs/) に追記する。pull したレシピから学習し、組織のナレッジベースを拡充する。
---

# $learn-recipe

レシピ JSON を分析し、発見した知見を **組織ナレッジ層 `org/docs/`** に直接追記するスキル。
中間ファイルへの蓄積ではなく、各ドキュメントを直接拡充する。

書き込み先は **すべて `org/docs/` 配下**（kit の `docs/` は触らない）。詳細は `AGENTS.md`。

## 使い方

- `$learn-recipe <file-path>` — 特定のレシピを分析
- `$learn-recipe <project-name>` — プロジェクト内の全レシピを分析
- `$learn-recipe` — 全プロジェクトの全レシピを分析

## 分析対象と追記先

すべての追記先は `org/docs/<相対パス>`。kit の `docs/<同じ相対パス>` を Read して既知の情報と重複する内容は書かない（差分・補正・組織固有の追加情報のみ）。

### 1. フィールド情報（最重要）

各ステップから input/output フィールドスキーマを抽出する。

抽出元:
- `extended_output_schema` — アクション/トリガーの出力フィールド
- `extended_input_schema` — アクション/トリガーの入力フィールド
- `input` — 実際の入力値（datapill 参照含む）
- `parameters_schema_json` — Genie/Function のパラメータ（JSON 文字列）
- `result_schema_json` — Genie/Function の結果（JSON 文字列）
- `input.input.schema` — Custom Action のリクエストスキーマ
- `input.output` — Custom Action のレスポンススキーマ

**追記先**: `org/docs/connectors/<provider>.md` の該当アクション/トリガーセクション

フォーマット:
```markdown
### <action_name>

#### Input fields
| フィールド | 型 | 必須 | 説明 |
|---|---|---|---|
| field_name | type | Yes/- | label |

#### Output fields
| フィールド | 型 | 説明 |
|---|---|---|
| field_name | type | label |
| parent.child | type | label (nested) |
```

### 2. 新しいプロバイダー/アクション

レシピ内で未知の provider/name の組み合わせを発見した場合（kit の `docs/connectors/<provider>.md` に存在しないアクション）。

**追記先**:
- Pre-built コネクタ → `org/docs/connectors/<provider>.md` のトリガー/アクション一覧テーブル
- Workato 内部プロバイダー → `org/docs/platform/workflow-apps.md` または `org/docs/platform/agent-studio.md`

### 3. JSON 構造の知見

レシピ JSON の構造に関する新しい発見（新しい keyword、未知のフィールド、特殊な構造等）。組織のレシピで遭遇した範囲の知見として `org/docs/` に蓄積する。

**追記先**:
- レシピ構造全般 → `org/docs/learned-patterns.md`（後で kit に PR したい一般的な発見はここに）
- ロジック（if/loop/error）→ `org/docs/logic/` の該当ファイル

### 4. datapill パターン

新しい datapill 記法や参照パターンの発見。

**追記先**: `org/docs/logic/data-pills.md`

### 5. デプロイ関連の知見

push/pull 時の挙動に関する新発見（フィールドリセット、スキーマ展開、バージョン変更等）。

**追記先**: `org/docs/patterns/deployment-guide.md`

### 6. 分類が不明な知見

上記のどこにも当てはまらない新発見。

**追記先**: `org/docs/learned-patterns.md`（一時保管。後で適切なファイルに移動する）

## 分析手順

1. 対象レシピの `.recipe.json` を読み込む
2. 全ステップを再帰的に走査
3. 各ステップについて:
   a. `provider` と `name` が既知か確認（`docs/connectors/<provider>.md` と `org/docs/connectors/<provider>.md` の両方を参照）
   b. `extended_output_schema` / `extended_input_schema` があればフィールド情報を抽出
   c. 新しい構造パターンがあれば記録
4. 追記先（`org/docs/<...>`）のディレクトリが無ければ `mkdir -p` で作成
5. 追記先ファイルを読み、既存内容と重複しないか確認
6. kit 側の `docs/<同じ相対パス>` も読み、kit に既知の情報なら **書かない**
7. 新しい知見のみ追記

## 重複チェック

追記前に以下の 2 つを Grep で検索し、同じ内容が既にないか確認する:
- 追記先の `org/docs/<path>.md`
- 対応する kit 側 `docs/<同じパス>.md`

- kit 側に同じアクション名のフィールド情報がある → 差分（org 固有のフィールドや補正）のみ追加
- 同じルールが既にある → スキップ

## 出力

分析完了後、以下を報告:
- 分析したファイル数
- 追記したドキュメント一覧（すべて `org/docs/` 配下）と追記内容のサマリー
- 新たに発見したパターン（あれば）

## Unlearned Actions の整理

プロジェクトを対象に実行した場合、`projects/<project-name>/specs/` 配下の **全フィーチャー** の `plan.md` と `tasks.md` をスキャンし、今回学習した `provider` / `action` に対応するエントリを整理する（`AGENTS.md` の「レシピ実装ライフサイクル」参照）。

### plan.md の `## Unlearned Actions` 表

`projects/<project-name>/specs/<NNN>-<slug>/plan.md` ごとに以下を実行:

1. `## Unlearned Actions` 表があるか確認
2. 今回学習した `provider` / `action` に該当する行があれば **削除**
3. 全行が削除されたら表を「（学習済み）」と注記して残す（表自体は削除せず、履歴として保持）

### tasks.md の `[learn]` タスク

`projects/<project-name>/specs/<NNN>-<slug>/tasks.md` ごとに以下を実行:

1. `[learn]` タグ付きで `provider/action` を含む未完了タスク（`- [ ]`）を検索
2. 該当タスクを `- [x]` にチェック
3. 完了後の `Last updated` を更新

### 報告

```
Unlearned Actions の整理:
- plan.md から削除: <N> 行 (<feature> 等)
- tasks.md でチェックオン: <M> タスク (<feature> 等)

未完了の Unlearned Actions が残るフィーチャー:
- <project>/specs/<NNN>-<slug>: <残数> 件
```

> **後方互換**: 旧形式 `projects/<project-name>/DESIGN.md` の `## Unlearned Actions` は **読み取らない**（Phase B でハードカットオーバー済み）。既存プロジェクトに DESIGN.md しか無い場合は `$design migrate` で先に specs/ に変換すること。

## Git 管理

書き込み先は **ワークスペースリポジトリ内の `org/docs/`** と `projects/<name>/specs/` 配下:

```bash
cd <workspace-root>
git add org/docs/ projects/<name>/specs/
git commit -m "docs(org): learn from <project-name> recipes"
```

**kit submodule (`kit/`) には commit しない**。kit 標準への還流が必要な一般的知見が溜まったら、別途 kit リポジトリに PR を立てる。
