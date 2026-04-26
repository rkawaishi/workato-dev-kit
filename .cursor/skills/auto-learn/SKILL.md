---
name: auto-learn
description: Workato UI を Claude in Chrome で操作し、1 コネクタ単位で全オペレーションのフィールド情報を自律的に収集して docs/connectors/<provider>.md に追記する。完全性より自律性を優先し、不確実なものは記録してスキップする（途中でユーザーに質問しない）。
---

# /auto-learn

Workato UI を Claude in Chrome で操作し、対象コネクタの全オペレーション（trigger / action）の input / output フィールドを能動収集して `docs/connectors/<provider>.md` に追記するスキル。

## 設計原則（重要）

このスキルは「**自律性優先・網羅性重視**」で設計する。完全な型・nest 構造の正確性より、**多くのコネクタにある程度のフィールド情報を行き渡らせる**ことを目的とする。細かな修正はマニュアルレシピや `/learn-recipe` で後追いする。

1. **対話禁止**: 1 回の呼び出しで対象コネクタの全 op を試す。途中でユーザーに質問しない。判断材料が無い場合は **defaults → skip + log**。
2. **フェイルソフト**: 各 op を try / catch で囲み、失敗しても次に進む。1 op の失敗で run 全体を止めない。
3. **記録駆動**: 取れたものは追記、取れなかったものは「学習失敗 / 部分学習」で残す。最後にレポートを出す。
4. **UI のみ**: 内部 API への新規 fetch / XHR は禁止（リバースエンジニアリング厳禁）。UI 操作で発生したレスポンスの**受動観察**のみ可。詳細は `docs/patterns/auto-learn-ui-operations.md` 参照。

## 使い方

```
/auto-learn <provider>
```

オプション:
- `--recipe-id <id>` — 検証用レシピ ID（既定: 規約レシピ名から推定 / 直前タブの URL から）
- `--workspace-url <url>` — ワークスペース base URL（既定: 直前タブから）
- `--force` — 既に docs にフィールド詳細があっても上書き学習
- `--triggers-only` / `--actions-only` — 範囲を絞る
- `--sandbox <json>` — 動的スキーマ用テストデータ（後述）

事前準備が無い場合（規約レシピ未作成・コネクション未認証など）は、**ユーザーに質問せず失敗ログだけ残して終了**する。

## 事前準備（ユーザーが 1 回だけ）

検証用ワークスペースに以下を用意:

### 1. 規約レシピ（コネクタごと、または共有 1 本）

推奨: プロジェクト名 `auto-learn-sandbox`、レシピ名 `<provider>` または共有 `auto-learn-scratch`。**4 ステップ構成で固定**:

| Step | 役割 | 既定で置く中身 |
|---|---|---|
| 1 | **Trigger 学習スロット** | 任意（スキルが上書きする） |
| 2 | 中継ステップ | 任意のシンプルなアクション（例: Google Sheets `Search rows`、列の少ない sandbox sheet 指定）。学習対象の前ステップとして固定し、出力 datapill を提供する |
| 3 | **Action 学習スロット** | 任意（スキルが順次上書きする） |
| 4 | **Action output 観察スロット** | 任意のシンプルなアクション（例: Workbot for Slack `Get user info`）。Step 3 output を Recipe data から覗くための踏み台 |

引数 `--recipe-id` 未指定時、スキルは:
- 直前タブの URL に `/recipes/<id>/edit` があれば、その ID を使う
- なければ **失敗ログだけ残して終了**

### 2. 認証済みコネクション（対象コネクタ）

複数あっても可。スキルは規約に従って 1 つ選ぶ:

1. 引数 `--connection <name>` 指定があればそれを使う
2. なければ「**最初の active コネクション**」（`w-connection-card` の DOM 順）を選ぶ
3. それも無ければ skip + log

### 3. 動的スキーマ用サンドボックスデータ（必要なコネクタのみ）

`extends_*_schema=true` 系のオペレーション（Google Sheets `search_rows`、Salesforce 各種等）を学習する場合のみ必要。

- 引数 `--sandbox '{"spreadsheet":"auto-learn-sample","sheet":"Memo"}'` で渡す
- なければ `scripts/sandbox-data/<provider>.json` を読む（任意のリポジトリ規約）
- どちらもなければ動的 probe を **静かにスキップ**して静的フィールドだけ記録

サンドボックスデータは **シンプル**であること（ヘッダー重複なし、3 列程度）。複雑なデータでは `"duplicated headers"` 等のエラーで動的 input が消える挙動が起きる。

## 実行フロー

### Phase 1: ブートストラップ

1. `docs/connectors/<provider>.md` を Read
2. Triggers / Actions テーブルから op 名・kind を列挙
3. 除外: `__adhoc_http_action`、deprecated（`[deprecated]` 等の注記がある行）
4. `--force` がない限り、既に `### <op>` で始まるセクションがあるものはスキップ。検出は **op 名のみで照合**（行頭の `### ` 直後のトークン）。括弧内の補足（display title など）は無視する。例: `### delete_message (Delete message)` も `### delete_message (Action)` も同じ op としてスキップ対象になる
5. 残った op リストを処理キューに

### Phase 2: タブ準備

1. `tabs_context_mcp` で既存タブを確認、なければ新規作成
2. `--recipe-id` または直前 URL から `/recipes/<id>/edit` に navigate
3. レシピが 4 ステップ構成（trigger + 3 action）になっているか DOM で確認。なければ失敗ログを残して終了

### Phase 3: 各 op を `processOperation` で順次処理

```
for op in queue:
    result = processOperation(op)        # try/catch で囲む
    results.append(result)
    if result.errors:
        log warning，continue（停止しない）
```

`processOperation` の中身:

```
1. switchStepToOp(op)
   - kind=trigger → Step 1 を上書き（App タブ → コネクタ → Trigger picker → 当該 op）
   - kind=action  → Step 3 を上書き（App タブ → コネクタ → Action picker → 当該 op）
   - 失敗（picker に op が見えない、auto-skip 異常 等）→ result.status='failed_to_open' を返して**早期終了**（後続の step 2-6 はスキップ）

2. waitForSetupTab()
   - 完了判定: button.tabs__label.tabs__label_active のテキスト === 'Setup'
   - timeout 8 秒。タイムアウトしたら result.status='failed_to_open' で**早期終了**

3. result.input = captureInputFields()
   - "Show optional fields" ボタンがあれば開いてモーダルから {label, type, visibleByDefault} 取得 → Cancel
   - フォームの top-level w-form-field を列挙 → {label, required, hint, controlComponent, hasToggleField}
   - 両者を label でマージ
   - ボタンが無ければモーダル抽出を skip（form のみ）

4. result.output = captureOutputFields(op.kind)
   - 当該 step の output グループ名を組み立て:
     - kind=trigger:  "Step 1 output"   → Step 2 を開いて Recipe data から覗く
     - kind=action:   "Step 3 output"   → Step 4 を開いて Recipe data から覗く
   - データツリー minimize なら展開、対象グループの内側 .data-tree-group__header を click
   - グループが現れなければ "no_output_schema"（fire-and-forget アクション）として null
   - 現れれば .data-tree-item を全列挙 → {label, type}

5. もし result.input に dynamic picklist 候補（w-toggle-field を持つ select 等）があり、
   かつ --sandbox が用意されていれば:
     try {
       applySandboxValues()
       result.dynamic = { input: captureInputFields(), output: captureOutputFields() }
     } catch (e) {
       result.errors.push("dynamic_probe_failed: " + e.message)
     }

6. ステータス確定:
   - ここまで result.status が未設定（=step 1〜2 で早期終了していない）なら、result.status = 'ok' を設定
   - errors 配列の有無は status に影響させない（部分学習は status='ok' + errors=[...] で表す）
   - ⚠ step 1 / 2 で 'failed_to_open' を設定して早期 return したケースは、ここに到達しないため status は上書きされない
```

### Phase 4: docs に追記

`docs/connectors/<provider>.md` の `## アクション詳細` / `## トリガー詳細` セクションに、各 op の結果を追記:

```markdown
### <op_name> (<Display Title>)

種別: Trigger | Action
学習元: /auto-learn (UI 観察) — <YYYY-MM-DD>[, output <YYYY-MM-DD>]

#### Input fields
| フィールド | 型 | 必須 | デフォルト表示 | 説明 |
|---|---|---|---|---|
| ... |

#### Output fields
| フィールド | 型 | 説明 |
|---|---|---|
| ... |

#### 動的フィールド（あれば）
- 決定条件: <picklist 名>
- 観測例: ... （PII を残さない範囲で）
```

ステータスは以下の 4 値のいずれか:

| status | 意味 |
|---|---|
| `ok` | processOperation が最後まで通った（`errors` が non-empty なら部分学習）|
| `failed_to_open` | step 1 / 2 で対象 op を開けず早期 return した |
| `error` | step 3〜5 のいずれかで例外発生（`errors` に詳細）|
| `unexpected_error` | processOperation そのものが投げた例外を上位 catch で受けた（後述） |

追記ルーティング（`'ok'` 以外はすべて学習失敗ログ扱い）:

- `status === 'ok'` & errors=[] → セクション本体に完全に追記
- `status === 'ok'` & errors!=[] → 注記行（`> ⚠ 部分学習: <errors>`）を加えてセクション本体に追記
- `status !== 'ok'`（=`failed_to_open` / `error` / `unexpected_error` / その他将来追加される非 ok ステータス全般）→ セクション本体は作らず、ファイル末尾「## 学習失敗ログ」セクションに 1 行追記（`- <op>: status=<status>, reason=<reason> — <date>`）

### Phase 5: レポート出力

標準出力に短く:

```
/auto-learn <provider> 完了
- 試行: N op
- 完全成功: M op
- 部分学習: K op  (主因: <theme>)
- 学習失敗: L op  (理由: <reason>)
- マニュアルでフィードバックすべき項目:
  - 重複ラベル: ...
  - ネスト深さ未確定: ...
  - その他観察された irregularity: ...
```

最後に追記したセクション一覧と git diff 概要を提示し、コミット可否はユーザー判断に任せる（**コミットは自動実行しない**）。

## 「止まらない」ための具体ルール

| 場面 | 対応 |
|---|---|
| `Show optional fields` ボタンが無い | モーダル抽出を skip、form 直接読みのみ |
| Trigger 1 個コネクタで Trigger picker auto-skip | `tabs__label_active` を監視。Connection に飛んでいれば Trigger 段階を skip して既定トリガーを採用 |
| Step output グループが Recipe data に無い | `output: null`（fire-and-forget アクション）として記録、続行 |
| Picker のタイトル誤表示（同名 op が複数） | canvas step text や badge 構成で区別。それでも区別不能なら DOM 順位 + 失敗時の input 内容で逆推測。最後の手段は skip + log |
| 動的 picklist で API エラー（duplicated headers 等） | 1 回だけリトライ（別の sandbox 値があれば）。再失敗で諦め、静的部分のみ記録 |
| Picker の仮想スクロール | 各 op 検索時、見つからなければスクロール → 再列挙を最大 3 回 |
| DOM 安定待ち | `wait` ではなく**特定セレクタの mutation 監視**を優先（spinner 消失、tabs_label_active 変化、modal の DOM 出現/消失） |
| クリックが効かない | 1 段親要素クリック → `dispatchEvent(MouseEvent)` → 物理座標クリック の順でリトライ |
| `unsaved changes` で navigate がブロック | 単に skip して在りもの recipe で続行（reload を試行しない） |
| コネクション複数 | 引数 → DOM 最初 → skip の順。動的に新規認証は試みない |

## 完了判定セレクタ集

- Setup タブ到達: `button.tabs__label.tabs__label_active` のテキスト === `Setup`
- パネル切替完了: `w-recipe-step-details w-panel-content` のクラスが `recipe-step-config` または `recipe-step-details-adapter` に変化
- Show optional fields モーダル出現: `w-dialog label.multi-select-list__item` 1 個以上
- Show optional fields モーダル消失: `w-dialog` が DOM から消失
- Recipe data tree 展開: `w-datatree:not(.recipe-editor-datatree_minimize)`
- Step output グループ開いた状態: `.data-tree-group_opened`

## docs 更新ルール

- 既存セクションがある場合（`--force` で再学習時）:
  - 学習元行を最新に更新
  - フィールド表は **ユニオンで追記**（同名は新情報で置換）
  - 重複ラベルは **末尾に注記**を残す（例: `> ⚠ 同一 label "User" が 2 箇所に出現。内部パスは要マニュアル確認`）
- 新規セクションは [/learn-recipe](../learn-recipe/SKILL.md) と同じフォーマット

## 残課題（マニュアルフィードバック前提）

このスキルはあくまで「広く浅く」を目指す。次のものは UI 観察だけでは取りきれず、マニュアルで埋めることを前提とする:

- 重複ラベル（Slack `User` 等、同名フィールドの内部パス区別）
- データツリーのネスト深さ（`paddingLeft: 0px` 問題）
- 動的 picklist の連鎖（spreadsheet → sheet → 列）の自動探索
- 内部 `name`（JSON キー）と表示 label のマッピング（UI には label しか出ない）
- フィールドの `parse_output` / 細かい制約（最大文字数等）

これらに気づくたびに `/learn-recipe` で個別レシピから埋めるか、ユーザーが直接 `docs/connectors/<provider>.md` を編集する。

## エラーハンドリングの設計指針

すべての例外は **1 op 単位の失敗** に閉じ込める:

```javascript
for (const op of queue) {
  try {
    const result = await processOperation(op);
    results.push(result);
  } catch (e) {
    // processOperation 内 try/catch を通り抜けた想定外例外も次の op に進める
    // status='unexpected_error' は Phase 4 ルーティング表で 'ok 以外' = 学習失敗ログ扱い
    results.push({ name: op.name, kind: op.kind, status: 'unexpected_error', errors: [e.message] });
    continue;
  }
}
```

タブが死んだ・ネットワークが切れた・ログアウトされた等、recoverable でない事態だけは早期 abort してレポートを返す。判定基準: 連続 3 op 以上失敗 → abort。

## Git 管理

書き込み先は外側 `workato-dev-kit/docs/connectors/<provider>.md` のみ。スキル自身はコミットしない（最後にユーザー判断）:

```bash
git add docs/connectors/<provider>.md
git commit -m "auto-learn: <provider> N op (M ok / K failed)"
```

詳細は `.cursor/rules/workato-multi-repo-git.mdc` 参照。

## 関連スキル / ドキュメント

- [/sync-connectors](../sync-connectors/SKILL.md) — Triggers/Actions 一覧の収集（このスキルの上流）
- [/learn-recipe](../learn-recipe/SKILL.md) — 既存レシピからのフィールド学習（マニュアルフィードバック手段）
- [docs/patterns/auto-learn-ui-operations.md](../../../docs/patterns/auto-learn-ui-operations.md) — UI 操作の DOM セレクタ完全リファレンス
- [Issue #27](https://github.com/rkawaishi/workato-dev-kit/issues/27) — 設計動機
