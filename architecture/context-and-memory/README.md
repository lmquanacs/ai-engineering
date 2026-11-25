# Context engineering & memory

_Last updated: 2026-11-26_

> Deciding what the model sees at each step: compaction, tool-result clearing, memory and caching. Retrieval lives in [RAG & retrieval](../rag-and-retrieval/README.md). Agent quality now depends more on this than on which model you pick.

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

## 🔬 Latest evidence

### Anthropic: the components of agent memory, and "dreaming" · 2026-11-06 (missed earlier) 🆕
Anthropic's write-up of its agent-memory evals. Telling Claude what a memory folder is for, but not how to use it, worked best for recent models; a fixed rule such as "record only failures" removed much of the gain for Opus 5 and Opus 4.7, while older models (Sonnet 4.6) needed explicit prompting to read memory before answering. "Dreaming" is an offline pass in which the agent checks its notes against the original transcripts, corrects wrong notes, builds linked wiki pages and promotes key notes into what loads at session start. On a 350,000-file internal corpus, wiki plus search scored 61% against 53% for search alone and used about 20,000 fewer tokens per question; on multi-document merger questions the wiki scored 87% against 73%, but it gave no clear gain where one document held the answer *(self-reported)*.
**Why it matters:** For memory files (including `CLAUDE.md`/`AGENTS.md`-style notes), state the purpose and let strong models judge salience instead of prescribing rules. Add a periodic pass that re-checks notes against transcripts, and build a linked summary layer only for corpora where answers span several documents.
Source: [Anthropic Engineering: The components of agent memory](https://www.anthropic.com/research/components-of-agent-memory) · Added: 2026-11-26

### Keep past attempts addressable, not summarised; delete unused lessons · arXiv 2611.28244 · 2026-11-20 🆕
This ablation of long-running "autoresearch" harnesses on MLE-Bench and KernelBench, using gpt-oss-120b and two GPT-6 models, tested what agents keep from earlier attempts. Keeping individually retrievable records beat a rolling summary, and context folding did best in all six settings, up to 19.2% above a recency-truncation baseline. For skills and lessons, deleting ones that kept going unused beat merging them or promoting them to standing rules *(self-reported)*.
**Why it matters:** For long agent loops, keep per-attempt records the agent can reopen instead of one ever-growing summary, and prune lessons that never get used before they pile up in `CLAUDE.md`/`AGENTS.md`-style files.
Source: [arXiv 2611.28244](https://arxiv.org/abs/2611.28244) · Added: 2026-11-25

### Compress for a small agent model, cache-friendly: DMC-5 · arXiv 2611.30412 · 2026-11-23 🆕
A general model maintains an append-only log of the full trajectory (so its own prefix stays cacheable), and a specialised agent model acts on a compact view: the compressed history plus recent raw steps, with tool-execution state protected from lossy compression. On AppWorld, OfficeBench and a QA set, the authors report 38.5–57.0% less agent input, 14.5–28.0% lower end-to-end cost and 78–85% compressor cache hits, with task scores 1.0–5.8% higher than no compression *(self-reported)*.
**Why it matters:** This is a pattern for agents built on fine-tuned or self-hosted models that lack cached-input discounts. It also avoids [the prefix-caching cost trap](#-latest-evidence) by never rewriting the compressor's own history.
Source: [arXiv 2611.30412](https://arxiv.org/abs/2611.30412) · Added: 2026-11-25

### Compaction is still lossy, often by corrupting task state · CompAct-Bench · arXiv 2611.25673 · 2026-11-19 🆕
The benchmark compacts context at points inside successful BrowseComp, SWE-bench and internal trajectories, then checks whether the agent can still finish. Claude- and GPT-family compactors did best, but accuracy still fell under aggressive compaction, and many failures came from distorted state, such as open issues summarised as settled.
**Why it matters:** Test compaction prompts on resume-and-finish tasks, not summary quality, and make them list open issues and settled results explicitly.
Source: [arXiv 2611.25673](https://arxiv.org/abs/2611.25673) · Added: 2026-11-21

### A plain log plus grep as agent memory · GrepMem · arXiv 2611.25123 · 2026-11-18 🆕
The agent keeps its full history in an append-only text log and recalls it with a regex-search tool: no embeddings, index or extraction model. With an RL-trained Qwen3.5-9B, the authors report 95–97% on ContextBench against at most 21% for lossy baselines *(self-reported)*.
**Why it matters:** A strong, simple baseline to beat before you build a vector memory store.
Source: [arXiv 2611.25123](https://arxiv.org/abs/2611.25123) · Added: 2026-11-21

### How much memory to inject depends on the model · IBM · arXiv 2611.26361 · 2026-11-19 🆕
IBM distils lessons from an agent's own trajectories into guidelines (shipped in the open-source `altk-evolve`). On AppWorld, strong models kept improving as more guidelines were added, while gpt-oss-120b did better with a selected subset (55.4%) than with all 199 (51.2%) *(self-reported)*.
**Why it matters:** Tune memory budgets per model; "inject everything" can hurt smaller ones.
Source: [arXiv 2611.26361](https://arxiv.org/abs/2611.26361) · Added: 2026-11-21

### GPT-6.2 changes what is cacheable and when reasoning is kept · OpenAI · 2026-11-17 🆕
OpenAI's migration guide says GPT-6.2 places top-level `instructions` after `input`, so reusable instructions must move into a leading `developer` message to be cached. Reasoning items are dropped when an earlier part of the conversation is edited (developer messages or tool-call history), or when the model, user or org changes, which costs quality and tokens. Teams coming from GPT-5.5 or earlier replace `prompt_cache_retention` with `prompt_cache_options.ttl`.
**Why it matters:** This is a second reason, after the cache-pricing study below, to append to history rather than rewrite it. Audit code that edits or compacts earlier turns before switching to GPT-6.2.
Source: [OpenAI migration guide](https://developers.openai.com/api/docs/guides/latest-model?model=gpt-6.2-astra#gpt-6.2-astra-migration-quickstart) · [API changelog](https://developers.openai.com/api/docs/changelog) · Added: 2026-11-20

### Trimming context can raise cost under prefix caching · arXiv 2611.22238 🆕
A study of more than 20,000 coding-agent runs (open models; SWE-bench Verified, SWE-bench, Loc-Bench) tracked uncached input, cached input and output tokens separately. When cached input costs a tenth of uncached input, **removing old observations raised cost by 38–116%** and **adding retrieved code raised it by 33–42%**, with no measurable gain in resolve rate. Without a cache discount, the same removal saved 19–36%. Shorter prompts can also lead to more steps.
**Why it matters:** Tool-result clearing and RAG injection both rewrite the prefix and throw away cache hits. Measure **cost per resolved task** with cache pricing switched on before you adopt a context-trimming trick, and prefer edits that append rather than rewrite. It also means concurrent experiments can share cached prefixes and skew cost comparisons.
Source: [arXiv 2611.22238](https://arxiv.org/abs/2611.22238) · Added: 2026-11-19

---

## 🔎 Retrieval

Embedding, reranker and parser models, vector databases and RAG patterns now have their own page: [RAG & retrieval](../rag-and-retrieval/README.md).

## 🧠 Memory & conventions

- **AGENTS.md / CLAUDE.md:** a repo-level instruction file is now a de facto standard across coding agents. Keep it short and link out to detail.
- **Managed memory stores on AWS:** AgentCore Memory, and since 2026-11-18 Amazon OpenSearch Memory (events in, derived memories out, hybrid search). → [AWS](../../platforms/aws/README.md)
- **Spring AI Session API:** event-sourced short-term memory with compaction for JVM agents. ([spring.io](https://spring.io/team/tzolov))
- **Skills as lazy context:** only the description is always loaded and the body loads on demand. → [Agent skills](../../build/agent-skills/README.md)
