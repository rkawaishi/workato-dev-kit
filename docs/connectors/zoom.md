# Zoom コネクタ

公式: https://docs.workato.com/en/connectors/zoom.html

## Triggers

| 名前 | 説明 |
|---|---|
| Meeting alerts | ミーティングで接続不良や不安定なビデオなどのアラートが発生したときにトリガーされる |
| Meeting started | ミーティングが開始されたときにトリガーされる |
| Meeting ended | ミーティングが終了したときにトリガーされる |
| Meeting created | 新しいミーティングが作成されたときにトリガーされる |
| Meeting updated | ミーティングの詳細が変更されたときにトリガーされる |
| Meeting deleted | ミーティングが削除されたときにトリガーされる |
| Meeting registration created | 参加者が登録したときにトリガーされる |
| Meeting registration approved | 登録が承認されたときにトリガーされる |
| Meeting registration cancelled | 参加者が登録をキャンセルしたときにトリガーされる |
| Meeting sharing started | 画面共有が開始されたときにトリガーされる |
| Meeting sharing ended | 画面共有が停止されたときにトリガーされる |
| Host/Participant joined meeting | 出席者がミーティングに参加したときにトリガーされる |
| Host/Participant left meeting | 出席者がミーティングを退出したときにトリガーされる |
| Participant waiting for host | 参加者が待機室にいるときにトリガーされる |
| Participant joined before host | 参加者がホストより先に参加したときにトリガーされる |
| Webinar alerts | ウェビナーでアラートが発生したときにトリガーされる |
| Webinar started | ウェビナーが開始されたときにトリガーされる |
| Webinar ended | ウェビナーが終了したときにトリガーされる |
| Webinar created | ウェビナーが作成されたときにトリガーされる |
| Webinar updated | ウェビナーが更新されたときにトリガーされる |
| Webinar sharing started | ウェビナーで画面共有が開始されたときにトリガーされる |
| Webinar sharing ended | ウェビナーで画面共有が停止されたときにトリガーされる |
| Webinar registration created | ウェビナー登録が作成されたときにトリガーされる |
| Webinar registration approved | ウェビナー登録が承認されたときにトリガーされる |
| Webinar registration cancelled | ウェビナー登録がキャンセルされたときにトリガーされる |
| Webinar registration denied | ウェビナー登録が拒否されたときにトリガーされる |
| Host/Participant joined webinar | ウェビナーに出席者が参加したときにトリガーされる |
| Host/Participant left webinar | ウェビナーから出席者が退出したときにトリガーされる |
| Recording started | クラウド録画が開始されたときにトリガーされる |
| Recording paused | クラウド録画が一時停止されたときにトリガーされる |
| Recording resumed | クラウド録画が再開されたときにトリガーされる |
| Recording stopped | クラウド録画が停止されたときにトリガーされる |
| Recording completed | クラウド録画が完了したときにトリガーされる |
| Recording renamed | クラウド録画が名前変更されたときにトリガーされる |
| Recording trashed | クラウド録画がゴミ箱に移動されたときにトリガーされる |
| Recording deleted | クラウド録画が削除されたときにトリガーされる |
| Recording recovered | クラウド録画が復元されたときにトリガーされる |
| Transcript completed | 録画の文字起こしが完了したときにトリガーされる |
| Transcript registration created | 文字起こし登録が作成されたときにトリガーされる |
| Transcript registration approved | 文字起こし登録が承認されたときにトリガーされる |
| Transcript registration denied | 文字起こし登録が拒否されたときにトリガーされる |
| User created | ユーザーが作成されたときにトリガーされる |
| User updated | ユーザーが更新されたときにトリガーされる |
| User invitation accepted | ユーザーが招待を承認したときにトリガーされる |
| User settings updated | ユーザー設定が更新されたときにトリガーされる |
| User deactivated | ユーザーが無効化されたときにトリガーされる |
| User activated | ユーザーが有効化されたときにトリガーされる |
| User disassociated | ユーザーの関連付けが解除されたときにトリガーされる |
| User deleted | ユーザーが削除されたときにトリガーされる |
| User presence status updated | ユーザーのプレゼンスステータスが更新されたときにトリガーされる |
| User personal notes updated | ユーザーの個人メモが更新されたときにトリガーされる |
| User signed in | ユーザーがサインインしたときにトリガーされる |
| User signed out | ユーザーがサインアウトしたときにトリガーされる |

## Actions

| 名前 | 説明 |
|---|---|
| Schedule meeting/webinar | トリガーに基づいてミーティングやウェビナーをスケジュールする |
| Update event details | ミーティング、ウェビナー、クラウド録画の設定（時間、投票、登録質問等）を変更する |
| Search event details | ミーティング、ウェビナー、クラウド録画の詳細を検索する |
| Get event details | ミーティング、ウェビナー、登録者、参加者、録画設定の包括的な情報を取得する |
| Retrieve webinar results | ウェビナーやミーティング参加者の回答を取得し、他のアプリケーションに送信する |
| Add registrants | ウェビナー、ミーティング、クラウド録画に登録者を追加する |
| Get registrants | ウェビナー、ミーティング、クラウド録画から登録者リストを取得する |
| Update registrant status | ミーティング、ウェビナー、クラウド録画の登録を承認、拒否、キャンセルする（最大30件） |
| Create user | Zoom組織で新しい従業員のZoomアカウントを自動プロビジョニングする |
| Update user | Zoom組織内のユーザー詳細、パスワード、プロフィール画像を変更する |
| Search users | Zoom組織内のユーザーを検索し、詳細を取得する |
| Get user | IDで特定のユーザー情報を取得する |
| Delete user | Zoom組織からユーザーを完全に削除またはSSOトークンを取り消す |
| Download cloud recording | Zoomからクラウド録画を直接ダウンロードし、下流のアプリケーションに送信する |
