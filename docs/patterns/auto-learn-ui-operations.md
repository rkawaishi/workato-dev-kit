# 自動ナレッジ収集: Workato UI 操作 / 内部 API リファレンス

[Issue #27](https://github.com/rkawaishi/workato-dev-kit/issues/27) のレベル 2 でコネクタの input/output フィールド情報を収集するためのリファレンス。

3 つの取得経路を比較した結果、**`/integrations/meta`（内部 API）を主軸**にし、動的フィールドのみ UI 自動化で補う設計を採用する。

## 結論サマリ ⭐

| 経路 | 用途 | 詳細 |
|---|---|---|
| **Tier 1**: `docs.workato.com` | 公式情報の補完 | 既存の `/sync-connectors` で活用済 |
| **Tier 2**: `/integrations/meta?name=<provider>` ⭐ | **静的スキーマの主データソース** | 構造化 JSON で全 trigger/action の input/output を一括取得 |
| **Tier 3**: UI DOM スクレイピング | 動的フィールド + フォールバック | `extends_*_schema=true` の場合や Tier 2 が取れないとき |

**Tier 2 で取れる情報（実測 — Gmail `new_email` トリガー）**:
- 全 input フィールド（`name`, `label`, `type`, `control_type`, `optional`, `hint`, `pick_list`, `toggle_field`, `parse_output`）
- 全 output フィールド（`name`, `label`, `type`, `of`, `properties[]` でネスト構造込み）
- `extends_input_schema` / `extends_output_schema` フラグ（dynamic 有無）

**UI からのみ取れる情報（Tier 3 を残す理由）**:
- dynamic picklist 選択後に生成される動的フィールド（テーブル列、シートヘッダ等）
- カスタムコネクタの一部メタ情報（要調査）
- 内部 API エンドポイントが将来変わったときのフォールバック

## Tier 2: `/integrations/meta` 内部 API ⭐

### エンドポイント

```
GET /integrations/meta?name=<provider>&cacheKey=<rotating_key>
```

- `name`: コネクタの内部 ID（例: `gmail`, `google_sheets`, `salesforce`）— `klass: "Adapters::<X>::Adapter"` から推測可能
- `cacheKey`: 16 進文字列（例: `eb5a9e02d42_en`）— ビルドごとに変わる、サーバ側でキャッシュキーとして利用
  - 取得方法: 一度ページを開いて DevTools / network 監視で `/integrations/meta?name=gmail&cacheKey=...` を観察 → 抽出
  - 期限切れ時は新しいキーで再取得（Workato 自身がやっているのと同じ）
- 認証: ログイン中のセッション cookie（Claude in Chrome 経由ならそのまま使える）

### レスポンス構造

```jsonc
{
  "<provider_name>": {
    "name": "gmail",
    "klass": "Adapters::Gmail::Adapter",
    "title": "Gmail",
    "categories": ["Productivity", "Sales Enablement"],
    "config": { /* OAuth / connection 設定 */ },
    "triggers": {
      "new_email": {
        "name": "new_email",
        "title": "New email",
        "title_hint": "Triggers when a new email is received",
        "help": "Checks for new emails every {{authUser.membership.poll_interval}} minutes...",
        "input": [ /* InputField[] */ ],
        "output": [ /* OutputField[] */ ],
        "extends_input_schema": false,
        "extends_output_schema": false,
        // ...
      }
    },
    "actions": {
      "send_mail": { /* 同じ構造 */ },
      "download_attachment": { /* ... */ },
      "get_email_or_draft_by_id": { /* ... */ },
      "__adhoc_http_action": { /* ... */ }
    },
    "data_pipeline_triggers": {},
    "triggers_count": 1,
    "actions_count": 4
  }
}
```

### `InputField` の構造

```jsonc
{
  "name": "___poll_interval",                  // 内部 JSON キー名（重要）
  "label": "Trigger poll interval",            // 表示ラベル
  "type": "integer",                           // データ型
  "control_type": "select",                    // UI レンダリング種別: text / select / date_time / checkbox / textarea / etc.
  "optional": true,                            // 必須/任意
  "hint": "How frequently to check...",        // ヒント文（フル）
  "parse_output": "integer_conversion",        // 型変換ヒント: integer_conversion / boolean_conversion / date_time_conversion
  "pick_list": [["5 minutes", 5], ["15 minutes", 15], ...],  // preset 値（ラベル + 内部 ID）
  "toggle_field": {                            // preset/custom 切替がある場合のフィールド設定
    "control_type": "...", "label": "...", "type": "...", "name": "..."
  },
  // 他にも: support_pills, disable_formula, sticky, default, etc.
}
```

### `OutputField` の構造

```jsonc
// 単純型
{
  "name": "subject",
  "label": "Subject",
  "type": "string"  // string / integer / number / boolean / date_time / array
}

// 配列（プリミティブ）
{
  "name": "labelIds",
  "label": "Label IDs",
  "type": "array",
  "of": "string"
}

// 配列（オブジェクト = ネスト構造体）
{
  "name": "attachments",
  "label": "Attachments",
  "type": "array",
  "of": "object",
  "properties": [
    { "name": "mimeType", "label": "Mime type", "type": "string", "control_type": "text" },
    { "name": "filename", "label": "Filename", "type": "string", "control_type": "text" },
    { "name": "filesize", "label": "Filesize", "type": "integer", "control_type": "text", "parse_output": "integer_conversion" },
    { "name": "attachmentId", "label": "Attachment ID", "type": "string", "control_type": "text" }
  ]
}
```

### 取得スニペット

```javascript
// 1 コネクタ全体のスキーマを取得
async function fetchConnectorMeta(provider, cacheKey) {
  const r = await fetch(`/integrations/meta?name=${provider}&cacheKey=${cacheKey}`, { credentials: 'include' });
  if (!r.ok) throw new Error(`HTTP ${r.status}`);
  const j = await r.json();
  return j[provider]; // top-level key = provider name
}

// 全 trigger/action のフィールド一覧を平坦化
function extractAllOperations(adapterMeta) {
  const ops = [];
  for (const [name, t] of Object.entries(adapterMeta.triggers || {})) {
    ops.push({ kind: 'trigger', name, ...t });
  }
  for (const [name, a] of Object.entries(adapterMeta.actions || {})) {
    if (name.startsWith('__')) continue; // skip __adhoc_http_action 等の内部用
    ops.push({ kind: 'action', name, ...a });
  }
  return ops;
}
```

### `cacheKey` の取得方法

ページの最初のロード時、`window` 上に Workato が露出させている場合がある（要確認）。  
確実な方法は network 監視:

```javascript
// 既に発生している /integrations/meta リクエストから抽出
async function getCacheKey() {
  // performance.getEntriesByType('resource') で過去のリソースリクエストを参照
  const entries = performance.getEntriesByType('resource')
    .filter(e => e.name.includes('/integrations/meta?'));
  const m = entries[0]?.name.match(/cacheKey=([^&]+)/);
  return m?.[1];
}
```

### 留意事項

- **動的スキーマ（`extends_*_schema: true`）**: 例えば Google Sheets の "search rows" アクションは sheet 選択後に列名フィールドが生成される。これは Tier 2 の単発リクエストでは取れず、別エンドポイント（`/recipe/<id>/picklist?...` 等）と組み合わせる必要がある。要追加調査。
- **カスタムコネクタ**: 別エンドポイント `/web_api/recipes/<id>/custom_adapters/pre_install.json` が存在。要追加調査。
- **`__` プレフィックスのアクション**: `__adhoc_http_action` 等は内部用なので除外する。
- **i18n**: `cacheKey` の末尾 `_en` は言語コード。スキーマの `label` / `hint` は言語に依存して返ってくるので、ナレッジ収集は **`_en` 固定**で行う。

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

## レベル 2 自動収集の標準フロー（再設計）

`/auto-learn` スキルは **Tier 2 を主軸**にし、必要に応じて Tier 3 で補完する。

### 前提
- Chrome で Workato にログイン済み + Claude in Chrome 拡張が有効
- 検証用ワークスペースに対象コネクタの認証済みコネクションがある（Tier 3 を使う場合のみ必須）

### Phase 1: cacheKey の取得（初回のみ）

```
navigate to /recipes/<any_recipe_id>/edit
wait for /integrations/meta?name=...&cacheKey=... が performance entries に現れる
extract cacheKey from URL query
```

`cacheKey` はワークスペース内では一定期間共有されるので、最初の 1 回取れば複数コネクタで使い回せる。

### Phase 2: コネクタ全体スキーマの取得（Tier 2）

```
fetch /integrations/meta?name=<provider>&cacheKey=<key>
parse triggers / actions
for each operation:
  記録: name, kind (trigger/action), title, help, extends_input_schema, extends_output_schema
  記録: input_fields[] = [{ name, label, type, control_type, optional, hint, pick_list, toggle_field, parse_output }]
  記録: output_fields[] = [{ name, label, type, of, properties[] (再帰) }]
```

これで **`extends_*_schema: false` のオペレーションは収集完了**（Pre-built コネクタの大半はここに該当）。

### Phase 3: 動的スキーマの収集（`extends_*_schema: true` のもののみ）

```
for each operation with extends_input_schema=true or extends_output_schema=true:
  navigate to /recipes/<id>/edit (operation を予め設定済みのスケルトンレシピ)
  click .recipe-step__header
  Setup タブ到達待ち

  if extends_input_schema:
    open Show optional fields modal
    extract all field labels + data-icon-id
    apply changes

    if dynamic picklist が想定される field 存在:
      pick a value
      wait for schema reload
      re-extract fields
      diff = dynamic input fields

  if extends_output_schema:
    expand Recipe data panel
    expand Current step output group
    extract .data-tree-item の (label, field-type)
    if any picklist was selected: 同じく差分で動的 output を識別
```

### Phase 4: 収集結果を docs に書き出し

```
docs/connectors/<provider>.md に
## triggers
### <name>
- title, description, help
- extends_input_schema: bool
- extends_output_schema: bool
- input_fields: <Tier 2 の構造をそのまま>
- output_fields: <Tier 2 の構造をそのまま>
- dynamic_input_fields: <Tier 3 で取れた差分（あれば）>
- dynamic_output_fields: <同上>

## actions
... (同じ構造)
```

### カスタムコネクタの扱い（要追加調査）

- `/web_api/recipes/<id>/custom_adapters/pre_install.json` で取得可能な可能性
- 取れない場合は、既存の `/sync-connectors` が `connector.rb` をパースしてカタログ化する仕組みを流用

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

## 残課題

### Tier 2 関連
- [ ] `cacheKey` の取得方法を確実にする（performance entries 経由 / `window.*` への露出有無 / 期限切れ時の再取得）
- [ ] **動的スキーマの取得経路** — `extends_*_schema: true` のオペレーションで Workato 自身がどのエンドポイントを叩いているかを観察（picklist 選択 → 再フェッチの URL を捕捉）
- [ ] **カスタムコネクタの meta API** — `/web_api/recipes/<id>/custom_adapters/pre_install.json` の構造調査
- [ ] エンドポイント変更耐性 — Workato が将来 `cacheKey` ベースから別形式に変えた場合のフォールバック設計
- [ ] レート制限 / 同時リクエスト制約の確認（300 コネクタを順次取得する際）

### Tier 3 関連（動的フィールド検出）
- [ ] dynamic picklist 選択 → スキーマ再読み込み の確実な検出方法（DOM 差分 vs network ピング）
- [ ] データツリーの**ネスト深さ判定** — Tier 2 では `properties[]` で取れるが、動的に追加されたフィールドのネスト判定方法（Tier 3 のみで完結する場合）
- [ ] 複数トリガー持ちコネクタの **Trigger ピッカー画面**の DOM 構造（自動スキップしないコネクタでの観察）

### Tier 1 関連
- [ ] `/sync-connectors` との役割分担を明確化（Tier 2 が主軸になった今、`/sync-connectors` はカスタムコネクタ専用 or 補完用に再定義）

## 参考

- Issue #27: 自動ナレッジ収集 — レシピ push/pull + ブラウザ自動化によるフィールド情報取得
- 既存の関連検証は同 Issue のコメント履歴に詳細あり
