# 自動ナレッジ収集: Workato UI 操作リファレンス

[Issue #27](https://github.com/rkawaishi/workato-dev-kit/issues/27) のレベル 2 でコネクタの input/output フィールド情報を収集するためのリファレンス。

**Workato の内部（非公開）API を直接叩く方式は採用しない**。情報源は (a) 公式ドキュメント `docs.workato.com` と (b) Workato UI の DOM 観察 の 2 つに限定する。

## 結論サマリ

| 情報源 | 用途 | 詳細 |
|---|---|---|
| **公式ドキュメント**: `docs.workato.com` | 静的スキーマの主データソース | 既存の `/sync-connectors` で API 経由活用済 |
| **UI DOM 観察**（本ドキュメントの主題） | 動的フィールド + 公式ドキュメントに無い情報 | Claude in Chrome でレシピ編集画面を操作 |

**UI から取れる情報**:
- 入力フィールド一覧（hidden 含む）と各フィールドの型 — `Show optional fields` モーダル
- フィールドのヒント文・必須・コントロール種別 — Setup フォーム
- Toggle picker（preset/custom 切替）の有無 — Setup フォーム
- 出力スキーマと各フィールドの型 — Recipe data パネル
- 動的フィールド（テーブル列等）— picklist 選択前後の DOM 差分

これにより `extended_input_schema` / `extended_output_schema` / `dynamicPickListSelection` / `toggleCfg` / `visible_config_fields` 相当のデータが、UI セッション 1 回で収集できる。

> **内部 API の扱い（重要な線引き）**:
> - ❌ **NG**: 内部 API（`/integrations/meta`、`/connections/<id>/extended_schema.json` 等）を**こちらで構築したリクエストで直接叩く**こと、およびリクエスト/レスポンスを総当たりで観察してリバースエンジニアリングすること。
> - ✅ **OK**: ユーザー（または自動化スクリプト）が **通常の UI 操作**を行った結果として Workato 自身が発火させたリクエストの**レスポンスを受動的に読む**こと。
>
> 本ナレッジ収集スキルは UI 操作を主軸にし、補助的にレスポンスを読み取って構造化データを得る設計にする。スキルから直接 fetch / XHR で内部エンドポイントを呼ぶことは行わない。

## Workato UI の DOM 規約

### Angular カスタム要素
画面の骨格は `w-` 接頭辞の Angular カスタム要素で構成される。クラス名はビルドごとに `ng-tns-c<hash>` のような可変サフィックスを持つので、**タグ名・属性・固定クラス（`recipe-step__header` 等）でセレクタを書く**。

### 命名規約
- 「コネクタ」は内部表記で **adapter**（`w-adapter-picker`、`adapter-picker__item`）
- 「ステップ詳細」は **recipe-step-details** で統一
- 「データツリー（datapill ソース）」は **data-tree** / **datatree**

### 型を表す共通アイコン規約 ⭐
Workato は型を `data-icon-id` 属性で表現する。これは入力フィールドモーダルでも出力データツリーでも共通:

```html
<w-svg-icon data-icon-id="field-type/text" ...>
```

| `data-icon-id` 値 | 意味 |
|---|---|
| `field-type/text` | 文字列 |
| `field-type/integer` | 整数 |
| `field-type/number` | 小数（推定 — 要他コネクタ検証） |
| `field-type/date-time` | datetime |
| `field-type/date` | 日付（推定） |
| `field-type/boolean` | boolean（推定） |
| `field-type/text-array` | 文字列配列 |
| `field-type/array` | オブジェクト配列 |
| `field-type/object` | オブジェクト（推定） |

未確認の型は他コネクタ調査で追記する。

## 画面別操作リファレンス

### 画面 1: Assets ビュー（プロジェクトのアセット一覧）

**URL**: `https://app.<region>.workato.com/?fid=<workspace_id>#assets`

| 役割 | セレクタ |
|---|---|
| プロジェクト切替 | 左サイドバーのプロジェクト名 |
| 新規アセット作成 | 右上 `Create` ボタン |
| アセット一覧 | レシピカード `<a>` リンクで `/recipes/<id>` に遷移 |

`/auto-learn` では基本的に Assets ビューを経由せず、レシピ ID を生成 → 直接 `/recipes/<id>/edit` に遷移する。

### 画面 2: レシピ編集画面（空のキャンバス）

**URL**: `https://app.<region>.workato.com/recipes/<recipe_id>/edit`

```
w-recipe-editor
├ w-recipe-editor-header                       ← ツールバー
│   ├ w-editable-text                          ← レシピ名
│   ├ w-header-mode-switch                     ← RECIPE / TEST JOBS タブ
│   └ w-header-toolbar-buttons                 ← Save / Test recipe / Refresh / Exit
└ w-recipe-viewer
    └ w-recipe-steps-canvas                     ← キャンバス全体
        └ w-recipe-viewer-steps
            └ w-recipe-steps
                └ w-recipe-step × N             ← 各ステップ
```

**主要な操作対象**:

| 役割 | セレクタ |
|---|---|
| ステップを開閉する本体 | `w-recipe-step .recipe-step__header` |
| 番号バブル（ステップ選択） | `.recipe-step__number-button` |
| ステップ間の `+` | `button.recipe-step-marker__button_add[aria-label="Add step"]` |
| 最初のアクション追加 `+` | `w-recipe-add-step button[aria-label="Add step"]` |
| Save | `<button>` text=`Save` |
| Exit | `<button>` text=`Exit` |
| RECIPE/TEST JOBS 切替 | `w-header-mode-switch` 内の `<button>` |

**初期状態の特徴**:
- Trigger ステップが 1 つだけ存在（プレースホルダ "Select an app and trigger event"）
- ACTIONS セクションは空で `w-recipe-add-step` の "+" だけ

### 画面 3: App ピッカーパネル（Trigger/Action クリック後）

**遷移**: `.recipe-step__header` をクリック → 右側に `w-recipe-step-details` パネルがスライドイン。

**パネル構造**:
```
w-recipe-step-details
└ w-recipe-step-details-adapter                 ← App ピッカーモード
    └ w-panel.recipe-step-details
        ├ w-panel-header (.panel-header)
        │   ├ .panel-header__wrapper            ← "Choose an app"
        │   └ button.panel-header__close[aria-label="Close side panel"]
        └ w-panel-content.recipe-step-details-adapter
            ├ .tabs__labels                      ← App / Trigger / Connection / Setup
            │   └ button.tabs__label             (.tabs__label_active で現在地)
            └ w-adapter-picker
                ├ input.search-field__input[placeholder="Search for an app"]
                └ w-adapter-picker-option × N
                    └ w-select-grid-option
                        └ button.select-grid-option   ← 内部 textContent = コネクタ名
```

**主要な操作**:

```javascript
// コネクタ選択（例: "Gmail"）
Array.from(document.querySelectorAll('w-adapter-picker-option button.select-grid-option'))
  .find(b => b.textContent.trim() === 'Gmail')
  ?.click();

// アプリ名で検索
const input = document.querySelector('input.search-field__input');
input.value = 'gmail';
input.dispatchEvent(new Event('input', { bubbles: true }));
```

### 画面 4: Connection ピッカー

**遷移**: コネクタを選ぶと自動で `Connection` 段階に進む（タブが切替）。

⚠ **重要な分岐ルール**: 選択可能なトリガーが **1 個** のコネクタは Trigger 段階を**自動スキップ**して既定トリガーを採用 → そのまま Connection に進む。複数トリガー持ちは Trigger ピッカー（後述）が出る。アクションは原則複数あるので Trigger と異なり毎回ピッカーが表示される（推定 — 要検証）。

**遷移先の判定**:
```javascript
// 現在のタブを確認
document.querySelector('button.tabs__label.tabs__label_active')?.textContent.trim();
// → "Connection" ならスキップ済み / "Trigger" ならピッカーが必要

// または panel-content のクラスで判定
document.querySelector('w-recipe-step-details w-panel-content')?.className;
// → "recipe-step-details-connection" / "recipe-step-details-trigger" / "recipe-step-config" 等
```

**Connection ピッカーの DOM**:
```
w-panel-content.recipe-step-details-connection
└ w-connection-list-picker
    ├ w-search-field                              ← "Search active connections"
    ├ w-paging-items-count                        ← "Showing N active connection(s)"
    ├ button "Refresh list"
    ├ .connection-list-picker__list
    │   └ w-connection-card × N
    │       ├ w-connection-title                   ← 例: "Sample1 | Gmail"
    │       └ w-folder-path                        ← 配置プロジェクト
    ├ w-paginator
    └ button.connection-list-picker__new-connection-button "New connection"
```

**操作**:
```javascript
// 既存コネクションを選ぶ
Array.from(document.querySelectorAll('w-connection-card'))
  .find(c => c.textContent.trim().startsWith('Sample1 | Gmail'))
  ?.click();
```

タブの enable/disable:
- Setup タブはコネクションを選ぶまで `disabled`
- Trigger タブは戻れるが、Trigger スキップ動作の場合は省略可

### 画面 5: Setup（フィールド入力）画面 — 本命

**遷移**: コネクションを選ぶと自動で Setup タブに進む。

**パネル構造**:
```
w-recipe-step-details
└ w-recipe-step-details (config モード)
    └ w-panel.recipe-step-details
        ├ w-panel-header                          ← 例: "New email in Gmail"
        └ w-panel-content.recipe-step-config
            ├ w-recipe-step-config-search          ← "Find" 検索
            ├ w-optional-fields-button             ← "Show optional fields"
            ├ button "Reset"
            ├ w-recipe-step-help / w-tips          ← HELP バナー
            └ w-recipe-operation-step-config
                └ w-endless-scroll
                    └ w-in-view-item × N
                        └ w-form-field × N         ← 1 フィールド
```

**1 フィールドの内訳**:
```
w-form-field
└ .form-field
    └ .form-field__body
        ├ w-form-field-simple-label
        │   └ .form-field-label.form-field-simple-label   ← ラベル文字列（必須は末尾 "*"）
        └ .form-field-controls
            ├ w-formula-switcher                          ← Text/Formula 切替（あるとき）
            ├ w-form-field-ai-button                      ← AI 補助
            ├ .form-field-input-wrapper
            │   └ <入力タイプ別 w-* 要素>
            └ .form-field-hint
                └ .form-field-hint__content                ← 説明文
```

**入力タイプ別の `w-*` 要素**:

| タグ | 意味 |
|---|---|
| `w-text-field` | プレーンテキスト / 数値 / datetime |
| `w-text-field-type` | Text/Formula 種別の picklist |
| `w-text-field-preview` | プレビュー表示 |
| `w-select` / `w-select-field` | enum / picklist |
| `w-boolean-select-field` | Yes/No picklist |
| `w-toggle-field` | "Select from list / Custom value" 切替（**dynamic picklist の入り口**） |
| `w-date-time-field` | datetime ピッカー（推定） |
| `w-textarea-field` | 複数行テキスト（推定） |

**🔑 `w-form-field` は入れ子構造**:
toggle picker のあるフィールドは外側 `w-form-field`（picker 用）と内側 `w-form-field`（実値用）の 2 階層。フィールド一覧を取るときは**トップレベルのみ**にフィルタ:
```javascript
const topLevel = Array.from(document.querySelectorAll('w-recipe-step-details w-form-field'))
  .filter(f => !f.parentElement?.closest('w-form-field'));
```

**ヘッダーボタン**:
| 役割 | セレクタ |
|---|---|
| Find（フィールド検索） | `<button>` text=`Find` |
| Show optional fields | `<button>` text=`Show optional fields` |
| Reset | `<button>` text=`Reset` |
| パネルを閉じる | `button.panel-header__close` |

### 画面 5b: Show optional fields モーダル ⭐

**遷移**: Setup ヘッダーの `Show optional fields` ボタン → `w-dialog` がモーダルで開く。

```
w-dialog
├ ヘッダー: "Show optional fields" + ✕
├ w-text-filter                                    ← 検索ボックス
├ w-select-filter "All optional fields"            ← カテゴリ絞り込み
├ "M of N results selected" カウンタ
└ multi-select-list
    ├ label.multi-select-list__checkbox            ← "Select all"（indeterminate あり）
    └ cdk-virtual-scroll-viewport                  ← 仮想スクロール
        └ cdk-virtual-scroll-content-wrapper
            └ label.multi-select-list__item × N
                ├ input[type=checkbox]              ← visible-by-default 状態
                ├ w-svg-icon.multi-select-list__item-icon
                │   data-icon-id="field-type/<TYPE>"   ⭐ 型情報
                └ span.multi-select-list__item-content
                    └ span.multi-select-list__item-title  ← フィールド名
└ Cancel / Apply changes
```

**全フィールドリスト + 型の抽出**:
```javascript
const items = Array.from(document.querySelectorAll('label.multi-select-list__item')).map(label => ({
  label: label.querySelector('.multi-select-list__item-title')?.textContent.trim(),
  type: (label.querySelector('.multi-select-list__item-icon')?.getAttribute('data-icon-id') || '').replace(/^field-type\//,''),
  visibleByDefault: label.querySelector('input[type="checkbox"]')?.checked,
}));
```

**全フィールド展開 → Apply**:
```javascript
document.querySelector('label.multi-select-list__checkbox')?.click();        // Select all
Array.from(document.querySelectorAll('button')).find(b => b.textContent.trim() === 'Apply changes')?.click();
```

### 画面 5c: Recipe data パネル — 出力スキーマ ⭐

**位置**: Setup 画面の左下に常駐するフローティングパネル（最初は minimize 状態）。

```
w-recipe-step-details
└ w-recipe-editor-datatree
    └ w-datatree.recipe-editor-datatree(.recipe-editor-datatree_default | _minimize)
        └ .data-tree.trigger-line.data-tree_static
            ├ .data-tree__heading
            │   ├ h4.data-tree__title             ← "Recipe data"
            │   └ .data-tree-resize-controls > w-svg-icon  ← 展開/最小化トグル
            ├ .data-tree__description              ← "To use data from a previous step..."
            └ .data-tree__scroll
                └ .data-tree__groups
                    ├ .data-tree-group(.data-tree-group_opened)
                    │   ← "Properties"（ワークスペース/レシピメタ情報のデータピル群）
                    │   └ items...
                    └ .data-tree-group(.data-tree-group_current)
                        ← "Current step output / New email (Step 1 output)"
                        ├ .data-tree-group__heading
                        ├ .data-tree-group__header              ⚠ 内側をクリックで展開
                        └ items...
```

**1 データピルの内訳**:
```
.data-tree-item
├ .data-tree-item__toggle (.data-tree-item__toggle_open)         ← caret（ネスト展開）
├ .data-tree-item__icon
│   └ w-svg-icon[data-icon-id="field-type/<TYPE>"]                ⭐ 型情報
├ w-data-tree-pill.data-tree-item__pill                           ← フィールド名（label）
└ .data-tree-item__sample                                         ← サンプル値（PII 注意）
```

**展開とスキーマ抽出**:
```javascript
// 1. パネルを最大化
const datatree = document.querySelector('w-datatree');
if (datatree?.classList.contains('recipe-editor-datatree_minimize')) {
  document.querySelector('.data-tree-resize-controls__icon, .data-tree-resize-controls w-svg-icon')?.click();
}

// 2. Current step output グループを展開（内側 __header が click target）
const stepGroup = Array.from(document.querySelectorAll('.data-tree-group'))
  .find(g => /Step \d+ output|Current step output/.test(g.textContent));
stepGroup?.querySelector('.data-tree-group__header')?.click();

// 3. 全アイテム抽出
const items = Array.from(stepGroup?.querySelectorAll('.data-tree-item') || []).map(it => {
  const label = (it.querySelector('w-data-tree-pill, .data-tree-item__pill')?.textContent||'').trim();
  const iconId = it.querySelector('.data-tree-item__icon w-svg-icon, .data-tree-item__icon [data-icon-id]')?.getAttribute('data-icon-id') || '';
  return { label, type: iconId.replace(/^field-type\//,'') };
});
```

⚠ **PII 注意**: `.data-tree-item__sample` には実データ値（メール件名、本文断片、メールアドレス等）が含まれる。**ナレッジ収集ではサンプル値を保存しない**。フィールド名と型のみで `extended_output_schema` の役割は果たせる。

⚠ **ネスト深さ問題（残課題）**: `paddingLeft` が一律 0 で、配列の子要素もフラットに並んで見える。実用上は:
- toggle が `_closed` → コンテナで子要素を持つ（クリックで展開可能）
- toggle が `leaf` → 葉ノード
- toggle が `_open` → 既に展開された親（直後の leaf 群が子）
- 確実な深さ判定はさらに調査要

### 画面 6: アクション追加導線 / Action ピッカー

アクションを追加する場合、トリガーと違って **2 段階のピッカー**を経由する。

#### 6-a: ステップタイプピッカー

ACTIONS セクションの `+` (`button[aria-label="Add step"]`) をクリックすると、ステップ種別を選ぶ小ポップオーバーが出る。

```
ステップ種別: Action in app | Recipe function | IF condition | Repeat for each | Repeat while | Stop job | Handle errors
```

入力フィールド調査では `Action in app` を選ぶ。

#### 6-b: App ピッカー → Action ピッカー

`Action in app` を選ぶと App ピッカー（画面 3 と同じ）が出る。コネクタを選んだ後、トリガーが 1 個でスキップされる動作とは違い、アクションは原則複数あるので **Action ピッカー画面が必ず出る**:

```
w-recipe-step-details
└ w-recipe-step-details (operation モード)
    └ w-panel.recipe-step-details
        ├ w-panel-header                          ← "Choose an action"
        └ w-panel-content.recipe-step-details-operation
            └ w-operation-picker
                ├ w-search-field                  ← "Search for an action"
                └ li.operation-picker__item × N    ← 各アクション
                    └ w-operation
                        ├ "<Title>"                ← e.g. "Search rows"
                        ├ w-operation-badge        ← "Batch" バッジ等
                        └ "<description>"          ← e.g. "Search rows in selected sheet"
```

**操作**:
```javascript
// アクション選択（例: "Search rows"）
Array.from(document.querySelectorAll('li.operation-picker__item'))
  .find(li => li.textContent.trim().startsWith('Search rows'))
  ?.click();
```

App ピッカーがアイコングリッド形式だったのに対し、Action ピッカーは**1 行 1 アクションの詳細リスト形式**（タイトル + Batch 等のタグ + 説明文）。

タブの遷移: `App → Action → Connection → Setup`（trigger フローの `App → Trigger → Connection → Setup` と「2 段目だけ」異なる）。

### 画面 7: 動的フィールド検出（picklist 選択 → 新フィールド出現）⭐

`/integrations/meta` で `extends_input_schema=true` または `extends_output_schema=true` とマークされたオペレーションは、ユーザーが特定の picklist を選択した結果として、**新しい入力フィールド・出力フィールドが UI に追加される**。

**実例**: Google Sheets `search_spreadsheet_rows_v4_new` (Search rows)
- 初期表示: `Google Drive`, `Spreadsheet`
- Spreadsheet 選択後: `Sheet`, `Search result size` が追加される
- Sheet 選択後: `Columns` が追加され、その配下に**シートのヘッダー列ごとに `w-form-field` が動的生成**される

**実測の DOM 構造**（SAMPLE シート選択後、4 列のシート）:
```
w-form-field (top-level)         ← "Columns" (required, has 4 nested children)
└ .form-field__body
    └ .form-field-controls
        └ .form-field-input-wrapper
            ├ w-form-field        ← child 0: label="open_time" (sheet 列名)
            ├ w-form-field        ← child 1: label="open_price"
            ├ w-form-field        ← child 2: label="type"
            └ w-form-field        ← child 3: label="time_1m"
```

つまり、**親 `w-form-field` の配下に inner `w-form-field` が「列数だけ」並ぶ**のが動的フィールドの基本パターン。

**検出アルゴリズム**:
```javascript
// 0. 初期スナップショット (picklist 選択前)
const before = snapshotFields();   // top-level w-form-field の labels を記録

// 1. ユーザーが picklist を選択（UI 操作）
//    selectPicklist(...) — 例: Sheet picklist で値を選ぶ

// 2. DOM の安定を待つ（ローディング消失 / 一定時間 DOM 変化なし）
await waitForDomStable();

// 3. 再スナップショット
const after = snapshotFields();

// 4. 差分を計算 → 新出フィールドが「動的フィールド」
const newTopLevelFields = after.filter(f => !before.some(b => b.label === f.label));

// 5. 内側の子（per-column）も収集
function snapshotFields() {
  const top = Array.from(document.querySelectorAll('w-recipe-step-details w-form-field'))
    .filter(f => !f.parentElement?.closest('w-form-field'));
  return top.map(f => {
    const label = (f.querySelector('.form-field-label')?.textContent||'').trim().replace(/\s*\*$/,'');
    const innerFields = Array.from(f.querySelectorAll('w-form-field')).map(inner => ({
      label: (inner.querySelector('.form-field-label')?.textContent||'').trim().replace(/\s*\*$/,''),
      controlComponent: inner.querySelector('.form-field-input-wrapper > *')?.tagName.toLowerCase(),
    }));
    return { label, innerFields };
  });
}
```

**ナレッジ収集対象（動的フィールド検出時に記録すべき情報）**:
- **決定条件**: どの picklist の選択に依存するか（例: `spreadsheet + sheet`）
- **生成パターン**: 親フィールド名（例: `Columns`）+ 子要素の生成ルール（例: `シートのヘッダー列ごとに 1 つ`）
- **インスタンス固有値は記録しない**: `open_time`, `open_price` 等の実際の列名はテストデータ依存なので保存対象外

**動的 OUTPUT フィールド**: 同じパターンが Recipe data パネルにも反映される。**前ステップの output を見るには、その下に新しいステップを追加してそのステップの Setup 画面を開く**（Recipe data パネルは「現在のステップから見える前ステップ群の output」を表示する仕様）。

検出ロジックは [画面 5c](#画面-5c-recipe-data-パネル--出力スキーマ-) のとおり、`.data-tree-item` の `data-icon-id` で型情報も取れる。

✅ **実証済み**: Google Sheets `search_spreadsheet_rows_v4_new` で Spreadsheet → Sheet (SAMPLE) を選択 → Step 3 を追加して Setup を開くと、Recipe data パネルに `Search rows (Step 2 output)` グループが出現し、SAMPLE シートの実際の列ヘッダー 17 個が `Rows (array)` の子要素として `field-type/text` で出現することを確認。
- 静的 output: `Spreadsheet ID`, `Spreadsheet name`, `Sheet name`, `Rows (array)`, `List size`, `List index`
- 動的 output: `Rows[].Row number` + シートの全列ヘッダー（インスタンス固有）

つまり**動的 input の列名と動的 output の列名は同じ集合**になり、検出パターンも同じ DOM 構造（`w-form-field` ネスト → `Rows`/`Columns` 親要素配下）になる。

⚠ **入力フィールドと出力フィールドの粒度差**: SAMPLE シートでは UI の `Columns` 入力フィールド配下には 4 個の inner `w-form-field` しか表示されなかったが、実際の OUTPUT 側では 17 列すべてが見えた（Workato の入力 UI が「最初の N 列」だけ表示する仕様の可能性。要追加検証）。

## レベル 2 自動収集の標準フロー

`/auto-learn` スキルは **公式ドキュメント（`/sync-connectors`）と UI DOM 観察の組み合わせ**で構築する。Workato の内部 API は呼ばない。

### 前提
- Chrome で Workato にログイン済み + Claude in Chrome 拡張が有効
- 検証用ワークスペースに対象コネクタの認証済みコネクションがある
- 検証用プロジェクトに対象オペレーション（trigger / action）を使うスケルトンレシピを事前作成（`workato push` 経由で JSON から生成）

### Phase 1: 公式ドキュメントから静的情報を収集（既存の /sync-connectors）

```
/sync-connectors を実行 → docs.workato.com の各コネクタページを WebFetch
→ docs/connectors/<provider>.md にトリガー・アクションのリストと概要を反映
```

これで「どのコネクタにどんな trigger / action があるか」のカタログは取れる。  
ただし入力フィールドの hint や型、出力スキーマの詳細などは公式ドキュメントには載っていないことがある — そこを Phase 2 で補う。

### Phase 2: UI 観察で詳細フィールド情報を収集

対象オペレーションごとに:

```
1. navigate to /recipes/<id>/edit （対象 operation を設定済みのスケルトンレシピ）
2. click .recipe-step__header → Setup タブ到達を待つ

3. 静的入力フィールドの収集:
   - button:contains("Show optional fields") を click
   - w-dialog 出現を待つ
   - label.multi-select-list__item を全列挙
     → label + data-icon-id="field-type/<TYPE>" + visibleByDefault を取得
   - label.multi-select-list__checkbox を click（Select all）
   - button:contains("Apply changes") を click → モーダル消失を待つ
   - w-recipe-step-details w-form-field（top-level のみ）を列挙
     → hint, required (*), control component, has w-toggle-field を取得
   - label をキーにモーダル / フォームの情報をマージ
   - この時点で field の集合 = "静的入力フィールド" として記録

4. 静的出力フィールドの収集:
   - w-datatree が _minimize なら .data-tree-resize-controls をクリック
   - .data-tree-group_current の .data-tree-group__header を click（外側 __heading ではなく内側）
   - .data-tree-item を全列挙 → pill (label) + data-icon-id (type) を取得
   - この時点の集合 = "静的出力フィールド" として記録

5. 動的フィールドの検出（picklist 依存）:
   - 画面 7 を参照
   - スナップショット → picklist 選択（例: Sheet を選ぶ）→ DOM 安定待ち → 再スナップショット → 差分
   - 差分: トップレベルの新出 w-form-field + 既存フィールドの内側に新出 w-form-field 群
   - 動的 input の集合と「決定条件」（どの picklist が起点か）を記録
   - 同様に Recipe data パネルを再走査して動的 output 集合を取得
   - ⚠ インスタンス固有値（実際の列名 'open_time' 等）は構造のみ保存し、値は ナレッジに残さない
```

### Phase 3: 収集結果を docs に書き出し

```
docs/connectors/<provider>.md に
## triggers
### <operation_name>
- title, description, help（Phase 1 から）
- input_fields:
  - label, type, required, hint, default_visible, has_toggle_picker（Phase 2 から）
- output_fields:
  - label, type（Phase 2 から）
- dynamic_input_fields:
  - 決定条件（どの picklist 選択で生成されるか）+ 例（Phase 2 の差分から）
- dynamic_output_fields:
  - 同上

## actions
... （同じ構造）
```

### カスタムコネクタの扱い

- 既存の `/sync-connectors` がカスタムコネクタの `connector.rb` をパースしてカタログ化する仕組みを流用
- UI 経由の Phase 2 はカスタム / Pre-built 関係なく適用可能

## 実装上の注意

### クラス名のサフィックス
`ng-tns-c2016029271-7` のような Angular の view encapsulation サフィックスはビルド毎に変わる。**セレクタには使わない**。固定クラス（`recipe-step__header` 等）と要素タグで指定する。

### 仮想スクロール
`cdk-virtual-scroll-viewport` を使っているリストは画面外要素が DOM に存在しない場合がある。スクロールしてからクエリし直すか、データ量が少ない場合のみフラット展開する。

### Shadow DOM
現時点では Workato 主要コンポーネントに Shadow DOM の壁は確認されていない。すべて light DOM で取得可能。

### クリックの不発
Angular のイベントリスナーは要素自身ではなく親に張られているケースがある。クリックが効かないときは:
- 1 段親をクリック
- `dispatchEvent(new MouseEvent('click', {bubbles: true}))`
- 物理座標クリック（`computer.left_click`）

`.data-tree-group_current` の展開は **外側の `__heading` ではなく内側の `__header`** を click しないと効かなかった（実測）。

### PII の取り扱い
`.data-tree-item__sample` や `panel.querySelectorAll` の戻り値にはユーザーの実データが含まれる。ナレッジ収集スキルは:
- **サンプル値を docs に書かない**
- **トランスクリプトに dump しない**
- フィールド名と型情報のみを保存

### レスポンスの受動観察（任意）

UI 操作の結果として Workato 自身が発火させたリクエストのレスポンスは、補助情報として読んでよい（直接 fetch / XHR を新規発行するのは NG）。

例: ステップを開いたとき、picklist を選んだとき、Workato は内部エンドポイントを叩く。それらのレスポンスには DOM スクレイピングより構造化された情報（フィールドの内部 `name`、データ型、`pick_list` の値ペア等）が含まれることがある。

実装パターン:
1. `XMLHttpRequest` / `fetch` を **観測専用にラップ**して、レスポンスをコピーして辞書に格納するだけの interceptor を入れる
2. 通常の UI 操作（ステップを開く、picklist を選ぶ等）を実行
3. 該当レスポンスが格納されていたら、DOM 抽出結果と突き合わせて補強

注意:
- **新規リクエストを送らない**。リクエストの URL や body を真似て fetch すること、CSRF トークン回避、ヘッダ偽装などはすべて NG。
- **エンドポイントの仕様調査として総当たり的にいじらない**。観測するのは、UI 操作の自然な結果として発生したリクエストに限る。
- レスポンスにユーザーの実データ（メール、シート名、列値等）が含まれる場合は **PII の取り扱い** ルールに従い、フィールド構造のみを抽出して値は破棄する。
- 内部 API の URL や body 構造を docs に詳細記載しない（変わる可能性があり、依存ナレッジを残すと有害）。

## 残課題

### UI 観察関連
- [ ] dynamic picklist 選択 → スキーマ再読み込みの確実な検出方法（DOM 変化の終了を判定する条件 — ローディングインジケータ消失 / 一定時間の DOM 安定）
- [ ] データツリーの **ネスト深さ判定** — `paddingLeft` が一律 0 でフラット表示されるため、配列の子要素を親と紐づける確実な手段（toggle state ヒューリスティック以外）
- [ ] 複数トリガー持ちコネクタの **Trigger ピッカー画面**の DOM 構造（Gmail のように 1 個でスキップされない場合の観察）
- [ ] 大量フィールドコネクタでの仮想スクロール（`cdk-virtual-scroll-viewport`）追従
- [ ] saved レシピと unsaved レシピで Recipe data パネルの出方が違うかの確認

### 公式ドキュメント関連
- [ ] `/sync-connectors` で取れる情報と UI 観察で取れる情報の差分整理（重複の解消、相補的な使い分け）

### スキル化
- [ ] `/auto-learn` スキルの実装（公式ドキュメント + UI 観察の組み合わせ）
- [ ] スキルの長時間実行（300+ コネクタ）に耐える設計（中断 / 再開、進捗管理）

## 参考

- Issue #27: 自動ナレッジ収集 — レシピ push/pull + ブラウザ自動化によるフィールド情報取得
- 既存の関連検証は同 Issue のコメント履歴に詳細あり
