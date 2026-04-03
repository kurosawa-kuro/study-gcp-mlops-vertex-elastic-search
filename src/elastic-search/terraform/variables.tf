variable "project_id" {}
variable "region" { default = "asia-northeast1" }
variable "elastic_cloud_api_key" { sensitive = true }  # Elastic CloudのOrg APIキー
variable "elastic_api_key"       { sensitive = true }  # ESのAPIキー (既存流用可)
