# Security Policy

## Supported Versions

workato-dev-kit はまだ正式なバージョンタグを切っていません。
セキュリティ修正は **`main` ブランチの最新コミット** に対してのみ適用されます。
利用者は `git submodule update --remote kit` で最新を取り込んでください。

| Version | Supported |
|---|---|
| `main` (latest) | ✅ |
| それ以前のコミット | ❌ |

## 脆弱性の報告 / Reporting a Vulnerability

セキュリティ脆弱性を発見した場合は、**公開イシューを立てずに**以下の方法で報告してください。

### 推奨: GitHub Security Advisories

1. リポジトリの [Security タブ](https://github.com/rkawaishi/workato-dev-kit/security/advisories/new) を開く
2. 「Report a vulnerability」を選択
3. 詳細を記入

GitHub の Private Vulnerability Reporting 機能でメンテナーと安全に連絡できます。

### フォールバック: メール

GitHub Security Advisories が利用できない場合は、以下に直接メールしてください。

- **Email**: kantannano@gmail.com
- **件名プレフィックス**: `[SECURITY] workato-dev-kit:` を付けてください

## 報告に含めると助かる情報

- 影響を受けるファイル/コンポーネント（例: `setup.sh`, `scripts/sync_agents.py`, 特定のスキル）
- 再現手順（最小限の PoC）
- 想定される影響範囲（情報漏洩 / 任意コード実行 / 権限昇格 など）
- 報告者のクレジット表記の希望（不要な場合はその旨）

## 対応プロセス

メンテナーは可能な限り迅速に対応しますが、本プロジェクトはボランティアベースで運営されているため、対応時期について保証はできません。目安として:

| ステップ | 目標時間 |
|---|---|
| 受領確認 | 7 日以内 |
| 影響評価 | 14 日以内 |
| 修正リリース | 重大度に応じて調整 |

## スコープ

このリポジトリのコードベースに含まれる脆弱性が対象です。

**スコープ外**:

- Workato プラットフォーム本体の脆弱性（[Workato 公式](https://www.workato.com/legal/security) に報告してください）
- 利用者リポジトリの設定不備（`.workatoenv` の漏洩など、利用者責任の領域）
- Workato Platform CLI 本体の脆弱性（[workato-platform-cli](https://github.com/workato-devs/workato-platform-cli) に報告してください）
- 依存している外部サービス（Claude Code, Cursor, Codex CLI, Gemini CLI など）の脆弱性

## 開示ポリシー

- 修正リリース完了後、GitHub Security Advisories を通じて公開
- 報告者の協力に対し、希望に応じてクレジットを記載
- CVE 番号の取得は重大度に応じて検討
