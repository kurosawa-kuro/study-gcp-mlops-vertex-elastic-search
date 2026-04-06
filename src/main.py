import json
import os
import sys
from pathlib import Path

from elasticsearch import Elasticsearch
from google.cloud import secretmanager

INDEX_NAME = "hello"
DATA_DIR = Path(__file__).parent / "data"


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


def load_documents() -> list[dict]:
    """data/ディレクトリ内の全JSONファイルを読み込む。"""
    docs = []
    for path in sorted(DATA_DIR.glob("*.json")):
        with open(path) as f:
            data = json.load(f)
        if isinstance(data, list):
            docs.extend(data)
        else:
            docs.append(data)
        print(f"loaded: {path.name} ({len(data) if isinstance(data, list) else 1} docs)")
    return docs


def cleanup(es: Elasticsearch) -> None:
    """既存インデックスを削除する（存在する場合のみ）。"""
    if es.indices.exists(index=INDEX_NAME):
        es.indices.delete(index=INDEX_NAME)
        print(f"index '{INDEX_NAME}' deleted")
    else:
        print(f"index '{INDEX_NAME}' does not exist (skip)")


def ingest(es: Elasticsearch) -> None:
    """クリーンアップ→data/のJSONをESに投入→確認検索。データは残す。"""
    print("=== 1. cleanup ===")
    cleanup(es)

    print("\n=== 2. info ===")
    info = es.info()
    print(f"cluster_name: {info['cluster_name']}")
    print(f"version: {info['version']['number']}")

    print(f"\n=== 3. index documents ({INDEX_NAME}) ===")
    docs = load_documents()
    if not docs:
        print("no documents found in data/")
        return

    for i, doc in enumerate(docs):
        resp = es.index(index=INDEX_NAME, document=doc)
        print(f"  [{i+1}/{len(docs)}] {resp['result']}: {doc.get('title', doc)}")

    print("\n=== 4. search (match_all) ===")
    es.indices.refresh(index=INDEX_NAME)
    result = es.search(index=INDEX_NAME, query={"match_all": {}})
    print(f"total hits: {result['hits']['total']['value']}")
    for hit in result["hits"]["hits"]:
        print(f"  -> {hit['_source']}")

    print(f"\ndone. index '{INDEX_NAME}' retained for search testing.")


def search(es: Elasticsearch, keyword: str) -> None:
    """既存インデックスに対してキーワード検索する。"""
    if not es.indices.exists(index=INDEX_NAME):
        print(f"index '{INDEX_NAME}' does not exist. run 'make ingest' first.")
        sys.exit(1)

    print(f'=== search: "{keyword}" ===')
    es.indices.refresh(index=INDEX_NAME)
    result = es.search(
        index=INDEX_NAME,
        query={"multi_match": {"query": keyword, "fields": ["*"]}},
    )
    hits = result["hits"]["total"]["value"]
    print(f"total hits: {hits}")
    for hit in result["hits"]["hits"]:
        print(f"  score={hit['_score']:.4f}  {hit['_source']}")

    if hits == 0:
        print("  (no results)")


def main() -> None:
    es = get_es_client()

    keyword = os.environ.get("SEARCH_KEYWORD")
    if keyword:
        search(es, keyword)
    else:
        ingest(es)


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"ERROR: {type(e).__name__}: {e}", file=sys.stderr)
        sys.exit(1)
