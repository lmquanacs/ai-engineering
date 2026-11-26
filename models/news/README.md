# LLM news: models, trends, techniques

_Last updated: 2026-11-26 · This page keeps about 30 days; older items move to [archive/](archive/)_

> Only what changes a builder's decision. Every model row carries its **API ID** and a primary source. Benchmark numbers are vendor claims unless marked otherwise.

## ⚡ Action items

| Deadline | What | Do this |
|---|---|---|
| **2026-11-30** | Claude Sonnet 4.5 retirement | Move pinned `claude-sonnet-4-5*` IDs to `claude-sonnet-5-5` or `claude-haiku-5-5` and re-run your evals. On Amazon Bedrock the model stays available until **2027-04-08** ([AWS](../../platforms/aws/README.md)). ([release notes](https://platform.claude.com/docs/en/release-notes/overview)) |
| **2026-11-30** | Claude Opus 4.8 fast mode removed | Requests to `claude-opus-4-8` with `speed: "fast"` will error; use Claude Opus 5.5 for fast mode. ([release notes](https://platform.claude.com/docs/en/release-notes/overview)) |
| **2026-11-30** | OpenAI shuts down `/v1/prompts` (reusable prompt objects), the Evals dashboard/API/graders and Agent Builder (announced 2026-06-03) | Move prompt content into your code, evals to another tool (OpenAI suggests Promptfoo), and Agent Builder flows to the Agents SDK or ChatKit. ([OpenAI deprecations](https://developers.openai.com/api/docs/deprecations)) |
| **2026-12-01** | OpenAI shuts down `gpt-image-1-mini`, `gpt-image-1.5`, `gpt-image-1.5-2025-12-16` and `chatgpt-image-latest` | Move to `gpt-image-2.6-sunburst` or `gpt-image-2.6-flare`. ([OpenAI deprecations](https://developers.openai.com/api/docs/deprecations)) |
| **2026-12-11** | OpenAI shuts down `gpt-5`, `gpt-5-mini`, `gpt-5-nano`, `gpt-5-pro`, `o3` and `o3-pro` (and their dated snapshots) | Replacements per OpenAI: `gpt-5`/`o3` → `gpt-6.1-sol`; `gpt-5-mini` → `gpt-6.1-terra`; `gpt-5-nano` → `gpt-6-luna`; `gpt-5-pro`/`o3-pro` → `gpt-6.1-sol` with `reasoning.mode: pro` (Responses API). Fine-tuned models on these bases go too. ([OpenAI deprecations](https://developers.openai.com/api/docs/deprecations)) |
| **2027-01-06** | OpenAI shuts down `tts-1`, `tts-1-hd` and `gpt-4o-mini-tts*`; self-serve fine-tuning job creation ends | Move speech to `gpt-realtime-2.1-mini`; inference on existing fine-tunes continues until the base model is retired. ([OpenAI deprecations](https://developers.openai.com/api/docs/deprecations)) |
| **2027-01-11** | OpenAI EU data residency: fast and priority tiers end for GPT-5.2, GPT-5.4 and GPT-5.4 mini | Switch to the default `service_tier` or move to GPT-6.2. ([OpenAI deprecations](https://developers.openai.com/api/docs/deprecations)) |
| **2027-01-14** | OpenAI shuts down the `gpt-4o-2024-08-06`, `gpt-4o-2024-11-20`, `gpt-4o-mini-2024-07-18`, `gpt-4.1-2025-04-14` and `gpt-4.1-mini-2025-04-14` snapshots | Move to `gpt-6-luna` and re-run evals. ([OpenAI deprecations](https://developers.openai.com/api/docs/deprecations)) |
| **2027-01-20** | OpenAI shuts down `gpt-realtime`, `gpt-realtime-mini`, `gpt-audio`, `gpt-audio-mini` and the `gpt-4o` realtime/audio variants | `gpt-realtime-2.1`, `gpt-realtime-2.1-mini` or `gpt-audio-1.5`. ([OpenAI deprecations](https://developers.openai.com/api/docs/deprecations)) |
| **2027-01-22** | Claude Opus 4.5 retirement (deprecated 2026-11-23) on the Claude API, Claude Platform on AWS, Google Cloud (Anthropic managed) and Microsoft Foundry; Bedrock and Google-managed Vertex set their own dates | Move `claude-opus-4-5` / `claude-opus-4-5-20251101` to `claude-opus-5-5` using the [migration guide](https://platform.claude.com/docs/en/models/opus-5-5/migration-guide#migrating-from-claude-opus-45). ([model deprecations](https://platform.claude.com/docs/en/about-claude/model-deprecations)) |
| **2027-02-10** | OpenAI shuts down `gpt-image-2` and `gpt-image-2-2026-04-21` (announced 2026-11-10) | Move image generation to `gpt-image-2.6-sunburst` or `gpt-image-2.6-flare` and re-check output quality and cost. ([OpenAI deprecations](https://developers.openai.com/api/docs/deprecations)) |
| when you switch | GPT-6.2 Astra / Sol migration | `gpt-6.2-astra` and `gpt-6.2-sol` reject reasoning effort `none`, need the Responses API for tool calling, and change how reasoning is preserved when you edit a conversation prefix and how top-level `instructions` are handled. Read the migration quickstart before swapping IDs. ([changelog](https://developers.openai.com/api/docs/changelog) · [migration guide](https://developers.openai.com/api/docs/guides/latest-model?model=gpt-6.2-astra#gpt-6.2-astra-migration-quickstart)) |
| ongoing | Short model lifetimes | DeepSeek-V4-Flash went from beta (Jul 31) to retired (Sep 10), and Gemini 3.7 Flash was deprecated eight weeks after release. Pin dated IDs and watch deprecation trackers. ([source](https://nhimg.org/llm-release-tracker)) |

---

## 🆕 New models (Nov 2026)

Newest first. Status is as of release.

| Date | Provider | Model | API ID | Status | Source |
|---|---|---|---|---|---|
| 2026-11-24 | OpenAI | Healthcare configurations: select models paired with a clinical-question harness; web search uses a dedicated index of medical sources. Pricing is in the healthcare section of OpenAI's pricing page | `gpt-6.2-astra-healthcare`, `gpt-6.2-sol-healthcare`, `gpt-6-astra-healthcare`, `gpt-6.1-sol-healthcare` | Released (Responses API only) | [Changelog](https://developers.openai.com/api/docs/changelog.md) |
| 2026-11-20 (missed earlier) | Thinking Machines | Inkling 2 Mini, **open weights** (Apache 2.0): 26.4B total / 3.4B active (looped MoE), 1M context, text + image input. Supported in vLLM, SGLang, Ollama, llama.cpp (GGUF) and Unsloth per the lab; on AI Gateway since 11-24 | — (HF `thinkingmachines/Inkling-2-Mini`) | Open weights; API via Tinker | [Thinking Machines](https://thinkingmachines.ai/news/inkling-2-mini/) · [Hugging Face](https://huggingface.co/thinkingmachines/Inkling-2-Mini) |
| 2026-11-18 (missed earlier) | Google | **Gemini 4 Neon**: mid tier between Hydrogen and Carbon, 1M context; $3/$15 per 1M in/out (cached $0.15); Google says 32% cheaper per task than Carbon at default effort (self-reported) | `gemini-4-neon` | Gemini API paid tier (AI Studio), Antigravity, Gemini app | [Google blog](https://blog.google/innovation-and-ai/models-and-research/gemini-models/introducing-gemini-4-neon/) · [AI Gateway](https://vercel.com/changelog/gemini-4-neon-now-available-on-ai-gateway) |
| 2026-11-19 | OpenAI | GPT-Live-1.1: realtime voice model with better pronunciation, accent consistency and transcription in multilingual conversations | `gpt-live-1.1` | Released (Live API) | [Changelog](https://developers.openai.com/api/docs/changelog) |
| 2026-11-17 | OpenAI | **GPT-6.2 Astra** (hardest reasoning and coding); $8/$40 per 1M in/out, cheaper than GPT-6 Astra's $10/$50; 1.05M context, 128K max output | `gpt-6.2-astra` | Released (Responses + Chat Completions) | [Changelog](https://developers.openai.com/api/docs/changelog) · [Model page](https://developers.openai.com/api/docs/models/gpt-6.2-astra) |
| 2026-11-17 | OpenAI | **GPT-6.2 Sol** (everyday coding and agents); $2/$10 per 1M in/out, same as GPT-6.1 Sol; 1.05M context, 128K max output | `gpt-6.2-sol` | Released (Responses + Chat Completions) | [Changelog](https://developers.openai.com/api/docs/changelog) · [Model page](https://developers.openai.com/api/docs/models/gpt-6.2-sol) |
| 2026-11-16 | Alibaba | Qwen4-Max: 2.4T total / ~71B active, 1M context; ~35% fewer tokens than Qwen3.8-Max on Alibaba's Work360 benchmark (self-reported). Not open weights; smaller open Qwen4 models promised | `qwen4-max` | API (Model Studio); $1.50/$4.50 per 1M in/out (international), cache hit $0.075 | [Alibaba Cloud](https://www.alibabacloud.com/press-room/alibaba-unveils-qwen4-max) · [Model Studio pricing](https://www.alibabacloud.com/help/en/model-studio/model-pricing) |
| 2026-11-12 | Google | Gemini 4 Hydrogen (fast tier, ~2.5× faster than Gemini 3.8 Flash per Google) | `gemini-4-hydrogen` | Released (Vertex); $1.50/$7.50 per 1M in/out (global) | [Vertex model versions](https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/model-versions) · [Vertex pricing](https://cloud.google.com/vertex-ai/generative-ai/pricing) |
| 2026-11-10 → 12 | Google | Gemini 4 Carbon (top model), now GA; 60.4% CursorBench (high effort, self-reported) | `gemini-4-carbon` | GA; $2/$10 per 1M in/out until Nov 30, then $4/$20 | [Google blog](https://blog.google/innovation-and-ai/models-and-research/gemini-models/gemini-4-carbon-now-available/) · [Vertex pricing](https://cloud.google.com/vertex-ai/generative-ai/pricing) |
| 2026-11-09 | Anthropic | **Claude Fable 5.2**; $8/$40 per 1M in/out tokens (20% cheaper than 5.1) | `claude-fable-5-2` | GA (paid plans + API) | [Release notes](https://platform.claude.com/docs/en/release-notes/overview) |
| 2026-11-09 | Anthropic | Claude Mythos 5.2 (same underlying model as Fable; Fable adds extra biology and cyber safeguards) | `claude-mythos-5-2` | Restricted to verified orgs | [Release notes](https://platform.claude.com/docs/en/release-notes/overview) |
| 2026-11-05 → 12 (missed earlier) | Thinking Machines | Inkling 2 Small: 594B total / 17B active MoE, 1M context; hosted on Tinker from 11-05, **open weights** (Apache 2.0, NVFP4 and MXFP8 repos) from 11-12 | — | Open weights; API via Tinker and third-party hosts | [Model card](https://thinkingmachines.ai/model-card/inkling-2-small/) · [Announcement](https://thinkingmachines.ai/news/inkling-2-small) |
| 2026-11-05 | Mistral AI | Mistral Large 4, **open weights** | `mistral-large-4` | GA | [Model card](https://docs.mistral.ai/models/mistral-large-4-0.md) |
| 2026-11-05 | Moonshot AI | Kimi K3.1 Pro, **open weights**: 2.8T MoE, 104B active, 1M context, image input; licence has conditions for large products | — | Open weights | [Hugging Face](https://huggingface.co/moonshotai/Kimi-K3.1-Pro) |
| 2026-11-05 | Cognition | SWE-2 Flash: fast, cheap coding model at ~⅕ the cost of SWE-2 | — | Released | [Cognition blog](https://cognition.com/blog/swe-2-flash) |
| 2026-11-05 | Ricursive | Ripple-65B Preview: dense 65B trained from scratch, Apache 2.0; 80.5% TerminalBench 2.1 (self-reported) | — | Open weights | [Blog](https://www.ricursive.com/ripple) |
| 2026-11-05 | Tencent | Hy4: first Hy model with vision + computer use, 1M context; weights promised later | — | API (OpenRouter) | [Blog](https://hy.tencent.ai/research/hy4?langVersion=en) |
| 2026-11-05 | OpenAI | GPT-6 Cyber: security model for the Daybreak program | `gpt-6-cyber` | Restricted | [OpenAI](https://openai.com/index/introducing-gpt-6-cyber/) |

Older rows: [archive/](archive/). Trackers used: [nhimg LLM release tracker](https://nhimg.org/llm-release-tracker) · [nocode.mba November tracker](https://www.nocode.mba/ai-release-tracker/2026/11) · [ThursdAI November releases](https://thursdai.news/releases/2026-11)

---

## 📰 Launch notes

### Gemini 4 Neon · Google · 2026-11-18 (missed earlier) 🆕
Google's new mid-tier Gemini 4 model sits between Hydrogen ($1.50/$7.50) and Carbon. It costs $3/$15 per 1M tokens with cached input at $0.15, has a 1M-token window, and is on the Gemini API paid tier through AI Studio. Google reports it costs 32% less per task than Carbon at default effort *(self-reported)*. It is already the default model in Antigravity and GA in GitHub Copilot.
**Why it matters:** Carbon doubles to $4/$20 on 2026-12-01, so Neon is the obvious model to evaluate for agentic coding before that date. The blog post doesn't say whether Neon is preview or GA, or give a Vertex date, so check before you pin it in production.
Source: [Google blog](https://blog.google/innovation-and-ai/models-and-research/gemini-models/introducing-gemini-4-neon/) · [AI Gateway changelog](https://vercel.com/changelog/gemini-4-neon-now-available-on-ai-gateway) (`google/gemini-4-neon`) · Added: 2026-11-26

### GPT-6.2 Astra & Sol · OpenAI · 2026-11-17
OpenAI's next point release: `gpt-6.2-astra` for demanding reasoning and coding, and `gpt-6.2-sol` for everyday coding and agent workflows. Astra drops to $8/$40 per 1M tokens (cached input $0.40), and Sol stays at $2/$10. Both have a 1.05M-token window (922K max input) and 128K max output.
**Why it matters:** Astra-class work gets 20% cheaper. It is not a drop-in swap, though: reasoning effort `none` is rejected, tool calling needs the Responses API, and reasoning-preservation and `instructions` behaviour change. Re-run your evals and follow the migration quickstart. Also on Bedrock → [AWS](../../platforms/aws/README.md).
Source: [OpenAI API changelog](https://developers.openai.com/api/docs/changelog) · [Astra model page](https://developers.openai.com/api/docs/models/gpt-6.2-astra) · [Sol model page](https://developers.openai.com/api/docs/models/gpt-6.2-sol) · Added: 2026-11-19

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
