---
name: tasks
description: plan.md を読んで実行可能タスクを tasks.md に分解する。並列マーク [P] と種類タグ（[recipe]/[page]/[learn] 等）で $implement が振り分けられる形に。
---

# $tasks

`plan.md` を **実行可能なタスクリスト** に分解し、`tasks.md` を生成するスキル。

仕様駆動ワークフローで `$plan` の後に位置する。タグと依存関係を明示することで、後段の `$implement` が既存スキルにタスクを振り分けられるようにする。

## 使い方

- `$tasks <project>/<NNN>-<slug>` — 指定フィーチャーの tasks.md を生成
- `$tasks <project>` — plan.md があり tasks.md が無い最新フィーチャーを自動選択

## ワークフロー

```
$spec → $clarify → $plan → $tasks → $analyze → $implement
                            ↑
                          ここ
```

## 手順

### 1. plan.md を読む

- `projects/<project>/specs/<NNN>-<slug>$plan.md` を読む
- 既存 `tasks.md` があれば **更新モード**（チェック状態を保持して差分追加）

### 2. タスクを抽出してタグ付け

`plan.md` の各セクションからタスクを切り出し、**種類タグ** と **並列マーク** を付ける。

#### 種類タグ（必須、1 つだけ）

| タグ | 担当スキル | 例 |
|---|---|---|
| `[connection]` | （手作業 or `$create-recipe` 内で生成） | コネクション JSON を作成 |
| `[connector]` | `$create-connector` | カスタムコネクタを実装 |
| `[data-table]` | `$create-workflow-app` | Data Table スキーマを作成 |
| `[page]` | `$create-workflow-app` | Workflow App ページを作成 |
| `[recipe]` | `$create-recipe` | レシピ JSON を生成 |
| `[function]` | `$create-recipe` | Recipe Function を生成 |
| `[handler]` | `$create-recipe` | ハンドラレシピ（Slack ボタン等） |
| `[mcp]` | `$create-genie` | MCP サーバー / Genie / スキル |
| `[validate]` | `$validate-recipe` | JSON 構造検証 |
| `[push]` | `$push-project` | Workato へデプロイ |
| `[pull]` | `$pull-project` | UI 調整後の取り込み |
| `[learn]` | `$learn-recipe` | Unlearned Actions の学習 |
| `[learn-pattern]` | `$learn-pattern` | 構築パターンをカタログに追加 |
| `[manual]` | （ユーザー作業） | UI でのコネクション認証、リソース設定等 |
| `[test]` | （ユーザー or `$implement`） | エンドツーエンドテスト |

#### 並列マーク `[P]`

依存関係がなく **並列実行可能** なタスクには `[P]` を付ける。`$implement` がこのマークを見て並列起動可否を判断する。

例:
- `[P] [data-table] requests テーブル` と `[P] [data-table] approvals テーブル` は並列可
- `[recipe] approval_main` と `[handler] slack_approve_handler` は依存ありなので並列不可（前者の `as` を後者が参照）

### 3. 依存関係の表現

並列マークだけでは表現できない順序依存は **タスクの並び順** と必要に応じて `(depends: <task-id>)` 注記で示す。

```
1. [data-table] requests テーブルを作成
2. [data-table] approvals テーブルを作成
3. [P] [page] 申請フォームページ (depends: 1)
4. [P] [page] 承認画面ページ (depends: 1, 2)
5. [recipe] approval_main を生成 (depends: 1, 2)
6. [handler] slack_approve_handler を生成 (depends: 5)
7. [validate] 全レシピを検証 (depends: 5, 6)
8. [push] Workato にデプロイ (depends: 7)
9. [manual] Slack/Jira コネクション認証 (depends: 8)
10. [test] 申請 → 承認 → 起票の E2E (depends: 9)
11. [pull] UI 調整内容を取り込み (depends: 10)
12. [learn] jira/create_issue を学習 (depends: 11)
```

### 4. Unlearned Actions の自動展開

`plan.md` の `## Unlearned Actions` 表に行があれば、必ず `[learn]` タスクに展開する:

```
| provider | action/trigger | 備考 |
|---|---|---|
| jira | create_issue | カスタムフィールドあり |
| servicenow | create_record | input スキーマ不明 |
```

↓

```
- [ ] [learn] jira/create_issue を $learn-recipe で学習しドキュメント化
- [ ] [learn] servicenow/create_record を $learn-recipe で学習しドキュメント化
```

**重要**: `[learn]` タスクは `[push]` → `[pull]` の後に配置する（実装後の学習サイクルを反映）。

### 5. デプロイガイドの組み込み

`docs/patterns/deployment-guide.md` の「レシピのデプロイフロー」に従い、以下を必ずタスク化:

1. `[validate]` — push 前検証
2. `[push]` — Workato へデプロイ
3. `[manual]` — 新規コネクションがある場合は認証案内
4. `[manual]` — UI でテスト実行
5. `[pull]` — 調整内容を取り込み
6. `[learn]` — Unlearned Actions を学習
7. `[learn-pattern]` — 新しい構築パターンがあれば追加

### 6. tasks.md を生成

下記テンプレートに従いファイルに書き出す。

### 7. 次ステップの案内

```
✓ tasks.md を作成しました: projects/<project>/specs/<NNN>-<slug>$tasks.md

合計 <N> タスク（並列可能: <M> 件、学習タスク: <L> 件）

次は $analyze <project>/<NNN>-<slug> で spec ↔ plan ↔ tasks の整合性を検証してから、
$implement <project>/<NNN>-<slug> で実装に進めます。
```

## tasks.md テンプレート

```markdown
# <フィーチャー名> — Tasks

## Metadata
- Status: Draft
- Created: <YYYY-MM-DD>
- Last updated: <YYYY-MM-DD>
- Spec: .$spec.md
- Plan: .$plan.md

## Progress
- Total: <N>
- Completed: <0>
- In Progress: <0>
- Blocked: <0>

## Tag Legend
- `[P]` 並列実行可能
- 種類タグ: `[recipe]`, `[function]`, `[handler]`, `[page]`, `[data-table]`, `[connection]`, `[connector]`, `[mcp]`, `[validate]`, `[push]`, `[pull]`, `[learn]`, `[learn-pattern]`, `[manual]`, `[test]`
- `(depends: N, M)` 先行タスク ID

## Tasks

### Phase 1: 基盤構築

- [ ] 1. [P] [data-table] `<table_name>` を作成（フィールド: <一覧>）
- [ ] 2. [P] [data-table] `<table_name>` を作成
- [ ] 3. [connection] `<connection_name>` を作成（provider: <provider>, 新規/既存）

### Phase 2: フロー実装

- [ ] 4. [page] 申請フォームページ (depends: 1)
- [ ] 5. [P] [page] 承認画面ページ (depends: 1, 2)
- [ ] 6. [P] [page] 却下通知ページ (depends: 1)
- [ ] 7. [function] マネージャー取得 Function (depends: 3)
- [ ] 8. [recipe] `approval_main` レシピ (depends: 1, 2, 7)
- [ ] 9. [handler] `slack_approve_handler` (depends: 8)
- [ ] 10. [mcp] MCP サーバー / スキルレシピ（任意）(depends: 8)

### Phase 3: 検証とデプロイ

- [ ] 11. [validate] 全 JSON を $validate-recipe で検証 (depends: 8, 9)
- [ ] 12. [push] $push-project でデプロイ (depends: 11)
- [ ] 13. [manual] 新規コネクションの認証（UI 操作）(depends: 12)
- [ ] 14. [test] 申請 → 承認 → 起票の E2E テスト (depends: 13)

### Phase 4: 学習とフィードバック

- [ ] 15. [pull] $pull-project で UI 調整内容を取り込み (depends: 14)
- [ ] 16. [learn] `<provider>/<action>` を $learn-recipe で学習 (depends: 15)
- [ ] 17. [learn-pattern] 新規パターンを $learn-pattern でカタログ化（該当時）(depends: 15)

## Notes
<!-- $implement 実行時の注意点、ロールバック条件など -->
- <注記>
```

## 守るべきルール

- **種類タグは必須**: タグなしのタスクは `$implement` が振り分けられない
- **並列マーク `[P]` は誠実に**: 並列起動して壊れるなら付けない（特にレシピは前段の `as` を後段が参照することが多い）
- **学習タスクを省略しない**: `Unlearned Actions` を `[learn]` 化しないとナレッジ欠落が放置される
- **plan.md の本文は書き換えない**: タスク化中に設計を変えたくなったら `$plan` を再実行

## Git 管理

```bash
git add projects/<project-name>/specs/<NNN>-<slug>$tasks.md
git commit -m "tasks(<project>/<slug>): initial breakdown"
git push origin
```
