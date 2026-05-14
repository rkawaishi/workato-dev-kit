# Automated knowledge collection: Workato UI operations reference

Reference for collecting connector input/output field information at level 2 of [Issue #27](https://github.com/rkawaishi/workato-dev-kit/issues/27).

**Do not adopt any approach that directly hits Workato's internal (non-public) APIs**. Information sources are limited to (a) the official documentation at `docs.workato.com` and (b) DOM observation of the Workato UI.

## Summary of conclusions

| Source | Purpose | Details |
|---|---|---|
| **Official docs**: `docs.workato.com` | Primary data source for static schemas | Already used via API by the existing `/sync-connectors` |
| **UI DOM observation** (the subject of this document) | Dynamic fields plus information missing from the official docs | Operate the recipe editor through Claude in Chrome |

**Information obtainable from the UI**:
- Full list of input fields (including hidden ones) along with each field's type — `Show optional fields` modal
- Field hint text, required flag, and control kind — Setup form
- Presence or absence of a Toggle picker (preset/custom switch) — Setup form
- Output schema and the type of each field — Recipe data panel
- Dynamic fields (table columns and the like) — DOM diff before and after picklist selection

This lets data equivalent to `extended_input_schema` / `extended_output_schema` / `dynamicPickListSelection` / `toggleCfg` / `visible_config_fields` be collected in a single UI session.

> **Internal API policy (the key boundary)**:
> - NG: directly hitting internal APIs (`/integrations/meta`, `/connections/<id>/extended_schema.json`, etc.) **with requests we construct ourselves**, and brute-force observation of requests/responses to reverse-engineer them.
> - OK: **passively reading the responses** to requests that Workato itself fires as a result of **normal UI operations** performed by the user (or by an automation script).
>
> Design this knowledge-collection skill so that UI operations are the primary mechanism, with response reading used only as a supplementary way to obtain structured data. Do not have the skill call internal endpoints directly via fetch / XHR.

## Workato UI DOM conventions

### Angular custom elements
The skeleton of the screen is built from Angular custom elements with the `w-` prefix. Class names carry mutable suffixes such as `ng-tns-c<hash>` that change with every build, so **write selectors against tag names, attributes, and stable classes (such as `recipe-step__header`)**.

### Naming conventions
- A "connector" is internally referred to as an **adapter** (`w-adapter-picker`, `adapter-picker__item`)
- A "step details" pane is consistently called **recipe-step-details**
- A "data tree (datapill source)" is **data-tree** / **datatree**

### Shared icon convention for types
Workato expresses types via the `data-icon-id` attribute. This is shared between input-field modals and the output data tree:

```html
<w-svg-icon data-icon-id="field-type/text" ...>
```

| `data-icon-id` value | Meaning |
|---|---|
| `field-type/text` | String |
| `field-type/integer` | Integer |
| `field-type/number` | Decimal (inferred — needs verification against other connectors) |
| `field-type/date-time` | datetime |
| `field-type/date` | Date (inferred) |
| `field-type/boolean` | boolean (inferred) |
| `field-type/text-array` | Array of strings |
| `field-type/array` | Array of objects |
| `field-type/object` | Object (inferred) |

Append unverified types as other connectors are investigated.

## Per-screen operations reference

### Screen 1: Assets view (project asset list)

**URL**: `https://app.<region>.workato.com/?fid=<workspace_id>#assets`

| Role | Selector |
|---|---|
| Project switcher | Project name in the left sidebar |
| Create new asset | `Create` button at the top right |
| Asset list | Recipe card `<a>` link navigates to `/recipes/<id>` |

`/auto-learn` typically bypasses the Assets view, generating the recipe ID and going directly to `/recipes/<id>/edit`.

### Screen 2: Recipe editor (empty canvas)

**URL**: `https://app.<region>.workato.com/recipes/<recipe_id>/edit`

```
w-recipe-editor
├ w-recipe-editor-header                       ← toolbar
│   ├ w-editable-text                          ← recipe name
│   ├ w-header-mode-switch                     ← RECIPE / TEST JOBS tabs
│   └ w-header-toolbar-buttons                 ← Save / Test recipe / Refresh / Exit
└ w-recipe-viewer
    └ w-recipe-steps-canvas                     ← entire canvas
        └ w-recipe-viewer-steps
            └ w-recipe-steps
                └ w-recipe-step × N             ← each step
```

**Main interaction targets**:

| Role | Selector |
|---|---|
| Body that expands / collapses the step | `w-recipe-step .recipe-step__header` |
| Number bubble (step selection) | `.recipe-step__number-button` |
| The `+` between steps | `button.recipe-step-marker__button_add[aria-label="Add step"]` |
| The `+` to add the first action | `w-recipe-add-step button[aria-label="Add step"]` |
| Save | `<button>` text=`Save` |
| Exit | `<button>` text=`Exit` |
| RECIPE/TEST JOBS toggle | `<button>` inside `w-header-mode-switch` |

**Characteristics of the initial state**:
- Only one trigger step exists (placeholder "Select an app and trigger event")
- The ACTIONS section is empty and shows only the `+` from `w-recipe-add-step`

### Screen 3: App picker panel (after clicking Trigger/Action)

**Transition**: clicking `.recipe-step__header` slides a `w-recipe-step-details` panel in from the right.

**Panel structure**:
```
w-recipe-step-details
└ w-recipe-step-details-adapter                 ← App picker mode
    └ w-panel.recipe-step-details
        ├ w-panel-header (.panel-header)
        │   ├ .panel-header__wrapper            ← "Choose an app"
        │   └ button.panel-header__close[aria-label="Close side panel"]
        └ w-panel-content.recipe-step-details-adapter
            ├ .tabs__labels                      ← App / Trigger / Connection / Setup
            │   └ button.tabs__label             (.tabs__label_active marks the current tab)
            └ w-adapter-picker
                ├ input.search-field__input[placeholder="Search for an app"]
                └ w-adapter-picker-option × N
                    └ w-select-grid-option
                        └ button.select-grid-option   ← internal textContent = connector name
```

**Main operations**:

```javascript
// Select a connector (e.g. "Gmail")
Array.from(document.querySelectorAll('w-adapter-picker-option button.select-grid-option'))
  .find(b => b.textContent.trim() === 'Gmail')
  ?.click();

// Search by app name
const input = document.querySelector('input.search-field__input');
input.value = 'gmail';
input.dispatchEvent(new Event('input', { bubbles: true }));
```

### Screen 4: Connection picker

**Transition**: selecting a connector automatically advances to the `Connection` stage (tab switches).

**Important branching rule**: connectors with **exactly one** selectable trigger **automatically skip** the Trigger stage and adopt the default trigger, advancing directly to Connection. Connectors with multiple triggers show the Trigger picker (described later). Actions in principle have multiple choices, so unlike Trigger the picker is shown every time (inferred — needs verification).

**Detecting the destination**:
```javascript
// Check the current tab
document.querySelector('button.tabs__label.tabs__label_active')?.textContent.trim();
// → "Connection" means it was skipped / "Trigger" means the picker is needed

// Or determine it from the panel-content class
document.querySelector('w-recipe-step-details w-panel-content')?.className;
// → "recipe-step-details-connection" / "recipe-step-details-trigger" / "recipe-step-config" etc.
```

**Connection picker DOM**:
```
w-panel-content.recipe-step-details-connection
└ w-connection-list-picker
    ├ w-search-field                              ← "Search active connections"
    ├ w-paging-items-count                        ← "Showing N active connection(s)"
    ├ button "Refresh list"
    ├ .connection-list-picker__list
    │   └ w-connection-card × N
    │       ├ w-connection-title                   ← e.g. "Sample1 | Gmail"
    │       └ w-folder-path                        ← containing project
    ├ w-paginator
    └ button.connection-list-picker__new-connection-button "New connection"
```

**Operation**:
```javascript
// Select an existing connection
Array.from(document.querySelectorAll('w-connection-card'))
  .find(c => c.textContent.trim().startsWith('Sample1 | Gmail'))
  ?.click();
```

Tab enable/disable behaviour:
- The Setup tab stays `disabled` until a connection is selected
- The Trigger tab can be returned to, but in the trigger-skip case it may be omitted

### Screen 5: Setup (field entry) screen — the main target

**Transition**: selecting a connection automatically advances to the Setup tab.

**Panel structure**:
```
w-recipe-step-details
└ w-recipe-step-details (config mode)
    └ w-panel.recipe-step-details
        ├ w-panel-header                          ← e.g. "New email in Gmail"
        └ w-panel-content.recipe-step-config
            ├ w-recipe-step-config-search          ← "Find" search
            ├ w-optional-fields-button             ← "Show optional fields"
            ├ button "Reset"
            ├ w-recipe-step-help / w-tips          ← HELP banner
            └ w-recipe-operation-step-config
                └ w-endless-scroll
                    └ w-in-view-item × N
                        └ w-form-field × N         ← one field
```

**Breakdown of a single field**:
```
w-form-field
└ .form-field
    └ .form-field__body
        ├ w-form-field-simple-label
        │   └ .form-field-label.form-field-simple-label   ← label string ("*" at the end if required)
        └ .form-field-controls
            ├ w-formula-switcher                          ← Text/Formula switcher (when present)
            ├ w-form-field-ai-button                      ← AI assistant
            ├ .form-field-input-wrapper
            │   └ <w-* element per input type>
            └ .form-field-hint
                └ .form-field-hint__content                ← description text
```

**`w-*` elements by input type**:

| Tag | Meaning |
|---|---|
| `w-text-field` | Plain text / number / datetime |
| `w-text-field-type` | Picklist for Text/Formula kind |
| `w-text-field-preview` | Preview display |
| `w-select` / `w-select-field` | enum / picklist |
| `w-boolean-select-field` | Yes/No picklist |
| `w-toggle-field` | "Select from list / Custom value" switcher (**entry point for the dynamic picklist**) |
| `w-date-time-field` | datetime picker (inferred) |
| `w-textarea-field` | Multi-line text (inferred) |

**Key: `w-form-field` is nested**:
Fields that have a toggle picker carry a two-layer structure with an outer `w-form-field` (for the picker) and an inner `w-form-field` (for the actual value). When taking a field list, filter down to **top-level only**:
```javascript
const topLevel = Array.from(document.querySelectorAll('w-recipe-step-details w-form-field'))
  .filter(f => !f.parentElement?.closest('w-form-field'));
```

**Header buttons**:
| Role | Selector |
|---|---|
| Find (field search) | `<button>` text=`Find` |
| Show optional fields | `<button>` text=`Show optional fields` |
| Reset | `<button>` text=`Reset` |
| Close the panel | `button.panel-header__close` |

### Screen 5b: Show optional fields modal

**Transition**: the `Show optional fields` button in the Setup header opens a `w-dialog` as a modal.

```
w-dialog
├ Header: "Show optional fields" + ✕
├ w-text-filter                                    ← search box
├ w-select-filter "All optional fields"            ← category filter
├ "M of N results selected" counter
└ multi-select-list
    ├ label.multi-select-list__checkbox            ← "Select all" (supports indeterminate)
    └ cdk-virtual-scroll-viewport                  ← virtual scroll
        └ cdk-virtual-scroll-content-wrapper
            └ label.multi-select-list__item × N
                ├ input[type=checkbox]              ← visible-by-default state
                ├ w-svg-icon.multi-select-list__item-icon
                │   data-icon-id="field-type/<TYPE>"   ← type information
                └ span.multi-select-list__item-content
                    └ span.multi-select-list__item-title  ← field name
└ Cancel / Apply changes
```

**Extract the full list of fields plus their types**:
```javascript
const items = Array.from(document.querySelectorAll('label.multi-select-list__item')).map(label => ({
  label: label.querySelector('.multi-select-list__item-title')?.textContent.trim(),
  type: (label.querySelector('.multi-select-list__item-icon')?.getAttribute('data-icon-id') || '').replace(/^field-type\//,''),
  visibleByDefault: label.querySelector('input[type="checkbox"]')?.checked,
}));
```

**Expand every field then Apply**:
```javascript
document.querySelector('label.multi-select-list__checkbox')?.click();        // Select all
Array.from(document.querySelectorAll('button')).find(b => b.textContent.trim() === 'Apply changes')?.click();
```

### Screen 5c: Recipe data panel — output schema

**Position**: a floating panel pinned to the lower-left of the Setup screen (starts minimized).

```
w-recipe-step-details
└ w-recipe-editor-datatree
    └ w-datatree.recipe-editor-datatree(.recipe-editor-datatree_default | _minimize)
        └ .data-tree.trigger-line.data-tree_static
            ├ .data-tree__heading
            │   ├ h4.data-tree__title             ← "Recipe data"
            │   └ .data-tree-resize-controls > w-svg-icon  ← expand/minimize toggle
            ├ .data-tree__description              ← "To use data from a previous step..."
            └ .data-tree__scroll
                └ .data-tree__groups
                    ├ .data-tree-group(.data-tree-group_opened)
                    │   ← "Properties" (datapills for workspace/recipe metadata)
                    │   └ items...
                    └ .data-tree-group(.data-tree-group_current)
                        ← "Current step output / New email (Step 1 output)"
                        ├ .data-tree-group__heading
                        ├ .data-tree-group__header              ← click the inner element to expand
                        └ items...
```

**Breakdown of one datapill**:
```
.data-tree-item
├ .data-tree-item__toggle (.data-tree-item__toggle_open)         ← caret (nest expansion)
├ .data-tree-item__icon
│   └ w-svg-icon[data-icon-id="field-type/<TYPE>"]                ← type information
├ w-data-tree-pill.data-tree-item__pill                           ← field name (label)
└ .data-tree-item__sample                                         ← sample value (PII caution)
```

**Expand and extract the schema**:
```javascript
// 1. Maximize the panel
const datatree = document.querySelector('w-datatree');
if (datatree?.classList.contains('recipe-editor-datatree_minimize')) {
  document.querySelector('.data-tree-resize-controls__icon, .data-tree-resize-controls w-svg-icon')?.click();
}

// 2. Expand the Current step output group (the inner __header is the click target)
const stepGroup = Array.from(document.querySelectorAll('.data-tree-group'))
  .find(g => /Step \d+ output|Current step output/.test(g.textContent));
stepGroup?.querySelector('.data-tree-group__header')?.click();

// 3. Extract every item
const items = Array.from(stepGroup?.querySelectorAll('.data-tree-item') || []).map(it => {
  const label = (it.querySelector('w-data-tree-pill, .data-tree-item__pill')?.textContent||'').trim();
  const iconId = it.querySelector('.data-tree-item__icon w-svg-icon, .data-tree-item__icon [data-icon-id]')?.getAttribute('data-icon-id') || '';
  return { label, type: iconId.replace(/^field-type\//,'') };
});
```

**PII caution**: `.data-tree-item__sample` contains real data values (email subjects, body fragments, addresses, etc.). **Do not persist sample values in knowledge collection**. Field names plus types are enough to fulfil the role of `extended_output_schema`.

**Nesting depth issue (open)**: `paddingLeft` is uniformly 0, so array children visually sit flat alongside their parent. In practice:
- toggle `_closed` → container with children (can be expanded by clicking)
- toggle `leaf` → leaf node
- toggle `_open` → already-expanded parent (the leaves that follow are its children)
- Reliable depth detection needs further investigation

### Screen 6: Action add path / Action picker

When adding an action, unlike the trigger flow you go through **two pickers**.

#### 6-a: Step type picker

Clicking the `+` (`button[aria-label="Add step"]`) in the ACTIONS section opens a small popover for choosing the step kind.

```
Step kinds: Action in app | Recipe function | IF condition | Repeat for each | Repeat while | Stop job | Handle errors
```

For input-field investigation pick `Action in app`.

#### 6-b: App picker → Action picker

Choosing `Action in app` brings up the App picker (same as Screen 3). After selecting a connector, unlike the single-trigger skip behaviour, actions generally have multiple choices, so the **Action picker screen always appears**:

```
w-recipe-step-details
└ w-recipe-step-details (operation mode)
    └ w-panel.recipe-step-details
        ├ w-panel-header                          ← "Choose an action"
        └ w-panel-content.recipe-step-details-operation
            └ w-operation-picker
                ├ w-search-field                  ← "Search for an action"
                └ li.operation-picker__item × N    ← each action
                    └ w-operation
                        ├ "<Title>"                ← e.g. "Search rows"
                        ├ w-operation-badge        ← e.g. "Batch" badge
                        └ "<description>"          ← e.g. "Search rows in selected sheet"
```

**Operation**:
```javascript
// Select an action (e.g. "Search rows")
Array.from(document.querySelectorAll('li.operation-picker__item'))
  .find(li => li.textContent.trim().startsWith('Search rows'))
  ?.click();
```

Whereas the App picker was an icon-grid layout, the Action picker is a **one-action-per-row detailed list** (title + tags such as Batch + description).

Tab progression: `App → Action → Connection → Setup` (the trigger flow `App → Trigger → Connection → Setup` differs only in the second stage).

### Screen 7: Dynamic field detection (picklist selection → new fields appear)

Operations marked in `/integrations/meta` with `extends_input_schema=true` or `extends_output_schema=true` have **new input/output fields added to the UI** as a result of the user choosing a particular picklist value.

**Concrete example**: Google Sheets `search_spreadsheet_rows_v4_new` (Search rows)
- Initial display: `Google Drive`, `Spreadsheet`
- After selecting Spreadsheet: `Sheet` and `Search result size` are added
- After selecting Sheet: `Columns` is added, and **`w-form-field`s are dynamically generated under it, one per header column of the sheet**

**Observed DOM structure** (after selecting the SAMPLE sheet, a 4-column sheet):
```
w-form-field (top-level)         ← "Columns" (required, has 4 nested children)
└ .form-field__body
    └ .form-field-controls
        └ .form-field-input-wrapper
            ├ w-form-field        ← child 0: label="open_time" (sheet column name)
            ├ w-form-field        ← child 1: label="open_price"
            ├ w-form-field        ← child 2: label="type"
            └ w-form-field        ← child 3: label="time_1m"
```

In other words, the basic dynamic-field pattern is **"`w-form-field` parent containing as many inner `w-form-field`s as there are columns"**.

**Detection algorithm**:
```javascript
// 0. Initial snapshot (before picklist selection)
const before = snapshotFields();   // record the labels of the top-level w-form-fields

// 1. User picks a picklist value (UI operation)
//    selectPicklist(...) — e.g. pick a value in the Sheet picklist

// 2. Wait for the DOM to settle (loading indicator disappears / DOM stays unchanged for a fixed period)
await waitForDomStable();

// 3. Re-snapshot
const after = snapshotFields();

// 4. Diff → the newly appearing fields are the "dynamic fields"
const newTopLevelFields = after.filter(f => !before.some(b => b.label === f.label));

// 5. Also collect inner (per-column) children
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

**Information to record during dynamic field detection**:
- **Determining condition**: which picklist selection it depends on (e.g. `spreadsheet + sheet`)
- **Generation pattern**: the parent field name (e.g. `Columns`) plus the rule for generating children (e.g. `one per header column of the sheet`)
- **Do not record instance-specific values**: actual column names like `open_time`, `open_price` are test-data dependent and therefore out of scope

**Dynamic OUTPUT fields**: the same pattern is also reflected in the Recipe data panel. **To see the output of a previous step, add a new step beneath it and open that step's Setup screen** (the Recipe data panel is designed to show "outputs from previous steps visible from the current step").

The detection logic follows [Screen 5c](#screen-5c-recipe-data-panel--output-schema): `.data-tree-item`'s `data-icon-id` also carries the type information.

**Verified**: With Google Sheets `search_spreadsheet_rows_v4_new`, selecting Spreadsheet → Sheet (SAMPLE) then adding Step 3 and opening its Setup screen reveals a `Search rows (Step 2 output)` group in the Recipe data panel, with all 17 actual header columns of the SAMPLE sheet appearing as children of `Rows (array)` with `field-type/text`.
- Static output: `Spreadsheet ID`, `Spreadsheet name`, `Sheet name`, `Rows (array)`, `List size`, `List index`
- Dynamic output: `Rows[].Row number` plus every header column of the sheet (instance specific)

So **the column names of the dynamic input match the column names of the dynamic output**, and the detection pattern is the same DOM structure (`w-form-field` nesting → under a `Rows`/`Columns` parent element).

**Granularity gap between input and output fields**: for the SAMPLE sheet the UI's `Columns` input field showed only 4 inner `w-form-field`s, while the OUTPUT side revealed all 17 columns (possibly because the Workato input UI is designed to display only "the first N columns" — needs further verification).

## Standard flow for level-2 automated collection

The `/auto-learn` skill is built from a **combination of official documentation (`/sync-connectors`) and UI DOM observation**. It does not call Workato's internal APIs.

### Prerequisites
- Already logged in to Workato in Chrome plus Claude in Chrome extension enabled
- The verification workspace has an authenticated connection for the target connector
- A skeleton recipe in the verification project that already uses the target operation (trigger / action) has been created in advance (generated from JSON via `workato push`)

### Phase 1: collect static information from the official documentation (existing /sync-connectors)

```
Run /sync-connectors → WebFetch each connector page on docs.workato.com
→ reflect the list and summary of triggers/actions into docs/connectors/<provider>.md
```

This yields a catalog of "which connectors have which triggers / actions".
However, things like input-field hints and types, or output schema details, are sometimes absent from the official documentation — Phase 2 fills those gaps.

### Phase 2: collect detailed field information via UI observation

For each target operation:

```
1. navigate to /recipes/<id>/edit (a skeleton recipe with the target operation already configured)
2. click .recipe-step__header → wait for arrival at the Setup tab

3. Collect static input fields:
   - click button:contains("Show optional fields")
   - wait for w-dialog to appear
   - enumerate every label.multi-select-list__item
     → capture label + data-icon-id="field-type/<TYPE>" + visibleByDefault
   - click label.multi-select-list__checkbox (Select all)
   - click button:contains("Apply changes") → wait for the modal to disappear
   - enumerate w-recipe-step-details w-form-field (top-level only)
     → capture hint, required (*), control component, presence of w-toggle-field
   - merge modal / form info keyed by label
   - At this point the set of fields = "static input fields" — record it

4. Collect static output fields:
   - if w-datatree is _minimize, click .data-tree-resize-controls
   - click .data-tree-group_current's .data-tree-group__header (the inner one, not the outer __heading)
   - enumerate every .data-tree-item → capture pill (label) + data-icon-id (type)
   - At this point the set = "static output fields" — record it

5. Detect dynamic fields (picklist dependent):
   - See Screen 7
   - snapshot → select picklist (e.g. pick Sheet) → wait for DOM stability → re-snapshot → diff
   - Diff: newly appearing top-level w-form-fields + newly appearing inner w-form-fields under existing fields
   - Record the set of dynamic inputs together with the "determining condition" (which picklist is the trigger)
   - Likewise re-scan the Recipe data panel to obtain the dynamic output set
   - Instance-specific values (actual column names such as 'open_time') are recorded as structure only; do not leave values in the knowledge base
```

### Phase 3: write the collected results out to docs

```
In docs/connectors/<provider>.md write:
## triggers
### <operation_name>
- title, description, help (from Phase 1)
- input_fields:
  - label, type, required, hint, default_visible, has_toggle_picker (from Phase 2)
- output_fields:
  - label, type (from Phase 2)
- dynamic_input_fields:
  - determining condition (which picklist selection produces them) + example (from the Phase 2 diff)
- dynamic_output_fields:
  - same as above

## actions
... (same structure)
```

### Custom connectors

- Reuse the existing `/sync-connectors` mechanism that parses a custom connector's `connector.rb` to build the catalog
- Phase 2 via the UI applies equally to custom and pre-built connectors

## Implementation notes

### Class-name suffixes
Angular's view-encapsulation suffixes like `ng-tns-c2016029271-7` change between builds. **Do not use them in selectors.** Specify with stable classes (such as `recipe-step__header`) and element tags.

### Virtual scroll
Lists using `cdk-virtual-scroll-viewport` may not have off-screen elements in the DOM. Either scroll first and re-query, or fully expand only when the dataset is small.

### Shadow DOM
At this point no Shadow DOM walls have been confirmed in the main Workato components. Everything is reachable through light DOM.

### Click misfires
Angular event listeners are sometimes attached to a parent rather than to the element itself. When a click does not take effect:
- Click one level up
- `dispatchEvent(new MouseEvent('click', {bubbles: true}))`
- Physical coordinate click (`computer.left_click`)

Expanding `.data-tree-group_current` did not work clicking the outer `__heading` — the inner `__header` must be clicked (observed).

### Handling PII
`.data-tree-item__sample` and the return value of `panel.querySelectorAll` may contain the user's real data. The knowledge-collection skill must:
- **Not write sample values into docs**
- **Not dump them into the transcript**
- Only persist field names and type information

### Passive response observation (optional)

Responses to requests Workato itself fires as a result of UI operations may be read as auxiliary information (issuing new fetch / XHR is NG).

Example: when a step is opened or a picklist is selected, Workato hits internal endpoints. Those responses sometimes contain more structured information than DOM scraping (the field's internal `name`, data type, `pick_list` value pairs, etc.).

Implementation pattern:
1. **Wrap `XMLHttpRequest` / `fetch` for observation only**, with an interceptor that simply copies the response into a dictionary
2. Perform normal UI operations (open a step, pick a picklist value, etc.)
3. If the corresponding response has been captured, cross-reference it with the DOM extraction results to enrich them

Caveats:
- **Do not send new requests.** Mimicking the URL or body of a request via fetch, bypassing CSRF tokens, or spoofing headers are all NG.
- **Do not probe endpoints exhaustively as an investigative exercise.** Only observe requests that arise as a natural consequence of UI operations.
- When responses include the user's real data (emails, sheet names, column values, etc.), follow the **PII handling** rules — extract only the field structure and discard values.
- Do not document internal API URLs or body structures in detail in docs (they may change, and leaving dependent knowledge behind is harmful).

## Open issues

### UI observation
- [ ] Reliable detection of dynamic picklist selection → schema reload (criteria for deciding DOM changes have ended — loading indicator disappears / DOM stable for a fixed period)
- [ ] **Nesting depth detection** for the data tree — because `paddingLeft` is uniformly 0 and items render flat, a reliable way to associate array children with their parent (other than the toggle-state heuristic)
- [ ] DOM structure of the **Trigger picker screen** for connectors with multiple triggers (observation for cases where it is not skipped as it is in Gmail)
- [ ] Tracking virtual scroll (`cdk-virtual-scroll-viewport`) in connectors with many fields
- [ ] Confirm whether the Recipe data panel appears differently for saved vs unsaved recipes

### Official documentation
- [ ] Map the diff between what `/sync-connectors` can fetch and what UI observation can fetch (eliminate overlap, work out complementary usage)

### Turning it into a skill
- [ ] Implement the `/auto-learn` skill (combining official documentation with UI observation)
- [ ] Design that survives long-running execution (300+ connectors) (pause / resume, progress management)

## References

- Issue #27: automated knowledge collection — fetching field information via recipe push/pull plus browser automation
- Detailed prior validations live in the same issue's comment history
