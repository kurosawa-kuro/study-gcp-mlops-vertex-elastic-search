include .env
export

# Terraform用環境変数（TF_VAR_で自動認識）
export TF_VAR_project_id            := $(PROJECT_ID)
export TF_VAR_region                := $(REGION)
export TF_VAR_deployment_name       := $(DEPLOYMENT_NAME)
export TF_VAR_job_name              := $(JOB_NAME)
export TF_VAR_repo_name             := $(REPO_NAME)
export TF_VAR_secret_name           := $(SECRET_NAME)
export TF_VAR_elastic_api_key       := $(ELASTIC_API_KEY)
export TF_VAR_elastic_cloud_api_key := $(ELASTIC_CLOUD_API_KEY)

SCRIPTS := PYTHONPATH=scripts python3

.PHONY: run install build build-gcr push docker-run clean \
        create-repo auth-docker create-secret create-job \
        execute logs deploy deploy-all destroy-all cleanup-gcp \
        tf-init tf-plan tf-apply tf-apply-infra tf-import tf-destroy help

# ===== ローカル =====

run:
	python3 main.py

install:
	pip install -r requirements.txt

build:
	$(SCRIPTS) scripts/docker_ops.py build

build-gcr:
	$(SCRIPTS) scripts/docker_ops.py build-gcr

push:
	$(SCRIPTS) scripts/docker_ops.py push

docker-run:
	$(SCRIPTS) scripts/docker_ops.py docker-run

clean:
	$(SCRIPTS) scripts/docker_ops.py clean

# ===== GCP デプロイ =====

create-repo:
	$(SCRIPTS) scripts/gcp_ops.py create-repo

auth-docker:
	$(SCRIPTS) scripts/gcp_ops.py auth-docker

create-secret:
	$(SCRIPTS) scripts/gcp_ops.py create-secret

create-job:
	$(SCRIPTS) scripts/gcp_ops.py create-job

execute:
	$(SCRIPTS) scripts/gcp_ops.py execute

logs:
	$(SCRIPTS) scripts/gcp_ops.py logs

deploy:
	$(MAKE) push
	$(MAKE) create-secret
	$(MAKE) create-job

deploy-all:
	$(MAKE) tf-apply-infra
	$(MAKE) push
	$(MAKE) tf-apply

destroy-all:
	$(MAKE) tf-destroy
	$(MAKE) clean

cleanup-gcp:
	$(SCRIPTS) scripts/gcp_ops.py cleanup

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
	@echo "ローカル:"
	@echo "  make install      依存パッケージインストール"
	@echo "  make run          ローカル実行"
	@echo "  make build        Dockerイメージビルド"
	@echo "  make docker-run   Docker実行"
	@echo "  make clean        ローカルイメージ削除"
	@echo ""
	@echo "GCPデプロイ:"
	@echo "  make create-repo  Artifact Registryリポジトリ作成"
	@echo "  make auth-docker  Docker認証設定"
	@echo "  make build-gcr    GCR向けイメージビルド"
	@echo "  make push         Artifact Registryへpush"
	@echo "  make create-secret Secret Manager登録"
	@echo "  make create-job   Cloud Run Job作成"
	@echo "  make deploy       一括デプロイ (push→secret→job) ※gcloud版"
	@echo "  make deploy-all   Terraform全構築 (infra→push→job)"
	@echo "  make destroy-all  全リソース削除 (terraform destroy→docker clean)"
	@echo "  make execute      Cloud Run Job実行"
	@echo "  make logs         ログ確認"
	@echo ""
	@echo "Terraform:"
	@echo "  make tf-init      terraform init"
	@echo "  make tf-plan      差分確認"
	@echo "  make tf-apply     全リソース適用"
	@echo "  make tf-apply-infra インフラのみ適用（Cloud Run Job除外）"
	@echo "  make tf-import    既存リソースをstateにimport"
	@echo "  make tf-destroy   全リソース削除"
	@echo ""
	@echo "クリーンアップ:"
	@echo "  make cleanup-gcp  GCPリソース削除"
