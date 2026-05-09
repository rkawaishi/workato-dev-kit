# workato-dev-kit （フレームワーク本体の開発）

このリポジトリは Workato 開発用のフレームワーク（スキル・ルール・ドキュメント・スクリプト）そのものを開発する場所。
**Workato レシピを書く場所ではない**。レシピ開発は、このリポジトリを `kit/` として submodule 追加した組織のワークスペースリポジトリで行う。

利用者向けのスキル（`/create-recipe` など）や Workato 向けのルールは [framework/claude/](../framework/claude/) に格納されており、
このルートの `.claude/` には **kit 自体を開発するための設定** だけを置く（混在を避けるため）。

## リポジトリ構造

```
workato-dev-kit/                  ← このリポジトリ
├── .claude/                      ← kit 開発用（このディレクトリ。Workato 用ルール/スキルは含まない）
│   ├── CLAUDE.md                 # 本ファイル
│   └── settings.json             # kit 開発時の最小許可設定
├── framework/                    ← 配布物（利用者リポジトリに symlink される対象）
│   └── claude/
│       ├── CLAUDE.md             # 利用者向けの Workato 開発ルール
│       ├── rules/                # Workato 開発用ルール（recipe フォーマット等）
│       ├── skills/               # Workato 開発用スキル（/create-recipe 等）
│       ├── hooks/                # Workato 用フック
│       └── settings.json         # 利用者の .claude/settings.json テンプレート
├── docs/                         # ナレッジベース（コネクタ情報、ロジック、プラットフォーム）
├── guides/                       # ライフサイクル等のガイド
├── connectors/                   # カスタムコネクタのドキュメント雛形（利用者は connector.rb をここに追加）
├── projects/                     # 利用者プロジェクトの patterns/ など
├── scripts/                      # ユーティリティ（sync-cursor-rules.sh, workato-api.py）
├── templates/                    # 利用者リポジトリ向けのテンプレ（gitignore 等）
├── setup.sh                      # 利用者リポジトリで実行され、symlink を張る
└── README.md
```

## 利用者ビュー

利用者リポジトリ（kit を submodule 追加した側）では `bash kit/setup.sh` を実行すると、以下の symlink が張られる：

| 利用者側のパス | symlink 先 |
|---|---|
| `.claude/rules/<file>.md` | `kit/framework/claude/rules/<file>.md` |
| `.claude/skills/<name>/` | `kit/framework/claude/skills/<name>/` |
| `.claude/hooks/<file>.sh` | `kit/framework/claude/hooks/<file>.sh` |
| `.claude/settings.json` | （初回コピー、hook パスを `kit/framework/claude/hooks/...` に展開） |
| `.claude/CLAUDE.md` | （初回コピー、`framework/claude/CLAUDE.md` の内容を取り込み） |

利用者はこれら symlink と同じディレクトリに **独自ファイルを追加できる**（setup.sh は既存の非 symlink ファイルを保持する）。

## 開発時のルール

### 配布物（framework/）の編集

- スキルを追加・修正する場合は `framework/claude/skills/<name>/SKILL.md` を編集する
- ルールを追加・修正する場合は `framework/claude/rules/<name>.md` を編集する
- 編集後、必ず **`bash scripts/sync-cursor-rules.sh`** を実行して `.cursor/` に反映する。コミットには両方を含めること
- スキル本文中の `@.claude/rules/...` のような参照は **利用者ビュー基準** で書く（`framework/claude/rules/...` ではない）

### setup.sh の変更

- 利用者リポジトリ側のディレクトリ構造（`.claude/`, `docs/`, `guides/`, `scripts/`, `templates/`）を変更する場合、利用者がフレームワーク更新時に `bash kit/setup.sh` を再実行する想定で **冪等性** を維持すること
- 既存の利用者リポジトリで動かすことを意識し、破壊的変更（既存 symlink の張り替え以外で利用者ファイルを消すような変更）を避ける

### ドキュメント（docs/）の編集

- `docs/connectors/<provider>.md` などは利用者が `@docs/...` で参照するナレッジベース。利用者ビューで `@docs/` のままで動くよう、リンク先を kit 内パスに書き換えない

### Cursor 配布

- `.cursor/` は現状 setup.sh で symlink されない。利用者が Cursor を使う場合は手動で `.cursor/` をコピーする運用（将来的に `framework/cursor/` への分離を検討）

## テスト

- `setup.sh` を変更したら、テスト用ディレクトリで実行して symlink が正しく張られることを確認する：
  ```
  rm -rf /tmp/kit-test && mkdir -p /tmp/kit-test && cd /tmp/kit-test
  ln -s "$(git -C <kit-repo> rev-parse --show-toplevel)" kit
  bash kit/setup.sh
  ls -la .claude/rules .claude/skills .claude/hooks
  ```
- `scripts/sync-cursor-rules.sh` を変更したら、リポジトリで実行して `.cursor/rules/*.mdc` と `.cursor/skills/*/SKILL.md` が再生成されることを確認する

## 注意

- このリポジトリでは `/create-recipe` などの Workato 用スキルは **利用しない** 想定。誤って起動しないよう、ルート `.claude/skills/` は空にしてある
- 個人ローカル設定は `.claude/settings.local.json`（git 管理外）で管理。許可リストの蓄積はそこに置く
