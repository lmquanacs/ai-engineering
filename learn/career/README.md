# AI engineer career & skills

_Last updated: 2026-11-23_

> What the AI engineer role asks for, how to build those skills, and where to learn them. Useful whether you're moving into the role, levelling up in it, or hiring for it.

## 🧭 Skills map

Each row links to the part of this repo that keeps it current.

| Skill area | What "good" looks like | Where to keep up |
|---|---|---|
| **Software engineering first** | Production code, APIs, testing, CI, cost awareness: AI features are still software | [Libraries](../../build/libraries/README.md) · [Coding agents](../../build/coding-agents/README.md) · [Claude Code mastery](../../build/claude-code/README.md) |
| **Calling models well** | Structured outputs, tool calling, streaming, picking and pinning models | [LLM APIs](../../build/llm-apis/README.md) · [LLM news](../../models/news/README.md) |
| **Context & retrieval** | Deciding what the model sees; RAG that you can measure | [Context engineering](../../architecture/context-and-memory/README.md) · [RAG & retrieval](../../architecture/rag-and-retrieval/README.md) |
| **Agents** | Orchestration patterns, tools via MCP, knowing when *not* to use an agent | [Agentic workflows](../../architecture/agentic-workflows/README.md) · [MCP servers](../../build/mcp-servers/README.md) |
| **Evals** | A labelled test set, automated scoring, regression checks on every change | [Evals & observability](../../architecture/evals-and-observability/README.md) |
| **Production & cost** | Gateways, fallbacks, rate limits, caching, cost per task | [Architecture hub](../../architecture/README.md) · [Inference & cost](../../models/cost-and-serving/README.md) |
| **Security** | Prompt injection, least-privilege tools, data handling | [AI security](../../architecture/security/README.md) |
| **Adapting models** | Knowing when fine-tuning beats prompting and retrieval, and how to evaluate it | [Fine-tuning](../../models/fine-tuning/README.md) |
| **Learning from others** | Reading postmortems and measured results, not launch posts | [Case studies](../case-studies/README.md) · [Successful projects](../successful-projects/README.md) |

## 🎯 Interview topics that keep coming up

- Design a RAG system for a given corpus, and how you would evaluate it.
- Design an agent with tools: failure modes, permissions, cost limits, human approval.
- Make an LLM feature reliable: retries, fallbacks, structured output, timeouts.
- Measure quality: build an eval set, choose metrics, use LLM-as-judge carefully.
- Cut cost or latency by half without losing quality.
- Defend against prompt injection in a feature that reads user or web content.

---

## 🗞️ Latest

<!-- newest first: writing on the role, hiring trends with named sources, courses, books, talks -->

### Runway: what engineers do once agents ship most of the code · 2026-11-20 🆕
Runway's write-up on handing its delivery pipeline to agents describes how the engineering job changed. Each time agents sped up one stage, the bottleneck moved to the next (review, then approval, then QA, then coordination). Engineers now spend their time on enabling work: removing access and infrastructure blockers, making codebases easier for agents to work in, and measuring friction.
**Why it matters:** It shows, with measurements, which skills matter in an "AI-native" engineering team: deciding how much autonomy to allow by risk, choosing success criteria before reading results, and designing safety rails from real failures. Numbers: [Successful projects](../successful-projects/README.md).
Source: [Runway engineering](https://runway.com/news/engineering/building-a-software-factory) · Added: 2026-11-23

### AI Engineer Code Summit 2026 talks · free recordings 🆕
The Code Summit (San Francisco, 2026-11-10 to 2026-11-12) ran two days of single-track talks on coding agents, and both full days are on YouTube.
**Why it matters:** It is free, current material on building, evaluating and shipping coding agents, from the conference series this page tracks.
Sources: [Event page](https://www.ai.engineer/code) · [Day 1 recording](https://www.youtube.com/watch?v=ZZ19zhYnDKY) · [Day 2 recording](https://www.youtube.com/watch?v=y9JtCCZP2MQ) · Added: 2026-11-23

## 📚 Reference

<!-- older or background entries -->
