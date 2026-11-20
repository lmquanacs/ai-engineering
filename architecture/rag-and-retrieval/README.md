# RAG & retrieval

_Last updated: 2026-11-20_

> Getting the right facts from your own data into the model: chunking, search, reranking and the models and databases behind them. For what happens to context once it's in the window, see [Context engineering & memory](../context-and-memory/README.md).

## 🧭 The retrieval pipeline

| Stage | Decisions to make | Common default |
|---|---|---|
| **Parse** | PDF/HTML/table extraction, OCR, keeping layout | A layout-aware parser; treat tables and figures as their own chunks |
| **Chunk** | Size, overlap, structure-aware vs fixed, adding document context to each chunk | Split on document structure first, then by size |
| **Embed** | Model, dimensions, multilingual, multimodal, open vs API | Pick from current MTEB results for *your* language and domain, then test on your own queries |
| **Index & search** | Vector DB vs existing database (pgvector, OpenSearch), hybrid (BM25 + vector), metadata filters | Hybrid search; start in the database you already run |
| **Rerank** | Cross-encoder or listwise reranker, top-k in and out | Retrieve wide, rerank down to a handful |
| **Generate** | Citations, "I don't know" handling, how much to pass | Ask for citations to chunk IDs and check them |
| **Evaluate** | Retrieval recall/precision vs answer faithfulness | A small labelled query set, scored on every change → [Evals](../evals-and-observability/README.md) |

**Agentic retrieval:** instead of one search before generation, the agent calls search as a tool, reformulates and searches again. It helps on multi-hop questions and costs more steps; measure both. → [Agentic workflows](../agentic-workflows/README.md)

**Cost note:** injecting retrieved text rewrites the prompt prefix and can break prompt caching. See the cache study in [Context engineering](../context-and-memory/README.md#-latest-evidence).

---

## 🗞️ Latest

<!-- newest first: retrieval patterns with evidence, vector DB releases, RAG eval methods -->

---

## 🔎 Retrieval models (embeddings, rerankers, parsers)

### NVIDIA Nemotron 3.5 Embed / Rerank / Parse · 2026-10-21 🆕
Five open, commercially usable retrieval models: Embed (8B and 1B, plus a 1B NVFP4 variant), an 8B reranker and a 631M document parser. NVIDIA reports first place among dense retrievers on ViDoRe v3.1 (61.17 nDCG@10) and top reranker scores as of Oct 20 *(self-reported)*. Available on Hugging Face and as NIM.
**Why it matters:** These are strong open models for multimodal retrieval over PDFs, charts and tables, and NVIDIA pitches better retrieval as a way to cut agent token spend.
Sources: [Let's Data Science](https://letsdatascience.com/news/nvidia-expands-open-nemotron-35-models-for-enterprise-retrie-f464c19f) · [Unite.AI](https://unite.ai/nvidia-debuts-open-nemotron-3-5-models-for-embedding-reranking-parsing) · Added: 2026-11-18

### Cohere Embed 5 + Rerank 5 (Context Focus) · Oct–Nov 2026 🆕
Rerank 5 adds an optional **Context Focus** mode that returns the relevant text spans along with document scores. Both models have been on OpenRouter since 2026-11-04, so existing OpenRouter keys work.
**Why it matters:** Returning spans means you pass less text to the generator, which saves context and cost.
Source: [Neoteo](https://www.neoteo.com/en/cohere-brings-embed-5-and-rerank-5-to-openrouter) · Added: 2026-11-18

### jina-reranker-v3.5 · 2026-08-03
A 0.6B listwise reranker. Jina reports it matches 4B models on BEIR and leads compact models on multilingual MIRACL *(self-reported)*. The weights are **non-commercial**; commercial use goes through Jina's API or Elastic.
Source: [Jina AI](https://jina.ai/news/jina-reranker-v3-5-faster-listwise-reranking-hybrid-attention-self-distillation) · Added: 2026-11-18

**Pattern:** a cheap embedding model plus a precise reranker usually beats one large embedding model on cost per quality point.

