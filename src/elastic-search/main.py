import os
from dotenv import load_dotenv
from elasticsearch import Elasticsearch

load_dotenv()

ELASTIC_CLOUD_URL = os.environ["ELASTIC_CLOUD_URL"]
ELASTIC_API_KEY   = os.environ["ELASTIC_API_KEY"]

es = Elasticsearch(
    ELASTIC_CLOUD_URL,
    api_key=ELASTIC_API_KEY
)

# 1. 疎通確認
print("=== 1. info ===")
info = es.info()
print(f"cluster_name: {info['cluster_name']}")
print(f"version: {info['version']['number']}")

# 2. インデックス作成 + ドキュメント投入
print("\n=== 2. index document ===")
resp = es.index(
    index="hello",
    document={"message": "hello world", "tag": "test"}
)
print(f"result: {resp['result']}")
print(f"_id: {resp['_id']}")

# 3. 検索
print("\n=== 3. search ===")
es.indices.refresh(index="hello")
result = es.search(
    index="hello",
    query={"match": {"message": "hello"}}
)
print(f"total hits: {result['hits']['total']['value']}")
for hit in result['hits']['hits']:
    print(f"  -> {hit['_source']}")

# 4. クリーンアップ
print("\n=== 4. cleanup ===")
es.indices.delete(index="hello")
print("index deleted")
