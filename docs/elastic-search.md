# Elastic Cloud + GCP Cloud Run Job 技術ガイド

---

## 1. 概要

Elastic Cloud (Elasticsearch + Kibana) にPythonから接続し、Cloud Run Jobとして実行する構成。
Terraformで全インフラをIaC管理し、ES接続情報はSecret Managerに自動格納する。

```
[ローカル]                [GCP]                         [Elastic Cloud]
  │                        │                               │
  ├─ make deploy-all       │                               │
  │   ├─ tf-apply-infra ──►├─ Artifact Registry            │
  │   │                    ├─ Secret Manager          ┌────┤
  │   │                    │                          │ ec_deployment
  │   │                    │                          │ (ES + Kibana)
  │   ├─ push ────────────►├─ Docker image            │
  │   └─ tf-apply ────────►├─ Cloud Run Job ─────────►│
  │                        │                          │
  ├─ make ingest ─────────►├─ Job実行(投入) ─────────►│ データ投入
  ├─ make search Q=... ───►├─ Job実行(検索) ─────────►│ キーワード検索
  └─ make logs ◄───────────┘                          └────┘
```

---

## 2. アプリケーション

### 動作モード

| モード | トリガー | 動作 |
|--------|---------|------|
| ingest | `SEARCH_KEYWORD` 未設定 | クリーンアップ → data/*.json投入 → 確認検索 → **データ残す** |
| search | `SEARCH_KEYWORD` 設定済 | 既存インデックスに対して `multi_match` 検索 |

### src/main.py

```python
def get_es_client() -> Elasticsearch:
    """Secret Managerから接続情報を取得してElasticsearchクライアントを生成する。"""
    project = os.environ["GCP_PROJECT"]
    secret_name = os.environ["ES_SECRET_NAME"]
    client = secretmanager.SecretManagerServiceClient()
    name = f"projects/{project}/secrets/{secret_name}/versions/latest"
    response = client.access_secret_version(name=name)
    secret = json.loads(response.payload.data.decode())
    return Elasticsearch(
        secret["cloud_url"],
        basic_auth=(secret["username"], secret["password"]),
    )

def ingest(es):
    # 1. cleanup（既存インデックスがあれば削除）
    # 2. info（疎通確認）
    # 3. data/*.json を読み込み投入
    # 4. match_all で確認検索
    # → データを残す（searchモードで利用するため）

def search(es, keyword):
    # 既存インデックスに対して multi_match 検索
    # インデックスが存在しなければエラー（make ingest を先に実行）
```

### src/data/

投入用JSONファイルを格納する。配列形式・単体オブジェクトどちらにも対応。

```json
[
  {"title": "Elasticsearch入門", "content": "Elasticsearchは分散型の検索・分析エンジンです。", "tag": "search"},
  {"title": "Terraform入門", "content": "Terraformはインフラをコードとして管理するIaCツールです。", "tag": "infra"},
  {"title": "Cloud Run概要", "content": "Cloud RunはGCPのサーバーレスコンテナ実行環境です。", "tag": "gcp"}
]
```

### src/Dockerfile

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY main.py .
COPY data/ data/
CMD ["python", "main.py"]
```

### src/requirements.txt

```
elasticsearch==8.13.0
google-cloud-secret-manager==2.22.0
```

---

## 3. Terraform

### APIキー管理の設計

```
ec_deploymentから自動取得 → JSON形式でSecret Managerに格納

Secret Manager格納内容:
{
  "cloud_url":  "https://xxx.asia-northeast1.gcp.cloud.es.io:443",
  "username":   "elastic",
  "password":   "auto-generated-password"
}

Cloud Run Jobには GCP_PROJECT と ES_SECRET_NAME だけ渡し、
Python側でSecret Managerクライアントから読み取る。
→ 手動APIキー管理が不要、Terraform完結。
```

### リソース構成

| Terraform resource | 名前 | 用途 |
|---|---|---|
| `ec_deployment` | hello-elastic | Elastic Cloud（ES + Kibana） |
| `google_artifact_registry_repository` | hello-elastic-repo | Dockerイメージ保管 |
| `google_secret_manager_secret` + `_version` | hello-elastic-api-key | ES接続情報JSON |
| `google_secret_manager_secret_iam_member` | — | Cloud Run → Secret読み取り |
| `google_cloud_run_v2_job` | hello-elastic-job | コンテナ実行 |

### Elastic Cloud Org APIキーの発行（provider用）

```
https://cloud.elastic.co/
  → 左メニュー: Organization
  → API keys
  → Create API key (Org level)
```

> ES接続用の認証情報は手動発行不要。Terraformが`ec_deployment`作成時に自動生成する
> `username`/`password`をSecret Managerに格納する。
> Org APIキーはTerraform providerの認証にのみ使用。

---

## 4. トラブルシューティング

### Artifact Registry push失敗

```bash
make gcp-setup-docker

# 権限不足の場合
gcloud projects add-iam-policy-binding ${PROJECT_ID} \
  --member="user:$(gcloud config get-value account)" \
  --role="roles/artifactregistry.writer"
```

### Secret Manager アクセスエラー

```bash
make tf-apply
```

### Cloud Run APIs が未有効

```bash
make gcp-setup-apis
```
