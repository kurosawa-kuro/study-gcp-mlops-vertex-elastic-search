variable "project_id" {
  description = "GCPプロジェクトID"
}

variable "region" {
  description = "GCPリージョン"
}

variable "deployment_name" {
  description = "Elastic Cloudデプロイメント名"
}

variable "job_name" {
  description = "Cloud Run Job名"
}

variable "repo_name" {
  description = "Artifact Registryリポジトリ名"
}

variable "secret_name" {
  description = "Secret Manager シークレット名（ES接続情報JSON格納先）"
}

variable "elastic_cloud_api_key" {
  description = "Elastic Cloud Org APIキー（プロバイダ認証用）"
  sensitive   = true
}
