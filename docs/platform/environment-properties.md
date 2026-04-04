# Environment Properties

公式: https://docs.workato.com/en/features/account-properties.html

## 概要

ワークスペース全体で使えるレシピの設定パラメータ（名前-値ペア）。環境変数や設定変数とも呼ばれる。複数レシピで共通の設定値を一元管理できる。

## 制限

| 項目 | 上限 |
|---|---|
| プロパティ数/環境 | 1,000 |
| プロパティ名 | 100 文字 |
| プロパティ値 | 1,024 文字 |

## 設定方法

Tools > Environment properties から名前-値ペアを作成。

## レシピでの使用

全レシピの **Properties** データツリーに自動表示される。レシピ実行時に動的に値を取得。

## 重要な動作

> **ジョブ実行中にプロパティ値の変更は反映されない。**
> 値はジョブ開始時にフリーズされる。動的な値の検出が必要な場合は Lookup Tables を使用。

## 用途例

- 通知先メールアドレスの一元管理
- 環境ごとの API エンドポイント URL
- フラグによる機能の有効/無効切り替え
- 外部サービスのテナント ID

## Platform CLI での管理

```bash
workato properties list
workato properties set <name> <value>
```
