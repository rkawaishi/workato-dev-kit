# 設計思想・アーキテクチャ

Workato Dev Kit の設計判断と、その背景にある考え方を説明する。

## コア思想: AI エディタで Workato 開発を完結させる

Workato の自動化開発は通常 Web UI で行うが、以下の課題がある:

- **再現性がない** — UI 操作は手順書化しにくく、属人化する
- **レビューできない** — JSON の差分比較が困難
- **知見が蓄積しない** — 「このフィールドにはこの値を入れる」というノウハウが個人の記憶に留まる

本ツールキットは Claude Code / Cursor などの AI エディタを使い、**レシピ JSON の生成・検証・デプロイ・学習** をコードベースで行う。

### 対応エディタ

| エディタ | 利用者から見える場所 | 配布方法 | 正本（kit 内の実体） |
|---|---|---|---|
| **Claude Code** | `.claude/skills/`, `.claude/rules/`, `.claude/hooks/` | symlink | `kit/framework/claude/...` |
| **Cursor** | `.cursor/skills/`, `.cursor/rules/`, `.cursor/hooks.json` | **コピー** | `kit/framework/cursor/...`（`python3 scripts/sync_agents.py` で生成） |
| **Codex CLI** | `.agents/skills/` | symlink | `kit/framework/codex/skills/`（同上、slash 構文を `$` に書き換え） |
| **Gemini CLI** | `.gemini/skills/` | symlink | `kit/framework/gemini/skills/`（同上） |
| **エージェント中立** | `AGENTS.md` / `GEMINI.md`（同じ実体） | symlink | `kit/framework/AGENTS.md`（同上、CLAUDE.md + rules を集約） |

> **なぜ Cursor だけコピー？**: Cursor IDE は `.cursor/rules/*.mdc` や `.cursor/skills/<name>/` の symlink を確実に解決できない（[forum.cursor.com](https://forum.cursor.com/t/cursor-no-longer-can-follow-symlinks-to-rules-mdc-files/146010) で多数の報告。silent load failure、再起動後に検出されなくなる等）。v2.5 で部分修正されたが再発報告あり。Cursor 向けだけは `bash kit/setup.sh` で実ファイルとしてコピーし、kit を更新する度に再実行して再コピーする必要がある。
>
> kit-managed なファイルは `.cursor/.kit-manifest` で追跡され、kit から削除されたファイルは次回 setup.sh 実行時に prune される。利用者が `.cursor/rules/` 等に追加した独自ファイル（manifest に含まれないもの）は保持される。

> **kit 開発者向け**: スキルやルールを変更するときは `framework/claude/` 配下を編集する。利用者の `.claude/`、`.agents/`、`.gemini/` はそこへの symlink なので、kit のリリースが更新された瞬間に反映される（Cursor は再 setup 必要）。

どちらのエディタでも同じスキル (`/create-recipe`, `/push-project` 等) を同じ形式で呼び出せる。セットアップ手順はそれぞれのクイックスタートガイドを参照:
- [Claude Code クイックスタート](quickstart-claude-code.md)
- [Cursor クイックスタート](quickstart-cursor.md)

## リポジトリ構成

workato-dev-kit は組織のワークスペースリポジトリに `kit/` として submodule 追加して使う。

```
my-org-workato/               ← 組織のワークスペースリポジトリ（作業ルート）
├── .claude/                  # kit から symlink（+ 組織独自ルール/スキル）
│   ├── rules/
│   ├── skills/
│   └── hooks/
├── .cursor/                  # kit からコピー（Cursor 用、symlink 非対応のため）
├── docs/ → kit/docs/         # symlink（ナレッジベース）
├── guides/ → kit/guides/     # symlink
├── kit/                              ← git submodule（workato-dev-kit、読み取り専用）
│   ├── framework/claude/skills/      # 開発スキル（利用者の .claude/skills/ の symlink 元）
│   ├── framework/claude/rules/       # フォーマットルール（同上）
│   ├── framework/claude/hooks/       # 自動化フック（同上）
│   ├── docs/                         # AI 向けナレッジベース
│   └── guides/                       # 利用者向けガイド
│
├── projects/                 ← 組織のレシピ
│   └── <project-name>/
│       ├── DESIGN.md
│       ├── Recipes/
│       └── ...
│
└── connectors/               ← 組織のカスタムコネクタ
    └── <name>/connector.rb
```

### フレームワークと組織データの分離

| 観点 | フレームワーク (kit/) | 組織データ (projects/ connectors/) |
|---|---|---|
| 変更頻度 | スキル改善時 | 日常の開発作業 |
| 共有範囲 | チーム・組織横断 | プロジェクト固有 |
| 機密性 | 低（汎用ナレッジ） | 高（接続設定、業務ロジック） |
| 進化方法 | kit リポジトリに PR | ワークスペースリポジトリでコミット |

`kit/` は submodule として読み取り専用で参照する。

## ナレッジ階層

AI がレシピを生成する際、以下の優先順位で知識を参照する:

```
1. docs/connectors/         ← Pre-built コネクタの仕様（最優先、kit canonical）
                              + org/docs/connectors/  ← 組織側の補正・追記（併読）
2. connectors/docs/         ← カスタムコネクタの仕様
3. docs/logic/              ← ロジックステップの組み方
                              + org/docs/logic/       ← 組織側の補正（併読）
4. docs/platform/           ← プラットフォーム機能
                              + org/docs/platform/    ← 組織側の補正（併読）
5. .claude/rules/           ← JSON フォーマットルール
6. docs/patterns/recipe-patterns/      ← レシピ構築パターン（kit canonical）
   + org/docs/patterns/recipe-patterns/ ← 組織が記録したパターン（書き込み先）
   + projects/docs/patterns/           ← レガシー（読み込みのみ）
7. docs/patterns/           ← デプロイガイド等
```

矛盾する記述は **org 側が優先**（`@.claude/rules/org-knowledge-overlay.md` 参照）。

この階層は「具体 → 抽象」の順序になっている。コネクタ固有のフィールド名やデータ型が最も重要で、汎用的なパターンは補助的に使われる。

## 学習サイクル

本ツールキットの最大の特徴は **使うほどナレッジが育つ** 仕組みにある。

```
                    ┌──────────────────────┐
                    │   Workato UI で調整   │
                    └──────────┬───────────┘
                               ▼
              /pull-project で JSON を取得
                               │
                    ┌──────────▼───────────┐
                    │  /learn-recipe       │
                    │  /learn-pattern      │── ナレッジに反映
                    │  /sync-connectors   │
                    └──────────┬───────────┘
                               ▼
              docs/ に知見が蓄積される
                               │
                    ┌──────────▼───────────┐
                    │  /create-recipe      │
                    │  /plan               │── 次の開発に活用
                    └──────────────────────┘
```

Workato の JSON には UI でしか設定できないフィールドや、ドキュメント化されていない構造が多い。UI で調整 → pull → 学習 のサイクルを回すことで、これらの暗黙知がナレッジベースに蓄積される。

詳細は [ナレッジ管理ガイド](knowledge-management.md) を参照。

## 仕様駆動開発

各プロジェクトの各フィーチャーを `projects/<project>/specs/<NNN>-<slug>/` 配下の 3 ファイルに分けて管理する:

- **`spec.md`** — ユーザー体験と業務要件（WHAT/WHY、Workato 用語禁止）
- **`plan.md`** — Workato 構成（HOW、Data Table / Recipe / Connection / 適用パターン / Unlearned Actions）
- **`tasks.md`** — 実行可能タスク（`[P]` 並列マーク + `[recipe]` / `[page]` / `[learn]` 等のタグ）

`/spec` → `/clarify` → `/plan` → `/tasks` → `/analyze` → `/implement` の順で進める。中断耐性のため Open Questions は spec.md に永続化され、`/clarify` で再開できる。

> 旧 DESIGN.md 単一ファイル形式は `/design migrate` で specs/ に分割移行する。`/design new` は廃止済み（[ライフサイクルと責務マップ](lifecycle.md) の Deprecation フェーズを参照）。

## スキル体系

スキルは開発ライフサイクルの各フェーズをカバーする:

| フェーズ | スキル | 役割 |
|---|---|---|
| **仕様化** | `/spec`, `/clarify` | spec.md の作成・Open Questions 消化 |
| **設計** | `/plan`, `/tasks`, `/analyze` | plan.md / tasks.md の生成と整合性チェック |
| **構築** | `/implement`, `/create-recipe`, `/create-workflow-app`, `/create-genie`, `/create-connector` | アセット生成 |
| **検証** | `/validate-recipe` | JSON 構造チェック |
| **同期** | `/push-project`, `/pull-project` | Workato との同期 |
| **学習** | `/learn-recipe`, `/learn-pattern`, `/sync-connectors` | ナレッジ蓄積 |
| **整理** | `/catalog` | 共有アセットの棚卸し |
| **レガシー** | `/design migrate` | 旧 DESIGN.md → specs/ への移行ツール |

各スキルの詳細は [スキルリファレンス](skills-reference.md) を参照。

## ルール体系

`.claude/rules/` のルールファイルは、パスパターンに応じて自動適用される:

| ルール | 対象パス | 内容 |
|---|---|---|
| `workato-recipe-format.md` | `Recipes/**` | レシピ JSON の構造・フィールド仕様 |
| `workato-agentic-format.md` | `Agents/**` | Genie/Skill/MCP JSON 仕様 |
| `workato-page-components.md` | `Pages/**` | ページコンポーネントの仕様 |
| `workato-connector-sdk.md` | `connectors/**` | Connector SDK のフォーマット |
| `workato-project-structure.md` | `projects/**` | プロジェクト構造ルール（共有アセットの判断基準も含む） |
| `workato-cli.md` | (CLI 操作時) | CLI コマンドリファレンス |

Claude Code / Cursor ともにファイル編集時に該当ルールを自動参照し、正しい JSON 構造を生成する。Cursor では `.cursor/rules/` に同期されたルールがパスパターンに応じて自動適用される。

### マルチエディタ同期の注意点

kit リポジトリで `framework/claude/rules/` や `framework/claude/skills/` を変更した場合は、必ず同期スクリプトを実行して Cursor / Codex / Gemini 用ディレクトリと `AGENTS.md` を再生成する:

```bash
python3 scripts/sync_agents.py
```

コミット時は `framework/claude/` と `framework/{cursor,codex,gemini}/`、`framework/AGENTS.md` の変更を全て含めること。CI ([.github/workflows/sync-check.yml](../.github/workflows/sync-check.yml)) がドリフトを自動検出する。
