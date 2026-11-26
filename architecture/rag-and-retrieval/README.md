# RAG & retrieval

_Last updated: 2026-11-27_

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

### Cheap cacheable scorers in front of your reranker · arXiv 2611.33844 🆕
The paper composes rerankers of different kinds (lexical, single-vector, late-interaction, cross-encoder) without training them together. Putting two lightweight scorers with cacheable passage representations in front of a CrossEncoder or Provence raised answer accuracy on NoLiMa 32K with Gemma by 4.02–9.43 points and made online pruning 1.57–1.88× faster. Fusing one with ColBERTv2 via reciprocal rank fusion gave +4.60 points at 1.36× speed. The gains depended on the reader and the pairing, and a cascade could beat its final reranker yet lose to its coarse first stage alone *(self-reported)*.
**Why it matters:** a two-stage rerank can be both faster and more accurate, but only measure it with stage-removal ablations: test each stage alone as well as the full cascade.
Source: [arXiv 2611.33844](https://arxiv.org/abs/2611.33844) · Added: 2026-11-27

### Run agentic RAG evals more than once · arXiv 2611.31266 🆕
A study of a deployed agentic RAG system for product-documentation questions ran each of 739 questions ten times. The correct page was retrieved in at least one run 69.4% of the time but in all ten runs only 50.9% of the time. Retrieval caused most run-to-run divergence (43.9%), and the number of parallel searches the agent chose at its first step alone explained 20.1% of divergent pairs, while answers stayed similar in meaning (BERTScore 0.90) *(self-reported; NeurIPS 2026 workshop paper)*.
**Why it matters:** A single-run retrieval score overstates how reliable an agentic RAG system is. Report "found in every run" alongside "found in any run", and consider fixing or bounding the agent's first search fan-out.
Source: [arXiv 2611.31266](https://arxiv.org/abs/2611.31266) · Added: 2026-11-26

### SOARS: a fast model reranks inside the search loop · arXiv 2611.32917 · 2026-11-24 🆕
A training-free method for deep-search agents: at each step a fast "System One" model picks the relevant passages from long documents and reranks candidates in one call, using both the original question and the agent's sub-query. Across six backbones on BrowseComp-Plus and WebShaper, the authors report better accuracy and evidence recall with fewer search calls; on BrowseComp-Plus GPT-5.4 Mini went from 73.9% to 84.7% while search calls fell from 23 to 14 *(self-reported)*.
**Why it matters:** If your agent calls search many times, a cheap per-step rerank that also sees the original question can cut both steps and cost; a full cross-encoder at every step is often too slow.
Source: [arXiv 2611.32917](https://arxiv.org/abs/2611.32917) · Added: 2026-11-26

### OpenSearch 3.10: per-query hybrid fusion, template-based agentic search · 2026-11-17 🆕
The `hybrid` query gains a fusion mode: normalisation and combination are set in the query body instead of a search pipeline, fused hybrid queries can nest inside `bool` or `dis_max`, and a `weights` parameter sets subquery weights per request (min-max, z-score, L2 and RRF remain). `half_float` vectors add 2-bit and 4-bit scalar quantisation. Experimental: search templates for agentic search, where the LLM fills in a registered template rather than writing the whole query, and an Intel SVS engine that OpenSearch reports at 2.6× Faiss HNSW-fp16 throughput at 0.95 recall *(self-reported)*.
**Why it matters:** Hybrid weights become a per-request knob you can tune and A/B, and template-based agentic search bounds what an LLM-written query can do.
Source: [OpenSearch blog: Explore OpenSearch 3.10](https://opensearch.org/blog/explore-opensearch-3-10/) · Added: 2026-11-20

Also checked (no notes worth an entry): Qdrant 1.20.1/1.20.2 patch images, Weaviate 1.40.6, Milvus v3.0.5 (2026-10-30); pgvector 0.8.7 is still the latest (2026-10-01) and now has `pg19` images. **Weaviate 1.41.0:** a `1.41.0` image (also tagged `latest`) appeared on Docker Hub on 2026-11-23, and as of 2026-11-26 the [docs' release table](https://docs.weaviate.io/weaviate/release-notes) lists v1.41.0 (2026-11-23) as the latest release, but with no highlights and no matching client library versions yet, so wait for the release notes before upgrading. The RC lists namespaces with RF=3, a lower-memory HNSW node format, semi-automatic shard rebalancing (preview) and reranking with decision models.

**On AWS:** Amazon Textract Insights (GA 2026-11-20) extracts schema-defined fields from mixed document packets with a confidence score and page/bounding-box grounding per value. → [AWS](../../platforms/aws/README.md)

---

## 🔎 Retrieval models (embeddings, rerankers, parsers)

### EmbeddingGemma 2 · open multimodal embeddings · 2026-10-06 🆕
Google's open embedding model (740M parameters, built on Gemma 4) maps text, code, images, video and audio into one vector space; text-only use needs as little as 270M because the vision and audio encoders are optional. It has an 8K-token context and 768-dimensional vectors that can be truncated to 512, 256 or 128 (Matryoshka). Google reports MTEB Code rising from 68.76 to 78.68 over the first EmbeddingGemma *(self-reported)*. Licence: Apache 2.0. Weights are on Hugging Face (`google/embeddinggemma-2`) and Kaggle, and run in sentence-transformers, vLLM, SGLang, Ollama, llama.cpp and transformers.js; Vertex AI availability is "coming soon". The technical report followed on 2026-11-17.
**Why it matters:** A commercially usable, self-hostable model for multimodal RAG that is small enough for CPUs and phones. Benchmark it against your current embedder on your own queries before re-indexing.
Sources: [Google blog: EmbeddingGemma 2](https://blog.google/innovation-and-ai/technology/developers-tools/embeddinggemma-2/) · [Technical report overview](https://blog.google/innovation-and-ai/technology/developers-tools/embeddinggemma-2-technical-report/) · Added: 2026-11-24

### NVIDIA Nemotron 3.5 Embed / Rerank / Parse · 2026-10-21
Five open, commercially usable retrieval models: Embed (8B and 1B, plus a 1B NVFP4 variant), an 8B reranker and a 631M document parser. NVIDIA reports first place among dense retrievers on ViDoRe v3.1 (61.17 nDCG@10) and top reranker scores as of Oct 20 *(self-reported)*. Available on Hugging Face and as NIM.
**Why it matters:** These are strong open models for multimodal retrieval over PDFs, charts and tables, and NVIDIA pitches better retrieval as a way to cut agent token spend.
Licence: OpenMDW-1.1.
Sources: [NVIDIA on Hugging Face](https://huggingface.co/blog/nvidia/nemotron-retriever-world-class-agentic-retrieval) · [Nemotron-3.5-Embed-8B model card](https://huggingface.co/nvidia/Nemotron-3.5-Embed-8B-BF16) · [Nemotron-3.5-Parse model card](https://huggingface.co/nvidia/Nemotron-3.5-Parse) · Added: 2026-11-18 · Updated: 2026-11-20

### Cohere Embed 5 + Rerank 5 (Context Focus) · Sep–Nov 2026
Rerank 5 adds an optional **Context Focus** mode that returns the relevant text spans along with document scores. Both models have been on OpenRouter since 2026-11-04, so existing OpenRouter keys work.
**Why it matters:** Returning spans means you pass less text to the generator, which saves context and cost.
Embed 5 (Pro and Fast) launched 2026-09-30 and Rerank 5 (Pro and Fast, with calibrated relevance scores) on 2026-10-21.
Sources: [Cohere changelog: Embed 5](https://docs.cohere.com/v2/changelog/embed-v5) · [Rerank 5](https://docs.cohere.com/v2/changelog/rerank-v5) · [On OpenRouter](https://docs.cohere.com/v2/changelog/embed-rerank-v5-openrouter) · Added: 2026-11-18 · Updated: 2026-11-20

### jina-reranker-v3.5 · 2026-08-03
A 0.6B listwise reranker. Jina reports it matches 4B models on BEIR and leads compact models on multilingual MIRACL *(self-reported)*. The weights are **non-commercial**; commercial use goes through Jina's API or Elastic.
Source: [Jina AI](https://jina.ai/news/jina-reranker-v3-5-faster-listwise-reranking-hybrid-attention-self-distillation) · Added: 2026-11-18

**Pattern:** a cheap embedding model plus a precise reranker usually beats one large embedding model on cost per quality point.

