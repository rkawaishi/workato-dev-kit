---
name: learn-pattern
description: レシピ構築パターンを組織ナレッジ層 (org/docs/patterns/ または projects/docs/patterns/) に記録・更新する。Workato エキスパートが他者サポート用にナレッジを蓄積する。
---

# /learn-pattern

Workato エキスパートが構築パターンを **組織ナレッジ層 (`org/docs/patterns/recipe-patterns/` または `projects/docs/patterns/`)** に記録するスキル。
エキスパートが既に持っている知見をドキュメント化することが目的。レシピは参考素材として任意で指定する。

書き込み先はすべて **ワークスペースリポジトリ側**（kit submodule の `docs/` には書かない）。詳細は `.cursor/rules/org-knowledge-overlay.mdc`。

## 使い方

- `/learn-pattern` — パターンの記録を開始（対話）
- `/learn-pattern ページネーションループ` — パターン名を指定して記録
- `/learn-pattern 承認ワークフロー 注意点追加` — 既存パターンに追記
- `/learn-pattern <file-path>` — レシピを参考素材として指定（パターンは対話で決める）

## 手順

### 1. エキスパートの意図を確認

まず既存パターンを把握する（kit canonical と組織側を併読、矛盾は org 側優先）:
- `docs/patterns/recipe-patterns/_index.md` — kit canonical の汎用パターン
- `org/docs/patterns/recipe-patterns/_index.md` — 組織が学習した汎用パターン（存在すれば）
- `projects/docs/patterns/_index.md` — 組織ドメインのパターン（存在すれば）

利用者に何をしたいかを確認する:

```
何を記録しますか？

A. 新しいパターンを追加（例: ページネーションループ、バッチ処理 etc.）
B. 既存パターンに知見を追記（注意点、バリエーション etc.）

蓄積先:
- 汎用（org/docs/patterns/recipe-patterns/）: <パターン名を列挙>
- 組織ドメイン（projects/docs/patterns/）: <パターン名を列挙>
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

#### 新規パターンのテンプレート

```markdown
# <パターン名> (<English Name>)

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

- パターンは **特定のコネクタや組織に依存しない汎用的な形** で記述する
- レシピの具体的な値（チャンネル名、プロジェクト名等）は抽象化する
- 「なぜこの構造にするのか」の理由を設計判断ポイントに含める
- エキスパートが口頭で伝えるような実装上の勘所を「既知の注意点」に記録する

#### 既存パターンへの追記

追記前に Grep で重複がないか確認し、新しい知見のみ追記する:
- 新しい設計判断ポイント
- 新しい注意点（Gotcha）
- 構成図のバリエーション

### 4. インデックスの更新

新しいパターンを作成した場合、蓄積先に応じたインデックスを更新する:

- **汎用パターン**: `org/docs/patterns/recipe-patterns/_index.md` のパターン一覧テーブルに行を追加（ファイル/ディレクトリが存在しなければ `mkdir -p` で作成し、`docs/patterns/recipe-patterns/_index.md`（kit canonical）と同じ形式で新規作成）
- **組織ドメインパターン**: `projects/docs/patterns/_index.md` に行を追加（ファイルが存在しなければ kit canonical と同じ形式で作成）

### 5. 確認

作成・更新したパターンファイルの内容を利用者に提示し、過不足がないか確認する。
エキスパートの知見が正確に反映されているかが最も重要。

## 蓄積先の判断

パターンには 2 つの蓄積先がある。どちらに置くかは利用者が判断する:

| 蓄積先 | 内容 | 例 |
|---|---|---|
| `org/docs/patterns/recipe-patterns/` | Workato プラットフォームに紐づく汎用パターン（組織が学習した範囲） | ページネーションループ、ブロッキングアクションの配置ルール |
| `projects/docs/patterns/` | 組織ドメインに紐づくパターン | 社内承認フローの構成、特定 SaaS 連携の定石 |

迷った場合の目安: 「Workato を使う他の組織でも同じ構成になるか？」→ Yes なら汎用 (`org/docs/patterns/recipe-patterns/`)、No なら組織ドメイン (`projects/docs/patterns/`)。

両方とも存在しなければディレクトリを `mkdir -p` で作成する。

**kit canonical な `docs/patterns/recipe-patterns/` には書き込まない**（kit submodule の変更になる）。汎用パターンが十分に洗練されて kit に還流する価値が出てきたら、別途 kit リポジトリに PR を立てる（現時点ではスコープ外）。

## 出力

完了後、以下を報告:

- 作成・更新したパターンファイルと内容のサマリー
- 関連するフィールド知識の蓄積が必要なら `/learn-recipe` を案内

## Git 管理

書き込み先はすべて **ワークスペースリポジトリ**（kit submodule の外）:

| 蓄積先 | リポジトリ | コミット先 |
|---|---|---|
| `org/docs/patterns/recipe-patterns/` | ワークスペースリポジトリ | ワークスペースルートでコミット |
| `projects/docs/patterns/` | ワークスペースリポジトリ | ワークスペースルートでコミット |

いずれか実際に書き込んだディレクトリだけを add する（両方を一度に add すると、片方が存在しないワークスペースで pathspec エラーになる）:

```bash
cd <workspace-root>

# 汎用パターンを書き込んだ場合:
git add org/docs/patterns/recipe-patterns/

# 組織ドメインパターンを書き込んだ場合:
git add projects/docs/patterns/

git commit -m "docs(org): record pattern <pattern-name>"
```

**kit submodule (`kit/`) には commit しない**。汎用パターンを kit canonical (`docs/patterns/recipe-patterns/`) に還流したい場合は別途 kit リポジトリに PR を立てる（現時点ではスコープ外）。
