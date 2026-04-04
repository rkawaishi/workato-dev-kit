# Workbot

公式: https://docs.workato.com/en/workbot/overview.html

## 概要

Workato のチャットボットフレームワーク。Slack / Microsoft Teams / Facebook Workplace 上で動作し、ビジネスアプリケーションをチャットインターフェースに統合する。

## 対応プラットフォーム

| プラットフォーム | ドキュメント | provider |
|---|---|---|
| Slack | https://docs.workato.com/en/workbot/workbot.html | `slack_bot` |
| Microsoft Teams | https://docs.workato.com/en/workbot-for-teams/workbot.html | (要確認) |

## 主な機能

### モニタリング & 通知
ビジネスイベント（顧客チケット、フォーム送信、DevOps アラート等）をチャンネルに通知。ユーザー指定のフィルタによるスマート通知対応。

### データ操作
チャットからビジネスアプリのデータを取得・作成・更新。アプリを切り替えずに操作可能。

### リクエスト自動化
社内リソースのプロビジョニングワークフローをチャットから実行。

## 動作の仕組み

- Workbot をチャンネルに招待する必要がある
- チャンネルでは `@workbot` でメンション（DM では不要）
- チャンネル内の全員が Workbot コマンドを使用可能
- インストール時に Workato アカウントの最新アプリコネクションを自動検出

## レシピとの関係

Workbot のトリガー/アクションはレシピで使用する:
- **トリガー**: Slack/Teams のイベントやコマンドを検知
- **アクション**: メッセージ投稿、Block Kit 表示、ボタン操作

詳細なトリガー/アクション一覧:
- Slack: `@docs/connectors/workbot-for-slack.md`
- Teams: `@docs/connectors/workbot-for-teams.md`

## Custom OAuth Profile

標準コネクタにないイベント（`reaction_added` 等）や権限（`channels.history` 等）が必要な場合、Custom OAuth Profile を設定して追加の Slack/Teams スコープを取得する。

詳細: `@docs/learned-patterns.md` の「slack vs slack_bot」セクション参照

## 備考

- CN データセンターでは利用不可
- プリビルトレシピが用意されており、最小限のセットアップで利用可能
- Genie（AI エージェント）のチャットインターフェースとしても使用可能
