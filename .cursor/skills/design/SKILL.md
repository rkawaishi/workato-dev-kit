---
name: design
description: プロジェクトの設計書 (DESIGN.md) を作成・更新・参照する。セッション開始時やタスク完了時に使用。
---

# /design

プロジェクトの設計書 (DESIGN.md) を管理するスキル。設計書はセッション跨ぎの計画・進捗・意思決定の永続記録。

## 使い方

- `/design` — 現在のプロジェクトの設計書を表示
- `/design <project-name>` — 指定プロジェクトの設計書を表示
- `/design new <project-name>` — 新規設計書を作成（ヒアリング → 設計）
- `/design update` — 現在の進捗で設計書を更新

## 設計書の場所

`projects/<project-name>/DESIGN.md`

プロジェクトフォルダ直下に配置。`.workatoignore` に `DESIGN.md` を含めて `workato pull` で消えないようにする。

## `/design new` — ヒアリングから設計書作成

### Phase 1: ユーザー体験のヒアリング

まず **何を実現したいか**（技術的な詳細ではなく業務の言葉で）を聞く。

```
このプロジェクトについて教えてください:

1. **誰が・何をしたいですか？**
   例: 新入社員の IT セットアップを申請したい、経費を申請して承認を得たい

2. **どんな流れをイメージしていますか？**
   例: フォームで申請 → マネージャーが承認 → IT チームに通知

3. **関わる人は誰ですか？**
   例: 申請者、マネージャー（承認者）、IT チーム（実行者）

4. **最終的に何が起きれば成功ですか？**
   例: Jira チケットが作られて IT チームが作業を開始できる

5. **既存のツールやデータソースはありますか？**
   例: マネージャー情報は Google Sheets にある、通知は Slack で行いたい
```

ユーザーの回答を待つ。一度に全て聞かず、回答に応じて深掘りする。

### Phase 2: ユーザー体験の整理

ヒアリング結果を**ユーザーストーリー**として整理し、ユーザーに確認する。

```
## ユーザー体験（案）

### 申請者の体験
1. Workflow App のフォームを開く
2. 必要情報を入力して送信
3. ステータスが「承認待ち」に変わる
4. 承認されると通知を受け取る

### 承認者の体験
1. Slack DM で承認依頼が届く（ボタン付き）
2. 内容を確認して承認 or 却下をクリック
3. Workflow App のタスク画面からも操作可能

### 後続処理
1. 承認: Jira チケット自動起票 → Slack チャンネルに通知
2. 却下: 申請者に却下通知

この体験で合っていますか？追加や変更はありますか？
```

### Phase 3: 技術設計への落とし込み

ユーザー体験が確定したら、Workato の具体的な構成に変換する。

**まず `projects/CATALOG.md` を確認**し、既存の共有アセットで対応可能な部分を特定する:
- 共有 Recipe Function（マネージャー取得、通知送信等）が使えるか
- 共有コネクション（Slack, Jira 等）が使えるか
- 既存の Workflow App やパターンを参考にできるか

カタログがない場合は `/catalog scan` で生成できることを案内。

**次にパターンカタログを確認**し、ユーザー体験に合致する構築パターンを特定する:
- `docs/patterns/recipe-patterns/_index.md`（汎用）と `projects/docs/patterns/`（組織ドメイン）を読み、該当パターンを検索
- 合致するパターンがあればユーザーに提案:
  ```
  このプロジェクトには以下のパターンが使えそうです:
  - **承認ワークフロー**: フォーム申請 → 承認者が判断 → 後続処理
  - **エラー通知**: 各レシピに共通エラーハンドラを組み込み

  パターンの詳細を確認しますか？
  ```
- 合致するパターンの構成図とステップ構成を設計書の Architecture セクションに反映

**判断ポイント:**

| ユーザー体験 | Workato 構成要素 |
|---|---|
| フォームで申請 | Workflow App + Data Table + 送信ページ |
| 承認フロー | human_review_on_existing_record + ステージ |
| Slack 通知（ボタン付き） | slack_bot/post_bot_message + attachment_buttons + bot_command_v2 ハンドラ |
| Slack 通知（情報のみ） | slack_bot/post_bot_message |
| メール通知 | gmail/send_email or human_review の email notification |
| 外部チケット起票 | jira/create_issue, servicenow 等 |
| データ検索（マネージャー等） | Recipe Function (Google Sheets, HRMS, etc.) |
| API からの申請 | MCP サーバー + スキルレシピ |
| 複数段階の承認 | 複数 human_review + ステージ |
| 条件分岐 | if/elsif/else |
| データの更新 | update_request / workato_db_table |

**レシピの分割判断:**
- 独立して再利用できるロジック → Recipe Function に切り出す
- ブロッキングアクション（human_review）→ 呼び出し元レシピに配置（Recipe Function に入れない）
- 外部トリガー（Slack ボタン等）→ 別レシピ（complete_task で連携）
- MCP 対応 → スキルレシピ（add_record + ワークフロー起動）

### Phase 4: 設計書の生成

ヒアリング結果と技術設計をテンプレートに落とし込んでファイルに書き出す。

## 設計書のテンプレート

```markdown
# <プロジェクト名>

## Status: <Draft | In Progress | Testing | Done>
Last updated: <YYYY-MM-DD>

## User Experience

### <ロール1>（例: 申請者）
1. <ステップ>
2. <ステップ>

### <ロール2>（例: 承認者）
1. <ステップ>
2. <ステップ>

### 後続処理
1. <承認時の処理>
2. <却下時の処理>

## Architecture

### 適用パターン
<!-- パターンカタログ (docs/patterns/recipe-patterns/) から該当パターンを記載 -->
- <パターン名>: <適用箇所と理由>

### 既存アセットの再利用
<!-- カタログ (projects/CATALOG.md) から該当するアセットを記載 -->
- <共有 Function / コネクション名>: <用途>

### 新規作成
- **Data Table**: <テーブル名>
  - フィールド: <一覧>
- **ステージ**: <ステージ遷移>
- **外部連携**: <サービス一覧と用途>
- **レシピ構成**:
  - メインレシピ: <トリガー → フロー概要>
  - Recipe Function: <名前 — 用途>
  - ハンドラ: <名前 — 用途>（Slack ボタン等）
  - MCP スキル: <名前 — 用途>（必要な場合）

## Implementation Checklist
- [ ] Data Table スキーマ
- [ ] ページ（送信/レビュー/承認/却下）
- [ ] メインレシピ
- [ ] Recipe Function
- [ ] コネクション認証
- [ ] MCP サーバー（必要な場合）
- [ ] エンドツーエンドテスト
- [ ] pull → learn-recipe

## Decisions
<!-- 設計判断とその理由を記録 -->

## Open Issues
<!-- 未解決の問題 -->
```

## 操作

### `/design` / `/design <project-name>` — 参照

1. `projects/<project-name>/DESIGN.md` を読む
2. 内容を表示
3. 未完了のチェックリスト項目があれば次のアクションを提案

### `/design update` — 更新

1. 現在の DESIGN.md を読む
2. プロジェクト内のファイルを確認し、実装済み項目を特定:
   - `*.recipe.json` があれば → レシピ項目をチェック
   - `*.lcap_page.json` があれば → ページ項目をチェック
   - `*.workato_db_table.json` があれば → Data Table 項目をチェック
   - `*.mcp_server.json` があれば → MCP 項目をチェック
   - `*.connection.json` があれば → コネクション項目をチェック
3. チェックリストを更新
4. Status と Last updated を更新
5. 新たな Decisions や Open Issues があれば追記
6. 変更内容をサマリー表示

## `.workatoignore` の管理

新規プロジェクトで DESIGN.md を作成する際、`.workatoignore` がなければ作成する:

```
DESIGN.md
```

既存の `.workatoignore` に `DESIGN.md` がなければ追記する。
