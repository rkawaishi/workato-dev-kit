---
paths:
  - "projects/**"
  - "connectors/**"
---

# 3 リポジトリ構成での git 操作

このツールキットは 3 つの独立した git リポジトリが入れ子になっている。**どのリポジトリで `git` コマンドを実行するかを常に意識する必要がある。**

| リポジトリ | パス | 役割 | 遠隔 |
|---|---|---|---|
| 外側（フレームワーク） | `workato-dev-kit/` | スキル、ルール、ナレッジ docs | Anthropic/Workato 側のフレームワーク共有 |
| 内側: projects | `workato-dev-kit/projects/` | レシピ、ページ、DESIGN.md | 組織の git サーバー |
| 内側: connectors | `workato-dev-kit/connectors/` | カスタムコネクタ (connector.rb) | 組織の git サーバー |

外側の `.gitignore` は `projects/` と `connectors/` を除外しているため、外側での `git status` には内側の変更が一切映らない。**「外側で `git status` を見たら空だった」は「ファイルが生成されていない」を意味しない。** 必ず対応する内側リポジトリでも確認する。

## 原則: ファイル所属 = コミット先

ファイルが置かれたパスで、どのリポジトリにコミットすべきかが一意に決まる:

| 生成/編集されたパス | コミット先 |
|---|---|
| `docs/`, `.claude/`, `.cursor/`, `guides/`, `scripts/`, `templates/` | 外側 (`workato-dev-kit`) |
| `projects/<name>/**` (Recipes, Pages, Connections, DESIGN.md 等) | 内側 (`projects/`) |
| `connectors/<name>/**` (connector.rb, Gemfile 等) | 内側 (`connectors/`) |
| `connectors/docs/**` (/sync-connectors が自動生成) | 内側 (`connectors/`) |

## 定型パターン

### 内側リポジトリでの git 操作

**内側リポジトリは `projects/` 自体、`connectors/` 自体が git root**（各プロジェクト/コネクタ単位ではない。README のセットアップ手順で `cd projects; git init` している）。したがって全プロジェクトが 1 つの `projects` リポジトリに入る。

**必ず `cd` で入ってから実行する**（サブシェル `(cd … && …)` でも可）。外側のワーキングツリーからパス指定しても内側リポジトリには届かない:

```bash
# 正: 内側リポジトリ (projects/) のコンテキストで実行。パスは <project-name>/... でプレフィクス
(cd projects && git status)
(cd projects && git checkout -b feature/<branch>)
(cd projects && git add <project-name>/Recipes/ <project-name>/Connections/ <project-name>/DESIGN.md && git commit -m "<msg>")
(cd projects && git push origin feature/<branch>)

# 誤: 外側から内側のファイルを add しようとする
git add projects/<project-name>/Recipes/foo.recipe.json   # → gitignored なので何も起きない

# 誤: projects/<project-name> を git root と勘違いする
(cd projects/<project-name> && git status)   # → fatal: not a git repository
```

### スキル実行後のコミットフロー

スキル実行 → ファイル配置 → **配置先リポジトリで commit**。

```bash
# 例: /create-recipe で projects/my-project/Recipes/ に生成した場合
(cd projects && git status)
(cd projects && git checkout -b feature/my-project-<task>)
(cd projects && git add my-project/Recipes/ my-project/Connections/ && git commit -m "Add recipe: <name>")

# 例: /sync-connectors 実行後は 2 リポジトリをそれぞれコミット
git add docs/connectors/                                          # 外側
git commit -m "docs: update pre-built connector info"
(cd connectors && git add docs/ && git commit -m "docs: update custom connector info")   # 内側
```

### ブランチ戦略の独立性

内側リポジトリは外側と **独立したブランチ空間** を持つ。外側が `main` でも内側は別のブランチに居てよい:

```bash
# 外側
git branch --show-current              # main
# 内側
(cd projects && git branch --show-current)   # feature/my-project-foo
```

`projects/` は 1 つのリポジトリに全プロジェクトが同居するため、ブランチ名に `<project-name>-` プレフィクスを付けると他プロジェクトと混在しない（例: `feature/it-onboarding-add-approval`）。

大規模タスクで外側と内側の両方を触る場合は、**それぞれで同名のフィーチャーブランチ** を切って並走させると混乱が少ない。

## スキル × リポジトリ対応表

| スキル | 書き込み先 | コミット先 |
|---|---|---|
| `/create-recipe` | `projects/<name>/**` | 内側 projects |
| `/create-workflow-app` | `projects/<name>/**` | 内側 projects |
| `/create-genie` | `projects/<name>/Agents/` | 内側 projects |
| `/design` | `projects/<name>/DESIGN.md` | 内側 projects |
| `/wpull` | `projects/<name>/**` (Workato から取得) | 内側 projects |
| `/wpush` | なし (Workato API への push のみ) | **git への影響なし** |
| `/create-connector` | `connectors/<name>/**` | 内側 connectors |
| `/sync-connectors` | `docs/connectors/` (外側) + `connectors/docs/` (内側) | **両方** |
| `/learn-recipe` | `docs/connectors/`, `docs/logic/` 等 | 外側 |
| `/learn-pattern` | `docs/patterns/recipe-patterns/` (外側) または `projects/docs/patterns/` (内側 projects) | 書き込み先に従う |
| `/catalog` | 読み取りのみ (書き込む場合は `projects/CATALOG.md` → 内側) | 内側 projects |

**`/wpush` と `git push` は別物。** `/wpush` は Workato API へのデプロイで、ローカル git 履歴には何もしない。ローカルの変更を git リモートにも残したい場合は、別途 `(cd projects && git push)` が必要。

## 事故パターンと対処

### 事故 1: スキル実行後に外側で `git status` を見て「空だ、失敗した」と判断

→ 生成先は内側リポジトリ。**常に対応する内側でも `git status` を見る**。

### 事故 2: 外側で `git add projects/<name>/…` を打って何も起きない

→ 外側の `.gitignore` で弾かれている。`cd` で内側に入るか `(cd … && git add …)` を使う。

### 事故 3: `/wpush` しただけで git に履歴を残した気になる

→ `/wpush` は Workato API へのデプロイ。git 履歴には何も記録されない。必要なら内側リポジトリで別途コミット・プッシュする。

### 事故 4: 外側のフィーチャーブランチをマージしたら、内側の編集が一緒に main に流れてしまうと思っている

→ 外側と内側は完全に独立。外側のマージは内側に一切影響しない (逆も同様)。内側は内側で PR を出す。

### 事故 5: `/sync-connectors` 実行後、外側だけコミットして内側を忘れる

→ **両方**のリポジトリに書き込むスキル。実行後は必ず両方で `git status` を確認。

## チェックリスト（タスク開始時）

- [ ] 触るファイルが外側・内側どちらに属するか把握した
- [ ] 必要なリポジトリで適切なブランチを切った（`git checkout -b` は各リポジトリで個別に）
- [ ] `/wpush` / `/wpull` は git 操作と独立していることを認識している
- [ ] 2 リポジトリにまたがるスキル（`/sync-connectors`）を使う場合は両方コミットする
