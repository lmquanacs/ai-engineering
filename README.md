# 🧰 AI Engineering Utilities

> A field guide, refreshed every day, for software engineers building with AI. It covers agent skills, MCP servers, models, architecture, agentic patterns and libraries, with a focus on **Python**, **TypeScript** and **Java/Kotlin (Spring Boot)**, plus AWS.

<!-- BADGES:START -->
![Last updated](https://img.shields.io/badge/last%20updated-2026--11--19-2563eb)
![Schedule](https://img.shields.io/badge/updates-daily%20~9am%20Brisbane-16a34a)
![Editions](https://img.shields.io/badge/daily%20editions-2-9333ea)
<!-- BADGES:END -->
[![License: MIT](https://img.shields.io/badge/license-MIT-blue)](LICENSE)
[![PRs welcome](https://img.shields.io/badge/PRs-welcome-brightgreen)](CONTRIBUTING.md)
[![Atom feed](https://img.shields.io/badge/feed-Atom-f26522)](https://raw.githubusercontent.com/lmquanacs/ai-engineering/main/feed.xml)
[![Buy me a coffee](https://img.shields.io/badge/buy%20me%20a%20coffee-support-ffdd00?logo=buymeacoffee&logoColor=black)](https://buymeacoffee.com/lmquanacs8)

An automated research agent updates this repo every morning, around **9:00 AM Brisbane time** (AEST, UTC+10). Each run checks releases from primary sources, adds what is worth your attention to the right category, and writes a dated digest. If you only have two minutes, read the digest.

**Stay current:** ⭐ star the repo · 👀 **Watch → Custom → Releases** for a weekly roll-up · 📡 subscribe to the [Atom feed](https://raw.githubusercontent.com/lmquanacs/ai-engineering/main/feed.xml) for every daily edition.

---

## 📰 Today's digest

<!-- TODAY:START -->
### [19 Nov 2026 →](daily/2026/11/2026-11-19.md)

- **Security:** Microsoft's `agent-framework` 1.26.1/1.26.2 on PyPI shipped a credential stealer (pin 1.26.0 and rotate secrets), and the reference `mcp-server-git` fixes three code-execution paths. → [AI security](architecture/security/README.md)
- **Models:** OpenAI **GPT-6.2 Astra** ($8/$40) and **GPT-6.2 Sol** are on the API, Codex and Bedrock, and background mode is 30–40% cheaper. → [LLM news](models/news/README.md) · [Cost](models/cost-and-serving/README.md)
- **Tools:** upgrade Claude Code to ≥ 2.1.325; `codex exec` now needs `--trust` for repo config; the MCP TypeScript SDK has four CVEs, fixed in 1.32.0. → [Coding agents](build/coding-agents/README.md) · [MCP servers](build/mcp-servers/README.md)
- **AWS:** new AgentCore runtimes default to V2; Kiro CLI 3.5 adds org sign-in for MCP. → [AWS](platforms/aws/README.md)
- **Action items:** Claude Sonnet 4.5 retires on **30 Nov** · Gemini 4 Argon doubles on **1 Dec** · Pydantic AI ≥ 2.60 changes how tool retries are reported. → [Libraries](build/libraries/README.md)
<!-- TODAY:END -->

📚 All past editions: [daily/](daily/README.md)

---

## 🗂️ Categories

<!-- CATEGORIES:START -->
### 🛠️ Build: tools you use every day

Agent skills, MCP servers, libraries and coding agents: what you install and use while building.

| Category | What you'll find | Best for | Checked |
|---|---|---|---|
| [**Agent skills**](build/agent-skills/README.md) | Popular SKILL.md skills with install commands, by stack: [Python](build/agent-skills/python.md) · [TypeScript](build/agent-skills/typescript.md) · [Java/Kotlin + Spring Boot](build/agent-skills/jvm-spring-kotlin.md) · [starter skills](build/agent-skills/starter-skills/) | Making coding agents follow your team's conventions | daily |
| [**MCP servers**](build/mcp-servers/README.md) | MCP servers for software development, spec changes, tool-budget and security notes | Wiring agents to your tools | daily |
| [**Libraries**](build/libraries/README.md) | Agent and LLM libraries for [Python](build/libraries/python.md) · [TypeScript](build/libraries/typescript.md) · [JVM](build/libraries/jvm.md) | Choosing a framework | daily |
| [**Coding agents & IDEs**](build/coding-agents/README.md) | Actionable releases of Claude Code, Codex, Cursor, Copilot, Gemini CLI, Antigravity, Devin, Kiro | Keeping your daily tools current | daily |
| [**AI-native languages**](build/ai-native-languages/README.md) | Programming languages designed for LLMs and agents, plus the essays debating them | Seeing where tooling is heading | weekly (Mon) |

### 🧠 Models: what to run and what it costs

Which models exist, what they cost, how to serve them, and how to adapt them.

| Category | What you'll find | Best for | Checked |
|---|---|---|---|
| [**LLM news**](models/news/README.md) | New models with API IDs, trends, new techniques, deprecations (about 30 days kept; older items in `archive/`) | Picking and pinning models | daily |
| [**Inference, cost & serving**](models/cost-and-serving/README.md) | Price snapshot, upcoming price changes, cost levers, vLLM and self-hosting | Keeping the bill down | daily |
| [**Fine-tuning & post-training**](models/fine-tuning/README.md) | LoRA/QLoRA, GRPO/RLVR, distillation; TRL, Unsloth, Axolotl | Specialising open models | daily |

### 🏗️ Architecture & production

How the pieces fit together in production. Start at the [architecture hub](architecture/README.md) for reference architectures, the gateway layer, the reliability checklist and decision records.

| Category | What you'll find | Best for | Checked |
|---|---|---|---|
| [**AI system architecture (hub)**](architecture/README.md) | Reference architectures (RAG, agentic backend, coding-agent platform, Spring Boot + AI), LLM gateways, reliability, guardrail and eval placement, decision records | Designing an AI system end to end | weekly (Mon) |
| [**Agentic workflows**](architecture/agentic-workflows/README.md) | Orchestration patterns, harness engineering, evidence on what actually works | Designing agent behaviour | daily |
| [**Context engineering & memory**](architecture/context-and-memory/README.md) | Compaction, tool-result clearing, memory, caching; embeddings, rerankers, parsers | Agents that stay sharp on long tasks | daily |
| [**Agent infrastructure & runtimes**](architecture/agent-infrastructure/README.md) | Sandboxes, durable execution, hosting, agent identity and permissions | Running agents safely | daily |
| [**Evals & observability**](architecture/evals-and-observability/README.md) | Tracing, evals, benchmarks, OpenTelemetry GenAI | Knowing whether it works | daily |
| [**AI security**](architecture/security/README.md) | Prompt injection, MCP and skill supply chain, agent permissions | Not getting owned | daily |

### ☁️ Platforms

Cloud-specific services for building and running AI. Add Azure or Google Cloud here when needed.

| Category | What you'll find | Best for | Checked |
|---|---|---|---|
| [**AWS**](platforms/aws/README.md) | Bedrock models, AgentCore, Strands Agents, Kiro, AWS MCP servers, re:Invent | Building and running AI on AWS | daily |

### 📚 Learn from others

What shipped, what broke, and what's coming.

| Category | What you'll find | Best for | Checked |
|---|---|---|---|
| [**Successful AI projects**](learn/successful-projects/README.md) | Shipped projects with measurable results (Ramp, Spotify, Coinbase, Stripe…) and open-source projects that took off | Seeing what success looks like | weekly (Mon) |
| [**Case studies & postmortems**](learn/case-studies/README.md) | Lessons and failures from production, plus a weekly 'Learn this week' pick | Learning from others' mistakes | weekly (Mon) |
| [**Research to watch**](learn/research/README.md) | Papers and experiments likely to reach practice | Staying ahead | daily |
<!-- CATEGORIES:END -->

> Spotted something outdated, or know a tool that belongs here? [Open an issue](../../issues/new/choose) or send a PR. See [Contributing](#-contributing).

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
| [`feed.xml`](feed.xml) | Atom feed of the latest digests, written by `update_index.py` |
| [`.automation/GROWTH.md`](.automation/GROWTH.md) | Daily share kit, share card and community loop for the scheduled agent (drafts only, never posts) |
| [`.automation/make_card.py`](.automation/make_card.py) | Renders the 1200×630 share card for a digest |
| [`.automation/weekly_release.py`](.automation/weekly_release.py) | Notes for the Monday GitHub release that rolls up the week's digests |
| [`.automation/templates/`](.automation/templates/) | Templates for a new category page and for a daily digest |

**To add a category:** add an entry to `categories.json`, create `<path>/README.md` from the template, then run `python3 .automation/update_index.py && python3 .automation/check_links.py`. No other files need editing.

## ⚠️ Before you install anything

Agent skills and MCP servers run with **your** permissions. Read the `SKILL.md` and any bundled scripts, prefer official or vendor-maintained servers, use scoped OAuth tokens rather than long-lived keys, and load only the toolsets you need. See [AI security](architecture/security/README.md).

## 🤝 Contributing

The daily agent is fast but not infallible, and people who use these tools every day catch what it misses. The most useful contributions are small:

- **Fix something outdated:** a version, price, model ID or install command that no longer matches its source.
- **Suggest an item** that would change an engineer's decision (adopt, upgrade, migrate, avoid).
- **Propose a category**, such as Azure or Google Cloud under ☁️ Platforms.

Read [CONTRIBUTING.md](CONTRIBUTING.md) for the entry format and the bar for inclusion, then [open an issue](../../issues/new/choose) or a pull request.

## ☕ Support

This guide is free and always will be. If it saves you time, you can [buy me a coffee](https://buymeacoffee.com/lmquanacs8) to help cover the research runs. Support never affects what gets listed or how it's ranked.

## 📄 License

[MIT](LICENSE). Use it, fork it, share it; a link back is appreciated.
