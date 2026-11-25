# Evals & observability

_Last updated: 2026-11-26_

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
SWE-bench scores also carry test noise: a 2026-11-24 study flags 23% of Verified and 35% of Pro tasks as having overspecified tests → [Research](../../learn/research/README.md).

## 📰 Recent releases & results

### Braintrust Patterns GA; Patterns and Loop start using credits on 2026-12-07 · 2026-11-23 (missed earlier) 🆕
Patterns, which mines agent traces and logs for recurring problems (user frustration, unfinished workflows, unnecessary model calls, cost or latency shifts) even when calls succeed, is now generally available. Loop's GitHub and external MCP integrations are GA too. Model credits are renamed **Braintrust credits**, one balance for Patterns, Loop, Topics and built-in inference; Starter includes 10 a month and Pro 100. With your own provider key, the provider bills inference but Braintrust still charges credits for its own work.
**Why it matters:** **Billing for Patterns and Loop starts 2026-12-07** on Starter and Pro with no action needed. Enterprise admins must accept the updated terms in Billing by the end of 2026-12-06 to opt in. Check scheduled Patterns rules before then if you don't want them drawing credits.
Source: [Braintrust blog: Patterns](https://www.braintrust.dev/blog/patterns) · [Braintrust pricing](https://www.braintrust.dev/pricing) · Added: 2026-11-26

### Agent security benchmark verdicts move with the hash seed and tool order · TARE · arXiv 2611.30259 · 2026-11-23 🆕
On Agent Security Bench, changing only the Python hash seed changed up to 17% of an agent's verdicts. The seed acts through tool order, and sorting the tool list instead of reverse-sorting it raised attack success by up to 19 points, because the benchmark's naming puts attacker tools first. Reordering the same evidence flipped six of seven LLM judges' decisions on 17–91% of 98 proposed actions. Across 18 agent–defence pairs, the authors' worst-case test could attribute effects to only two of three defences, one of them in opposite directions on two agents. In those decreases, 35–69% of the "stopped" attacks simply ended without any tool call *(self-reported)*.
**Why it matters:** Before trusting a "defence X cuts ASR by N points" claim, or your own, rerun it with shuffled tool and evidence order and different seeds, and report the spread.
Source: [arXiv 2611.30259](https://arxiv.org/abs/2611.30259) · Added: 2026-11-26

### Langfuse Topics (public beta): cluster production traces by intent, sentiment, outcome and issue · 2026-11-24 🆕
Topics summarises each finished trace from four angles (intent, sentiment, outcome, issues), embeds the summaries, and clusters and names them. You can run it as daily-rebuilt live maps over filtered, sampled traffic, or as one-off snapshots, for example to compare dataset coverage with production. Agents can query topics through the API, MCP and CLI. It runs on models from your own LLM connections, and each facet summary is one billable unit. It is available on Langfuse Cloud and self-hosted Langfuse v4.
**Why it matters:** It is a cheap way to find failure modes you aren't tracking, then filter to those traces and turn them into evaluators or dataset items. Set a sample rate first, because every summary is a model call on your key.
Source: [Langfuse changelog](https://langfuse.com/changelog/2026-11-24-topics) · Added: 2026-11-25

### Judge error rates measured once can mis-rank agents · arXiv 2611.30742 · 2026-11-23 🆕
If an LLM judge's errors depend on the trajectory, and agents produce different kinds of trajectories, correcting every agent's score with one judge error rate is biased. In the authors' semi-synthetic four-agent benchmark, that scalar correction never recovered the true ranking in 250 runs. A small random human audit combined with AIPW estimation kept maximum bias below 0.003 *(self-reported)*.
**Why it matters:** When you rank agents or harnesses with an LLM judge, have humans label a random sample of each agent's trajectories, rather than reusing one calibration set across all of them.
Source: [arXiv 2611.30742](https://arxiv.org/abs/2611.30742) · Added: 2026-11-25

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
