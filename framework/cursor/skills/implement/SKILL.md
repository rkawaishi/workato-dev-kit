---
name: implement
description: tasks.md の未完了タスクを既存スキル（/create-recipe, /create-workflow-app 等）に振り分ける薄い orchestrator。タスク自体は実装せず、各スキルに委譲する。
---

# /implement

`tasks.md` の未完了タスクを **既存スキルに振り分ける薄い orchestrator**。

このスキル自身は JSON 生成や実装を行わず、タグ別に該当する既存スキルを起動するだけ。実装の責務は `/create-recipe`、`/create-workflow-app` 等が引き続き担う（二重実装を避けるため）。

## 使い方

- `/implement <project>/<NNN>-<slug>` — 指定フィーチャーのタスクを順次実行
- `/implement <project>/<NNN>-<slug> --task <ID>` — 単一タスクを実行
- `/implement <project>/<NNN>-<slug> --phase <N>` — Phase N のタスクを実行
- `/implement <project>/<NNN>-<slug> --dry-run` — 実行内容のみ表示

## ワークフロー

```
/spec → /clarify → /plan → /tasks → /analyze → /implement
                                                  ↑
                                                ここ
```

`/analyze` の BLOCKER が 0 件であることが推奨前提（強制ではない）。

## タグ → スキル マッピング

| タグ | 起動するスキル / アクション |
|---|---|
| `[connection]` | `/create-recipe` 内で扱う（独立タスクの場合は手動 or テンプレ生成） |
| `[connector]` | `/create-connector` |
| `[data-table]` | `/create-workflow-app`（Data Table 単独タスクとして実行） |
| `[page]` | `/create-workflow-app`（Page 単独タスクとして実行） |
| `[recipe]` | `/create-recipe` |
| `[function]` | `/create-recipe`（Recipe Function フラグ付き） |
| `[handler]` | `/create-recipe`（ハンドラレシピとして） |
| `[mcp]` | `/create-genie` |
| `[validate]` | `/validate-recipe` |
| `[push]` | `/push-project` |
| `[pull]` | `/pull-project` |
| `[learn]` | `/learn-recipe` |
| `[learn-pattern]` | `/learn-pattern` |
| `[manual]` | ユーザーに作業内容を案内、完了報告を待つ |
| `[test]` | ユーザーにテストシナリオを案内、結果報告を待つ |

## 手順

### 1. 前提チェック

- `projects/<project>/specs/<NNN>-<slug>/tasks.md` を読む
- 存在しなければ「先に /tasks を実行してください」と案内して中断
- `/analyze` を実行することを推奨（未実行なら警告）

### 2. 未完了タスクを抽出

- `- [ ]` の行のみ拾う
- 依存関係 (`depends: N, M`) を確認し、未完了の先行タスクがあるタスクは **スキップ候補**
- 実行可能なタスクをリストアップ

```
実行可能なタスク: <K> 件 / 未完了: <N> 件

次に実行可能（依存関係を満たす）:
  3. [connection] connection_name を作成
  4. [P] [data-table] requests テーブル
  5. [P] [data-table] approvals テーブル
  7. [function] マネージャー取得 Function

依存待ち（先行タスク未完了）:
  6. [page] 申請フォームページ (depends: 4)
  ...
```

### 3. 実行モードの選択

ユーザーに以下を提示:

```
実行方法を選んでください:
1. 順次実行: 1 タスクずつ確認しながら進める
2. Phase 単位: 同じ Phase 内のタスクをまとめて実行
3. 単一タスク: タスク番号を指定（--task で指定可）
4. dry-run: 実行内容のみ表示、起動しない
```

`[P]` 付きタスクは Phase 単位実行時に **並列起動の選択肢** を提示する。

### 4. タスクごとの実行

各タスクに対して:

#### 4a. プリブリーフ

```
========================================
タスク <ID>: <タグ> <内容>
依存: <depends>
担当スキル: <スキル名>
========================================
```

#### 4b. コンテキスト引き渡し

該当スキルに渡すべき情報を `spec.md` / `plan.md` / `tasks.md` から抽出:

例 `[recipe] approval_main` の場合:
- `plan.md` の Recipes セクションから当該レシピの定義（トリガー、フロー、入出力）
- `plan.md` の Resource Inventory（リソース選択値）
- `plan.md` の Reused Assets（参照すべき共有 Function）

#### 4c. スキル起動

該当スキルを `Agent` ツールで呼び出すか、ユーザーに `/create-recipe` 等の起動を案内する。

> **重要**: `/implement` 自身が JSON を生成してはいけない。必ず該当スキルに委譲する。

#### 4d. 完了確認とチェックオン

スキル完了後、生成物を確認:
- ファイルが期待パスに作成されたか
- 必要なら簡易バリデーション

問題なければ `tasks.md` の該当行を `- [x]` に更新し、`Last updated` を更新。
失敗した場合は `- [ ] <内容> ⚠️ FAILED: <理由>` に書き換えて次へ進むか中断するか問う。

### 5. Phase 完了 / 全体完了

Phase 末尾に達したら:

```
✓ Phase <N> 完了
完了タスク: <K> 件 / 失敗: <F> 件 / 残り: <R> 件

次の Phase に進みますか？
```

全タスク完了:

```
🎉 全タスク完了

サマリ:
- 生成ファイル: <一覧>
- 学習済みアクション: <一覧>
- パターン蓄積: <件数>

次のアクション候補:
- /design update（DESIGN.md 移行期の場合）
- /catalog scan（共有アセットを更新する場合）
- 次フィーチャーの /spec
```

## 並列実行（`[P]` タスク）

Phase 単位実行時、`[P]` マーク付きの連続タスクを並列起動できる。

```
Phase 2 に [P] タスクが 3 件あります:
  4. [P] [page] 申請フォームページ
  5. [P] [page] 承認画面ページ
  6. [P] [page] 却下通知ページ

並列起動しますか？ (Y/N)
```

並列起動は **独立した Agent コール** として実行。失敗したものだけ後から再実行できる。

> **注意**: 並列実行は CONTEXT 消費が大きい。3 件以上の `[P]` は逐次推奨。

## `[manual]` / `[test]` の扱い

これらはユーザー作業:

```
タスク 13 [manual]: 新規コネクション (slack_bot, jira) の認証

以下の URL で UI を開いてください:
  https://<workato-region>/folders/<folder_id>

認証完了したら教えてください（"完了" / "失敗"）。
```

完了報告を受けてからチェックオン。

## 守るべきルール

- **自分で実装しない**: `/implement` は orchestrator。レシピ JSON 等は必ず該当スキルに任せる
- **タスクのチェック更新は確実に**: 完了 → `[x]`、失敗 → `⚠️ FAILED`。曖昧なまま次に進まない
- **依存関係を尊重**: `depends:` を無視して並列起動しない
- **dry-run を推奨**: 大量タスクを一気に流す前に `--dry-run` で確認

## エラーハンドリング

- スキル起動失敗 → ユーザーに状況を報告、中断 or スキップを問う
- 並列起動の一部失敗 → 成功分はチェックオン、失敗分は `⚠️ FAILED` でマーク、ユーザー判断
- 依存タスクの完了状態が tasks.md と実態でズレ → ユーザーに確認して tasks.md を修正

## Git 管理

タスクごとに commit するか Phase 単位で commit するかはユーザー判断。デフォルトは Phase 単位:

```bash
git add projects/<project-name>/specs/<NNN>-<slug>/tasks.md projects/<project-name>/Recipes/ ...
git commit -m "implement(<project>/<slug>): phase <N> complete"
git push origin
```
