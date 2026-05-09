# Org Knowledge Overlay

組織ナレッジを kit のナレッジベース (`docs/`) と分離して蓄積するための規約。
kit を update しても組織の学習結果が失われない・上書きされないことを保証する。

## 構造

```
<workspace-root>/
├── docs/                       ← kit/docs/ への symlink（read-only）
│   ├── connectors/<name>.md
│   ├── logic/<topic>.md
│   ├── platform/<topic>.md
│   ├── patterns/<...>
│   └── learned-patterns.md
└── org/                        ← 組織ナレッジ。kit が一切 touch しない
    └── docs/                   ← docs/ と同じ階層を mirror
        ├── connectors/<name>.md
        ├── logic/<topic>.md
        ├── platform/<topic>.md
        ├── patterns/<...>
        └── learned-patterns.md
```

`org/` はワークスペースリポジトリで管理する（kit submodule の外）。
`org/docs/` 配下のディレクトリは必要に応じて作成してよい（事前に空ディレクトリを用意する必要はない）。

## 役割分担

| ナレッジの種類 | 置き場所 | 書き込むスキル |
|---|---|---|
| Workato 公式の仕様・全コネクタの API 情報 | `docs/` (kit) | `/sync-connectors`, `/auto-learn` |
| 組織が利用する範囲のフィールド情報・運用知見 | `org/docs/` | `/learn-recipe`, `/learn-pattern` |
| kit doc の誤り訂正・補足 | `org/docs/<同じ相対パス>` | 利用者が手動編集 |
| 組織独自のコネクタ・ロジック・パターン | `org/docs/<...>` | 利用者が手動編集 |

**kit の `docs/` を直接編集してはならない**（kit submodule への commit になる）。
誤りを発見した場合も `org/docs/<同じ相対パス>` に補正を書く。
将来 kit へ還流したくなった場合は別途 PR を立てる（現時点ではスコープ外）。

## 参照規約（読み込み）

スキルやレシピ作成プロセスが `@docs/<path>` を参照するときは、対応する `@org/docs/<path>` の存在を必ず確認し、存在すれば併せて読み込む：

1. `@docs/<path>` を読み込む
2. `@org/docs/<path>` が存在すれば読み込む
3. 両者で内容が矛盾する場合は **org 版を採用**（組織側が kit 標準より優先）
4. 両者で重複しない情報は両方とも採用

例:
- `@docs/connectors/clearbit.md` を参照する場合 → `@org/docs/connectors/clearbit.md` も確認
- `@docs/logic/data-pills.md` を参照する場合 → `@org/docs/logic/data-pills.md` も確認
- `@org/docs/connectors/<internal>.md` のように kit に対応 doc がない場合は org 単独で読む

## 書き込み規約

### 学習系スキル（`/learn-recipe` 等）

組織のレシピやプロジェクトから得た知見はすべて `org/docs/<相対パス>` に書く。

| 知見の種類 | 書き込み先 |
|---|---|
| connector のフィールド情報（input/output） | `org/docs/connectors/<provider>.md` |
| 新規 provider / action の発見 | `org/docs/connectors/<provider>.md` |
| Workato 内部プロバイダー | `org/docs/platform/<topic>.md` |
| ロジックステップの仕様 | `org/docs/logic/<topic>.md` |
| datapill パターン | `org/docs/logic/data-pills.md` |
| デプロイ関連の発見 | `org/docs/patterns/deployment-guide.md` |
| 分類不明な知見 | `org/docs/learned-patterns.md` |

書き込み前に対応する kit の `docs/<同じ相対パス>` を Read し、重複情報は書かない（kit 版で既知の内容は再記述しない。**差分・補正・組織固有の追加情報のみ** を `org/docs/` に記述する）。

### sync 系スキル（`/sync-connectors`, `/auto-learn`）

これらは Workato 公式から得た情報を kit canonical な `docs/` に書き込む。引き続き `kit/docs/connectors/<name>.md` 等に書く（kit submodule 内 commit）。組織側の `org/docs/connectors/<name>.md` には触らない。

## Git 管理

`org/docs/` 配下の変更はワークスペースリポジトリ側でコミットする：

```bash
cd <workspace-root>
git add org/docs/
git commit -m "docs(org): learn from <project-name> recipes"
```

kit submodule (`kit/`) には commit しない。

## ディレクトリの初期化

`org/docs/` は最初は存在しない。`/learn-recipe` 等が初めて書き込むときに自動作成する：

```bash
mkdir -p org/docs/connectors org/docs/logic org/docs/platform org/docs/patterns
```

スキル側が `Write` 時に必要なディレクトリを作る前提で、利用者が事前に作る必要はない。
