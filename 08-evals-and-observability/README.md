# 08 · Evals & observability

_Last updated: 2026-11-18_

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

⚠️ Most launch numbers are **self-reported** and many depend on the harness. Treat them as hints and run your own evals on your own tasks.

## ☕ JVM corner

- **Spring AI Bench:** a benchmark suite for agents on goal-directed enterprise Java workflows, paired with Spring AI Agents. ([spring.io](https://spring.io/blog/2025/10/28/agents-and-benchmarks/))
- **Spring AI LLM-as-a-judge** and **recursive advisors** patterns for in-app evaluation loops.

## 🧪 Technique: probability-scored judging
Google's **Gemini Decisions API** returns probabilities for yes/no, multiple-choice and rubric questions. That makes LLM-as-judge scores calibrated and cheap ($0.10 per 1M input tokens, up to 1,000 questions per call). → [LLM news](../02-llm-news/README.md#-new-techniques)
