---
description: Workato レシピ JSON を対話的に生成する。プロバイダー、トリガー、アクションを指定して .recipe.json と .connection.json を作成。
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, Agent
---

# /create-recipe

Workato レシピ JSON ファイルを対話的に生成するスキル。

## 手順

1. ユーザーに以下を確認:
   - **レシピの目的**: 何を自動化したいか
   - **トリガー**: どのアプリのどのイベントで起動するか（例: Gmail で新着メール受信）
   - **アクション**: トリガー後に何をするか（例: Google Drive にファイルをアップロード）
   - **条件**: フィルタ条件があるか
   - **格納先プロジェクト**: どのプロジェクトディレクトリに作成するか

2. コネクタのナレッジを確認:
   - `@docs/connectors/_index.md` で利用するコネクタを特定
   - `@docs/connectors/<connector>.md` を読み、利用可能なトリガー/アクションとフィールド情報を確認

3. フィールド情報の確認（重要）:
   - コネクタドキュメントに該当アクションの Input/Output fields セクションがあればそれを使用
   - **フィールド情報が未蓄積の場合**: 公式ドキュメントを WebFetch で取得
     - URL パターン: `https://docs.workato.com/en/connectors/<name>/<action-name>.html`
     - または: `https://docs.workato.com/en/connectors/<name>/actions.html`
   - 取得したフィールド情報は `docs/connectors/<connector>.md` に追記して蓄積する

4. JSON 構造のリファレンスを読む:
   - `@.claude/rules/workato-recipe-format.md`
   - ロジックステップが必要なら `@docs/logic/` の該当ファイル

5. 独自知見と既存パターンを参照:
   - `@docs/learned-patterns.md` で JSON 構造の独自知見を確認
   - 同じプロジェクト内の既存レシピがあれば参照

6. ファイルを生成:
   - `<project>/<snake_case_name>.recipe.json` — レシピ本体
   - `<project>/<prefix>_<provider>.connection.json` — 使用するコネクション（未存在の場合のみ）

## 生成ルール

- `number` はトリガーが 0、以降のステップは 1, 2, 3... と連番
- 各ステップに `uuid` (v4) を生成する
- `as` フィールドはステップの参照名。Genie ワークフロー以外では `name` と同じ値を使う
- Genie ワークフローの場合は `as` にランダムな8文字 hex を使う
- `config` 配列には使用する全プロバイダーのコネクション参照を含める
- `version` は新規作成時は 1
- `private` は true
- `concurrency` は 1（デフォルト）

## input フィールドの設定

各ステップの `input` にはコネクタドキュメントのフィールド情報を参照して正しいフィールド名を使う。
フィールド情報がドキュメントにない場合は、`input` を空 `{}` にして push し、UI で設定後に pull して学習する。

## datapill 生成

入力フィールドで他ステップの出力を参照する場合:
```
#{_dp('{"pill_type":"output","provider":"<provider>","line":"<as>","path":["<field>"]}')}
```

- `provider` と `line` は参照元ステップの値を使う
- `path` はフィールド名の配列（ネスト時は複数要素）
- **path の値はコネクタドキュメントの Output fields を参照して正確に指定する**

## 出力例

生成完了後、以下を表示:
- 生成したファイル一覧
- レシピの構造サマリー（トリガー → アクションのフロー）
- `workato push` で Workato にアップロードできることを案内
