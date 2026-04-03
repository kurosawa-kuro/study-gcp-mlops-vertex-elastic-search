PROJECT_ID   := mlops-dev-a
REGION       := asia-northeast1
IMAGE_NAME   := es-hello
REPO_NAME    := hello-elastic
IMAGE_URI    := $(REGION)-docker.pkg.dev/$(PROJECT_ID)/$(REPO_NAME)/$(IMAGE_NAME):latest

include .env
export

.PHONY: run install build docker-run clean \
        create-repo auth-docker build-gcr push create-secret \
        create-job execute logs deploy cleanup-gcp \
        tf-init tf-plan tf-apply tf-destroy help

# ===== ローカル =====

run:
	python3 main.py

install:
	pip install -r requirements.txt

build:
	docker build -t $(IMAGE_NAME) .

docker-run: build
	docker run --env-file .env $(IMAGE_NAME)

clean:
	docker rmi $(IMAGE_NAME) 2>/dev/null || true

# ===== GCP デプロイ =====

create-repo:
	gcloud artifacts repositories create $(REPO_NAME) \
	  --repository-format=docker \
	  --location=$(REGION) \
	  --description="Hello Elastic Docker images"

auth-docker:
	gcloud auth configure-docker $(REGION)-docker.pkg.dev

build-gcr:
	docker build -t $(IMAGE_URI) .

push: build-gcr
	docker push $(IMAGE_URI)

create-secret:
	echo -n "$(ELASTIC_API_KEY)" | \
	  gcloud secrets create elastic-api-key \
	  --data-file=- \
	  --replication-policy=user-managed \
	  --locations=$(REGION)

create-job:
	gcloud run jobs create $(IMAGE_NAME) \
	  --image=$(IMAGE_URI) \
	  --region=$(REGION) \
	  --set-env-vars="ELASTIC_CLOUD_URL=$(ELASTIC_CLOUD_URL)" \
	  --set-secrets="ELASTIC_API_KEY=elastic-api-key:latest" \
	  --task-timeout=60s \
	  --max-retries=0 \
	|| gcloud run jobs update $(IMAGE_NAME) \
	  --image=$(IMAGE_URI) \
	  --region=$(REGION) \
	  --set-env-vars="ELASTIC_CLOUD_URL=$(ELASTIC_CLOUD_URL)" \
	  --set-secrets="ELASTIC_API_KEY=elastic-api-key:latest" \
	  --task-timeout=60s \
	  --max-retries=0

execute:
	gcloud run jobs execute $(IMAGE_NAME) \
	  --region=$(REGION) \
	  --wait

logs:
	gcloud logging read \
	  "resource.type=cloud_run_job AND resource.labels.job_name=$(IMAGE_NAME)" \
	  --limit=50 \
	  --format="value(textPayload)" \
	  --project=$(PROJECT_ID)

deploy:
	$(MAKE) push
	$(MAKE) create-secret
	$(MAKE) create-job

# ===== Terraform =====

tf-init:
	cd terraform && terraform init

tf-plan:
	cd terraform && terraform plan -var-file="terraform.tfvars"

tf-apply:
	cd terraform && terraform apply -var-file="terraform.tfvars"

tf-destroy:
	cd terraform && terraform destroy -var-file="terraform.tfvars"

# ===== クリーンアップ =====

cleanup-gcp:
	gcloud run jobs delete $(IMAGE_NAME) --region=$(REGION) --quiet
	gcloud artifacts docker images delete $(IMAGE_URI) --quiet
	gcloud secrets delete elastic-api-key --quiet

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
	@echo "  make deploy       一括デプロイ (push→secret→job)"
	@echo "  make execute      Cloud Run Job実行"
	@echo "  make logs         ログ確認"
	@echo ""
	@echo "Terraform:"
	@echo "  make tf-init      terraform init"
	@echo "  make tf-plan      差分確認"
	@echo "  make tf-apply     適用"
	@echo "  make tf-destroy   全リソース削除"
	@echo ""
	@echo "クリーンアップ:"
	@echo "  make cleanup-gcp  GCPリソース削除"
