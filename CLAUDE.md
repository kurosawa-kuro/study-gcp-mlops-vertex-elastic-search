# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

GCP Terraform + Elastic Cloud の学習プロジェクト。Cloud RunベースでElastic Cloud検索基盤を構築する。
GCPプロジェクト: `mlops-dev-a`、リージョン: `asia-northeast1`

## Architecture

```
[Cloud Run Job]
   ├── Secret Managerから接続情報取得（JSON: cloud_url/username/password）
   ├── ingestモード: クリーンアップ → src/data/*.json 投入 → 確認検索（データ残す）
   └── searchモード: 既存インデックスに対してキーワード検索（SEARCH_KEYWORD環境変数で切替）

[Elastic Cloud]
   ├── Elasticsearch（データ格納・全文検索）
   └── Kibana（管理UI）
```

- **src/**: アプリケーションコード（main.py, Dockerfile, requirements.txt）
- **src/data/**: 投入用JSONデータ
- **terraform/**: Elastic Cloud deployment, Artifact Registry, Secret Manager, Cloud Run Job, IAM
- **scripts/**: 設定(config.py)、Docker操作、GCP操作、Terraform操作ヘルパー
- **docs/**: 仕様・設計書、実装済み一覧、運用ガイド、技術ガイド

## Tech Stack

- **検索**: Elastic Cloud (Elasticsearch + Kibana)
- **Infra**: Cloud Run (Job), Artifact Registry, Secret Manager
- **IaC**: Terraform（GCP + Elastic Cloud、ec provider ~> 0.12 / google provider ~> 5.0）
- **CI/CD**: GitHub Actions（Terraform plan/apply）
- **言語**: Python 3.11

## Commands

```bash
make deploy-all              # 全構築（infra → push → job）
make destroy-all             # 全削除（課金停止）
make ingest                  # データ投入（クリーンアップ→投入→データ残す）
make search Q=Elasticsearch  # キーワード検索（投入済みデータ対象）
make logs                    # 最新executionのログ確認
make push                    # Dockerイメージ ビルド & push
make gcp-setup               # GCP初回セットアップ
make help                    # コマンド一覧
```

## Language

このプロジェクトのドキュメントやコミットメッセージは日本語で記述する。
