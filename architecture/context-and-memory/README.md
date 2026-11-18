# Context engineering & memory

_Last updated: 2026-11-18_

> Deciding what the model sees at each step: compaction, tool-result clearing, memory, retrieval (embeddings, rerankers, parsing) and caching. Agent quality now depends more on this than on which model you pick.

## 🧭 The core toolkit

| Technique | What it does | Use when |
|---|---|---|
| **Tool-result clearing** | Drop or shrink old tool outputs once they've been used | First line of defence; cheap and lossless for reasoning |
| **Compaction** | Summarise long history into a compact block | You must keep reasoning across a long dialogue |
| **External memory / notes** | The agent writes notes, plans and state to files or a store, then re-reads them | Multi-session or multi-hour work |
| **Context isolation (subagents)** | Give each subtask its own clean window | Breadth-first work such as research; less so for tightly coupled coding |
| **Context reset + hand-off artifact** | Start fresh from a structured summary | Long runs where compaction alone degrades quality |
| **Prompt caching** | Keep a stable, append-only prefix so the provider can reuse it | Always; cached input is often about 1/20–1/40 of the list price |

**Rule of thumb:** use tool-result clearing first and keep compaction for when reasoning must survive. Production agents read roughly 100 input tokens per output token, so context is where the cost goes. ([Tian Pan: memory, compaction and tool clearing](https://tianpan.co/blog/2026-02-26-context-engineering-memory-compaction-tool-clearing))

**Caching rule:** even a one-token difference in the prefix invalidates the cache. Keep system prompts and tool definitions stable, append rather than rewrite, and serialise deterministically. ([Context management strategies](https://agentic-ai.readthedocs.io/en/latest/ContextEngineering/strategies/))

---

## ⭐ Start here

### Anthropic: effective context engineering for AI agents
Treat context as a finite attention budget. Start with a minimal prompt and add instructions only in response to failures you have observed. Use structured note-taking (for example a todo list) to keep state outside the window.
Source: [Summary + links to both Anthropic posts](https://agentic-ai.readthedocs.io/en/latest/ContextEngineering/anthropic/) · Added: 2026-11-18

### Server-side compaction (Claude API)
A beta compaction strategy (`compact_20260112`) triggers at a configurable token threshold (minimum 50K, default 150K) and replaces earlier turns with a typed compaction block, so you don't have to write your own summariser.
Source: [Context management strategies](https://agentic-ai.readthedocs.io/en/latest/ContextEngineering/strategies/) · Added: 2026-11-18

### Production pattern: re-inject the plan and preview the data · Arize "Alex"
Arize's agent kept drifting because tool outputs buried the original request. They made planning mandatory through a todo tool, kept the plan outside the chat history and re-injected it on every call, and added a finish gate. For large data, the model gets a structure-preserving preview and queries the full data with small tools (jq, grep) under an output cap.
Source: [ZenML LLMOps database](https://www.zenml.io/llmops-database/building-alex-an-agent-first-ai-engineering-assistant-with-production-grade-llmops) · Added: 2026-11-18

### Context Engineering in 2026: compaction, memory & skills (talk)
A 100-slide practitioner deck (Towards AI, shown at AI Engineer). It argues that serious harnesses converged on the same habits: fresh sessions when switching tasks, narrow file scope, disconnecting unused tools, then compaction.
Source: [Slides](https://docs.google.com/presentation/d/1BVqX1h2DPyIDCEWUSNXSVFIPTQgbhM_ik4JBVaQ2f3k/htmlpresent) · Added: 2026-11-18

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

## 🧠 Memory & conventions

- **AGENTS.md / CLAUDE.md:** a repo-level instruction file is now a de facto standard across coding agents. Keep it short and link out to detail.
- **Spring AI Session API:** event-sourced short-term memory with compaction for JVM agents. ([spring.io](https://spring.io/team/tzolov))
- **Skills as lazy context:** only the description is always loaded and the body loads on demand. → [Agent skills](../../build/agent-skills/README.md)
