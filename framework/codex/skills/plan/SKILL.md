---
name: plan
description: spec.md を読んで Workato 構成（HOW）を plan.md に書き起こす。パターンカタログ・CATALOG.md・.resource-providers.yml を引いて技術選択を確定。
---

# $plan

`spec.md` の要件を **Workato 構成** に落とし込み、`plan.md` を生成するスキル。

仕様駆動ワークフローで `$spec` → `$clarify` の後に位置する。ここでは「Workato でどう組むか」だけを決め、具体的なタスク分解は `$tasks` の責務。

## 使い方

- `$plan <project>/<NNN>-<slug>` — 指定フィーチャーの plan.md を生成
- `$plan <project>` — プロジェクト内で plan.md が無い最新 spec を自動選択
- `$plan` — カレントセッションの文脈から推定

## ワークフロー

```
$spec → $clarify → $plan → $tasks → $analyze → $implement
                    ↑
                  ここ
```

`$clarify` で Open Questions を消化済みであることが前提。未消化があれば「先に $clarify を実行してください」と案内して中断する。

## 手順

### 1. 前提チェック

- `projects/<project>/specs/<NNN>-<slug>/spec.md` を読む
- `## Open Questions` の未チェック項目があれば中断:
  ```
  Open Questions が <N> 件未解決です。先に $clarify <project>/<NNN>-<slug> を実行してください。
  ```
- `plan.md` が既に存在する場合は **更新モード**（既存内容を尊重して差分追記）

### 2. リソース情報の自動取得

`.resource-providers.yml` を読み、spec の `External Touchpoints` に出てくる外部サービスのリソース情報を事前取得する。

1. `.resource-providers.yml` が存在しなければスキップ（plan.md の `Open Issues` に「デプロイ後に確認」と記録）
2. 定義済みプロバイダーに対して `docs/platform/resource-providers.md` の手順でツールを検出・実行
3. 取得例:
   - Jira プロジェクトの Issue Type・カスタムフィールド → Data Table のフィールド設計に反映
   - Slack チャンネル一覧 → 通知先の具体化
   - Google Sheets のヘッダー行 → フィールドマッピング設計

> **重要**: 取得失敗はサイレントにスキップ。エラーで止めない。

### 3. 共有アセットカタログを確認

`projects/CATALOG.md` を読み、spec の要件で **既存の共有アセット**で対応可能な部分を特定:

- 共有 Recipe Function（マネージャー取得、通知送信等）が使えるか
- 共有コネクション（Slack, Jira 等）が使えるか
- 既存の Workflow App やパターンを参考にできるか

カタログがない場合は plan.md の `Notes` に「`$catalog scan` で生成可能」と書く。

### 4. パターンカタログを確認

ユーザー体験に合致する **構築パターン** を特定:

- `docs/patterns/recipe-patterns/_index.md`（kit canonical）
- `org/docs/patterns/recipe-patterns/_index.md`（組織側、存在すれば）
- `projects/docs/patterns/`（レガシー、後方互換のため読み込みのみ）

矛盾は組織側が優先。合致パターンの構成図・ステップ構成・既知の注意点を取り込む。

### 5. Workato 構成への変換

`spec.md` の各 User Story を Workato 構成要素にマッピングする。

**判断ポイント:**

| ユーザー体験 | Workato 構成要素 |
|---|---|
| フォームで申請 | Workflow App + Data Table + 送信ページ |
| 承認フロー | `human_review_on_existing_record` + ステージ |
| Slack 通知（ボタン付き） | `slack_bot/post_bot_message` + `attachment_buttons` + `bot_command_v2` ハンドラ |
| Slack 通知（情報のみ） | `slack_bot/post_bot_message` |
| メール通知 | `gmail/send_email` or `human_review` の email notification |
| 外部チケット起票 | `jira/create_issue`, ServiceNow 等 |
| データ検索（マネージャー等） | Recipe Function (Google Sheets, HRMS, etc.) |
| API からの申請 | MCP サーバー + スキルレシピ |
| 複数段階の承認 | 複数 `human_review` + ステージ |
| 条件分岐 | if/elsif/else |
| データの更新 | `update_request` / `workato_db_table` |

**レシピの分割判断:**

- 独立して再利用できるロジック → Recipe Function に切り出す
- ブロッキングアクション（`human_review`）→ 呼び出し元レシピに配置（Recipe Function に入れない）
- 外部トリガー（Slack ボタン等）→ 別レシピ（`complete_task` で連携）
- MCP 対応 → スキルレシピ（`add_record` + ワークフロー起動）

### 6. Workato API 設計の判断

Workato API を扱う設計（CLI/MCP、API Platform、OEM 連携等）が含まれる場合、`docs/platform/workato-api-systems.md` の比較表と判断フローを必ず読む（4 系統の混同で設計やり直しを防ぐため）。

### 7. plan.md を生成

下記テンプレートに従いファイルに書き出す。

### 8. 未学習アクションの抽出

Workato 公式ドキュメントや `docs/connectors/`・`connectors/docs/` に **情報が無いアクション/トリガー** を使う場合は `Unlearned Actions` を埋める。これは `$tasks` で `[learn]` タグ付きタスクに展開される。

### 9. 次ステップの案内

```
✓ plan.md を作成しました: projects/<project>/specs/<NNN>-<slug>/plan.md

主要な構成:
- <Architecture サマリ 3-5 件>

未学習アクション: <N> 件（$learn-recipe で実装後に学習が必要）

次は $tasks <project>/<NNN>-<slug> で実行可能タスクへの分解に進めます。
```

## plan.md テンプレート

```markdown
# <フィーチャー名> — Plan

## Metadata
- Status: Draft
- Created: <YYYY-MM-DD>
- Last updated: <YYYY-MM-DD>
- Spec: ./spec.md
- Project: <project-name>

## Architecture Overview
<!-- 全体構成の 1 段落要約 + 必要なら ASCII 図 -->
<図示や箇条書きで全体像>

## Applied Patterns
<!-- パターンカタログから該当パターンを記載 -->
- **<パターン名>** (`docs/patterns/recipe-patterns/<file>.md`): <適用箇所と理由>
- **<パターン名>** (`org/docs/patterns/recipe-patterns/<file>.md`): <適用箇所と理由>

## Reused Assets
<!-- CATALOG.md から該当する共有アセットを記載。なければ "None" -->
- **<共有 Function 名>** (`projects/<path>`): <用途>
- **<共有コネクション名>**: <用途>

## New Components

### Data Tables
- **<テーブル名>** (`<project>/Data Tables/<file>.data_table.json`):
  - フィールド: `<field1>` (string), `<field2>` (datetime), ...
  - 主キー / インデックス: <定義>

### Pages
- **<ページ名>** (`<project>/Pages/<file>.lcap_page.json`):
  - 役割: <送信/レビュー/承認/却下>
  - 主要コンポーネント: <フォーム、テーブル、ボタン>

### Recipes
- **<メインレシピ名>** (`<project>/Recipes/<file>.recipe.json`):
  - トリガー: <provider/event>
  - フロー: <ステップ概要>
- **<Recipe Function 名>**:
  - 用途: <再利用ロジック>
  - 入力 / 出力: <スキーマ概要>
- **<ハンドラレシピ名>**（Slack ボタン等）:
  - トリガー: `slack_bot/bot_command_v2`
  - フロー: `complete_task` で連携

### Connections
- **<コネクション名>** (`<project>/Connections/<file>.connection.json`):
  - Provider: <provider>
  - 認証方式: <oauth2 / api_key / etc>
  - 既存 / 新規: <既存 or 新規作成>

### MCP / Genie（必要な場合のみ）
- **<MCP サーバー名>**:
  - スキル: <skill 一覧>
  - 用途: <API 経由での申請受付等>

## Stage Transitions（承認フロー等がある場合）
<!-- ステージ遷移図 -->
```
draft → submitted → approved → completed
                 → rejected → (end)
```

## Resource Inventory
<!-- Step 2 で取得できたリソース情報。デプロイ後 UI で設定する項目を明示。 -->
- **Jira**: プロジェクト `DEV`, Issue Type `Task`
- **Slack**: チャンネル `#it-onboarding` (`C0123456`)
- **Google Sheets**: シート `employees`, ヘッダー [employee_id, manager_email, ...]

## Unlearned Actions
<!-- docs にフィールド情報が無く、ベストエフォートで実装するアクション/トリガー。$tasks で [learn] タスクに展開される。 -->
| provider | action/trigger | 備考 |
|---|---|---|
| | | |

## Open Issues
<!-- リソース取得失敗、デプロイ後に確認が必要な項目など -->
- <項目>

## Decisions
<!-- 技術設計の判断と理由 -->
- <YYYY-MM-DD>: <決定> — <理由>
```

## 守るべきルール

- **spec の Open Questions が残っていたら作業しない**: 必ず先に `$clarify`
- **CATALOG / パターン引きを省略しない**: 既存資産の再利用機会を逃さないため
- **Unlearned Actions を必ず明示**: docs に無いものはここで顕在化させ、後工程の `[learn]` タスクで必ず学習する
- **spec.md の本文は書き換えない**: 技術用語を spec に逆流させない。修正が必要なら `$clarify` で要件側を直す

## Git 管理

```bash
git add projects/<project-name>/specs/<NNN>-<slug>/plan.md
git commit -m "plan(<project>/<slug>): initial workato design"
git push origin
```
