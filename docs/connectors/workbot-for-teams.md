# Workbot for Microsoft Teams コネクタ

公式: https://docs.workato.com/en/workbot-for-teams/workbot.html

## Triggers

| 名前 | 説明 |
|---|---|
| New command | Microsoft Teamsからレシピをトリガーし、接続されたアプリでアクションを実行する |
| New help message | ヘルプメッセージが送信されたときに実行され、デフォルトのヘルプ応答をカスタマイズできる |
| Tab opened | エンタープライズWorkbotインスタンスでユーザーがタブを開いたときに起動する |
| New message | アクティブなコマンドトリガーに一致しないダイレクトメッセージやチャンネルメンションに対してカスタム応答する |

## Actions

| 名前 | 説明 |
|---|---|
| Post reply | Workbotコマンド呼び出し時にユーザーへリッチメッセージング要素付きの返信を投稿する |
| Post simple reply | Markdown形式対応のテキストでTeamsユーザーまたはグループチャットに返信する |
| Post message | 動的にメッセージ受信者を指定してユーザーまたはチャンネルにメッセージを投稿する |
| Post simple message | リッチフォーマットなしのテキストベースメッセージをTeamsユーザーまたはチャンネルに投稿する |
| Delete message | 会話IDとメッセージIDを使用して以前に投稿されたメッセージを削除する |
| Get user info by User Principal Name | 表示名、メール、電話、役職などのユーザー詳細を取得する |
| Show tab using Adaptive Cards | タブオープントリガーイベントに応答してタブインターフェースを表示する |
| Custom action | Microsoft Graph API (v1.0)を使用した標準アクション以外の高度なカスタマイズ |
