# Workbot for Slack コネクタ

公式: https://docs.workato.com/en/workbot/workbot.html

## Triggers

| 名前 | 説明 |
|---|---|
| New command | カスタムWorkbotコマンドを設定し、指定されたコマンドを監視・実行する |
| New help message | DMまたはチャンネルメンションでヘルプをリクエストしたときに実行され、ヘルプ応答をカスタマイズできる |
| New event (real-time) | Slackワークスペースで指定されたイベントが発生したときにリアルタイムで実行する |
| New shortcut trigger | グローバルショートカットからワークフローを起動、またはSlackメッセージをタスク/チケットに変換する |
| New URL mention | Slack内の特定種類のURL（Salesforce、GitHub対応）を監視し、フォーマットされたデータをチャンネルに取得する |
| New dynamic menu event | ダイナミックメニューオプション内のフィールドにユーザーが入力したときに実行し、タイプアヘッド値を返す |

## Actions

| 名前 | 説明 |
|---|---|
| Post command reply | イベント完了時のWorkbot応答をカスタマイズする |
| Post message | スレッドサポートなど高度な機能付きで指定されたSlackチャンネルまたはDMにメッセージを送信する |
| Open/update or push modal view | ユーザーから情報を収集するリッチでインタラクティブなモーダルダイアログを構築する |
| Publish app home view | ブロックベースのコンテンツでカスタマイズされたアプリホームビューを公開する |
| Update blocks by block ID | ビュー全体を再作成せずにメッセージ、アプリホーム、モーダル内の特定ブロックを変更する |
| Return menu options | 動的にメニューオプションを生成し、Slackダイアログのダイナミックメニューに返す |
| Post notifications | オプションのフィルタリングパラメータ付きでSlackチャンネルにカスタマイズされた通知を投稿する |
| Download attachment | コマンドトリガー経由で受信したSlackの添付ファイルを取得し、さらなる処理に使用する |
| Delete message | 以前に投稿されたメッセージを削除する |
