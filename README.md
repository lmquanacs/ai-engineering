# 🧰 AI Engineering Utilities

> A field guide, refreshed every day, for software engineers building with AI. It covers agent skills, MCP servers, model APIs, RAG, architecture, agentic patterns, libraries and the AI engineer career, with a focus on **Python**, **TypeScript** and **Java/Kotlin (Spring Boot)**, plus the main cloud and edge platforms (AWS, Google Cloud, Azure, Vercel and Cloudflare).

<!-- BADGES:START -->
![Last updated](https://img.shields.io/badge/last%20updated-2026--11--25-2563eb)
![Schedule](https://img.shields.io/badge/updates-daily%20~9am%20Brisbane-16a34a)
![Editions](https://img.shields.io/badge/daily%20editions-8-9333ea)
<!-- BADGES:END -->

An automated research agent updates this repo every morning, around **9:00 AM Brisbane time** (AEST, UTC+10). Each run checks releases from primary sources, adds what is worth your attention to the right category, and writes a dated digest. If you only have two minutes, read the digest.

---

## 📰 Today's digest

<!-- TODAY:START -->
### [25 Nov 2026 →](daily/2026/11/2026-11-25.md)

- **Security:** LiteLLM MCP stdio and DBHub MCP 0-days with no patch, plus ECS MCP Server, browser-use and Supergateway fixes; tool-call smuggling research. → [AI security](architecture/security/README.md) · [MCP servers](build/mcp-servers/README.md)
- **Tools:** Antigravity's Auto mode now writes outside the workspace; Codex CLI 0.172.0 starts MCP servers lazily; tip on `permissions.deny` rules for secrets. → [Coding agents](build/coding-agents/README.md) · [Claude Code mastery](build/claude-code/README.md)
- **Platforms:** Bedrock Trusted Access API for Anthropic EFS/EDC; GPT-6.2 and Managed Compute GA in Foundry, with new retirement dates. → [AWS](platforms/aws/README.md) · [Azure](platforms/azure/README.md)
- **Open models:** GLM-5.4 on the Coding Plan only; pin dated DeepSeek Flash IDs on hosts. → [Open-weight model providers](models/open-model-providers/README.md)
<!-- TODAY:END -->

📚 All past editions: [daily/](daily/README.md)

---

## 🗂️ Categories

<!-- CATEGORIES:START -->
### 🛠️ Build: tools you use every day

Agent skills, MCP servers, libraries, model APIs and coding agents: what you install and call while building.

| Category | What you'll find | Best for | Checked |
|---|---|---|---|
| [**Agent skills**](build/agent-skills/README.md) | Popular SKILL.md skills with install commands, by stack: [Python](build/agent-skills/python.md) · [TypeScript](build/agent-skills/typescript.md) · [Java/Kotlin + Spring Boot](build/agent-skills/jvm-spring-kotlin.md) · [starter skills](build/agent-skills/starter-skills/) | Making coding agents follow your team's conventions | daily |
| [**MCP servers**](build/mcp-servers/README.md) | MCP servers for software development, spec changes, tool-budget and security notes | Wiring agents to your tools | daily |
| [**Libraries**](build/libraries/README.md) | Agent and LLM libraries for [Python](build/libraries/python.md) · [TypeScript](build/libraries/typescript.md) · [JVM](build/libraries/jvm.md) | Choosing a framework | daily |
| [**LLM APIs & structured output**](build/llm-apis/README.md) | Provider API features you code against: structured outputs, tool calling, streaming, batch, files, Responses/Messages API changes | Calling models reliably from code | daily |
| [**Coding agents & IDEs**](build/coding-agents/README.md) | Actionable releases of Claude Code, Codex, Cursor, Copilot, Gemini CLI, Antigravity, Devin, Kiro | Keeping your daily tools current | daily |
| [**Claude Code mastery**](build/claude-code/README.md) | Daily tip, key shortcuts, CLAUDE.md, skills, hooks, subagents, headless runs and parallel worktrees: how to use Claude Code well | Mastering Claude Code | daily |
| [**Voice & multimodal**](build/voice-and-multimodal/README.md) | Realtime voice agents, speech-to-text and text-to-speech, vision and document understanding, computer use | Building beyond text chat | weekly (Mon) |
| [**AI-native languages**](build/ai-native-languages/README.md) | Programming languages designed for LLMs and agents, plus the essays debating them | Seeing where tooling is heading | weekly (Mon) |

### 🧠 Models: what to run and what it costs

Which models exist, what they cost, how to serve them, and how to adapt them.

| Category | What you'll find | Best for | Checked |
|---|---|---|---|
| [**LLM news**](models/news/README.md) | New models with API IDs, trends, new techniques, deprecations (about 30 days kept; older items in `archive/`) | Picking and pinning models | daily |
| [**Inference, cost & serving**](models/cost-and-serving/README.md) | Price snapshot, upcoming price changes, cost levers, vLLM and self-hosting | Keeping the bill down | daily |
| [**Open-weight model providers**](models/open-model-providers/README.md) | Z.ai GLM, DeepSeek, Kimi, Qwen, MiniMax and the hosts that serve them (Fireworks, Together, DeepInfra, Baseten, Groq, Cerebras, OpenRouter, Vercel AI Gateway), with SDK wiring | Finding a cheaper or faster alternative to a frontier API | daily |
| [**Fine-tuning & post-training**](models/fine-tuning/README.md) | LoRA/QLoRA, GRPO/RLVR, distillation; TRL, Unsloth, Axolotl | Specialising open models | daily |

### 🏗️ Architecture & production

How the pieces fit together in production. Start at the [architecture hub](architecture/README.md) for reference architectures, the gateway layer, the reliability checklist and decision records.

| Category | What you'll find | Best for | Checked |
|---|---|---|---|
| [**AI system architecture (hub)**](architecture/README.md) | Reference architectures (RAG, agentic backend, coding-agent platform, Spring Boot + AI), LLM gateways, reliability, guardrail and eval placement, decision records | Designing an AI system end to end | weekly (Mon) |
| [**Agentic workflows**](architecture/agentic-workflows/README.md) | Orchestration patterns, harness engineering, evidence on what actually works | Designing agent behaviour | daily |
| [**RAG & retrieval**](architecture/rag-and-retrieval/README.md) | Chunking, hybrid search, reranking, agentic retrieval, GraphRAG; embedding, reranker and parser models; vector databases | Grounding answers in your own data | daily |
| [**Context engineering & memory**](architecture/context-and-memory/README.md) | Compaction, tool-result clearing, agent memory, prompt caching and instruction files | Agents that stay sharp on long tasks | daily |
| [**Agent infrastructure & runtimes**](architecture/agent-infrastructure/README.md) | Sandboxes, durable execution, hosting, agent identity and permissions | Running agents safely | daily |
| [**Evals & observability**](architecture/evals-and-observability/README.md) | Tracing, evals, benchmarks, OpenTelemetry GenAI | Knowing whether it works | daily |
| [**AI security**](architecture/security/README.md) | Prompt injection, guardrails, MCP and skill supply chain, agent permissions, data leakage | Not getting owned, and not leaking data | daily |

### ☁️ Platforms

Cloud and edge platforms for building and running AI: AWS, Google Cloud, Azure, Vercel and Cloudflare.

| Category | What you'll find | Best for | Checked |
|---|---|---|---|
| [**AWS**](platforms/aws/README.md) | Bedrock models, AgentCore, Strands Agents, Kiro, AWS MCP servers, re:Invent | Building and running AI on AWS | daily |
| [**Google Cloud**](platforms/google-cloud/README.md) | Gemini Enterprise Agent Platform (formerly Vertex AI), Agent Engine, ADK, Model Garden, Google Cloud MCP servers | Building and running AI on Google Cloud | daily |
| [**Azure**](platforms/azure/README.md) | Microsoft Foundry, Foundry Agent Service and hosted agents, Microsoft Agent Framework, Azure OpenAI in Foundry Models, Azure MCP servers | Building and running AI on Azure | daily |
| [**Vercel & Cloudflare**](platforms/vercel-cloudflare/README.md) | Vercel AI Gateway, Sandbox and Workflow; Cloudflare Workers AI, AI Gateway, Agents SDK and Sandbox SDK | Shipping TypeScript AI apps and agents at the edge | weekly (Mon) |

### 📚 Learn from others

What shipped, what broke, what's coming, and how to grow as an AI engineer.

| Category | What you'll find | Best for | Checked |
|---|---|---|---|
| [**Successful AI projects**](learn/successful-projects/README.md) | Shipped projects with measurable results (Ramp, Spotify, Coinbase, Stripe…) and open-source projects that took off | Seeing what success looks like | weekly (Mon) |
| [**Case studies & postmortems**](learn/case-studies/README.md) | Lessons and failures from production, plus a weekly 'Learn this week' pick | Learning from others' mistakes | weekly (Mon) |
| [**Research to watch**](learn/research/README.md) | Papers and experiments likely to reach practice | Staying ahead | daily |
| [**AI engineer career & skills**](learn/career/README.md) | What the role expects, a skills map, interview topics, and the best courses, books and talks | Growing into (or hiring for) the role | weekly (Mon) |
<!-- CATEGORIES:END -->

> Have an idea for a category, or spotted a correction? [Open an issue](../../issues/new/choose).

---

## 📖 How to read an entry

Every entry follows the same shape, so you can skim:

```
### Name · short tag                          🆕 = added in the last 7 days
What it is, in one or two sentences.
Why it matters: the practical reason you would care.
Source: primary link · Added: YYYY-MM-DD
```

- **Start here** at the top of each page is the short, curated list. Everything below it is reference.
- Numbers such as stars, installs, prices and benchmark scores are **snapshots** and carry the date they were read. Vendor claims are marked *self-reported*.
- Install commands are copied from the project's own docs or registry listing.

## ⚙️ How it's maintained

| File | Role |
|---|---|
| [`.automation/categories.json`](.automation/categories.json) | **Single source of truth** for categories: group, path, scope, cadence (daily or weekly) |
| [`.automation/DAILY_UPDATE.md`](.automation/DAILY_UPDATE.md) | The playbook the scheduled agent follows each morning |
| [`.automation/sources.md`](.automation/sources.md) | Trusted primary sources per area |
| [`.automation/update_index.py`](.automation/update_index.py) | Regenerates the category tables, group pages, digest index and badges, and expires 🆕 markers |
| [`.automation/check_links.py`](.automation/check_links.py) | Fails if any relative link or anchor is broken |
| [`.automation/templates/`](.automation/templates/) | Templates for a new category page and for a daily digest |

**To add a category:** add an entry to `categories.json`, create `<path>/README.md` from the template, then run `python3 .automation/update_index.py && python3 .automation/check_links.py`. No other files need editing.

## ⚠️ Before you install anything

Agent skills and MCP servers run with **your** permissions. Read the `SKILL.md` and any bundled scripts, prefer official or vendor-maintained servers, use scoped OAuth tokens rather than long-lived keys, and load only the toolsets you need. See [AI security](architecture/security/README.md).
