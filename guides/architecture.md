# 設計思想・アーキテクチャ

Workato Dev Kit の設計判断と、その背景にある考え方を説明する。

## コア思想: AI エディタで Workato 開発を完結させる

Workato の自動化開発は通常 Web UI で行うが、以下の課題がある:

- **再現性がない** — UI 操作は手順書化しにくく、属人化する
- **レビューできない** — JSON の差分比較が困難
- **知見が蓄積しない** — 「このフィールドにはこの値を入れる」というノウハウが個人の記憶に留まる

本ツールキットは Claude Code / Cursor などの AI エディタを使い、**レシピ JSON の生成・検証・デプロイ・学習** をコードベースで行う。

## デュアルリポジトリ構成

```
workato-dev-kit/              ← フレームワーク（このリポジトリ）
├── .claude/skills/           # 開発スキル
├── .claude/rules/            # フォーマットルール
├── docs/                     # AI 向けナレッジベース
├── guides/                   # 利用者向けガイド
│
├── projects/                 ← 組織リポジトリ（gitignore 対象）
│   └── <project-name>/
│       ├── DESIGN.md
│       ├── Recipes/
│       └── ...
│
└── connectors/               ← 組織リポジトリ（gitignore 対象）
    └── <name>/connector.rb
```

### なぜ分離するか

| 観点 | フレームワーク (workato-dev-kit) | 組織データ (projects/ connectors/) |
|---|---|---|
| 変更頻度 | スキル改善時 | 日常の開発作業 |
| 共有範囲 | チーム・組織横断 | プロジェクト固有 |
| 機密性 | 低（汎用ナレッジ） | 高（接続設定、業務ロジック） |
| 進化方法 | PR でスキル改善 | 組織内で開発・コミット |

`projects/` と `connectors/` は `.gitignore` に含まれており、フレームワークとは独立して git 管理する。

## ナレッジ階層

AI がレシピを生成する際、以下の優先順位で知識を参照する:

```
1. docs/connectors/         ← Pre-built コネクタの仕様（最優先）
2. connectors/docs/         ← カスタムコネクタの仕様
3. docs/logic/              ← ロジックステップの組み方
4. docs/platform/           ← プラットフォーム機能
5. .claude/rules/           ← JSON フォーマットルール
6. docs/patterns/recipe-patterns/  ← 汎用構築パターン
7. projects/docs/patterns/  ← 組織ドメインのパターン
8. docs/patterns/           ← デプロイガイド等
```

この階層は「具体 → 抽象」の順序になっている。コネクタ固有のフィールド名やデータ型が最も重要で、汎用的なパターンは補助的に使われる。

## 学習サイクル

本ツールキットの最大の特徴は **使うほどナレッジが育つ** 仕組みにある。

```
                    ┌──────────────────────┐
                    │   Workato UI で調整   │
                    └──────────┬───────────┘
                               ▼
              /wpull で JSON を取得
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
                    │  /design             │── 次の開発に活用
                    └──────────────────────┘
```

Workato の JSON には UI でしか設定できないフィールドや、ドキュメント化されていない構造が多い。UI で調整 → pull → 学習 のサイクルを回すことで、これらの暗黙知がナレッジベースに蓄積される。

詳細は [ナレッジ管理ガイド](knowledge-management.md) を参照。

## 設計書駆動開発

各プロジェクトに `DESIGN.md` を配置し、以下を管理する:

- **ユーザー体験**: 誰が・いつ・何をするか（ユーザーストーリー）
- **技術アーキテクチャ**: レシピ構成、コネクション、共有アセット
- **実装チェックリスト**: 各アセットの実装状況
- **設計判断**: なぜその構成を選んだか

`/design` スキルで作成・更新し、セッション開始時に読み込むことで、AI が一貫した設計判断を保てる。

## スキル体系

12 のスキルは開発ライフサイクルの各フェーズをカバーする:

| フェーズ | スキル | 役割 |
|---|---|---|
| **設計** | `/design` | 設計書の作成・更新 |
| **構築** | `/create-recipe`, `/create-workflow-app`, `/create-genie`, `/create-connector` | アセット生成 |
| **検証** | `/validate-recipe` | JSON 構造チェック |
| **同期** | `/wpush`, `/wpull` | Workato との同期 |
| **学習** | `/learn-recipe`, `/learn-pattern`, `/sync-connectors` | ナレッジ蓄積 |
| **整理** | `/catalog` | 共有アセットの棚卸し |

各スキルの詳細は [スキルリファレンス](skills-reference.md) を参照。

## ルール体系

`.claude/rules/` のルールファイルは、パスパターンに応じて自動適用される:

| ルール | 対象パス | 内容 |
|---|---|---|
| `workato-recipe-format.md` | `Recipes/**` | レシピ JSON の構造・フィールド仕様 |
| `workato-agentic-format.md` | `Agents/**` | Genie/Skill/MCP JSON 仕様 |
| `workato-page-components.md` | `Pages/**` | ページコンポーネントの仕様 |
| `workato-connector-sdk.md` | `connectors/**` | Connector SDK のフォーマット |
| `workato-project-structure.md` | `projects/**` | プロジェクト構造ルール |
| `workato-shared-assets.md` | (共有アセット関連) | 共有アセットの参照方法 |
| `workato-cli.md` | (CLI 操作時) | CLI コマンドリファレンス |

AI エディタはファイル編集時に該当ルールを自動参照し、正しい JSON 構造を生成する。
