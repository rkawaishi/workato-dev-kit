---
description: レシピ構築パターンを org/docs/patterns/recipe-patterns/ に記録・更新する。Workato エキスパートが他者サポート用にナレッジを蓄積する。
allowed-tools: Read, Write, Edit, Glob, Grep
---

# /learn-pattern

Workato エキスパートが構築パターンを **`org/docs/patterns/recipe-patterns/`** に記録するスキル。
エキスパートが既に持っている知見をドキュメント化することが目的。レシピは参考素材として任意で指定する。

書き込み先は組織ナレッジ層 1 箇所のみ（kit submodule の `docs/` には書かない）。詳細は `@.claude/rules/org-knowledge-overlay.md`。

## 使い方

- `/learn-pattern` — パターンの記録を開始（対話）
- `/learn-pattern ページネーションループ` — パターン名を指定して記録
- `/learn-pattern 承認ワークフロー 注意点追加` — 既存パターンに追記
- `/learn-pattern <file-path>` — レシピを参考素材として指定（パターンは対話で決める）

## 手順

### 1. エキスパートの意図を確認

まず既存パターンを把握する（kit canonical と組織側を併読、矛盾は org 側優先）:
- `docs/patterns/recipe-patterns/_index.md` — kit canonical の汎用パターン
- `org/docs/patterns/recipe-patterns/_index.md` — 組織が記録したパターン（存在すれば）
- `projects/docs/patterns/_index.md` — 組織ドメインのレガシーパターン（存在すれば、後方互換のため読み込みのみ）

利用者に何をしたいかを確認する:

```
何を記録しますか？

A. 新しいパターンを追加（例: ページネーションループ、バッチ処理 etc.）
B. 既存パターンに知見を追記（注意点、バリエーション etc.）

既存パターン:
- org/docs/patterns/recipe-patterns/: <パターン名を列挙>
- (legacy) projects/docs/patterns/: <パターン名を列挙、存在すれば>
```

引数でパターン名や意図が明確な場合はこの質問をスキップして先に進む。

### 2. パターンの内容をヒアリング

エキスパートにパターンの要点を聞く。全てを聞く必要はなく、利用者が話した内容をベースに構成する:

- **どういう場面で使うか** — どんな要件のときにこの構成にするか
- **構成の要点** — どのステップをどう組み合わせるか
- **なぜこの構成か** — 他の方法ではなくこの構成を選ぶ理由
- **ハマりどころ** — 知らないと踏む落とし穴

参考レシピが指定されている場合は `.recipe.json` を読み、構造を要約して提示する。エキスパートの説明と照合しながらパターンを具体化する。

### 3. パターンの記述

エキスパートの知見をドキュメント化する。

書き込み先は **`org/docs/patterns/recipe-patterns/<pattern-name>.md`** に統一。
ディレクトリが存在しなければ `mkdir -p org/docs/patterns/recipe-patterns/` で作成する。

#### 新規パターンのテンプレート

```markdown
# <パターン名> (<English Name>)

## スコープ

- [ ] 汎用 — Workato を使う他の組織でも同じ構成になる
- [ ] 組織ドメイン — 自組織の業務・SaaS 連携に紐づく

（該当する方にチェック。kit 還流を検討する場合は「汎用」のみが候補）

## いつ使うか

| 条件 | 該当 |
|---|---|
| <条件1> | Yes |
| <条件2> | Optional |

## レシピ構成図

\```
[コンテキスト]
    │
    ├── [Action/Loop/IF] <step description>
    └── ...
\```

## ステップ構成

| # | Provider | Action | 目的 |
|---|---|---|---|
| N | provider | action_name | 説明 |

## 設計判断ポイント

| 判断 | 推奨 | 理由 |
|---|---|---|

## 既知の注意点

- <注意点>

## 参照

- <関連ドキュメントやパターン>
```

**記述のガイドライン**:

- 汎用パターンは **特定のコネクタや組織に依存しない形** で記述する
- 組織ドメインパターンは具体的な業務・SaaS を含めて構わない
- レシピの具体的な値（チャンネル名、プロジェクト名等）のうち抽象化できるものは抽象化する
- 「なぜこの構造にするのか」の理由を設計判断ポイントに含める
- エキスパートが口頭で伝えるような実装上の勘所を「既知の注意点」に記録する

#### 既存パターンへの追記

追記前に Grep で重複がないか確認し、新しい知見のみ追記する:
- 新しい設計判断ポイント
- 新しい注意点（Gotcha）
- 構成図のバリエーション

### 4. インデックスの更新

新しいパターンを作成した場合、`org/docs/patterns/recipe-patterns/_index.md` のパターン一覧テーブルに行を追加する。
ファイルが存在しなければ `docs/patterns/recipe-patterns/_index.md`（kit canonical）と同じ形式で新規作成する。

### 5. 確認

作成・更新したパターンファイルの内容を利用者に提示し、過不足がないか確認する。
エキスパートの知見が正確に反映されているかが最も重要。

## 蓄積先

書き込み先は `org/docs/patterns/recipe-patterns/` の 1 箇所のみ。汎用 / 組織ドメインの区別はパターン本文の「スコープ」セクションで表現する（パスでは分けない）。

**書き込まない場所**:
- `docs/patterns/recipe-patterns/`（kit canonical、read-only）
- `projects/docs/patterns/`（レガシー。既存ファイルは読み込みのみ。新規書き込みは org 側に集約）

将来 kit へ還流する価値の高い汎用パターンが溜まったら、別途 kit リポジトリに PR を立てる（現時点ではスコープ外）。

## 出力

完了後、以下を報告:

- 作成・更新したパターンファイルと内容のサマリー
- 関連するフィールド知識の蓄積が必要なら `/learn-recipe` を案内

## Git 管理

書き込み先はワークスペースリポジトリの `org/docs/patterns/recipe-patterns/`（kit submodule の外）:

```bash
cd <workspace-root>
git add org/docs/patterns/recipe-patterns/
git commit -m "docs(org): record pattern <pattern-name>"
```

**kit submodule (`kit/`) には commit しない**。
