
# study-gcp-terraform-elastic-search

GCP Terraform + Elastic Cloud の学習プロジェクト。

---

## 目的

- Cloud RunベースでElastic Cloud接続を構築する
- Terraformで全インフラをコード管理する
- Elastic Cloudでドキュメント投入・キーワード検索を行う

---

## 技術スタック

| カテゴリ | 技術 |
|---------|------|
| 検索 | Elastic Cloud（Elasticsearch 9.3.2 + Kibana） |
| GCP | Cloud Run (Job), Artifact Registry, Secret Manager |
| IaC | Terraform（ec ~> 0.12, google ~> 5.0） |
| CI/CD | GitHub Actions（Terraform plan/apply） |
| 言語 | Python 3.11 |

---

## アーキテクチャ

```text
[Cloud Run Job]
   ├── Secret Managerから接続情報取得（JSON: cloud_url/username/password）
   ├── ingestモード: クリーンアップ → src/data/*.json 投入 → データ残す
   └── searchモード: 既存インデックスにキーワード検索

[Elastic Cloud]
   ├── Elasticsearch（データ格納・検索）
   └── Kibana（管理UI）

[Terraform]
   ├── ec_deployment → Elastic Cloud自動構築 + 認証情報自動取得
   ├── Secret Manager → 接続情報をJSON自動格納
   ├── Artifact Registry → Dockerイメージ保管
   └── Cloud Run Job → コンテナ実行（GCP_PROJECT, ES_SECRET_NAME注入）
```

---

## ディレクトリ構成

```text
.
├── src/                 # アプリケーションコード
│   ├── main.py          # Cloud Run Job（投入・検索）
│   ├── data/            # 投入用JSONデータ
│   ├── Dockerfile
│   └── requirements.txt
├── terraform/           # IaC定義
│   ├── main.tf          # リソース定義
│   ├── providers.tf     # プロバイダ設定
│   ├── variables.tf     # 変数定義
│   └── outputs.tf       # 出力値
├── scripts/             # オペレーション用スクリプト
│   ├── config.py        # 共通設定
│   ├── docker_ops.py    # Docker操作
│   ├── gcp_ops.py       # GCP操作（ingest, search, logs）
│   └── tf_ops.py        # Terraform操作
├── docs/                # ドキュメント
├── .github/workflows/   # CI/CD（Terraform）
├── Makefile
├── .env                 # 設定値（git管理外）
└── CLAUDE.md
```

---

## 使い方

### 初回セットアップ

```bash
gcloud init
make gcp-setup     # API有効化・SA権限・Docker認証
make install       # pip install
```

### デプロイ・削除

```bash
make deploy-all    # 全構築（Elastic Cloud + Artifact Registry + push + Cloud Run Job）
make destroy-all   # 全削除（課金停止）
```

### データ投入・検索

```bash
make ingest                  # データ投入（クリーンアップ→投入→データ残す）
make search Q=Elasticsearch  # キーワード検索（投入済みデータ対象）
make search Q=Cloud          # 別キーワードで再検索
make logs                    # 最新executionのログ確認
```

### コマンド一覧

```bash
make help
```
