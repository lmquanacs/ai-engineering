# LLM news: models, trends, techniques

_Last updated: 2026-11-18 · This page keeps about 30 days; older items move to [archive/](archive/)_

> Only what changes a builder's decision. Every model row carries its **API ID** and a primary source. Benchmark numbers are vendor claims unless marked otherwise.

## ⚡ Action items

| Deadline | What | Do this |
|---|---|---|
| **2026-11-30** | Claude Sonnet 4.5 retirement | Move pinned `claude-sonnet-4-5*` IDs to `claude-sonnet-5-5` or `claude-haiku-5-5` and re-run your evals. ([source](https://developertoolkit.ai/en/resources/whats-new.md)) |
| ongoing | Short model lifetimes | DeepSeek-V4-Flash went from beta (Jul 31) to retired (Sep 10), and Gemini 3.7 Flash was deprecated eight weeks after release. Pin dated IDs and watch deprecation trackers. ([source](https://nhimg.org/llm-release-tracker)) |

---

## 🆕 New models (Sep → Nov 2026)

Newest first. Status is as of release.

| Date | Provider | Model | API ID | Status | Source |
|---|---|---|---|---|---|
| 2026-11-12 | Google | Gemini 4 Hydrogen (fast tier, ~2.5× faster than Gemini 3.8 Flash per Google) | `gemini-4-hydrogen` | Released (Vertex) | [Vertex model versions](https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/model-versions) |
| 2026-11-10 → 12 | Google | Gemini 4 Carbon (top model), now GA; 60.4% CursorBench (high effort, self-reported) | `gemini-4-carbon` | GA; intro pricing until Nov 30 | [Google blog](https://blog.google/innovation-and-ai/models-and-research/gemini-models/gemini-4-carbon-now-available/) |
| 2026-11-09 | Anthropic | **Claude Fable 5.2**; $8/$40 per 1M in/out tokens (20% cheaper than 5.1) | `claude-fable-5-2` | GA (paid plans + API) | [Release notes](https://platform.claude.com/docs/en/release-notes/overview) |
| 2026-11-09 | Anthropic | Claude Mythos 5.2 (same underlying model as Fable; Fable adds extra biology and cyber safeguards) | `claude-mythos-5-2` | Restricted to verified orgs | [Release notes](https://platform.claude.com/docs/en/release-notes/overview) |
| 2026-11-05 | Mistral AI | Mistral Large 4, **open weights** | `mistral-large-4` | GA | [Model card](https://docs.mistral.ai/models/mistral-large-4-0.md) |
| 2026-11-05 | Moonshot AI | Kimi K3.1 Pro, **open weights**: 2.8T MoE, 104B active, 1M context, image input; licence has conditions for large products | — | Open weights | [Hugging Face](https://huggingface.co/moonshotai/Kimi-K3.1-Pro) |
| 2026-11-05 | Cognition | SWE-2 Flash: fast, cheap coding model at ~⅕ the cost of SWE-2 | — | Released | [Cognition blog](https://cognition.com/blog/swe-2-flash) |
| 2026-11-05 | Ricursive | Ripple-65B Preview: dense 65B trained from scratch, Apache 2.0; 80.5% TerminalBench 2.1 (self-reported) | — | Open weights | [Blog](https://www.ricursive.com/ripple) |
| 2026-11-05 | Tencent | Hy4: first Hy model with vision + computer use, 1M context; weights promised later | — | API (OpenRouter) | [Blog](https://hy.tencent.ai/research/hy4?langVersion=en) |
| 2026-11-05 | OpenAI | GPT-6 Cyber: security model for the Daybreak program | `gpt-6-cyber` | Restricted | [OpenAI](https://openai.com/index/introducing-gpt-6-cyber/) |
| 2026-10-26 | OpenAI | GPT-6.1 Terra | `gpt-6.1-terra` | Released | [Changelog](https://developers.openai.com/api/docs/changelog) |
| 2026-10-15 | Meta | Muse Spark Open: open weights, 816B total / 42B active | — | Muse Model License | [Meta research](https://research.meta.ai/blog/muse-spark-open) |
| 2026-10-13 | Google | Gemini 4 Argon | `gemini-4-argon` | GA | [Gemini changelog](https://ai.google.dev/gemini-api/docs/changelog) |
| 2026-10-07 | Anthropic | Claude Haiku 5.5 | `claude-haiku-5-5` | GA | [Release notes](https://platform.claude.com/docs/en/release-notes/overview) |
| 2026-09-29 | OpenAI | GPT-6.1 Sol | `gpt-6.1-sol` | Released | [Changelog](https://developers.openai.com/api/docs/changelog) |
| 2026-09-28 | Anthropic | Claude Sonnet 5.5 | `claude-sonnet-5-5` | GA | [Release notes](https://platform.claude.com/docs/en/release-notes/overview) |
| 2026-09-22 | Anthropic | Claude Opus 5.5 | `claude-opus-5-5` | GA | [Release notes](https://platform.claude.com/docs/en/release-notes/overview) |
| 2026-09-22 | OpenAI | GPT-6 Sol / GPT-6 Luna | `gpt-6-sol`, `gpt-6-luna` | Released | [Changelog](https://developers.openai.com/api/docs/changelog) |
| 2026-09-21 | xAI | Grok 4.7 | `grok-4.7` | Released | [xAI release notes](https://docs.x.ai/docs/release-notes) |

Trackers used: [nhimg LLM release tracker](https://nhimg.org/llm-release-tracker) · [ThursdAI November releases](https://thursdai.news/releases/2026-11)

---

## 📈 Trends

### The harness matters as much as the model
Builders increasingly frame it as *Agent = Model + Harness*. Several 2026 reports show the same model moving dozens of leaderboard places when only the harness changes. Spending on your harness (tools, context management, verification) often beats switching models. → [Agentic workflows](../../architecture/agentic-workflows/README.md)
_Added: 2026-11-18_

### Frontier-scale open weights keep arriving
Kimi K3.1 Pro (2.8T MoE), Mistral Large 4 and Meta's Muse Spark Open all shipped weights between mid-October and early November. Self-hosting near-frontier models is now realistic for well-resourced teams, but read the licences: Kimi's and Meta's carry commercial conditions.
_Added: 2026-11-18_

### Capability-gated models
Labs now ship dual-use variants behind approval: GPT-6 Cyber (Daybreak), GPT-6 Rosalind (approved orgs) and Claude Mythos 5.2 (verified orgs). Plan for capability tiers that depend on your organisation's verification status.
_Added: 2026-11-18_

## 🧪 New techniques

### Probability-returning "decision" APIs · Google Gemini Decisions API
A non-text API for yes/no, multiple-choice and rubric scoring that returns probabilities: up to 1,000 questions per call at $0.10 per 1M input tokens.
**Why it matters:** It is a better fit than free-text generation for classification, routing and LLM-as-judge evals, because you get calibrated scores instead of parsing prose.
Source: [Google blog](https://blog.google/innovation-and-ai/technology/developers-tools/gemini-decisions-api) · Added: 2026-11-18

### Weight-space programming · MIT CSAIL
GPT-6 Astra edited a small model's weights directly, with no training run, and raised MATH-500 from 7.9% to 48.1% by changing 0.016% of the weights (as reported).
**Why it matters:** This is early research, but it hints at a "model surgery" alternative to fine-tuning. → [Research to watch](../../learn/research/README.md)
Source: [Blog](https://rikiyat.github.io/blog/weight-space-programming/) · Added: 2026-11-18
