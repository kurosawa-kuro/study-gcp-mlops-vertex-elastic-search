```
SKTOP-REF6HHU:~/repos/study-gcp-teraform-elastic-search$ 
ubuntu@DESKTOP-REF6HHU:~/repos/study-gcp-teraform-elastic-search$ make execute 
PYTHONPATH=scripts python3 scripts/gcp_ops.py execute

execution: hello-elastic-job-v5fc9
=== 1. info ===
cluster_name: a1dce6802640427c9adb5217c418aa62
version: 9.3.2
=== 2. index documents (hello) ===
loaded: sample.json (3 docs)
  [1/3] created: Elasticsearch入門
  [2/3] created: Terraform入門
  [3/3] created: Cloud Run概要
=== 3. search ===
total hits: 3
  -> {'title': 'Elasticsearch入門', 'content': 'Elasticsearchは分散型の検索・分析エンジンです。', 'tag': 'search'}
  -> {'title': 'Terraform入門', 'content': 'Terraformはインフラをコードとして管理するIaCツールです。', 'tag': 'infra'}
  -> {'title': 'Cloud Run概要', 'content': 'Cloud RunはGCPのサーバーレスコンテナ実行環境です。', 'tag': 'gcp'}
=== 4. cleanup ===
index deleted
Container called exit(0).

ubuntu@DESKTOP-REF6HHU:~/repos/study-gcp-teraform-elastic-search$ make logs 
PYTHONPATH=scripts python3 scripts/gcp_ops.py logs
execution: hello-elastic-job-v5fc9
=== 1. info ===
cluster_name: a1dce6802640427c9adb5217c418aa62
version: 9.3.2
=== 2. index documents (hello) ===
loaded: sample.json (3 docs)
  [1/3] created: Elasticsearch入門
  [2/3] created: Terraform入門
  [3/3] created: Cloud Run概要
=== 3. search ===
total hits: 3
  -> {'title': 'Elasticsearch入門', 'content': 'Elasticsearchは分散型の検索・分析エンジンです。', 'tag': 'search'}
  -> {'title': 'Terraform入門', 'content': 'Terraformはインフラをコードとして管理するIaCツールです。', 'tag': 'infra'}
  -> {'title': 'Cloud Run概要', 'content': 'Cloud RunはGCPのサーバーレスコンテナ実行環境です。', 'tag': 'gcp'}
=== 4. cleanup ===
index deleted
Container called exit(0).

ubuntu@DESKTOP-REF6HHU:~/repos/study-gcp-teraform-elastic-search$ 
```