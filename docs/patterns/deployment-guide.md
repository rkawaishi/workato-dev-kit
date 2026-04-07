# デプロイガイド

Workato Platform CLI を使用したレシピ/プロジェクトのデプロイに関する知見。

## インポート/エクスポート挙動

> 以下は実際の push/pull 運用から得た知見である。

- push 時に datapill を含む input を設定しても、UI でコネクタ未設定だと **空 `{}` にリセット**される
- `version` は UI で編集するたびに自動インクリメント
- コネクション名が微妙に変わることがある（例: `helpdesk_ai` → `helpdesk_ai_by_workato`）
- 別プロジェクトのコネクションを参照する場合、`account_id.folder` にプロジェクト名が入る
- `pull` で削除確認が入る場合がある（`echo "y" | workato pull` で自動承認）

### push 後の JSON 変換

push した JSON は Workato 側で変換される:
- `extended_output_schema` が展開される
- `dynamicPickListSelection` が追加される
- `version` がインクリメントされる

pull すると push 時と異なるファイルが返ってくるのは正常動作。

### 対策

- push 前にコネクションを UI で設定しておく
- push → pull → diff で変更点を確認するサイクルを推奨
- コネクション名の変更は `pull` 後に確認する
