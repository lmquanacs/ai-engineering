# 🧰 AI Engineering Utilities

> A field guide, refreshed every day, for software engineers building with AI. It covers agent skills, MCP servers, new models, agentic patterns and libraries, with a focus on **Python**, **TypeScript** and **Java/Kotlin (Spring Boot)**.

<!-- BADGES:START -->
![Last updated](https://img.shields.io/badge/last%20updated-2026--11--18-2563eb)
![Schedule](https://img.shields.io/badge/updates-daily%20~9am%20Brisbane-16a34a)
![Editions](https://img.shields.io/badge/daily%20editions-1-9333ea)
<!-- BADGES:END -->

An automated research agent updates this repo every morning, around **9:00 AM Brisbane time** (AEST, UTC+10). Each run checks releases from primary sources, adds what is worth your attention to the right category, and writes a dated digest. If you only have two minutes, read the digest.

---

## 📰 Today's digest

<!-- TODAY:START -->
### [18 Nov 2026 · first edition →](daily/2026/11/2026-11-18.md)

- **Models:** Anthropic shipped **Claude Fable 5.2** (paid plans + API), and Google made **Gemini 4 Carbon** generally available. Kimi K3.1 Pro (Moonshot) and Mistral Large 4 both arrived as open weights. → [LLM news](02-llm-news/README.md)
- **Agentic workflows:** New controlled studies find that multi-subagent "committees" barely moved scores but cost up to 8× more. Spec-first TDD loops and end-of-turn goal checks did help. → [Agentic workflows](03-agentic-workflows/README.md)
- **MCP:** The **2026-07-28 stateless spec** is now the baseline. If you run a remote server, migrate it (Spring AI 2.0 supports `protocol=STATELESS`). → [MCP servers](04-mcp-servers/README.md)
- **JVM:** Spring AI 2.0 (Boot 4), Embabel 1.0 and Koog 1.0 are all GA. Spring Boot 4.2 is due this month. → [Libraries · JVM](05-libraries/jvm.md)
- **Action items:** **Claude Sonnet 4.5 retires on 30 Nov 2026**, so pin a newer model ID. **Gemini 4 Argon doubles in price on 1 Dec.** → [Coding agents](07-coding-agents-and-ides/README.md) · [Cost](12-inference-cost-and-serving/README.md)
- **New categories:** [context engineering](11-context-engineering-and-memory/README.md) · [inference & cost](12-inference-cost-and-serving/README.md) · [agent infrastructure](13-agent-infrastructure/README.md) · [case studies](14-case-studies/README.md) · [fine-tuning](15-fine-tuning-and-post-training/README.md)
<!-- TODAY:END -->

📚 All past editions: [daily/](daily/README.md)

---

## 🗂️ Categories

| # | Category | What you'll find | Best for |
|---|---|---|---|
| 01 | [**Agent skills**](01-agent-skills/README.md) | Popular `SKILL.md` skills with descriptions and install commands, split by stack: [Python](01-agent-skills/python.md) · [TypeScript](01-agent-skills/typescript.md) · [Java/Kotlin + Spring Boot](01-agent-skills/jvm-spring-kotlin.md) · [starter skills you can copy](01-agent-skills/starter-skills/) | Making Claude Code / Codex / Cursor / Copilot write code the way your team does |
| 02 | [**LLM news**](02-llm-news/README.md) | New models (with API IDs), trends, new techniques, deprecations | Picking and pinning models |
| 03 | [**Agentic workflows**](03-agentic-workflows/README.md) | Orchestration patterns, harness engineering, what the evidence says works | Designing agent systems |
| 04 | [**MCP servers**](04-mcp-servers/README.md) | MCP servers for software development, spec changes, security notes | Wiring agents to your tools |
| 05 | [**Libraries**](05-libraries/README.md) | Agent/LLM libraries for [Python](05-libraries/python.md) · [TypeScript](05-libraries/typescript.md) · [JVM](05-libraries/jvm.md) | Choosing a framework |
| 06 | [**AI-native languages**](06-ai-native-languages/README.md) | Programming languages designed for LLMs and agents | Watching where tooling is heading |
| 07 | [**Coding agents & IDEs**](07-coding-agents-and-ides/README.md) | Release notes that matter from Claude Code, Codex, Cursor, Copilot, Gemini CLI, Devin… | Keeping your daily tools current |
| 08 | [**Evals & observability**](08-evals-and-observability/README.md) | Tracing, evals, benchmarks, OpenTelemetry GenAI | Running agents in production |
| 09 | [**AI security**](09-ai-security/README.md) | Prompt injection, MCP/skill supply chain, agent permissions | Not getting owned |
| 10 | [**Research to watch**](10-research-to-watch/README.md) | Papers and experiments likely to reach practice | Staying ahead |
| 11 | [**Context engineering & memory**](11-context-engineering-and-memory/README.md) | Compaction, tool-result clearing, memory, caching, embeddings/rerankers/parsers | Agents that stay sharp on long tasks |
| 12 | [**Inference, cost & serving**](12-inference-cost-and-serving/README.md) | Price snapshot and upcoming price changes, cost levers, vLLM and self-hosting | Keeping the bill down |
| 13 | [**Agent infrastructure & runtimes**](13-agent-infrastructure/README.md) | Sandboxes, durable execution, hosting, agent identity and permissions | Running agents safely in production |
| 14 | [**Case studies & postmortems**](14-case-studies/README.md) · _weekly_ | How real teams shipped agents and what broke, plus a weekly "Learn this week" pick | Learning from others' mistakes |
| 15 | [**Fine-tuning & post-training**](15-fine-tuning-and-post-training/README.md) | LoRA/QLoRA, GRPO/RLVR, distillation; TRL, Unsloth, Axolotl | Specialising open models |

> Categories 07–15 go beyond the original brief. 06 (AI-native languages) and 14 (case studies) are checked weekly on Mondays; everything else is checked daily. Ideas for more categories are welcome: [open an issue](../../issues/new/choose).

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
- Numbers such as stars, installs and benchmark scores are **snapshots** and carry the date they were read. Vendor benchmark claims are marked *self-reported*.
- Install commands are copied from the project's own docs or registry listing.

## ⚙️ How the daily update works

- A scheduled agent runs once a day at about 9 AM Brisbane time. It follows the playbook in [`.automation/DAILY_UPDATE.md`](.automation/DAILY_UPDATE.md) and checks the sources in [`.automation/sources.md`](.automation/sources.md).
- It writes `daily/YYYY/MM/YYYY-MM-DD.md`, merges new items into the category pages (removing duplicates), refreshes the block above, and commits as `chore(daily): YYYY-MM-DD`.
- Fast-moving pages, such as LLM news, keep about 30 days on the main page. Older items move to an `archive/` file each month.

## ⚠️ Before you install anything

Agent skills and MCP servers run with **your** permissions. Read the `SKILL.md` and any bundled scripts, prefer official or vendor-maintained servers, use scoped OAuth tokens rather than long-lived keys, and load only the toolsets you need. See [AI security](09-ai-security/README.md).

## 🤝 Contributing

Spotted something wrong, outdated or missing? [Open an issue](../../issues/new/choose) and the next daily run will pick it up, or send a PR that follows the entry format above.
