# Open-weight model providers

_Last updated: 2026-11-25_

> Where to call GLM, DeepSeek, Kimi, Qwen, MiniMax and MiMo models: the labs' own APIs and coding plans, OpenAI- and Anthropic-compatible base URLs, which third-party hosts serve which model (and at what precision), routers, and how to wire them into AI SDK, Pydantic AI, Spring AI and LangChain4j. Launches and benchmarks are in [LLM news](../news/README.md). Frontier prices and self-hosting are in [Inference, cost & serving](../cost-and-serving/README.md). DeepSeek API feature changes are in [LLM APIs](../../build/llm-apis/README.md). Bedrock availability is in [AWS](../../platforms/aws/README.md).

## 🗺️ Who serves what (as of 2026-11-24)

Every cell was read on the named source page on 2026-11-24, except entries marked 2026-11-25, which were added the next day. "—" means we found no listing, and "not confirmed" means we could not verify it. Host model IDs differ from the lab's IDs, so copy them exactly.

| Model | First-party API (model ID + base URL) | Third-party hosts (confirmed on the host's own page) | AI SDK package / AI Gateway string |
|---|---|---|---|
| **GLM-5.3** (Z.ai; open weights, 1M context) | `glm-5.3` · OpenAI-compatible `https://api.z.ai/api/paas/v4` · Anthropic-compatible `https://api.z.ai/api/anthropic` · Responses `https://api.z.ai/api/v1` · GLM Coding Plan (OpenAI format) `https://api.z.ai/api/coding/paas/v4` | Fireworks `accounts/fireworks/models/glm-5p3` (serverless) · DeepInfra `zai-org/GLM-5.3` (FP4) · Baseten `zai-org/GLM-5.3`, `zai-org/GLM-5.3-Fast` · Together `zai-org/GLM-5.3` (FP4; the page also shows a "launching soon" banner) · Groq, Cerebras: — | `@ai-sdk/zai` + `glm-5.3` · Gateway `zai/glm-5.3` |
| **DeepSeek-V4-Pro** (DeepSeek; open weights, MIT) | `deepseek-v4-pro` · Anthropic-compatible `https://api.deepseek.com/anthropic` · OpenAI-format `https://api.deepseek.com` (from Spring AI's default; DeepSeek's own quick-start page could not be opened) | DeepInfra `deepseek-ai/DeepSeek-V4-Pro` (FP8; release not stated) · Baseten `deepseek-ai/DeepSeek-V4-Pro-0813` · Together (listed on its inference page; ID not confirmed) · Fireworks: listed but not serverless | `@ai-sdk/deepseek` + `deepseek-v4-pro` · Gateway `deepseek/deepseek-v4-pro` (dated `deepseek/deepseek-v4-pro-0813`) |
| **DeepSeek-V4.1-Flash** (DeepSeek) | `deepseek-flash` (alias for the current Flash) · same base URLs as above | Fireworks `accounts/deepseek-ai/models/deepseek-v4p1-flash` (serverless) · Baseten `deepseek-ai/DeepSeek-V4.1-Flash`, `-Fast`, and dated `deepseek-ai/DeepSeek-V4.1-Flash-1017`, `-1017-Fast` (2026-11-25; first-party `deepseek-flash` has pointed to the 1017 update since 2026-10-17, so pin `-1017` to match it) · Together `deepseek-ai/DeepSeek-V4.1-Flash` (via Together Link docs, 2026-11-25) | `@ai-sdk/deepseek` + `deepseek-flash` · Gateway string not confirmed |
| **Kimi K3.1 Pro** (Moonshot; open weights, 1M context) | `kimi-k3.1-pro`, `kimi-k3.1-pro-highspeed` · OpenAI-compatible `https://api.moonshot.ai/v1` · Anthropic-compatible `https://api.moonshot.ai/anthropic` | Fireworks `accounts/fireworks/models/kimi-k3p1-pro` (MXFP4 weights / MXFP8 activations, quantization-aware trained) · DeepInfra `moonshotai/Kimi-K3.1-Pro` (same scheme) · Baseten `moonshotai/Kimi-K3.1-Pro` · Together (listed on its inference page; ID not confirmed) | `@ai-sdk/moonshotai` + `kimi-k3.1-pro` · Gateway `moonshotai/kimi-k3.1-pro` |
| **Qwen3.8-2.4T-A95B** (Alibaba; open weights, 262K native context) | `qwen3.8-2.4t-a95b` · Singapore OpenAI-compatible `https://dashscope-intl.aliyuncs.com/compatible-mode/v1` · Anthropic-compatible `https://dashscope-intl.aliyuncs.com/apps/anthropic` | Fireworks `accounts/fireworks/models/qwen3p8-max` (serverless; the page links the Qwen3.8-2.4T-A95B weights, but the ID says "max", so check before pinning) · Together `Qwen/Qwen3.8-2.4T-A95B` (via Together Link docs, 2026-11-25) · Groq, Cerebras: only the small `qwen/qwen3.8-27b` | AI SDK package not confirmed (an Alibaba provider page exists) · Gateway `alibaba/qwen3.8-2.4t-a95b` |
| **MiniMax-M3** (MiniMax; weights under a "minimax-community" licence, 1M context) | `MiniMax-M3` (also `MiniMax-M3.1-Flash`, open weights) · Anthropic-compatible `https://api.minimax.io/anthropic` (MiniMax recommends it) · OpenAI-compatible `https://api.minimax.io/v1` | Fireworks `accounts/fireworks/models/minimax-m3` (serverless) · Together: M3.1 Flash only · Groq: preview `minimaxai/minimax-m2.7` only | Community `vercel-minimax-ai-provider` · Gateway `minimax/minimax-m3` |
| **MiMo-V2.6-Pro** (Xiaomi; open weights, MIT, 1M context) | `mimo-v2.6-pro` (also `-flash`, `-pro-ultraspeed`) · OpenAI-compatible `https://api.xiaomimimo.com/v1` · Anthropic-compatible `https://api.xiaomimimo.com/anthropic` | DeepInfra `XiaomiMiMo/MiMo-V2.6-Pro` (FP8) · Baseten: dedicated deployment of the `-MOPD` variant only | AI SDK package not confirmed · Gateway `xiaomi/mimo-v2.6-pro` |

**Not in the table:** GLM-5.4 is on the GLM Coding Plan only. Its pay-as-you-go API waits on a security assessment, and open weights are not announced (see Latest). Qwen4-Max (`qwen4-max`) is Alibaba's newest flagship, but it is API-only with no open weights. See [LLM news](../news/README.md). For DeepSeek and Qwen4-Max list prices, see the [price snapshot](../cost-and-serving/README.md).

**Watch the dated IDs.** On OpenRouter, the unversioned `deepseek/deepseek-v4-pro` page describes the 0423 release, and the GA release is the separate `deepseek-v4-pro-0813` slug. On AI Gateway, the unversioned ID moved to the updated weights on 2026-08-12. The same name can therefore reach different weights depending on the router, so pin the dated ID if you need reproducibility.

**Speed and price differ by host (snapshot 2026-11-24).** For GLM-5.3, AI Gateway lists 27 providers. Its own P50 throughput ranges from 27 to 223 tok/s, and input prices run from $0.07 to $1.73 per 1M tokens. The Z.ai first-party endpoint shows 70 tok/s at $1.40/$4.40. Artificial Analysis benchmarks 29 GLM-5.3 endpoints on a 5-day rolling window. Its fastest per task is an FP4 "FAST" endpoint, and its cheapest per task is Multiverse Computing. The Z.ai endpoint ranks near the bottom for time per task. Several fast endpoints are FP4, so check the precision column before you treat a host as equivalent to first-party.

Sources: [Z.ai GLM-5.3](https://docs.z.ai/guides/llm/glm-5.3.md) · [Z.ai API intro](https://docs.z.ai/api-reference/introduction.md) · [DeepSeek Anthropic API](https://api-docs.deepseek.com/guides/anthropic_api.md) · [Kimi model list](https://platform.kimi.ai/docs/guide/model-list) · [Kimi Messages API](https://platform.kimi.ai/docs/api/messages.md) · [Model Studio base URLs](https://www.alibabacloud.com/help/en/model-studio/base-url) · [Model Studio Anthropic API (model list)](https://www.alibabacloud.com/help/en/model-studio/anthropic-api-messages) · [Qwen3.8-2.4T-A95B on Hugging Face](https://huggingface.co/Qwen/Qwen3.8-2.4T-A95B) · [MiniMax models](https://platform.minimax.io/docs/guides/text-generation.md) · [MiniMax-M3 on Hugging Face](https://huggingface.co/MiniMaxAI/MiniMax-M3) · [MiMo models](https://mimo.mi.com/docs/en-US/quick-start/summary/model) · [MiMo first API call](https://mimo.mi.com/docs/en-US/quick-start/summary/first-api-call) · [DeepSeek-V4-Pro-0813 on Hugging Face](https://huggingface.co/deepseek-ai/DeepSeek-V4-Pro-0813) · [Fireworks model library](https://fireworks.ai/models.md) · [Fireworks GLM-5.3](https://fireworks.ai/models/fireworks/glm-5p3) · [Fireworks Kimi K3.1 Pro](https://fireworks.ai/models/fireworks/kimi-k3p1-pro) · [Fireworks Qwen3.8](https://fireworks.ai/models/fireworks/qwen3p8-max) · [DeepInfra GLM-5.3](https://deepinfra.com/zai-org/GLM-5.3) · [DeepInfra Kimi K3.1 Pro](https://deepinfra.com/moonshotai/Kimi-K3.1-Pro) · [DeepInfra DeepSeek-V4-Pro](https://deepinfra.com/deepseek-ai/DeepSeek-V4-Pro) · [DeepInfra MiMo-V2.6-Pro](https://deepinfra.com/XiaomiMiMo/MiMo-V2.6-Pro) · [Baseten Model APIs](https://docs.baseten.co/inference/model-apis/overview) · [Baseten MiMo-V2.6-Pro-MOPD](https://www.baseten.co/library/mimo-v26-pro-mopd/) · [Together GLM-5.3](https://www.together.ai/models/glm-5-3) · [Together Link models (2026-11-25)](https://docs.together.ai/docs/togetherlink.md) · [DeepSeek API updates](https://api-docs.deepseek.com/updates) · [Together inference](https://www.together.ai/inference) · [Groq models](https://console.groq.com/docs/models) · [Cerebras on OpenRouter](https://openrouter.ai/provider/cerebras) · AI Gateway: [GLM-5.3](https://vercel.com/ai-gateway/models/glm-5.3/status) · [DeepSeek V4 Pro](https://vercel.com/ai-gateway/models/deepseek/deepseek-v4-pro) · [Kimi K3.1 Pro](https://vercel.com/ai-gateway/models/kimi-k3.1-pro) · [Qwen3.8-2.4T-A95B](https://vercel.com/ai-gateway/models/qwen3.8-2.4t-a95b/about) · [MiniMax M3](https://vercel.com/ai-gateway/models/minimax-m3) · [MiMo V2.6 Pro](https://vercel.com/ai-gateway/models/mimo-v2.6-pro) · [OpenRouter DeepSeek V4 Pro](https://openrouter.ai/deepseek/deepseek-v4-pro) · [Artificial Analysis: GLM-5.3 providers](https://artificialanalysis.ai/models/glm-5-3/providers)

## ⭐ Start here

### Run Claude Code on an open model · Anthropic-compatible endpoints 🆕
All six labs now offer an Anthropic Messages-compatible base URL (see the table). You point `ANTHROPIC_BASE_URL` at it and supply that lab's key. DeepSeek also remaps any model name starting with `claude`: `claude-opus*` goes to `deepseek-v4-pro`, other `claude*` names go to `deepseek-flash`, and any other unknown name returns a 400 error.
**Why it matters:** You can try a cheaper open model inside the agent you already use, without new tooling. Run your own evals first, because tool-use quality varies, and set model names explicitly so a silent remap doesn't fool you.
```bash
export ANTHROPIC_BASE_URL=https://api.deepseek.com/anthropic
export ANTHROPIC_API_KEY=<your DeepSeek key>
```
Source: [DeepSeek Anthropic API](https://api-docs.deepseek.com/guides/anthropic_api.md) · [Kimi Messages API](https://platform.kimi.ai/docs/api/messages.md) · [Z.ai quick start](https://docs.z.ai/devpack/quick-start.md) · Added: 2026-11-24

### Coding plans: flat-rate subscriptions for coding agents 🆕
Z.ai (GLM Coding Plan), Moonshot (Kimi Code), Alibaba (Model Studio Coding Plan), MiniMax (M Plan, keys start `sk-cp-`) and Xiaomi (MiMo Token Plan) all sell coding subscriptions. Each has its **own key and base URL**: for example `https://api.kimi.ai/coding/` (overseas, Anthropic format), `https://coding-intl.dashscope.aliyuncs.com/apps/anthropic` and `https://token-plan-cn.xiaomimimo.com/anthropic`. Z.ai says its plan is only for officially supported tools. Kimi Code exposes plan-specific IDs such as `k3.1-pro` and `kimi-for-coding`, which differ from the platform's `kimi-k3.1-pro`.
**Why it matters:** For heavy agent use, a plan is often cheaper than per-token billing. The most common failure is a 401 from pairing a plan key with the pay-as-you-go URL (or the reverse), and Alibaba's docs warn about exactly this. Check each plan's terms before you use it from CI or a shared service.
Source: [Z.ai GLM Coding Plan](https://docs.z.ai/devpack/quick-start.md) · [Kimi Code docs](https://www.kimi.com/code/docs/en/) · [Model Studio Coding Plan for Claude Code](https://www.alibabacloud.com/help/en/model-studio/claude-code-coding-plan) · [MiniMax other tools](https://platform.minimax.io/docs/token-plan/other-tools.md) · [MiMo first API call](https://mimo.mi.com/docs/en-US/quick-start/summary/first-api-call) · Added: 2026-11-24

### One key, many hosts · Vercel AI Gateway and OpenRouter 🆕
Both routers spread a model across many hosts and show per-host price and throughput on their model pages. Each model page also lists the release date and pricing. AI Gateway also speaks the Anthropic Messages API at `https://ai-gateway.vercel.sh`, so Claude Code can use any Gateway model. Provider `order`/`only` and Zero Data Retention routing are set through `providerOptions`.
**Why it matters:** You get fallback across hosts and one bill, and you can require ZDR hosts. Routers resolve unversioned IDs differently (see the DeepSeek note above), so pin dated IDs. Restrict routing to the hosts and precisions you have tested.
Source: [AI Gateway Anthropic API](https://vercel.com/docs/ai-gateway/sdks-and-apis/anthropic-messages-api) · [OpenRouter GLM-5.3 providers](https://openrouter.ai/z-ai/glm-5.3/providers) · Added: 2026-11-24

### Same model, different precision: check FP4 vs FP8 before you switch hosts 🆕
Hosts often serve open weights quantised. DeepInfra and Together list GLM-5.3 as FP4. Baseten lists FP4 for its standard GLM-5.3 endpoint on OpenRouter and FP8 for its "Fast" endpoint. DeepInfra serves DeepSeek-V4-Pro and MiMo-V2.6-Pro as FP8. Kimi K3.1 Pro on Fireworks and DeepInfra uses MXFP4 weights trained that way (quantisation-aware), which those pages describe as the model's design.
**Why it matters:** A cheaper or faster endpoint may score differently from the lab's API. Artificial Analysis lists each GLM-5.3 endpoint separately, FP4 variants included. Re-run your evals when you change hosts, not only when you change models.
Source: [Artificial Analysis: GLM-5.3 providers](https://artificialanalysis.ai/models/glm-5-3/providers) · [DeepInfra GLM-5.3](https://deepinfra.com/zai-org/GLM-5.3) · [Fireworks Kimi K3.1 Pro](https://fireworks.ai/models/fireworks/kimi-k3p1-pro) · Added: 2026-11-24

## 🔌 SDK wiring

Package names below are copied from each framework's docs. None of the pages we read state a minimum version, so we list none.

- **AI SDK (TypeScript):** `@ai-sdk/deepseek` (`deepseek-flash`, `deepseek-v4-pro`; the `deepseek-chat` and `deepseek-reasoner` aliases were retired on 2026-07-24), `@ai-sdk/moonshotai` (`kimi-k3.1-pro`, `kimi-k3.1-pro-highspeed`, default base URL `https://api.moonshot.ai/v1`) and `@ai-sdk/zai` (`glm-5.3`). MiniMax has a community provider, `vercel-minimax-ai-provider`, with Anthropic-style and OpenAI-style exports. The docs we read list only its M2 IDs, but it accepts any model string. ai-sdk.dev also has Alibaba, Fireworks, Together AI, DeepInfra, Baseten, Groq and Cerebras provider pages, but we did not confirm their package names. Through AI Gateway you can skip the provider package and use strings such as `zai/glm-5.3` or `moonshotai/kimi-k3.1-pro`. → [ai-sdk.dev providers](https://ai-sdk.dev/providers/ai-sdk-providers) · [DeepSeek](https://ai-sdk.dev/v5/providers/ai-sdk-providers/deepseek) · [Moonshot AI](https://ai-sdk.dev/v7/providers/ai-sdk-providers/moonshotai) · [Z.ai](https://ai-sdk.dev/v5/providers/ai-sdk-providers/zai) · [MiniMax (community)](https://ai-sdk.dev/v5/providers/community-providers/minimax)
- **Pydantic AI (Python):** install `pydantic-ai-slim[openai]`. Named providers include `DeepSeekProvider` (`deepseek:deepseek-v4-pro`, `DEEPSEEK_API_KEY`), `MoonshotAIProvider` (`moonshotai:kimi-k3.1-pro`, `MOONSHOTAI_API_KEY`), `AlibabaProvider` (`alibaba:`, `DASHSCOPE_API_KEY`), `FireworksProvider`, `TogetherProvider`, `VercelProvider` (`vercel:`) and `OpenRouterProvider`. For Z.ai, MiniMax or MiMo, use `OpenAICompatibleProvider` with the base URL from the table. → [OpenAI-compatible providers](https://pydantic.dev/docs/ai/models/compatible-apis/) · [DeepSeek](https://pydantic.dev/docs/ai/models/deepseek/) · [Moonshot AI](https://pydantic.dev/docs/ai/models/moonshotai/)
- **Spring AI (Java/Kotlin):** DeepSeek has a dedicated starter, `spring-ai-starter-model-deepseek` (`spring.ai.deepseek.base-url` defaults to `https://api.deepseek.com`). Its docs still list `deepseek-v4-flash` as the default model and show the retired `deepseek-chat`/`deepseek-reasoner`, so set `spring.ai.deepseek.chat.model` explicitly. For MiniMax, Spring AI 2.x routes through the Anthropic integration (`spring.ai.anthropic.base-url=https://api.minimax.io/anthropic`, model `MiniMax-M3`). For other OpenAI-compatible endpoints, use `spring-ai-starter-model-openai` with `spring.ai.openai.base-url`. The ZhiPu AI page still shows a `glm-4-air` example, so treat it as stale for GLM-5.3. → [DeepSeek Chat](https://docs.spring.io/spring-ai/reference/api/chat/deepseek-chat.html) · [MiniMax Chat](https://docs.spring.io/spring-ai/reference/api/chat/minimax-chat.html) · [OpenAI Chat](https://docs.spring.io/spring-ai/reference/api/chat/openai-chat.html)
- **LangChain4j (Java):** use `dev.langchain4j:langchain4j-open-ai` (1.24.0 in the docs) with `OpenAiChatModel.builder().baseUrl(...)`. For streaming tool calls against DeepSeek or Qwen, set `accumulateToolCallId(false)`, because those APIs repeat the full tool-call ID in every chunk. → [OpenAI-compatible](https://docs.langchain4j.dev/integrations/language-models/openai-compatible)

More libraries: [Libraries](../../build/libraries/README.md).

## 🗞️ Latest

<!-- newest first -->

### GLM-5.4 ships on the GLM Coding Plan first; API comes later · 2026-11-23 🆕
Z.ai's newest model is available on all GLM Coding Plan tiers (Lite, Pro, Max), with 1M context and 128K max output. Its pay-as-you-go Model API will follow "upon completion of the security assessment", with no date given. In coding tools, use `glm-5.4`, or `glm-5.4[1m]` for the full 1M window. Weekly-quota plans get 1.5× their GLM-5.3 quota, and Z.ai quotes up to 200 tok/s off-peak and 70–80 tok/s at peak *(self-reported)*. As of 2026-11-25, Z.ai's pages don't mention open weights, and OpenRouter doesn't list the model.
**Why it matters:** Coding-plan users can switch now. API, router and third-party-host users stay on `glm-5.3` until the API and weights land. If Claude Code says the `[1m]` model doesn't exist, update Claude Code. Confirm the switch with `/status`.
```json
{
  "env": {
    "CLAUDE_CODE_AUTO_COMPACT_WINDOW": "1000000",
    "ANTHROPIC_DEFAULT_HAIKU_MODEL": "glm-5.4[1m]",
    "ANTHROPIC_DEFAULT_SONNET_MODEL": "glm-5.4[1m]",
    "ANTHROPIC_DEFAULT_OPUS_MODEL": "glm-5.4[1m]"
  }
}
```
Source: [Z.ai GLM Coding Plan: latest model](https://docs.z.ai/devpack/latest-model.md) · [Z.ai model guide](https://docs.z.ai/guides/llm) · [OpenRouter Z.ai models](https://openrouter.ai/~z-ai) · release date from [benchlm.ai tracker](https://benchlm.ai/model-updates) · Added: 2026-11-25

### Together Link: open models inside Claude Code, Codex and OpenCode (beta) · 2026-10-05 (missed earlier) 🆕
A launcher that points Claude Code, Codex CLI, OpenCode, Pi and the Claude and ChatGPT desktop apps at Together-hosted models without editing your own config files. It offers an "Auto" router plus Kimi K3, GLM 5.3, DeepSeek V4.1 Flash and Qwen 3.8, billed at Together's serverless rates. It needs a Together API key. An optional Anthropic key lets Auto send hard Claude Code requests to Claude Opus, billed to your Anthropic account. It is in beta, so commands and the model list may change.
**Why it matters:** It is the quickest way to A/B an open model in the agent you already use. Auto routing can quietly send work to Opus if you add an Anthropic key, so leave that key out if you want only open models.
```bash
curl -fsSL https://link.together.ai/install | bash
togetherlink configure
togetherlink claude
```
Source: [Together Link docs](https://docs.together.ai/docs/togetherlink.md) · [Together blog](https://together.ai/blog/together-link-frontier-quality-open-models-in-the-harness-you-already-use) · Added: 2026-11-25

### Kimi K3.1 Pro gets more ZDR hosts on AI Gateway · 2026-11-04
AI Gateway added Zero Data Retention providers for `moonshotai/kimi-k3.1-pro` and `-highspeed`, which Moonshot had served alone until then. If you set `zeroDataRetention: true`, a request fails rather than falling back to a non-ZDR host.
**Why it matters:** Kimi's flagship is now an option for teams that need ZDR, without self-hosting it.
Source: [Vercel changelog](https://vercel.com/changelog/kimi-k3-1-pro-now-has-more-zdr-providers-on-ai-gateway) · Added: 2026-11-24

## 📚 Reference

- **Upcoming:** on AI Gateway, Modal's Qwen3.8-2.4T-A95B endpoint is marked "Going away Dec 8, 2026". If you pinned it with `order`/`only`, move to Fireworks or Together. ([AI Gateway model page](https://vercel.com/ai-gateway/models/qwen3.8-2.4t-a95b/about))
- **Dashboards:** [Artificial Analysis: Fireworks endpoints](https://artificialanalysis.ai/providers/fireworks) · [AI Gateway: Moonshot AI models](https://vercel.com/ai-gateway/models/labs/moonshotai) · [OpenRouter: Z.ai models](https://openrouter.ai/~z-ai)
- **Self-hosting the same weights** (vLLM, SGLang): [Inference, cost & serving](../cost-and-serving/README.md)
