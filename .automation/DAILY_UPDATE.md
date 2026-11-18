# Daily update playbook

This file is the **source of truth** for the scheduled research agent that updates this repository every day at about 09:00 Australia/Brisbane (UTC+10, no DST). Humans can follow it too.

## 0. Setup
1. Work on the default branch `main` in `lmquanacs/ai-engineering`.
2. Set `TODAY` to today's date **in Australia/Brisbane** (`TZ=Australia/Brisbane date +%F`). Use it for every date written.
3. Read `README.md`, this playbook, `.automation/sources.md`, the latest file in `daily/`, and every category page you are about to edit.
4. Window: look for items published since the previous digest's date (normally 24–48h). If a run was missed, cover the whole gap.

## 1. Research (per category)
Use web search and fetch. Prefer **primary sources** (vendor changelogs, release notes, official blogs, GitHub releases, papers) over aggregators; use aggregators only to *discover* items, then confirm them at the source.

| Category | Look for | Typical sources |
|---|---|---|
| 01 Agent skills | Newly popular or rising skills for Python, TypeScript, Java/Kotlin + Spring Boot (incl. Gradle Kotlin DSL); official skills from vendors/frameworks | skills.sh, claudemarketplaces.com/best, skillselion, GitHub trending, vendor blogs |
| 02 LLM news | New models (with API IDs, status, pricing), deprecations/retirements, trends, new techniques | Provider release notes/changelogs, ThursdAI, release trackers |
| 03 Agentic workflows | New patterns, evidence (ablations, benchmarks), orchestration features in tools | Anthropic/OpenAI/Google engineering blogs, arXiv, Latent Space, Spring blog |
| 04 MCP servers | New official/vendor servers, notable community servers, spec/SDK changes, MCP CVEs | modelcontextprotocol blog, registry, GitHub releases |
| 05 Libraries | Releases of Pydantic AI, LangGraph, AI SDK, Mastra, Spring AI, Embabel, Koog, LangChain4j, MCP SDKs; notable new libs | GitHub releases, spring.io blog, package registries |
| 06 AI-native languages | New languages/releases for LLM/agent use, notable essays | GitHub, HN, InfoQ |
| 07 Coding agents & IDEs | Actionable releases of Claude Code, Codex, Cursor, Copilot, Gemini CLI, Antigravity, Devin, JetBrains AI, Kiro | Official changelogs, releases.sh |
| 08 Evals & observability | Tool releases, OTel GenAI convention changes, new benchmarks | Vendor blogs, OTel repo |
| 09 AI security | Prompt-injection research, agent/MCP/skill CVEs, security fixes in agent tools | Changelogs, OWASP, security blogs, arXiv |
| 10 Research to watch | Papers/experiments likely to reach practice within a year | arXiv, lab blogs |
| 11 Context engineering & memory | Compaction/memory/caching techniques and APIs, embedding/reranker/parser releases, retrieval patterns | Anthropic/OpenAI/Google docs, Hugging Face, Cohere/Jina/NVIDIA blogs, MTEB/ViDoRe |
| 12 Inference, cost & serving | **Price changes** (update the snapshot table and "price changes coming up"), caching/batch discount changes, vLLM/SGLang/llama.cpp/Ollama releases, self-hosting news | Provider pricing pages, pricing trackers, vLLM releases/blog |
| 13 Agent infrastructure & runtimes | Sandbox/runtime releases and pricing, durable execution for agents, agent hosting, agent identity/auth | E2B, Daytona, Modal, Vercel, Cloudflare, Temporal, Trigger.dev blogs |
| 14 Case studies & postmortems | **Weekly (Mondays):** 1–3 new production write-ups with transferable lessons; rotate the "Learn this week" pick. Other days, only exceptional postmortems. | Company engineering blogs, ZenML LLMOps database, conference talks |
| 15 Fine-tuning & post-training | TRL/Unsloth/Axolotl/LLaMA-Factory/verl releases, new methods (GRPO/RLVR/distillation), open datasets | Hugging Face blog, GitHub releases, arXiv |

| 16 AWS | Bedrock model availability (IDs, CRIS profiles, regions, pricing), AgentCore releases, Strands SDK releases, Kiro changes (and the Q Developer migration), AWS MCP servers, Spring AI ↔ AWS integrations | AgentCore release notes, AWS What's New, AWS ML blog (monthly "ICYMI"), AWS News Blog, Kiro changelog, Strands releases, awslabs/mcp |

**Cadence:** check 06 (AI-native languages) and 14 (case studies) on **Mondays** only, unless something major lands. Check all other categories daily.

**AWS re:Invent week (2026: 30 Nov – 4 Dec, Las Vegas; Brisbane runs on 1–5 Dec and the Monday after):** add a `## 🎰 AWS re:Invent` section near the top of each digest with the developer-relevant launches from the previous day's keynotes and announcements, and fold them into `16-aws/` and any other category they affect, such as new Bedrock models in 02 or AgentCore changes in 13. Skip marketing-only announcements. In other years, find the dates on AWS's event page and apply the same rule.

**Selection bar:** include an item only if a working engineer would change a decision because of it (adopt, upgrade, migrate, avoid, try). Aim for 0–5 items per category per day. "Nothing notable today" is a valid outcome; never pad.

## 2. Write entries
Use this exact shape on category pages (newest first within its section):

```markdown
### Name · short tag 🆕
One or two sentences on what it is, in your own words.
**Why it matters:** the practical reason an engineer cares.
<optional fenced install/config snippet, copied from official docs>
Source: [primary link](url) · <metric snapshot (date)> · Added: YYYY-MM-DD
```

Rules:
- **Deduplicate:** `grep -ri` the repo for the name and URL first. If an item exists, update it in place (version, date, metric) instead of adding a duplicate.
- **Accuracy:** never invent numbers, versions, API IDs or install commands. Copy commands from the official source. Label vendor benchmark claims *(self-reported)*. Write dates as `YYYY-MM-DD`.
- **Copyright:** paraphrase; at most one short quote (<15 words) per source; never paste articles.
- **Safety:** do not recommend skills or MCP servers you could not trace to a real repository; flag anything that asks for broad credentials.
- **🆕 marker:** add it to new entries; remove it from entries whose `Added` date is more than 7 days before `TODAY`.
- Update the page's `_Last updated: YYYY-MM-DD_` line when you edit it.

## 3. Housekeeping
- **LLM news:** keep about 30 days in the "New models" table. Move older rows (and stale trend or technique entries) to `02-llm-news/archive/YYYY-MM.md`, grouped by the month of the item's date.
- **Action items tables** (LLM news, coding agents): remove rows whose deadline has passed and add new deprecations or retirements.
- If a category grows past about 25 entries, move the least relevant ones into a `## Reference` section at the bottom, or to an `archive.md` in that folder.
- **Monday runs:** re-check the "Start here" picks on each page against current popularity and quality, and refresh star/install snapshots for those picks.
- **First run of each month:** add a short "Last month in review" section at the top of that day's digest.

## 4. Daily digest
Create `daily/YYYY/MM/TODAY.md` with:
1. A title (`# Daily digest · <Weekday> <D Mon YYYY>`) and a back-link line.
2. **TL;DR:** 3–6 bullets, most important first; include any action items.
3. One `##` section per category **that has news**, using the same numbering as the folders. Keep bullets short and link to the category page anchors. Omit empty categories or list them in a final line: "No notable updates: 06, 10".
4. The footer note used in previous editions.

Then update `daily/README.md`: add the edition at the top of the correct year/month inside the `INDEX` markers.

## 5. README refresh
- Replace the content between `<!-- TODAY:START -->` and `<!-- TODAY:END -->` with a link to today's digest and 3–5 highlight bullets, each linking to its category page.
- Update the badges between `<!-- BADGES:START -->` and `<!-- BADGES:END -->`: the last-updated date (`YYYY--MM--DD` with doubled dashes in shields.io URLs) and the edition count (number of files under `daily/`).

## 6. Validate
- Every relative link you added resolves: run `python3 .automation/check_links.py` and fix any failures.
- Markdown tables have consistent column counts.
- `git diff --stat` looks proportional, with no accidental mass deletions.

## 7. Commit & push
```bash
git add -A
git commit -m "chore(daily): TODAY update" -m "<one line per category touched>"
git push origin main
```
If the push is rejected because `main` moved, run `git pull --rebase origin main`, resolve conflicts (keep both sides' entries and deduplicate), and push again once. If it still fails, stop and report the error. **Never force-push.**

## 8. Report
Finish with a short summary: the digest path, the number of items added per category, any action items, and anything you could not verify.
