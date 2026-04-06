# Elasticsearch / Elastic Cloud 入門

---

## Elasticsearch = JSON を入れて全文検索するエンジン

```
{"title": "検索入門", "content": "全文検索の基礎"}  ← これを入れると
"検索" で探せる。スコア付きで関連順に返る。
```

---

## RDB との違い

| | RDB | Elasticsearch |
|---|---|---|
| データ | テーブルの行 | JSONドキュメント |
| 検索 | `WHERE LIKE '%検索%'`（遅い） | 転置インデックス（速い） |
| 結果順 | 自分で `ORDER BY` | **関連度スコア順（自動）** |

---

## Elastic Cloud = Elasticsearch のマネージドサービス

サーバー構築・運用不要。Kibana（ブラウザ管理UI）も自動で付く。

```
┌─ Elastic Cloud ──────────────────────────────┐
│                                              │
│  ┌─ Elasticsearch ─────────────────────┐     │
│  │  JSON格納・全文検索API              │     │
│  │  アプリから接続して読み書きする本体  │     │
│  └─────────────────────────────────────┘     │
│       ▲                                      │
│       │ 内部接続                              │
│       ▼                                      │
│  ┌─ Kibana ────────────────────────────┐     │
│  │  ブラウザで使える管理・可視化UI     │     │
│  │  クエリ実行・ダッシュボード作成     │     │
│  └─────────────────────────────────────┘     │
│                                              │
└──────────────────────────────────────────────┘
       ▲
       │ HTTPS
       │
  アプリ（Python等）
```

---

## 操作（Python）

```python
from elasticsearch import Elasticsearch
es = Elasticsearch("https://...", basic_auth=("elastic", "password"))

# 入れる
es.index(index="docs", document={"title": "検索入門", "content": "全文検索の基礎"})

# 反映
es.indices.refresh(index="docs")

# 探す
result = es.search(index="docs", query={"multi_match": {"query": "検索", "fields": ["*"]}})
for hit in result["hits"]["hits"]:
    print(hit["_score"], hit["_source"])   # スコア, 本体

# 消す
es.indices.delete(index="docs")
```

---

## 用語

| 用語 | 一言 |
|------|------|
| インデックス | JSONの入れ物（≒テーブル） |
| ドキュメント | 1件のJSON（≒行） |
| `_score` | 関連度スコア（自動計算） |
| refresh | 投入データを検索可能にする操作 |
| Kibana | ブラウザで使える管理・可視化UI |
| Elastic Cloud | Elasticsearch + Kibana のホスティングサービス |
