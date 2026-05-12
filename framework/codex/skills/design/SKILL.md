---
name: design
description: 【Deprecated】レガシー DESIGN.md の参照・更新と $design migrate での specs/ 移行のみ提供する。新規プロジェクトでは $spec を使うこと。
---

# $design — Deprecated

> ⚠️ **このスキルは deprecate されました。** 新規プロジェクトの設計は **`$spec` → `$clarify` → `$plan` → `$tasks` → `$analyze` → `$implement`** の仕様駆動ワークフローに完全移行しています。
>
> `$design` で残っている責務は次の 2 つのみ:
> - **`$design migrate <project>`** — 既存 `DESIGN.md` を `specs/<NNN>-<slug>/{spec,plan,tasks}.md` に分割移行（移行ツール）
> - **`$design` / `$design update`** — 既に DESIGN.md だけで運用している過渡期プロジェクト向けの **読み取り/更新の互換動作**（毎回 deprecation warning を表示）
>
> **`$design new` は削除されました。** 呼ばれた場合は実行を拒否し、`$spec` の利用を案内する。

## 使い方

- `$design <project-name>` — レガシー DESIGN.md を表示（warning 付き）
- `$design update` — レガシー DESIGN.md を実装状況に合わせて更新（warning 付き）
- `$design migrate <project-name>` — 既存 DESIGN.md を `specs/<NNN>-<slug>/{spec,plan,tasks}.md` に分割移行
- `$design new <project-name>` — **削除済み**。呼ばれた場合は拒否して `$spec` を案内

## 起動時の deprecation 案内

`$design migrate` 以外のサブコマンドが呼ばれたら、本処理の前に必ず次の警告を表示する:

```
⚠️ $design は deprecated です（spec-driven workflow に移行済み）。
   新規プロジェクト: $spec <project>
   既存 DESIGN.md の移行: $design migrate <project>

このまま続行する場合、レガシー DESIGN.md の参照/更新のみ行います。
```

`$design new` の場合だけは続行せず、次のメッセージを返して終了する:

```
❌ $design new は廃止されました。

新規プロジェクトの設計は $spec から始めてください:
  $spec <project-name>          # spec.md を作成 (要件 / WHAT・WHY)
  $clarify <project>/001-<slug> # Open Questions を消化
  $plan <project>/001-<slug>    # plan.md を作成 (Workato 構成)
  $tasks <project>/001-<slug>   # tasks.md にタスク分解
  $analyze <project>/001-<slug> # 整合性チェック
  $implement <project>/001-<slug> # 実装スキルへ振り分け

既存 DESIGN.md があるプロジェクトを spec-driven に乗せ換える場合:
  $design migrate <project-name>
```

`$design new` の旧ヒアリング・設計フローは本スキルから完全に削除されている。引き受けない。

## 設計書の場所（互換動作用）

`projects/<project-name>/DESIGN.md`

`.workatoignore` に `DESIGN.md` および `DESIGN.md.legacy.*` を含めて `workato pull` で消えないようにする。

## 操作

### `$design` / `$design <project-name>` — 参照（warning 付き）

1. 上記の deprecation 警告を表示
2. `projects/<project-name>/DESIGN.md` を読む
   - 存在しない場合は「DESIGN.md がありません。`$spec <project-name>` で仕様駆動ワークフローを開始してください」と案内して終了
3. 内容を表示
4. 未完了のチェックリスト項目があれば次のアクションを提案するが、**併せて `$design migrate <project-name>` で specs/ に移行することを推奨**

### `$design update` — 更新（warning 付き）

1. 上記の deprecation 警告を表示
2. 現在の DESIGN.md を読む
   - 存在しない場合は「DESIGN.md がありません。`$spec <project-name>` で仕様駆動ワークフローを開始してください」と案内して終了
3. プロジェクト内のファイルを確認し、実装済み項目を特定:
   - `*.recipe.json` があれば → レシピ項目をチェック
   - `*.lcap_page.json` があれば → ページ項目をチェック
   - `*.workato_db_table.json` があれば → Data Table 項目をチェック
   - `*.mcp_server.json` があれば → MCP 項目をチェック
   - `*.connection.json` があれば → コネクション項目をチェック
4. チェックリストを更新
5. Status と Last updated を更新
6. 新たな Decisions や Open Issues があれば追記
7. 変更内容をサマリー表示
8. 最後に「`$design migrate <project-name>` で specs/ に移行することを推奨」と案内

### `$design migrate <project-name>` — DESIGN.md → specs/ 移行

既存の `DESIGN.md` を仕様駆動ワークフローのアーティファクト (`spec.md` / `plan.md` / `tasks.md`) に **ベストエフォートで分割** する。完全に機械的にはマッピングできないため、不明瞭な点は `Open Questions` / `Open Issues` に書き出し、`$clarify` で続きを消化できる状態にする。

> このサブコマンドのみ deprecation warning は出さない（移行を促す本来の動線のため）。

#### 前提チェック

1. `projects/<project-name>/DESIGN.md` を読む。無ければ「DESIGN.md がありません。`$spec <project-name>` で新規作成してください」と案内して中断
2. `projects/<project-name>/specs/` が既に存在し中身がある場合は確認:
   ```
   既に specs/ 配下にアーティファクトがあります:
   - specs/001-foo/spec.md
   - specs/001-foo/plan.md
   
   どうしますか？
   1. 中断（手動マージ推奨）
   2. specs/002-migrated/ として並列で生成
   3. specs/001-foo/ を上書き（破壊的、非推奨）
   ```

#### 移行先の決定

- フィーチャースラグ: ユーザーに確認（デフォルト `main`、またはプロジェクト名から派生）
- 連番: **前提チェックの結果に従う**
  - `specs/` が存在しない or 空 → `001`
  - 既存 specs/ があり**並列生成（オプション 2）**を選択 → `specs/` 配下の最大連番 + 1（例: `001-foo/` があれば `002`）
  - 既存 specs/ があり**上書き（オプション 3）**を選択 → 上書き対象の既存連番をそのまま使用（例: `specs/001-foo/` を選んだなら `001`）
- 最終パス: `projects/<project-name>/specs/<NNN>-<slug>/{spec,plan,tasks}.md`（`<NNN>` は上で決まった連番）

#### セクション・マッピング

DESIGN.md の各セクションを以下の規則で振り分け:

| DESIGN.md セクション | 移行先 | 補足 |
|---|---|---|
| `# <タイトル>` | spec.md `# <タイトル>` + plan.md `# <タイトル> — Plan` + tasks.md `# <タイトル> — Tasks` | 共通タイトル |
| `## Status`, `Last updated` | 各アーティファクトの `## Metadata` | spec/plan/tasks 全てに引き継ぐ |
| `## User Experience` 配下のロール別ステップ | spec.md `## User Stories` | ほぼそのままコピー |
| `## Architecture` `### 適用パターン` | plan.md `## Applied Patterns` | パターン名と参照リンクを保持 |
| `## Architecture` `### 既存アセットの再利用` | plan.md `## Reused Assets` | アセット名と用途 |
| `## Architecture` `### 新規作成` `- **Data Table**:` | plan.md `## New Components` `### Data Tables` | フィールド一覧含む |
| `## Architecture` `### 新規作成` `- **ステージ**:` | plan.md `## Stage Transitions` | 遷移図化 |
| `## Architecture` `### 新規作成` `- **外部連携**:` | plan.md `## New Components` `### Connections` または spec.md `## External Touchpoints` | プロバイダー名のみは spec、技術詳細は plan |
| `## Architecture` `### 新規作成` `- **レシピ構成**:` | plan.md `## New Components` `### Recipes` | メイン/Function/ハンドラ別 |
| `## Implementation Checklist` | tasks.md `## Tasks` | 種類タグを推定して付与（下記） |
| `## Unlearned Actions` 表 | plan.md `## Unlearned Actions` 表 + tasks.md `[learn]` タスク化 | 両方に反映 |
| `## Decisions` | UX 系 → spec.md `## Decisions` / 技術系 → plan.md `## Decisions` | 文面から判断、迷ったら spec へ |
| `## Open Issues` | plan.md `## Open Issues` | デプロイ後確認系は plan へ |

#### Implementation Checklist の種類タグ推定

| Checklist 文言 | 推定タグ |
|---|---|
| 「Data Table スキーマ」「テーブル」 | `[data-table]` |
| 「ページ」「フォーム」「画面」 | `[page]` |
| 「レシピ」「Recipe Function」 | `[recipe]` / `[function]` |
| 「コネクション」「認証」 | `[connection]` |
| 「MCP」「Genie」「スキルレシピ」 | `[mcp]` |
| 「pull」「learn-recipe」 | `[pull]` / `[learn]` |
| 「テスト」「動作確認」「E2E」 | `[test]` |
| 「カスタムコネクタ」「connector.rb」 | `[connector]` |
| 上記いずれにも該当しない | `[manual]`（要手動確認のため `Open Issues` にも追記） |

依存関係はベストエフォートで推定（`[recipe]` は `[data-table]` `[connection]` の後、など）。確度が低い場合は注記に `(depends: ?)` と書き、`$analyze` で検出可能にする。

#### Open Questions / Open Issues の生成

機械的に判定できなかった項目は以下のいずれかに書き出す:

- spec.md `## Open Questions`:
  - User Stories の役割が不明瞭
  - Success Criteria が DESIGN.md に無い（要ヒアリング）
  - Out of Scope が明文化されていない（要確認）
- plan.md `## Open Issues`:
  - リソース未取得（Step 2 で取得すべき）
  - パターン適用の確信度が低い項目
  - ステージ遷移が不明瞭
- tasks.md には常に `[manual]` 化された不明瞭タスクが残る可能性あり

#### 移行後の処理

1. DESIGN.md を **`DESIGN.md.legacy.<YYYY-MM-DD>` にリネーム**（削除はしない、後から参照できるよう保存）
2. `.workatoignore` に `DESIGN.md.legacy.*` を追加（workato pull で消えないように）
3. 既存 `.workatoignore` に `specs/` が無ければ追記

#### 結果案内

```
✓ 移行完了: projects/<project-name>/

生成ファイル:
- specs/001-<slug>/spec.md         (<N> Open Questions あり)
- specs/001-<slug>/plan.md         (<M> Open Issues あり)
- specs/001-<slug>/tasks.md        (<T> タスク、うち <K> 件は [manual] で要確認)

リネーム:
- DESIGN.md → DESIGN.md.legacy.<YYYY-MM-DD>

次のアクション:
1. $clarify <project>/001-<slug> で Open Questions を消化
2. $analyze <project>/001-<slug> で整合性を確認
3. $implement <project>/001-<slug> で続きの実装に進む

レビュー推奨:
- spec.md の User Stories が DESIGN.md の意図を保っているか
- tasks.md の種類タグが妥当か（[manual] が多い場合は再分類が必要）
```

#### 移行時の禁則

- **DESIGN.md を削除しない**: リネームのみ。元データを失わない
- **specs/ を上書きしない**: 既に specs/ が存在する場合は明示的にユーザー確認を取る
- **不明確な技術用語を spec.md に持ち込まない**: DESIGN.md 内で Workato 用語（Recipe, Datapill, Workflow App 等）が User Experience に混ざっていたら、spec.md には業務語に意訳して書く（自信が無ければ Open Questions 化）

## Git 管理

レガシー DESIGN.md / `DESIGN.md.legacy.*` はワークスペースリポジトリの `projects/` で管理する。`$design update` 後または `$design migrate` 後はワークスペースリポジトリでコミット:

```bash
git add projects/<project-name>/DESIGN.md* projects/<project-name>/.workatoignore projects/<project-name>/specs/
git commit -m "Migrate legacy design: <project-name>"
git push origin
```
