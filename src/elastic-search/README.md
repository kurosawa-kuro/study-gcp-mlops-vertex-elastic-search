# Elasticsearch Hello World

Elastic Cloud への接続確認用スクリプト。疎通確認・ドキュメント投入・検索・クリーンアップを実行する。

## ファイル構成

```
src/elastic-search/
├── main.py            # メインスクリプト
├── requirements.txt   # 依存パッケージ
├── Dockerfile         # コンテナ実行用
├── Makefile           # タスクランナー
├── .env               # 認証情報（git管理外）
├── README.md
└── terraform/         # IaC定義
    ├── providers.tf       # プロバイダ設定 (elastic/ec, google)
    ├── variables.tf       # 変数定義
    ├── main.tf            # リソース定義
    ├── outputs.tf         # 出力値
    └── terraform.tfvars   # 変数の実値（git管理外）
```

## セットアップ

### 1. 環境変数の設定

`.env` ファイルを作成し、Elastic Cloud の認証情報を記載する。

```
ELASTIC_CLOUD_URL=https://<your-cloud-url>:443
ELASTIC_API_KEY=<your-api-key>
```

### 2. 依存パッケージのインストール

```bash
make install
```

## 実行

### ローカル実行

```bash
make run
```

### Docker 実行

```bash
make docker-run
```

## GCP デプロイ（Cloud Run Job）

### 初回セットアップ

```bash
make create-repo    # Artifact Registry リポジトリ作成
make auth-docker    # Docker 認証設定
```

### デプロイ（ビルド → push → Secret登録 → Job作成）

```bash
make deploy
```

### 実行・ログ確認

```bash
make execute        # Cloud Run Job 実行
make logs           # ログ確認
```

### クリーンアップ

```bash
make cleanup-gcp    # GCPリソース一括削除
```

### 全体フロー

```
[WSL]                    [GCP]
  │
  ├─ make push ────────► Artifact Registry
  │                           │
  ├─ make create-job ────────►│
  │                           ▼
  ├─ make execute ──────► Cloud Run Job
  │                           │
  │                           ▼
  │                      Elastic Cloud
  │                      (ES接続・検索)
  │                           │
  └─ make logs ◄──────────────┘
```

## Terraform（IaC）

手動構築した環境を Terraform で再現・管理する。

### リソース構成

| リソース | Terraform resource |
|---|---|
| Elastic Cloud デプロイメント | `ec_deployment` |
| Artifact Registry | `google_artifact_registry_repository` |
| Secret Manager | `google_secret_manager_secret` / `_version` |
| IAM (Secret アクセス権) | `google_secret_manager_secret_iam_member` |
| Cloud Run Job | `google_cloud_run_v2_job` |

### セットアップ

`terraform/terraform.tfvars` に実値を設定する。

```hcl
project_id            = "mlops-dev-a"
region                = "asia-northeast1"
elastic_cloud_api_key = "<Elastic Cloud Org APIキー>"
elastic_api_key       = "<ES接続用APIキー>"
```

### 実行

```bash
make tf-init       # プロバイダ初期化
make tf-plan       # 差分確認
make tf-apply      # 適用（全リソース作成）
make tf-destroy    # 全リソース削除（課金停止）
```

## コマンド一覧

```bash
make help
```

## 実行結果（例）

```
=== 1. info ===
cluster_name: e2ca746771d94d2781a841170364167c
version: 9.3.2

=== 2. index document ===
result: created
_id: ZO9VUZ0BlNtJQYqXNNHW

=== 3. search ===
total hits: 1
  -> {'message': 'hello world', 'tag': 'test'}

=== 4. cleanup ===
index deleted
```
