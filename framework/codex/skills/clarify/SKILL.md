---
name: clarify
description: spec.md の Open Questions を 1 件ずつ消化して本文に反映する。$spec の後、$plan の前に実行。中断後の再開はこのスキルから。
---

# $clarify

`spec.md` の `## Open Questions` セクションに残っている未確定事項を **1 件ずつ消化** し、回答を spec 本文に反映するスキル。

仕様駆動ワークフローで `$spec` と `$plan` の間に位置する。`$spec` が書き出した曖昧点をここで全て潰してから設計に進むことで、後工程の手戻りを防ぐ。

**中断耐性の要**: コンテキスト枯渇や中断で `$spec` の途中状態が失われても、Open Questions がファイルに残っている限り `$clarify` で再開できる。

## 使い方

- `$clarify <project>/<NNN>-<slug>` — 指定フィーチャーの Open Questions を消化
- `$clarify <project>` — プロジェクト内で Open Questions が残る最新フィーチャーを自動選択
- `$clarify` — カレントセッションの文脈から推定（曖昧なら確認）

## ワークフロー

```
$spec → $clarify → $plan → $tasks → $analyze → $implement
          ↑
        ここ
```

## 手順

### 1. spec.md を読む

- `projects/<project>/specs/<NNN>-<slug>$spec.md` を読む
- `## Open Questions` セクションの未チェック項目（`- [ ] ...`）を抽出
- 全てチェック済みなら「Open Questions は全て解決済みです。$plan に進めます。」と案内して終了

### 2. 質問を 1 件ずつ提示

**1 件ずつ** 提示する。まとめて聞かない（回答品質が落ちる）。

```
Open Questions が <N> 件残っています。1件ずつ確認させてください。

[1/N] <質問内容>

選択肢の候補（あれば）:
- A: <案>
- B: <案>
- C: その他（自由記述）

回答をお願いします。
```

### 3. 回答を反映

回答を得たら **その場で spec.md を更新** する:

1. 該当する Open Questions の項目を `- [x]` にチェック
2. 回答に応じて spec 本文の該当セクションを更新
   - 承認者の範囲が決まった → User Stories の該当ロールを更新
   - 通知経路が決まった → External Touchpoints を更新
   - 制約が判明 → Constraints / Non-functional に追記
   - 範囲外と判明 → Out of Scope に移動
3. `## Decisions` セクションに `<YYYY-MM-DD>: <決定> — <理由>` を追記
4. `Last updated` を更新

### 4. 派生する Open Questions の追加

回答から **新たな曖昧点** が浮かんだら、その場で Open Questions に追記する（同じセッションで連続消化可）。

例:
```
Q: 承認者は単一ですか複数ですか？
A: マネージャー1名 + 必要に応じて部門長
→ 新規 Open Question: 「部門長承認が必要な条件は？金額/カテゴリ/役職等」
```

### 5. 全消化後の案内

全 Open Questions がチェック済みになったら:

```
✓ Open Questions を全て解決しました（<N> 件）。

主要な決定:
- <Decisions から重要なものを 3-5 件サマリ>

次は $plan <project>/<NNN>-<slug> で Workato 構成への落とし込みに進めます。
```

## 質問の進め方のコツ

### Yes/No で済む質問は選択肢化

```
✗ 「再申請は可能ですか？」（オープン）
○ 「却下後の再申請を許可しますか？ A: 許可（編集して再提出）, B: 許可（新規作成のみ）, C: 不可」
```

### 業務シナリオで聞く

技術選択肢ではなくシナリオで聞く:
```
✗ 「Slack 通知の channel は public ですか private ですか？」
○ 「承認依頼が届いたとき、誰がそれを見られる必要がありますか？ 承認者だけ / 部門全員 / 全社」
```

### 「分からない」を許容

ユーザーが「今は決められない」と答えた場合:
- Open Questions に残したまま `- [ ] <質問>（deferred: <YYYY-MM-DD> 時点で未決）` に書き換える
- `$plan` 側で **仮置き + Decision Required** として扱う
- 後で再度 `$clarify` を呼べる

## 反映ルール

| 質問の種類 | 反映先 |
|---|---|
| ユーザーの行動・体験 | User Stories |
| 成功条件・観測点 | Success Criteria |
| 連携する外部サービス | External Touchpoints |
| 性能・セキュリティ・運用要件 | Constraints / Non-functional |
| やらないこと | Out of Scope |
| なぜそう決めたか | Decisions |

**禁止**: spec.md に技術用語（Recipe, Datapill, Workflow App 等）を入れない。技術への落とし込みは `$plan` の責務。

## 守るべきルール

- **1 件ずつ消化**: 一括で聞くと回答が浅くなる。1 件ずつファイル更新まで完結させる
- **ファイル更新を都度行う**: 5 件まとめてヒアリング → まとめて反映、は NG。各回答ごとに spec.md を save する（中断対策）
- **Decisions に理由も書く**: `A に決定` だけでなく `A に決定 — B はコストが高く C はユーザー教育が必要なため`

## Git 管理

```bash
git add projects/<project-name>/specs/<NNN>-<slug>$spec.md
git commit -m "clarify(<project>/<slug>): resolve open questions"
git push origin
```
