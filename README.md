# Vector Store From Scratch

A vector database built in pure Python — no ChromaDB, no FAISS, no external vector libraries. Built to understand what's actually happening under the hood of tools like ChromaDB and Pinecone before using them as black boxes.

## What it does

- **Stores embeddings** — each vector is saved with a unique ID and optional text metadata
- **CRUD operations** — add, get, update, delete
- **Similarity search** — cosine similarity, computed from scratch (no NumPy/libraries)
- **Persistence** — save and reload the entire store to/from a JSON file

## Why these design choices

**Cosine similarity over Euclidean distance or raw dot product**
Embeddings encode meaning primarily in *direction*, not magnitude. Cosine similarity measures the angle between two vectors, ignoring their length — so two vectors pointing the same way score highly even if one is "bigger" than the other. Dot product alone would conflate meaning with magnitude unless vectors are pre-normalized.

**Two separate dictionaries (`vectors`, `metadata`) instead of one combined structure**
`search()` only needs raw vectors to compute similarity — keeping vectors separate from metadata means the search loop isn't dragging extra data along for every comparison. This mirrors how production vector databases separate the searchable index from stored payloads.

**Brute-force O(n) search**
Every stored vector is compared against the query vector, one by one. This is intentional — it's the simplest correct implementation, and correctness came before performance. It does **not** scale past roughly tens of thousands of vectors.

**JSON persistence (for now)**
Simple, human-readable, zero setup. The tradeoff: every save rewrites the entire file, and there's no safe concurrent access. A SQLite version is planned as a deliberate upgrade — see Roadmap.

## What a production system would do differently

- **Indexing**: Real vector databases use approximate nearest neighbor (ANN) algorithms like HNSW or IVF instead of brute-force comparison, trading a small amount of accuracy for massive speed gains at scale.
- **Storage**: SQLite or a proper database instead of JSON, for safe partial writes, concurrent access, and indexed metadata filtering.
- **Normalization**: Vectors are often pre-normalized to unit length at insert time, so similarity search can use a cheaper dot product instead of computing magnitude on every comparison.
- **Batching**: Bulk insert/search operations instead of one-at-a-time, to reduce overhead at scale.

## Project structure

```
vectorstore/
├── similarity.py    # cosine similarity, implemented from scratch
├── store.py         # VectorStore class: CRUD + search + persistence
└── test_store.json  # example persisted output
```

## Usage

```python
from store import VectorStore

store = VectorStore()
store.add("1", [1, 0, 0], text="example text")
store.search([1, 0, 0], top_k=5)
store.save_to_file("data.json")
```

## Roadmap

- [ ] SQLite persistence layer (in progress)
- [ ] Metadata filtering during search
- [ ] Feeds into Project 2: a production RAG system using this store's concepts with FastAPI + ChromaDB

## Built as part of an AI engineering portfolio

Built entirely on a phone using Termux — no laptop, no Docker. Part of a series of projects moving toward backend/AI engineering roles.
