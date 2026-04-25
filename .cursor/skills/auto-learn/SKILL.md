---
name: auto-learn
description: Workato UI を Claude in Chrome で操作し、コネクタの input/output フィールド詳細を収集して docs/connectors/<provider>.md に追記する。/sync-connectors（一覧）と /learn-recipe（既存レシピから学習）の隙間を埋め、新規レシピを書かずに能動的にフィールドナレッジを蓄積する。
---

# /auto-learn

Workato UI のレシピ編集画面を Claude in Chrome で操作し、対象オペレーションのフィールド詳細（type / hint / required / picklist / 動的フィールド）を収集して `docs/connectors/<provider>.md` に追記するスキル。

`/sync-connectors` がトリガー/アクションの **一覧** を取り、`/learn-recipe` が既存レシピから **学習** するのに対し、`/auto-learn` は「**ドキュメントに無いオペレーションを能動的に学びにいく**」ポジションを担う。

## 使い方

- `/auto-learn <provider>` — 指定コネクタの全オペレーションを学習
- `/auto-learn <provider> <operation>` — 単一のトリガー/アクションのみ学習
- `/auto-learn <provider> --triggers` — トリガーのみ学習
- `/auto-learn <provider> --actions` — アクションのみ学習
- `/auto-learn <provider> --resume` — 前回中断したコネクタの未学習分から再開

## 動作モデル（重要）

**Workato 内部 API を直接叩いてリバースエンジニアリングするやり方は禁止**（`.cursor/rules/`、および [docs/patterns/auto-learn-ui-operations.mdc](../../../docs/patterns/auto-learn-ui-operations.md) の方針参照）。

このスキルは:
- ✅ Claude in Chrome で **Workato UI を実際に操作**して画面遷移する
- ✅ レンダリング後の **DOM を読み取って**フィールド情報を取得する
- ✅ `docs.workato.com` を WebFetch で参照する（補助的な型・hint 情報の補完）
- ❌ `/integrations/meta`、`/connections/<id>/extended_schema.json` 等の内部エンドポイントを fetch / XHR で**直接呼ばない**
- ❌ パラメータ総当たりや CSRF 偽装による探索を**しない**

UI 操作の結果として Workato 自身が発火させたリクエストのレスポンスを **観測専用 interceptor** で受動的に読むのは可。ただしレスポンスから取れる構造化情報を活用するときも、**新規リクエストの構築・送信は禁止**。

## 前提条件

実行前にユーザーは以下を準備:

1. **Chrome 環境**:
   - Chrome で Workato にログイン済み
   - Claude in Chrome 拡張が接続済み

2. **検証用ワークスペース / プロジェクト**:
   - 専用プロジェクト（推奨: `auto-learn-sandbox` など、本番に混ざらない名前）
   - 対象コネクタの認証済みコネクションが存在
   - 動的スキーマ系（Google Sheets、Salesforce、Database 等）を学ぶ場合: 学習用の**シンプルな**サンプルデータ（極小スプレッドシート、1 行のテーブル等）— PII を含まないもの

3. **検証用レシピ**:
   - 各オペレーションを開ける状態のスケルトンレシピ
   - 推奨: ユーザーがあらかじめスケルトン JSON を `workato push` 経由で作成 → スキルは push せず操作のみ
   - 1 レシピに複数オペレーションを並べてもよい（学習対象を Step 番号で指定する）

## 実行手順

### Phase 0: 前提確認

1. `docs/connectors/<provider>.md` を Read。学習対象オペレーションのリストを取得（Triggers / Actions テーブル）
   - `__adhoc_http_action` などの内部用途は除外
   - `## フィールド詳細` 配下に既にエントリがあるオペレーションは、`--force` 指定がない限りスキップ
2. ユーザーに以下を確認（対話）:
   - 検証用ワークスペースの URL（例: `https://app.trial.workato.com/?fid=23794`）
   - 学習に使うレシピ ID と、各オペレーションが何ステップ目にあるか
   - 動的スキーマ確認用のサンプルデータ（必要なら）
3. Claude in Chrome のタブを `tabs_context_mcp` で確保

### Phase 1: コネクタ単位のループ

対象オペレーションごとに Phase 2〜4 を実行。途中失敗時は `--resume` 用に進捗を保存。

### Phase 2: ステップを開く

1. `mcp__Claude_in_Chrome__navigate` で `https://app.<region>.workato.com/recipes/<id>/edit` に遷移
2. `mcp__Claude_in_Chrome__javascript_tool` で対象ステップを click:
   ```javascript
   document.querySelectorAll('w-recipe-step .recipe-step__header')[stepIndex].click();
   ```
3. パネル展開を待機（`recipe-step-config` クラスが `w-panel-content` に出るまで）
4. 現在のタブが `Setup` であることを確認:
   ```javascript
   document.querySelector('button.tabs__label.tabs__label_active')?.textContent.trim() === 'Setup'
   ```
   - 違うときは事前準備不足。ユーザーに「Connection 認証 / コネクタ未選択」をエスカレーション

### Phase 3: 静的フィールドの収集

DOM 操作の詳細セレクタは [docs/patterns/auto-learn-ui-operations.md](../../../docs/patterns/auto-learn-ui-operations.md) 参照。要点:

#### 3-a. Show optional fields モーダル経由でフィールド一覧 + 型を取得

```javascript
// "Show optional fields" ボタンをクリック → モーダル出現
const optBtn = Array.from(document.querySelectorAll('button')).find(b => b.textContent.trim() === 'Show optional fields');
optBtn?.click();
// ※ ボタンが存在しない場合（オプションフィールドが無いコネクタ）は 3-b に直接進む
```

```javascript
// モーダルから全フィールドリスト + 型を抽出
const items = Array.from(document.querySelectorAll('label.multi-select-list__item')).map(label => ({
  label: label.querySelector('.multi-select-list__item-title')?.textContent.trim(),
  type: (label.querySelector('.multi-select-list__item-icon')?.getAttribute('data-icon-id') || '').replace(/^field-type\//,''),
  visibleByDefault: label.querySelector('input[type="checkbox"]')?.checked,
}));
```

```javascript
// Select all → Apply changes でフォームに全フィールドを表示
document.querySelector('label.multi-select-list__checkbox')?.click();
Array.from(document.querySelectorAll('button')).find(b => b.textContent.trim() === 'Apply changes')?.click();
```

#### 3-b. フォーム DOM から hint / required / control component を取得

```javascript
// トップレベル w-form-field のみ列挙（toggle picker のあるフィールドは内側 w-form-field を持つので除外）
const topLevel = Array.from(document.querySelectorAll('w-recipe-step-details w-form-field'))
  .filter(f => !f.parentElement?.closest('w-form-field'));

const formFields = topLevel.map(f => {
  const labelText = (f.querySelector('.form-field-label, w-form-field-simple-label')?.textContent||'').trim().replace(/\s+/g,' ');
  const hint = (f.querySelector('.form-field-hint__content')?.textContent||'').trim();
  const innerInput = f.querySelector('w-form-field w-form-field .form-field-input-wrapper > *')
                   || f.querySelector('.form-field-input-wrapper > *');
  return {
    label: labelText.replace(/\s*\*$/,''),
    required: /\*$/.test(labelText),
    hint,
    controlComponent: innerInput?.tagName.toLowerCase() || null,
    hasToggleField: !!f.querySelector('w-toggle-field'),
  };
});
```

#### 3-c. 出力スキーマを Recipe data パネルから取得

```javascript
// 1) Recipe data パネルが minimize なら展開
const datatree = document.querySelector('w-datatree');
if (datatree?.classList.contains('recipe-editor-datatree_minimize')) {
  document.querySelector('.data-tree-resize-controls__icon, .data-tree-resize-controls w-svg-icon')?.click();
}

// 2) 当該ステップの output グループを探して開く
//    Trigger ステップの場合: "Current step output / <Title>(Step 1 output)"
//    Action ステップの場合: 当該ステップの output は「ステップ 1 つ後ろのステップを開いて」初めて見える
//    ※ Action の output 学習には、対象ステップの**直下に学習用の使い捨てステップを追加**する手順を推奨
const stepGroup = Array.from(document.querySelectorAll('.data-tree-group'))
  .find(g => /Step \d+ output|Current step output/.test(g.textContent));
stepGroup?.querySelector('.data-tree-group__header')?.click();

// 3) 全アイテム抽出
const outputItems = Array.from(stepGroup?.querySelectorAll('.data-tree-item') || []).map(it => ({
  label: (it.querySelector('w-data-tree-pill, .data-tree-item__pill')?.textContent||'').trim(),
  type: (it.querySelector('.data-tree-item__icon w-svg-icon, .data-tree-item__icon [data-icon-id]')?.getAttribute('data-icon-id')||'').replace(/^field-type\//,''),
}));
```

3-a / 3-b の結果を `label` でマージ → 静的入力フィールドの確定リストを得る。

### Phase 4: 動的フィールドの検出（任意）

対象オペレーションが picklist 依存型（例: Google Sheets `search_spreadsheet_rows_v4_new`、Salesforce オブジェクト系）の場合のみ。

1. Phase 3 のスナップショットを `before` として保持
2. ユーザーが事前に用意したサンプル picklist 値（例: 学習用スプレッドシート + シート名）を UI から選択:
   ```javascript
   // 例: スプレッドシート選択
   // 1. picklist を開く（input click or arrow click）
   // 2. text-filter があれば値を入力
   // 3. dropdown オプションをクリック
   ```
3. ローディング完了を待機（DOM 安定 = 一定時間 mutation なし）
4. Phase 3 を再実行 → `after` を取得
5. `before` / `after` を label で diff:
   - 新出のトップレベルフィールド = 動的入力フィールド（親）
   - 既存フィールドの内側に増えた `w-form-field` = 動的子フィールド（列・属性）
   - Recipe data パネルの新出 `.data-tree-item` = 動的出力フィールド
6. **インスタンス固有値は破棄**:
   - 列名 `open_time`, `open_price` のような実データは記録しない
   - 「決定条件（どの picklist 選択で動的列が増えるか）」と「生成パターン（"シートのヘッダーごとに 1 フィールド"）」のみ記録

### Phase 5: docs/connectors/<provider>.md に追記

既存の `## フィールド詳細` セクションに対象オペレーションのエントリを追加 / 更新。フォーマットは [/learn-recipe](../learn-recipe/SKILL.md) と同じ:

```markdown
### <operation_name> (Trigger | Action)

学習元: /auto-learn (UI 観察) — <YYYY-MM-DD>

#### Input fields
| フィールド | 型 | 必須 | 説明 |
|---|---|---|---|
| <label> | <type> | Yes/- | <hint の要約> |

#### Output fields
| フィールド | 型 | 説明 |
|---|---|---|
| <label> | <type> | <description if any> |
| <parent>[].<child> | <type> | <description if any> |

#### 動的フィールド（あれば）
- **決定条件**: <どの picklist 選択で生成されるか>
- **生成パターン**: <例: シートのヘッダー列ごとに 1 つの string 入力フィールドが Columns 配下に生成。出力では Rows 配列の要素として同じ列名フィールドが追加>
```

**重複チェック**: 追記前に既存セクションを Grep し、同名 operation のエントリがあれば diff して新情報のみマージ。値（PII）が docs に混入しないか念のため確認。

### Phase 6: 後始末

- 対象レシピを **保存しない**（学習は読み取り専用、Save は不要）
- ユーザーが事前に作ったレシピ・コネクションは破棄しない
- スキルが追加した一時ステップ（output 学習用の使い捨てステップ等）はユーザーの判断で削除

## 出力

実行後、以下を報告:

- 学習したコネクタ / オペレーション一覧
- `docs/connectors/<provider>.md` に追記したセクションのサマリ
- 動的フィールドが検出されたオペレーション
- スキップしたオペレーション（既存・認証なし・picker 未対応 等）と理由
- 失敗したオペレーション（DOM 構造不一致・タイムアウト等） — 残課題として `docs/learned-patterns.md` または GitHub Issue に記録するよう提案

## エラー処理

- **ステップが Setup にならない**: コネクション未選択 / 認証切れ。ユーザーに UI で対応してもらう
- **`Show optional fields` ボタン無し**: そのオペレーションは optional フィールドなし。Phase 3-a を飛ばし 3-b から
- **DOM が見つからない（クラス名変更）**: Workato UI の更新疑い。スキップして失敗ログを残す。`docs/patterns/auto-learn-ui-operations.md` の「残課題」に注記提案
- **picklist の値が無い**: そのコネクションは権限不足 or データ未準備。ユーザーにエスカレーション

## Git 管理

書き込み先は外側 `workato-dev-kit` リポジトリ:

```bash
git add docs/connectors/<provider>.md
git commit -m "auto-learn: <provider> <operation>(s) のフィールド情報を追加"
```

詳細は `.cursor/rules/workato-multi-repo-git.mdc` 参照。

## 関連スキル / ドキュメント

- [/sync-connectors](../sync-connectors/SKILL.md) — トリガー/アクション一覧の収集（このスキルの上流）
- [/learn-recipe](../learn-recipe/SKILL.md) — 既存レシピからのフィールド学習（このスキルと相補）
- [docs/patterns/auto-learn-ui-operations.md](../../../docs/patterns/auto-learn-ui-operations.md) — UI 操作の DOM セレクタ・操作スニペット完全リファレンス
- [Issue #27](https://github.com/rkawaishi/workato-dev-kit/issues/27) — 設計動機

## 制限事項（既知）

- 動的フィールド検出は **picklist 1 段** までしかカバーしない（spreadsheet → sheet）。多段（spreadsheet → sheet → ヘッダ行範囲）は要追加検討
- 仮想スクロール（`cdk-virtual-scroll-viewport`）配下のフィールドは画面外で取りこぼす可能性。多くの列を持つコネクタでは要スクロール
- 複数トリガー持ちコネクタの Trigger ピッカー / 動的 Trigger イベント変更は未検証（残課題）
- カスタムコネクタ向けは `connector.rb` パースで多くがカバーされるため、本スキルは Pre-built コネクタの補完を主用途とする
