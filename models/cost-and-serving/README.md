# Inference, cost & serving

_Last updated: 2026-11-21_

> What models cost, how to pay less, and how to serve open models yourself. Prices are list prices in USD per 1M tokens unless stated, and they change often, so check the provider's page before you budget.

## ⚡ Price changes coming up

| Date | Change | Source |
|---|---|---|
| **2026-11-30** | Gemini 4 Carbon introductory pricing ends | [Google blog](https://blog.google/innovation-and-ai/models-and-research/gemini-models/gemini-4-carbon-now-available/) |
| **2026-11-30** | OpenAI's promotional price for **GPT-5.6 Sol** ends (it does not cover GPT-6.x Sol) | [OpenAI pricing](https://developers.openai.com/api/docs/pricing) |
| **2026-12-01** | **Gemini 4 Argon doubles**: $2/$10 → **$4/$20** (cached $0.10 → $0.20) | [Google pricing](https://aistudio.google.com/docs/pricing) |
| **2027-01-01** | **Gemini 3.8 Flash and 3.6 Flash double**: $0.75/$3.75 → **$1.50/$7.50**; context-cache storage $0.50 → $1.00 per MTok-hour | [Google pricing](https://aistudio.google.com/docs/pricing) |
| **2027-01-11** | OpenAI ends fast/priority `service_tier` for **GPT-5.2, GPT-5.4, GPT-5.4 mini** with EU data residency (Standard only) | [OpenAI deprecations](https://developers.openai.com/api/docs/deprecations) |
| **2027-03-01** | **GPT-6.2 Astra / Sol Ultrafast** goes from 3× to **6× Standard** (Standard rates unchanged) | [OpenAI pricing](https://developers.openai.com/api/docs/pricing) |

## 💲 Price snapshot (list, standard tier, as of 2026-11-15)

| Model | Input | Cached input | Output | Discounts |
|---|---|---|---|---|
| Claude Fable 5.2 | $8 | $0.20 | $40 | Batch −50% |
| Claude Opus 5.5 | $4 | $0.20 | $20 | Batch −50% |
| Claude Sonnet 5.5 | $2 | $0.10 | $10 | Batch −50% |
| Claude Haiku 5.5 | $0.10 | $0.01 | $0.50 | Batch −50%; >100K-token prompts cost more |
| GPT-6.2 Astra | $8 | $0.40 | $40 | Background 2h −30% / 8h −40% (beta); Ultrafast option costs 3× |
| GPT-6 Astra | $10 | $1.00 | $50 | Lower tier at 50% |
| GPT-6.2 Sol | $2 | $0.10 | $10 | Background 2h −30% / 8h −40% (beta); Ultrafast option costs 3× |
| GPT-6.1 Sol | $2 | $0.10 | $10 | Lower tier at 50% |
| GPT-6 Luna | $0.10 | $0.01 | $0.50 | — |
| Gemini 4 Argon | $2 | $0.10 | $10 | Batch/Flex −50% · ⚠️ rises Dec 1 |
| Gemini 3.8 Flash | $0.75 | $0.075 | $3.75 | Batch/Flex −50% · ⚠️ rises Jan 1 |
| Grok 4.7 | $2 | $0.50 | $6 | Batch −20%; 200K+ prompts double |
| DeepSeek-V4.1-Flash (`deepseek-flash`) | $0.30 / $0.15 off-peak | $0.006 | $1.20 / $0.60 off-peak | Off-peak (by UTC hour) −50% |
| DeepSeek-V4-Pro (`deepseek-v4-pro`) | $1.32 / $0.66 off-peak | $0.044 / $0.022 | $3.96 / $1.98 off-peak | Off-peak −50% |
| Qwen4-Max (`qwen4-max`, international) | $1.50 | $0.075 (cache hit) | $4.50 | Explicit cache writes cost extra |
| Mistral Large 4 | $0.70 | $0.07 | $2.10 | Batch −50% (the pricing page also shows $0.50/$1.50, so confirm for your ID) |

Source: [nhimg LLM pricing tracker](https://nhimg.org/llm-pricing-tracker), read from provider pages on 2026-11-15; GPT-6.2 rows from [OpenAI pricing](https://developers.openai.com/api/docs/pricing) on 2026-11-19; DeepSeek-V4-Pro from [DeepSeek pricing](https://api-docs.deepseek.com/quick_start/pricing) and Qwen4-Max from [Model Studio pricing](https://www.alibabacloud.com/help/en/model-studio/model-pricing) on 2026-11-20. Gemini 4 Carbon, Gemini 4 Hydrogen and GPT-6 Sol are not yet in the table.

**More trackers:** [getdeploying.com/llms](https://getdeploying.com/llms) (199 models, hand-checked) · [benchlm.ai cost ledger](https://benchlm.ai/llm-pricing) (217 models, with value-for-money scores)

## 🪙 Cost levers, in order of effort

1. **Prompt caching:** cached input is 1/10 to 1/40 of list price. Keep prefixes stable (see [Context engineering](../../architecture/context-and-memory/README.md)).
2. **Batch / Flex / lower tiers:** −50% at most providers for work that isn't latency-sensitive (evals, backfills, nightly jobs). OpenAI now also offers 2-hour (−30%) and 8-hour (−40%) background completion windows.
3. **Right-size the model per step:** route classification and extraction to Haiku/Luna/Flash-class models, and keep frontier models for planning and hard reasoning.
4. **Off-peak pricing:** DeepSeek halves its rates by UTC hour, so schedule batch work then.
5. **Trim the harness:** heavyweight harnesses cost 3–5× more for under 2% accuracy. → [Agentic workflows](../../architecture/agentic-workflows/README.md#-latest-evidence-what-actually-moves-the-needle)

### OpenAI background completion windows · −30% / −40% · 2026-11-17 🆕
In the Responses API (public beta), a background request can choose a two-hour or eight-hour completion window, and token rates drop 30% or 40% below Standard. It covers `gpt-6.2-astra`, `gpt-6.2-sol`, `gpt-6.1-terra` and `gpt-6-luna`.
**Why it matters:** It is a middle ground between real-time and the Batch API. Agent sub-tasks, evals and enrichment jobs that can wait a few hours get a discount without restructuring into batch files.
Source: [OpenAI API changelog](https://developers.openai.com/api/docs/changelog) · [Background mode guide](https://developers.openai.com/api/docs/guides/background#use-discounted-completion-windows) · Added: 2026-11-19

---

### DeepSeek: built-in search and fetch now billed as tokens · 2026-11-18 🆕
From 2026-11-18 12:00 Beijing time, server-side search and web-fetch calls made during a model call are no longer billed as separate tool calls; their results go into the context and are billed as input tokens. The standalone Search and Fetch APIs still cost $0.75 per 1,000 successful requests. Peak hours (full price) are 01:00–04:00 and 06:00–10:00 UTC on weekdays.
**Why it matters:** Agents that lean on DeepSeek's built-in search now pay per token of fetched content, so long pages cost more. Re-estimate cost for tool-heavy runs.
Source: [DeepSeek pricing](https://api-docs.deepseek.com/quick_start/pricing) · Added: 2026-11-20

## 🖥️ Self-hosting & serving

### vLLM v0.34.0 · 2026-11-16 🆕
PyPI shows v0.34.0 uploaded on 2026-11-16. A copy of the release notes lists breaking changes, including removal of Model Runner V1, a larger default KV block size and a new `gpu_memory_utilization` default; we could not open the GitHub release to confirm them.
**Why it matters:** This looks like an upgrade that changes memory behaviour. Read the GitHub release notes and test on staging before rolling it out.
Source: [vLLM on PyPI](https://pypi.org/project/vllm/) · [GitHub release v0.34.0](https://github.com/vllm-project/vllm/releases/tag/v0.34.0) · Added: 2026-11-20

### vLLM v0.33.0 · 2026-11-01 🆕
Faster speculative decoding on NVIDIA and AMD, a ROCm decode path, new model support, and a `/v1/decisions` endpoint. **Breaking changes:** official builds are now **CUDA 13.0 only** (no more 12.9 wheels or images) and move to PyTorch 2.14. The LM Format Enforcer structured-output backend is deprecated: opt-in in v0.34, removed in v0.35.
**Why it matters:** Check GPU drivers before upgrading, and plan a move off LM Format Enforcer if you use it.
```bash
pip install -U vllm   # or image vllm/vllm-openai:v0.33.0
```
Source: [AI/TLDR release summary](https://ai-tldr.dev/releases/vllm-v0-33-0/) · Added: 2026-11-18

### vLLM tiered KV-cache offloading
vLLM can now offload KV cache to CPU memory and disk tiers, which helps agentic workloads with long, shared prefixes.
Source: [vLLM blog](https://vllm.ai/blog/2026-09-10-tiered-kv-offloading) · Added: 2026-11-18

### Run local models inside Claude Code / Codex · Unsloth
`unsloth start claude` (or another supported agent) connects coding agents to a local model served by Unsloth Studio.
**Why it matters:** It is the easiest route to offline or private coding-agent runs with open models.
Source: [Unsloth on PyPI](https://pypi.org/project/unsloth/2026.8.1/) · Added: 2026-11-18

### inferd · Incept5 · 2026-11-05 🆕
An Apache-2.0 inference engine for Macs, built to serve many concurrent agents (128 in their demo).
Source: [GitHub](https://github.com/Incept5-AI/inferd) · Added: 2026-11-18

## 🧩 Open-weight models worth serving
See [LLM news](../news/README.md): Kimi K3.1 Pro (2.8T MoE), Mistral Large 4, Ripple-65B (Apache 2.0) and Meta Muse Spark Open. Check each licence before commercial use.
