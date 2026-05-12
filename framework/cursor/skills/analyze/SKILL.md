---
name: analyze
description: spec.md / plan.md / tasks.md の整合性を検証する。/implement の前に実行して、要件と実装計画のズレを早期に検出。
---

# /analyze

`spec.md` ↔ `plan.md` ↔ `tasks.md` の **整合性** を検証するスキル。`/tasks` の後・`/implement` の前に実行することで、フェーズ間のドリフトを早期検出する。

## 使い方

- `/analyze <project>/<NNN>-<slug>` — 指定フィーチャーを検証
- `/analyze <project>` — プロジェクト内の最新フィーチャーを検証

## ワークフロー

```
/spec → /clarify → /plan → /tasks → /analyze → /implement
                                      ↑
                                    ここ
```

## 検証項目

### A. 完成度チェック

- [ ] spec.md の `## Open Questions` に未チェック項目が無い
- [ ] plan.md が存在する
- [ ] tasks.md が存在する
- [ ] それぞれの `Last updated` が古すぎないか（spec が plan より新しい → plan の再生成が必要かも）

### B. spec → plan のトレース

`spec.md` の **各要件が plan で扱われているか** を確認:

| spec 要素 | plan で対応する箇所 | 検出パターン |
|---|---|---|
| User Stories のロール | `New Components` で該当ロールが操作する Page/Recipe がある | 各ロールに対応するアクションが設計されているか |
| External Touchpoints | `New Components` の Connections or Reused Assets | 言及されたサービスが Connections に出てくるか |
| Success Criteria | Architecture Overview や Stage Transitions | 観測可能な状態遷移として設計されているか |
| Constraints | plan の Decisions や Notes | 性能・セキュリティ要件が設計に反映されているか |
| Out of Scope | plan の範囲外であることの確認 | spec で除外したものが plan で扱われていない |

**Mismatch の検出例**:
- spec に「却下時に申請者に通知」とあるが plan に対応するレシピが無い
- spec の External Touchpoints に「Confluence」とあるが plan の Connections に出てこない
- spec の Out of Scope に「他社員からの代理申請」とあるが plan で代理ロジックが組まれている

### C. plan → tasks のトレース

`plan.md` の **各 New Component がタスク化されているか** を確認:

| plan 要素 | tasks で対応するタグ | 検出パターン |
|---|---|---|
| Data Tables | `[data-table]` | 全テーブルに対応するタスクがある |
| Pages | `[page]` | 全ページに対応するタスクがある |
| Recipes（メイン） | `[recipe]` | 全メインレシピに対応するタスクがある |
| Recipe Functions | `[function]` | 全 Function に対応するタスクがある |
| Handlers | `[handler]` | 全ハンドラに対応するタスクがある |
| Connections（新規） | `[connection]` or `[manual]` | 新規コネクションに対応するタスクがある |
| MCP / Genie | `[mcp]` | 該当タスクがある |
| Unlearned Actions（行あり）| `[learn]` | 全 unlearned 行に対応する learn タスクがある |

**Mismatch の検出例**:
- plan に Data Table が 3 つあるが tasks に `[data-table]` タスクが 2 つしかない
- plan の `Unlearned Actions` 表に 2 行あるが `[learn]` タスクが 0 件
- tasks に `[recipe]` タスクがあるが plan に対応するレシピ記載がない（過剰実装）

### D. デプロイガイド準拠

`docs/patterns/deployment-guide.md` のフローが tasks に組み込まれているか:

- [ ] `[validate]` タスクが `[push]` の前にある
- [ ] `[push]` タスクがある
- [ ] 新規コネクションがあれば `[manual]` で認証案内タスクがある
- [ ] `[test]` タスクがある
- [ ] `[pull]` タスクが `[test]` の後にある
- [ ] `[learn]` タスクが `[pull]` の後にある（Unlearned Actions があれば）

### E. 依存関係の妥当性

- 並列マーク `[P]` が誤っていないか:
  - 同じ Data Table を更新する複数の Recipe を `[P]` にしていないか
  - レシピと、それを参照するハンドラを `[P]` にしていないか
- `(depends: N)` の指す先が存在するか
- 循環依存がないか

## 手順

### 1. ファイルを読み込み

```
projects/<project>/specs/<NNN>-<slug>/
  ├── spec.md
  ├── plan.md
  └── tasks.md
```

3 ファイルとも存在しなければ、不足を明示してエラー終了。

### 2. A〜E の各カテゴリで検証

各項目を上から順に検証し、結果を **issue list** にまとめる。

issue の重大度:
- **🔴 BLOCKER**: そのまま `/implement` するとほぼ確実に問題が出る（要件未対応、デプロイガイド違反）
- **🟡 WARNING**: 注意が必要だが進める判断もある（過剰実装、ドリフト疑い）
- **🟢 INFO**: 改善提案レベル（命名統一、Decision の追記推奨）

### 3. レポート出力

下記フォーマットで stdout に出力する。**ファイルには書かない**（レポートは一過性）。

```
# /analyze レポート: <project>/<NNN>-<slug>

## サマリ
- 🔴 BLOCKER: <N> 件
- 🟡 WARNING: <M> 件
- 🟢 INFO: <L> 件

## A. 完成度チェック
✓ Open Questions: 全て解決済み（<N> 件）
✓ plan.md / tasks.md: 存在
🟡 spec.md (2026-05-10) > plan.md (2026-05-08): spec が plan より新しい。plan の再生成を推奨

## B. spec → plan のトレース
✓ User Stories (申請者, 承認者, 実行者) → 対応する Page/Recipe あり
✓ External Touchpoints (Slack, Jira) → Connections に対応あり
🔴 spec の Success Criteria「却下時に申請者通知」→ plan に対応レシピなし
🟢 spec の Constraints に「7 日以内のレスポンス」あり、plan で言及なし（Decisions 追記推奨）

## C. plan → tasks のトレース
✓ Data Tables (2 件) → [data-table] タスク 2 件
🔴 plan.md の Unlearned Actions に 2 行あるが [learn] タスクは 1 件
🟡 tasks に [recipe] approval_audit があるが plan に対応記載なし（過剰実装の可能性）

## D. デプロイガイド準拠
✓ [validate] → [push] → [manual] → [test] → [pull] → [learn] の順序 OK

## E. 依存関係の妥当性
✓ 循環依存なし
🟡 タスク 5 [P] [page] と タスク 4 [page] が同じ Data Table を更新する可能性（並列化の再検討推奨）

## 推奨アクション
1. 🔴 spec の「却下通知」を /plan で扱う（plan.md に追記して再 /tasks）
2. 🔴 unlearned 2 件目を [learn] タスクとして追加（/tasks 再生成）
3. 🟡 タスク 5 の [P] を外す or タスク 4 との順序を明示

BLOCKER が 0 件になるまで /implement を実行しないことを推奨します。
```

### 4. 判断の案内

```
🔴 BLOCKER: <N> 件
  → /plan または /tasks の再実行で修正してください

🟡 WARNING のみ:
  → 内容を確認して問題なければ /implement に進めます

🟢 INFO のみ:
  → /implement に進めます
```

## 守るべきルール

- **ファイルを書き換えない**: `/analyze` は read-only。発見した問題の修正は `/plan` か `/tasks` の責務
- **判断はユーザーに残す**: WARNING は機械的にブロックしない。レポートを出して判断を委ねる
- **冪等**: 何度実行しても同じレポートが出る

## 限界

`/analyze` は **アーティファクト間の整合性** を見るだけで、Workato 仕様としての正しさは見ない。
- レシピ JSON の妥当性 → `/validate-recipe`
- フィールドスキーマの正しさ → `/learn-recipe` 後の再 `/analyze`

## Git 管理

`/analyze` はファイルを書かないので git commit 不要。
