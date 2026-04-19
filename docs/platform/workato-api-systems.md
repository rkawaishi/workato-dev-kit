# Workato の API 系統（Developer API / API Platform / OEM）

Workato には **「API Client」という名前の似て非なる 3 系統 API** がある。さらに OEM / Embedded を合わせると 4 系統。

設計着手前にこのドキュメントを必ず読み、どの系統を使うのか最初に決めること。混同すると設計そのものをやり直す手戻りが発生する（`workato-key-broker` プロジェクト初期の失敗事例）。

## 判断フロー

```
Workato 自体を API で操作したい？（レシピ CRUD、接続管理、API クライアント発行 など）
  └─ YES → Developer API
  └─ NO  → 外部公開した API を呼ぶ認証が欲しい？（自社の API Platform でエンドポイント公開済み）
             └─ YES → API Platform Clients（v1=Access Profiles は廃止進行中、v2=API Keys が現役）
             └─ NO  → パートナーとして顧客の Workato テナントを管理したい？（SaaS 組み込み）
                        └─ YES → OEM / Embedded API
                        └─ NO  → ここに来たら質問が曖昧。用途を言語化し直す
```

## 比較表

| 項目 | Developer API | API Platform Clients (v1 / Access Profiles) | API Platform Clients (v2 / API Keys) | OEM / Embedded API |
|---|---|---|---|---|
| **目的** | Workato 自体を操作 | 外部公開 API の呼び出し側認証（旧方式） | 外部公開 API の呼び出し側認証（現行） | パートナーが顧客テナントを管理 |
| **典型的な主体** | CLI / MCP / Dev Kit / 内部自動化 | 外部システム（レガシー） | 外部システム（新規） | ISV / SaaS ベンダー |
| **エンドポイント基底** | `/api/*`（例: `/api/recipes`、`/api/developer_api_clients/*`） | `/api/api_clients/*`（※ 内部観測 / 廃止対象） | `/api/v2/api_clients/*`（※ 内部観測） | `/oem/oem-api/*`（例: `/oem/oem-api/adapters`） |
| **スコープ単位** | Project / Folder（role に project scope を付与） | Access Profile 単位（= 紐づく API Collection 群） | Client + API Key 単位（IP 制限・mTLS 付き） | 顧客テナント単位 |
| **認証ヘッダ** | `Authorization: Bearer <token>`<br>※ 旧 `x-user-token` / `x-user-email` は 2025-07-14 廃止済み | `api-token` ヘッダ | `api-token` ヘッダ | Admin Console / JWT |
| **現役度（2026-04 時点）** | 現役 | **廃止進行中**<br>・2025-12-01: 新規作成・変更不可<br>・2026-07-01: 完全廃止（トークン無効化） | 現役（推奨） | 現役 |
| **UI 管理画面** | Workspace admin > API clients | API platform > Clients（Access Profiles タブ） | API platform > Clients（API Keys タブ） | Admin Console |
| **公式 docs** | [workato-api.html](https://docs.workato.com/en/workato-api.html) / [api-clients.html](https://docs.workato.com/workato-api/api-clients.html) | [api-client-mgmt.html](https://docs.workato.com/en/api-mgmt/api-client-mgmt.html) | 同上（API Keys セクション） | [oem.html](https://docs.workato.com/en/oem.html) / [oem-api.html](https://docs.workato.com/en/oem/oem-api.html) |

> **Note on "v1 / v2" 命名**
> 公式 docs では v1 / v2 とは呼ばず、「Access Profiles（legacy）」「API Keys（modern）」と呼ぶ。本ドキュメントの v1 / v2 は Developer API 経由で API Platform クライアントを操作する際の実観測パス（`/api/api_clients/*` vs `/api/v2/api_clients/*`）を指す便宜上のラベル。

## 系統ごとの詳細

### 1. Developer API

**一言で言うと**: 「Workato を Workato の外から操作する」ための API。

- CLI (`workato` コマンド)、MCP サーバ、ローカル Dev Kit の裏側で使われているのはこれ
- API Client を発行する場所: **Workspace admin > API clients**
- Role に Project scope を付けることで、その API Client が触れるプロジェクトを絞れる
- 旧認証 (`x-user-token` + `x-user-email`) は 2025-07-14 に廃止済み。今から書くコードは必ず `Authorization: Bearer` で組む

典型的なユースケース:
- `workato push` / `workato pull` を CI から叩く
- MCP から `/api/recipes` を叩いてレシピ一覧を取る
- 監査用にジョブ履歴を `/api/jobs` からエクスポート

### 2. API Platform Clients (v1 / Access Profiles) — 廃止進行中

**一言で言うと**: 「自分が Workato で公開した API を外部システムに呼ばせる」ための **旧方式** 認証。

- 概念: **Client** → **Access Profile** → **API Collections** の 3 層
- Access Profile 単位で「どの Collection を呼べるか」を決め、そこに API Token を紐づける
- 外部システムは `api-token` ヘッダで呼び出す
- Access Policy で rate limit / quota を Access Profile 単位で設定

廃止スケジュール:
- **2025-12-01**: 既存 Access Profile の変更・新規作成が不可（※ 2026-04-19 現在、すでに過ぎている）
- **2026-07-01**: 完全廃止。発行済み API Token が無効化される

既存システムは 2026-07-01 までに v2 (API Keys) へ移行する必要がある。

### 3. API Platform Clients (v2 / API Keys) — 現役

**一言で言うと**: v1 の後継。Access Profile を介さず、Client に直接 API Key を 1〜20 個ぶら下げる方式。

主な違い（v1 比）:
- **API Key が第一級リソース**: Client ごとに最大 20 本、個別にローテーション可能
- **IP 制限**: Key ごとに allow/block list
- **mTLS**: カスタムドメインで相互 TLS 必須化が可能
- **Auth 方式の拡張**: Auth Token / OAuth 2.0 / JWT / OpenID Connect
- **Portal**: クライアントが自分で Key を管理するセルフサービス Portal を提供可能

新規構築はすべてこちらで行う。

### 4. OEM / Embedded API

**一言で言うと**: ISV / SaaS ベンダーが、自社プロダクトに Workato を組み込んで「エンドカスタマーの Workato テナントを管理する」ための API。

- Multi-tenant な Admin Console を提供する構造
- エンドカスタマーは iframe + JWT 認証で partner プロダクト内から操作
- Developer API とは別世界。顧客テナントの recipe / connection / adapter を partner 側が作れる
- 典型的な主体: Workato Embedded を契約した ISV

一般的なレシピ開発では使わない。プラットフォーム製品を作る場合のみ検討対象。

## 設計時のチェックリスト

新しい連携の設計に着手する前に、以下を明言してから進める:

- [ ] どの系統か（Developer API / API Platform v1 / v2 / OEM）
- [ ] 呼ぶ側は誰か（内部の CLI/MCP / 外部システム / パートナープロダクト）
- [ ] スコープ単位は何か（Project / Folder / Access Profile / Client+Key / テナント）
- [ ] 認証ヘッダは何か（`Authorization: Bearer` / `api-token` / JWT）
- [ ] v1 Access Profile を新規に使おうとしていないか（廃止済み）

## 参考

- Developer API: https://docs.workato.com/en/workato-api.html
- Developer API Clients 管理: https://docs.workato.com/workato-api/api-clients.html
- 旧認証からの移行 FAQ: https://docs.workato.com/workato-api/moving-to-api-client-authentication-faq.html
- API Platform 概要: https://docs.workato.com/en/api-management.html
- API Platform Client 管理（Access Profiles / API Keys）: https://docs.workato.com/en/api-mgmt/api-client-mgmt.html
- OEM / Embedded: https://docs.workato.com/en/oem.html
- OEM API: https://docs.workato.com/en/oem/oem-api.html
