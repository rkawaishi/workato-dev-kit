---
name: spec
description: フィーチャーの要件（UX・WHAT/WHY）を spec.md に書き起こす。技術詳細は扱わない。プロジェクト開始時やフィーチャー追加時に使う。
---

# $spec

フィーチャーの **要件（WHAT/WHY）** を `projects/<project>/specs/<NNN>-<slug>$spec.md` に書き起こすスキル。

仕様駆動ワークフローの最初のステップ。技術スタック（Workato 構成）には踏み込まず、ユーザー体験と業務要件だけを固める。技術への落とし込みは `$plan` の責務。

## 使い方

- `$spec <project-name>` — 新規フィーチャーの spec.md を作成
- `$spec <project-name> <feature-slug>` — slug を指定して作成
- `$spec <project-name>/<NNN>-<slug>` — 既存 spec.md を更新

## ワークフロー

```
$spec → $clarify → $plan → $tasks → $analyze → $implement
  ↑
ここ
```

`$spec` 完了後、`Open Questions` が残っていれば `$clarify` を案内する。残っていなければ `$plan` に進める。

## 手順

### 1. フィーチャーの特定

- `<project-name>` がなければプロジェクト名を聞く
- `projects/<project-name>/specs/` を `ls` し、既存のフィーチャー番号から **次の連番** を決める（`001`, `002`, ...）
- フィーチャーのスラグ（短い英語キーワード、kebab-case）をユーザーに確認
  - 例: `it-onboarding`, `expense-approval`, `slack-digest`
- 最終パス: `projects/<project-name>/specs/<NNN>-<slug>$spec.md`

### 2. UX ヒアリング

**技術用語を避け、業務の言葉**で聞く。一度に全て聞かず、回答に応じて深掘りする。

```
このフィーチャーについて教えてください:

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

### 3. ユーザー体験の整理と確認

ヒアリング結果を **ユーザーストーリー** にまとめ、ユーザーに確認する。

```
## ユーザー体験（案）

### 申請者の体験
1. フォームを開く
2. 必要情報を入力して送信
3. ステータスが「承認待ち」に変わる
4. 承認されると通知を受け取る

### 承認者の体験
1. 承認依頼が届く（ボタン付き通知）
2. 内容を確認して承認 or 却下
3. 別経路（タスク画面等）からも操作可能

### 後続処理
- 承認時: 外部チケット起票 → 通知
- 却下時: 申請者に却下通知

この体験で合っていますか？追加や変更はありますか？
```

### 4. Open Questions の抽出（中断耐性のため必須）

ヒアリング中に**確定できなかった点**を洗い出して `Open Questions` に必ず書き出す。これは `$clarify` で消化する。

典型的な未確定事項:
- 承認者は単一か複数か？階層承認は必要か？
- 却下時の再申請は可能か？
- 通知の経路は Slack か Email か両方か？
- 申請データの保管期間は？
- 既存アカウントとの重複チェックは必要か？

**重要**: 「現時点で答えがあるが要確認」も Open Questions に入れる（その旨を注釈で書く）。完全に確定したものだけが本文に入る。

### 5. spec.md を生成

下記テンプレートに従いファイルに書き出す。**Workato 用語は使わない**（Recipe, Datapill, Connection 等は禁止）。

### 6. 次ステップの案内

```
✓ spec.md を作成しました: projects/<project>/specs/<NNN>-<slug>$spec.md

Open Questions が <N> 件残っています。
次は $clarify <project>/<NNN>-<slug> で消化してください。

（Open Questions が無い場合のみ）
このまま $plan <project>/<NNN>-<slug> に進めます。
```

## spec.md テンプレート

```markdown
# <フィーチャー名>

## Metadata
- Status: Draft
- Created: <YYYY-MM-DD>
- Last updated: <YYYY-MM-DD>
- Project: <project-name>
- Feature ID: <NNN>-<slug>

## Why（なぜやるか）
<業務上の課題、解決したい問題、得たい価値。1-3 段落。>

## User Stories

### <ロール1>（例: 申請者）
1. <ステップ>
2. <ステップ>
3. <ステップ>

### <ロール2>（例: 承認者）
1. <ステップ>
2. <ステップ>

### <ロール3>（例: 実行者）
1. <ステップ>

## Success Criteria
<!-- 何が起きれば成功か。観測可能な条件で書く。 -->
- [ ] <条件1>
- [ ] <条件2>

## External Touchpoints
<!-- 連携する外部サービス・データソース。業務名で書く（"チケット管理システム" 等）。技術選定は $plan で行う。 -->
- <サービス名>: <用途>
- <サービス名>: <用途>

## Constraints / Non-functional
<!-- 性能・セキュリティ・運用要件など。ある場合のみ。 -->
- <制約>

## Out of Scope
<!-- 今回やらないこと。後続フィーチャーに回すものを明記。 -->
- <項目>

## Open Questions
<!-- $clarify で消化する未確定事項。中断後の再開はこのチェックリストが起点。 -->
- [ ] <質問1>
- [ ] <質問2>

## Decisions
<!-- ヒアリング中に確定した重要な判断と理由。後から振り返る用。 -->
- <YYYY-MM-DD>: <決定> — <理由>
```

## 守るべきルール

- **Workato 用語禁止**: spec.md は技術中立。Recipe, Connection, Datapill, Workflow App などの単語を使わない（業務語に変換する）
- **Open Questions の永続化必須**: 曖昧な点はコンテキストに置かずファイルに書き出す。`$clarify` で再開できることが中断耐性の要
- **DESIGN.md は触らない**: 既存プロジェクトに DESIGN.md があっても spec.md は新規ファイルとして作る。移行は `$design migrate` の責務（Phase C で実装予定）

## `.workatoignore` の管理

新規プロジェクトで spec.md を作成する際、`.workatoignore` がなければ作成する:

```
DESIGN.md
specs/
```

既存の `.workatoignore` に `specs/` がなければ追記する。

## Git 管理

```bash
git add projects/<project-name>/specs/<NNN>-<slug>$spec.md projects/<project-name>/.workatoignore
git commit -m "spec(<project>/<slug>): initial spec"
git push origin
```

`workato push` は spec.md を Workato にデプロイしない（`.workatoignore` で除外）。
