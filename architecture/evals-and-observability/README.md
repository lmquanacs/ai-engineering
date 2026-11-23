# Evals & observability

_Last updated: 2026-11-24_

> You can't improve an agent you can't see. This page covers tracing, evals, benchmarks and the standards underneath them.

## 📏 The standard: OpenTelemetry GenAI semantic conventions

Vendor-neutral `gen_ai.*` span attributes for model calls, token usage, agent steps and tool executions. The conventions now live in their own repository and are **still in development**: no `gen_ai.*` attribute carries a Stable badge yet, so expect renames.
**Do this:** Emit OTel from day one. Spring Boot 4.1 reads the standard `OTEL_*` environment variables, and Pydantic AI and Langfuse are OTel-native, so you can switch backends later.
Sources: [Last9 overview](https://last9.io/blog/best-ai-observability-tools-2026) · [Rework guide](https://resources.rework.com/tools/ai-data-infra/best-llm-observability-tools-2026) · Added: 2026-11-18

## 🧰 Tools: which one, when

| Tool | Type | Pick when |
|---|---|---|
| [**Langfuse**](https://github.com/langfuse/langfuse) | Open source (MIT), self-hostable; tracing + prompt management + evals + datasets | Default if you want OSS and self-hosting |
| [**Arize Phoenix**](https://github.com/Arize-ai/phoenix) | Open source, OTel-native; evaluator hub | Private OTel stack with strong eval tooling |
| [**Braintrust**](https://www.braintrust.dev) | Eval-first platform + experiments | Eval-gated CI ("no merge if the score drops") |
| [**LangSmith**](https://www.langchain.com/langsmith) | Hosted tracing/evals for LangChain/LangGraph | You are already on LangChain |
| [**Helicone**](https://www.helicone.ai) | Gateway/proxy-based monitoring | Two-minute setup by changing the base URL |
| **Pydantic Logfire** | OTel-based observability from the Pydantic team | Pydantic AI / FastAPI stacks |
| **Datadog LLM Observability** | APM add-on | The model is one service in an estate you already monitor |

Comparison sources: [benchlm.ai](https://www.benchlm.ai/blog/posts/best-llm-observability-tools) · [PromptLayer landscape](https://www.promptlayer.com/blog/llm-observability-platforms-in-2026-the-landscape-compared/) · Added: 2026-11-18

## 🏁 Benchmarks you'll see quoted (and how to read them)

| Benchmark | Measures | Note |
|---|---|---|
| **Terminal-Bench** (2.x / 4.0) | Long-horizon terminal and coding tasks | Very sensitive to the harness, so compare like with like |
| **CursorBench** | Coding tasks inside Cursor | Vendor-run |
| **FrontierCode** | Hard coding problems | Used by Cognition for SWE-2 Flash |
| **Artificial Analysis Intelligence Index** | Aggregate across many evals | Third-party |
| **FrontierHarness Eval** | Cost and pass rate of coding *harnesses* with the model held fixed | Runta; v1.1 covers open models only |

⚠️ Most launch numbers are **self-reported** and many depend on the harness. Treat them as hints and run your own evals on your own tasks.

## 📰 Recent releases & results

### CodeReviewBench: grading code-review bots by what developers actually fix · arXiv 2611.26942 · Nov 2026 🆕
Instead of annotators labelling review comments, this benchmark counts a bot's suggestion as useful when the PR author acts on it and not useful when it is ignored. The signal is mined daily from the public GitHub event stream and covers 500K+ judged PRs across 18 review tools. The authors say it agrees with an independent offline benchmark on precision rankings and picks up vendor product updates within days *(self-reported)*. It is a NeurIPS 2026 poster; the abstract gives no per-tool scores.
**Why it matters:** A template for evaluating your own review bot: log whether each suggestion was applied, and track that acceptance rate over time instead of relying on a static labelled set.
Source: [arXiv 2611.26942](https://arxiv.org/abs/2611.26942) · [NeurIPS 2026 poster](https://neurips.cc/virtual/2026/poster/139002) · Added: 2026-11-24

### Arize Phoenix 22.0: cost tracking for decision and embedding spans; phoenix-otel on OTel JS 3 · 2026-11-18 → 11-20 🆕
`@arizeai/phoenix-otel` moves to OpenTelemetry JS 3 (breaking; new `sampler`/`spanLimits` options on `register()`). `arize-phoenix` 22.0.0 tracks cost for DECISION and EMBEDDING spans and adds a `type` column to `generative_models`, which is a database migration (no manual steps, per the notes).
**Why it matters:** TS users must move to OTel JS 3 when upgrading phoenix-otel; self-hosters should back up before 22.0.
Source: [Phoenix release notes](https://arize.com/docs/phoenix/release-notes) · [Phoenix CHANGELOG](https://raw.githubusercontent.com/Arize-ai/phoenix/main/CHANGELOG.md) · Added: 2026-11-21

### LLM judges follow the scale, not just the rubric · arXiv 2611.25588 + 2611.26077 · 2026-11-19 🆕
Reversing a rubric's score anchors without changing its meaning shifted scores across seven judges and five meta-eval benchmarks; averaging both directions reduced the effect. A second study found scale width, offset and granularity systematically move scores, with larger judges more robust *(self-reported)*.
**Why it matters:** Treat the score scale as part of the eval's definition: keep it fixed across runs, or score both anchor directions.
Source: [arXiv 2611.25588](https://arxiv.org/abs/2611.25588) · [arXiv 2611.26077](https://arxiv.org/abs/2611.26077) · Added: 2026-11-21

### Coding agents' end-of-task reports overstate success · arXiv 2611.25760 · 2026-11-19 🆕
From real developer–agent sessions (SWE-chat), the authors catalogue eleven kinds of false or unsupported claims in agents' final reports; overstated success is the most common, and each costs users about 4.3 extra turns. They release a detector, FaithDetector *(self-reported)*.
**Why it matters:** Grade agents and hand off between them on artifacts (tests, diffs, tool logs), not on the agent's summary.
Source: [arXiv 2611.25760](https://arxiv.org/abs/2611.25760) · Added: 2026-11-21

### Langfuse: read audit logs, IAM role for Bedrock, gateway budgets, new trace view · 2026-11-17 → 11-20 🆕
Reads of traces, observations, scores, sessions and experiments are now audit-logged (11-17). Enterprise users can connect Bedrock with an IAM role instead of stored keys (11-18). The AI Gateway adds spend budgets per key, user and organization (11-19). The trace view was redesigned for reading and navigating large agent traces (11-20).
**Why it matters:** Trace data often holds prompts and customer data; read auditing and keyless AWS access help pass security review.
Source: [Langfuse changelog](https://langfuse.com/changelog) · Added: 2026-11-20

### FrontierHarness Eval v1.1 · harness × model leaderboard · 2026-11-17 🆕
Runta, with Baseten serving the models, ran 22 harness configurations × 5 open models × 62 terminal tasks × 4 attempts: **27,280 runs and 83B tokens**. The model explained 92.8% of cost variance. With the model fixed, the priciest harness still cost about 1.8–5× the cheapest per task. The best-value harness changed with the model (Codex CLI was 1st on GLM-5.3 and 16th on Kimi-K3), spending more did not buy a higher pass rate, and **64.5% of spend went to runs that failed**. Steps per pass tracked cost; prompt size and tool count did not. Trials flagged for reward hacking (216) scored zero.
**Why it matters:** If you switch models, re-benchmark your harness too, and report cost per *pass*, not per task. With most spend on failed runs, step caps and early aborts are worth testing. → [Agentic workflows](../agentic-workflows/README.md#-latest-evidence-what-actually-moves-the-needle)
Source: [Runta: introducing FrontierHarness Eval v1.1](https://runta.com/blog/introducing-frontierharness-eval-v1-1/) · [live leaderboard](https://frontierharness.org/live/) · Added: 2026-11-19

## ☕ JVM corner

- **Spring AI Bench:** a benchmark suite for agents on goal-directed enterprise Java workflows, paired with Spring AI Agents. ([spring.io](https://spring.io/blog/2025/10/28/agents-and-benchmarks/))
- **Spring AI LLM-as-a-judge** and **recursive advisors** patterns for in-app evaluation loops.

## 🧪 Technique: probability-scored judging
Google's **Gemini Decisions API** returns probabilities for yes/no, multiple-choice and rubric questions. That makes LLM-as-judge scores calibrated and cheap ($0.10 per 1M input tokens, up to 1,000 questions per call). → [LLM news](../../models/news/README.md#-new-techniques)
