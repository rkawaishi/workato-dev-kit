# Contributing to workato-dev-kit

workato-dev-kit へのコントリビューションをご検討いただきありがとうございます。
このドキュメントは、開発・PR 提出・新スキル追加の流れをまとめたものです。
英語話者の方は GitHub Issues で英語で起票していただいて構いません（メンテナーは日本語/英語両対応します）。

---

## 開発のセットアップ

このリポジトリは **kit 単体でも開発可能**です（利用者ワークスペースのように `submodule` として追加する必要はありません）。

```bash
git clone https://github.com/rkawaishi/workato-dev-kit.git
cd workato-dev-kit
```

開発に必要なのは:

- `bash` (macOS の zsh 環境でも `bash` が必要)
- `python3` (3.8+ — 標準ライブラリのみ使用)
- `git`

Workato CLI 本体は kit 自体の開発には不要です（利用者ワークスペース側で必要）。

詳しいリポジトリ構造とディレクトリの役割は [.claude/CLAUDE.md](.claude/CLAUDE.md) を参照してください。

---

## 配布物 (`framework/`) の編集ルール

**正本は `framework/claude/`** です。スキル・ルール・hooks はここを編集します。

```
framework/
├── claude/        ← canonical source（編集対象）
├── cursor/        ← scripts/sync_agents.py で生成（直接編集禁止）
├── codex/         ← 同上
├── gemini/        ← 同上
└── AGENTS.md      ← 同上
```

> **重要**: `framework/claude/` を編集したら、必ず `python3 scripts/sync_agents.py` を実行して
> Cursor / Codex / Gemini / AGENTS.md を再生成してください。
> CI ([sync-check workflow](.github/workflows/sync-check.yml)) がドリフトを自動検出し、PR を block します。

Cursor 専用の手書きファイル（sync 対象外）:

- `framework/cursor/rules/workato-project.mdc` — `alwaysApply: true` のプロジェクト全体ルール
- `framework/cursor/hooks.json` — Cursor の hook 設定

これら以外の Cursor ファイルは sync が上書きするため直接編集しないでください。

---

## ブランチ命名規則

`<type>/<slug>` の形式を使ってください。`<type>` は Conventional Commits に揃えます:

| Type | 用途 |
|---|---|
| `fix/` | バグ修正 |
| `feat/` | 新機能 |
| `docs/` | ドキュメントのみの変更 |
| `chore/` | ビルド・補助ツール・雑務 |
| `refactor/` | 機能変更を伴わないリファクタ |
| `ci/` | CI 設定変更 |
| `test/` | テスト追加・修正 |

例: `fix/setup-python-shell-escape`, `docs/governance-files`, `feat/add-pull-recipe-skill`

---

## コミットメッセージ

[Conventional Commits](https://www.conventionalcommits.org/ja/v1.0.0/) に従ってください。

```
<type>(<scope>): <subject>

<body — 何故その変更が必要か>

Closes #<issue-number>
```

例:

```
fix(setup): pass paths to python via env to avoid shell-escape breakage

setup.sh の python3 -c がシェル変数を直接展開していたため、
パスにクォートが含まれると Python コードが破綻していた。
ヒアドキュメント + os.environ パターンに切り替えて隔離。

Closes #92
```

---

## Pull Request の流れ

1. **Issue を確認/作成**: 既存 issue がない場合は先に立ててください（小さな typo 修正は除く）
2. **ブランチ作成**: `git checkout -b <type>/<slug>`
3. **実装 + ローカル検証**:
   - `framework/claude/` を編集したら `python3 scripts/sync_agents.py` 実行
   - テストがある領域は `python3 -m unittest scripts/tests/test_*.py` で実行
4. **コミット**: Conventional Commits 準拠
5. **Push + PR 作成**: `gh pr create --base main` または GitHub Web UI
6. **CI チェック確認**: `sync-check` workflow が green になること
7. **レビュー対応**: マージは原則メンテナーが行います

PR 本文には「Summary」「Test plan」「Closes #N」を含めてください。

---

## テスト

現状のテスト:

```bash
python3 -m unittest scripts/tests/test_sdk_push_frontmatter.py
```

新しい機能を追加したら、可能な範囲でテストも追加してください。
特に [scripts/sync_agents.py](scripts/sync_agents.py) のリライト規則周りはテストカバレッジ拡充を歓迎します（[#101](https://github.com/rkawaishi/workato-dev-kit/issues/101) 参照）。

---

## 新規スキル追加時のチェックリスト

`framework/claude/skills/<new-skill>/SKILL.md` を追加する際:

- [ ] frontmatter の `description` が「いつこのスキルを起動すべきか」を機械可読な形で書かれているか
- [ ] `allowed-tools` に必要なツールを全て宣言したか（Chrome MCP 等の外部ツールも含む）
- [ ] スキル本文中の `@.claude/...` 参照が利用者ビュー（symlink 後の相対パス）になっているか
- [ ] スキル間で重複している責務がないか
- [ ] `python3 scripts/sync_agents.py` を実行し、`framework/{cursor,codex,gemini}/skills/<new-skill>/` が生成されたか
- [ ] `framework/AGENTS.md` への影響を確認したか（必要に応じて）
- [ ] [docs/skills-reference.md](guides/skills-reference.md) と README のスキル一覧表に追記したか

---

## ドキュメント (`docs/`) の編集ルール

`docs/` 配下のナレッジベース（コネクタ情報・ロジック・プラットフォーム機能）は、
利用者が `@docs/<path>` で参照することを前提に書かれています。
リンク先を kit 内部パスに書き換えないでください。

組織独自の補正・追記は利用者リポジトリ側の `org/docs/` に置く設計のため、
kit の `docs/` には Workato 公式ドキュメント由来の汎用情報のみを記載してください。

---

## バグ報告 / 機能要望

[GitHub Issues](https://github.com/rkawaishi/workato-dev-kit/issues) からどうぞ。
（イシューテンプレートは [#95](https://github.com/rkawaishi/workato-dev-kit/issues/95) で整備中です）

セキュリティ脆弱性については [SECURITY.md](SECURITY.md) を参照してください。

---

## 行動規範

このプロジェクトは [Contributor Covenant Code of Conduct](CODE_OF_CONDUCT.md) を採用しています。
コントリビュートする際は遵守をお願いします。

---

## ライセンス

このリポジトリへのコントリビューションは [MIT License](LICENSE) の元で公開されることに同意したものとみなされます。
