include .env
export

# .envから派生する変数（重複定義を避ける）
export GCP_PROJECT    := $(PROJECT_ID)
export ES_SECRET_NAME := $(SECRET_NAME)

# Terraform用環境変数（TF_VAR_で自動認識）
export TF_VAR_project_id            := $(PROJECT_ID)
export TF_VAR_region                := $(REGION)
export TF_VAR_deployment_name       := $(DEPLOYMENT_NAME)
export TF_VAR_job_name              := $(JOB_NAME)
export TF_VAR_repo_name             := $(REPO_NAME)
export TF_VAR_secret_name           := $(SECRET_NAME)
export TF_VAR_elastic_cloud_api_key := $(ELASTIC_CLOUD_API_KEY)

SCRIPTS := PYTHONPATH=scripts python3
TF_SA   := terraform@$(PROJECT_ID).iam.gserviceaccount.com

.PHONY: run install build push docker-run clean \
        ingest search logs \
        deploy-all destroy-all \
        tf-init tf-plan tf-apply tf-apply-infra tf-import tf-destroy \
        gcp-setup gcp-setup-apis gcp-setup-sa gcp-setup-docker help

# ===== ローカル =====

run:
	python3 src/main.py

install:
	pip install -r src/requirements.txt

build:
	$(SCRIPTS) scripts/docker_ops.py build

push:
	$(SCRIPTS) scripts/docker_ops.py push

docker-run:
	$(SCRIPTS) scripts/docker_ops.py docker-run

clean:
	$(SCRIPTS) scripts/docker_ops.py clean

# ===== GCP操作 =====

ingest:
	$(SCRIPTS) scripts/gcp_ops.py ingest

search:
	SEARCH_KEYWORD="$(Q)" $(SCRIPTS) scripts/gcp_ops.py search

logs:
	$(SCRIPTS) scripts/gcp_ops.py logs

# ===== GCPセットアップ（初回のみ） =====

gcp-setup-apis:
	gcloud services enable \
	  artifactregistry.googleapis.com \
	  run.googleapis.com \
	  compute.googleapis.com \
	  iam.googleapis.com \
	  cloudresourcemanager.googleapis.com \
	  secretmanager.googleapis.com \
	  --project=$(PROJECT_ID)

gcp-setup-sa:
	gcloud projects add-iam-policy-binding $(PROJECT_ID) \
	  --member="serviceAccount:$(TF_SA)" \
	  --role="roles/editor" --quiet
	gcloud projects add-iam-policy-binding $(PROJECT_ID) \
	  --member="serviceAccount:$(TF_SA)" \
	  --role="roles/run.admin" --quiet

gcp-setup-docker:
	gcloud auth configure-docker $(REGION)-docker.pkg.dev

gcp-setup: gcp-setup-apis gcp-setup-sa gcp-setup-docker

# ===== デプロイ =====

deploy-all:
	$(MAKE) tf-apply-infra
	$(MAKE) push
	$(MAKE) tf-apply

destroy-all:
	$(MAKE) tf-destroy
	$(MAKE) clean

# ===== Terraform =====

tf-init:
	$(SCRIPTS) scripts/tf_ops.py init

tf-plan:
	$(SCRIPTS) scripts/tf_ops.py plan

tf-apply:
	$(SCRIPTS) scripts/tf_ops.py apply

tf-apply-infra:
	$(SCRIPTS) scripts/tf_ops.py apply-infra

tf-import:
	$(SCRIPTS) scripts/tf_ops.py import

tf-destroy:
	$(SCRIPTS) scripts/tf_ops.py destroy

# ===== ヘルプ =====

help:
	@echo "=== Setup（初回のみ） ==="
	@echo "  make gcp-setup          GCP初回セットアップ一括（API有効化・SA権限・Docker認証）"
	@echo ""
	@echo "=== デプロイ ==="
	@echo "  make deploy-all         全構築（infra → push → job）"
	@echo "  make destroy-all        全削除（terraform destroy → docker clean）"
	@echo ""
	@echo "=== GCP操作 ==="
	@echo "  make ingest            Cloud Run Job実行（データ投入テスト）"
	@echo "  make search Q=キーワード  キーワード検索テスト"
	@echo "  make logs               最新executionのログ確認"
	@echo ""
	@echo "=== Docker ==="
	@echo "  make build              Dockerイメージビルド"
	@echo "  make push               ビルド & Artifact Registryへpush"
	@echo "  make docker-run         ローカルDocker実行"
	@echo "  make clean              ローカルイメージ削除"
	@echo ""
	@echo "=== ローカル ==="
	@echo "  make install            pip install"
	@echo "  make run                ローカル実行"
	@echo ""
	@echo "=== Terraform ==="
	@echo "  make tf-init            プロバイダ初期化"
	@echo "  make tf-plan            差分確認"
	@echo "  make tf-apply           全リソース適用"
	@echo "  make tf-apply-infra     インフラのみ適用（Cloud Run Job除外）"
	@echo "  make tf-import          既存リソースをstateにimport"
	@echo "  make tf-destroy         全リソース削除"
