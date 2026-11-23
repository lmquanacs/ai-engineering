# Vercel & Cloudflare

_Last updated: 2026-11-24_

> The two edge platforms most AI apps ship on: Vercel (AI Gateway, Sandbox, Workflows) and Cloudflare (Workers AI, AI Gateway, Agents SDK, Sandbox SDK, Durable Objects, hosted MCP servers). For platform engineers choosing where to run model calls, agents and sandboxes. AI SDK releases live in [Libraries · TypeScript](../../build/libraries/typescript.md), and cross-vendor sandbox comparisons in [Agent infrastructure](../../architecture/agent-infrastructure/README.md).

## ⚡ Action items & dates

| When | What | Do this |
|---|---|---|
| now (since 2026-11-20) | **Workers AI deprecated models are switched off** and return HTTP 410 (error code 5028) | Search your code for old `@cf/` model IDs and move to the replacements in the changelog post (for example `@cf/google/embeddinggemma-300m` → `@cf/google/embeddinggemma-2`). Changing embedding models means re-embedding your index. ([Cloudflare changelog](https://developers.cloudflare.com/changelog/product-group/ai)) |
| now | **Sandbox SDK 0.x images before 0.12.14 trust compromised eMudhra intermediate CAs** | On 0.x, install `@cloudflare/sandbox@0.12.14` and use the matching `cloudflare/sandbox:0.12.14` base image. On 1.x, re-pull base images, prune the build cache, redeploy and recreate snapshots. ([Cloudflare changelog, 2026-10-22](https://developers.cloudflare.com/changelog/product-group/ai/2)) |
| now (since 2026-11-03) | **New Cloudflare AI Gateways require authentication**, and it can't be turned off once on | Make sure HTTP clients send a Cloudflare API token before you enable it on existing gateways; Workers bindings are already authenticated. ([AI Gateway changelog](https://developers.cloudflare.com/ai-gateway/changelog/)) |
| **2026-12-01** | **Cloudflare AI Search billing starts** (postponed from 2026-11-01; default sync interval is now 24 h) | Check usage on any AI Search instances before the first billed month. ([Cloudflare changelog](https://developers.cloudflare.com/changelog/product-group/ai)) |
| **2026-12-31** | **Sandbox SDK 0.x stops getting bug and security fixes** | Plan the move to Sandbox SDK 1.0. ([Cloudflare changelog, 2026-09-30](https://developers.cloudflare.com/changelog/product-group/ai/2)) |

---

## ⭐ Start here

### Vercel AI Gateway · one endpoint for many model providers
A hosted gateway at `https://ai-gateway.vercel.sh` with OpenAI Chat Completions, OpenAI Responses, Anthropic Messages and AI SDK interfaces. It handles provider and model fallbacks, BYOK, budgets, request logs with per-request cost, and cross-provider prompt caching. Vercel says it adds no markup to provider token prices, including with BYOK *(self-reported)*. Your app doesn't have to run on Vercel; a team-scoped API key works from anywhere.
```bash
export AI_GATEWAY_API_KEY="your_ai_gateway_api_key"
pnpm add ai@latest
# or route a coding agent (Claude Code and others) through the gateway:
npx vercel@latest ai-gateway setup
```
**Why it matters:** Centralised keys, spend limits and failover without running your own proxy. Data controls (ZDR, provider allowlists, regional inference) are per request or team-wide.
Sources: [AI Gateway docs](https://vercel.com/docs/ai-gateway) · [Getting started](https://vercel.com/docs/ai-gateway/getting-started) · Added: 2026-11-24

### Vercel Sandbox · Linux microVMs for untrusted code
Isolated, on-demand microVMs driven from a TypeScript or Python SDK or the `vercel sandbox` CLI. Sandboxes stop after 5 minutes by default and are persistent by default (the filesystem is snapshotted on stop and restored on resume; snapshots count toward storage billing, so pass `persistent: false` for one-off jobs). Authentication comes from a linked Vercel project via OIDC.
```bash
vercel link && vercel env pull
npm install @vercel/sandbox dotenv @types/node tsx typescript   # TypeScript
uv add vercel python-dotenv                                     # Python
```
**Why it matters:** The default code-execution backend for agents built with eve or the AI SDK on Vercel. Python SDK 1.0 and eve 1.0 are covered in [Agent infrastructure](../../architecture/agent-infrastructure/README.md).
Source: [Sandbox quickstart](https://vercel.com/docs/sandbox/quickstart) · Added: 2026-11-24

### Cloudflare Agents SDK · stateful agents on Durable Objects
The `agents` package adds a lifecycle that starts capabilities such as a harness and WebSockets on a Durable Object, so each agent keeps its own state and can hibernate between events. Recent releases centre on durable harnesses (Pi, OpenCode, Codex) and on `createAI`, which now replaces the separate Workers AI and AI Gateway providers. Needs Node.js 22.19 or later.
```bash
npm create cloudflare@latest -- my-agent --type=hello-world --lang=ts
cd my-agent
npm i agents @earendil-works/pi-durable @earendil-works/pi-ai @earendil-works/pi-schema @earendil-works/chord @cloudflare/computer
```
**Why it matters:** One agent per user or task with no idle compute cost. Release notes (latest `agents` 0.34.0, with breaking changes and no rollback) are tracked in [Agent infrastructure](../../architecture/agent-infrastructure/README.md).
Sources: [Agents quick start](https://developers.cloudflare.com/agents/getting-started/quick-start) · [github.com/cloudflare/agents](https://github.com/cloudflare/agents) · Added: 2026-11-24

### Cloudflare Sandbox SDK 1.0 · containers controlled from a Durable Object
`@cloudflare/sandbox` 1.0 (2026-09-30) lets your Durable Object control its container directly through `this.ctx.container`, with `Files`, `S3Mount` and `DirectoryBackup` helpers, instance sizes such as `lite`, and an `enableInternet` switch. Snapshots and the `durable_object` scheduling policy are in public beta. Local development needs Docker and Wrangler 4.141.0 or later.
```bash
npm create cloudflare@latest -- sandbox-linux --category=hello-world --type=hello-world --lang=ts --no-deploy --no-git --no-agents
```
**Why it matters:** Run agent-generated code next to the agent's state on Cloudflare, with outbound internet off unless you allow it. 0.x support ends 2026-12-31.
Sources: [Sandbox get started](https://developers.cloudflare.com/sandbox/get-started/) · [Changelog: Sandbox SDK 1.0](https://developers.cloudflare.com/changelog/post/2026-09-30-sandbox-sdk-1-0/) · Added: 2026-11-24

---

## 🔼 Vercel

<!-- newest first -->

### AI Gateway: route only to providers headquartered in countries you choose · 2026-11-23 🆕
Set `headquarters` in `providerOptions.gateway` to a list of ISO country codes to allow (`['US', 'GB']`) or to exclude (`['!US']`); a list can't mix both. It filters providers, not models, so a model stays available if any allowed provider serves it. Providers with no country on record, stealth models and non-matching BYOK keys are excluded too. Per request it's free on all plans; a team-wide list (Pro and Enterprise) costs $0.10 per 1,000 billed requests, and request lists can only narrow it. The same day Vercel's changelog also announced that AI Gateway now runs canary ZDR audits; details weren't confirmed for this entry.
**Why it matters:** Lets you meet "no provider based in country X" rules with one option. Note that it controls who owns the provider, not where inference runs; use `inferenceRegion` (US/EU, since 2026-07-27) for that.
Sources: [Docs: provider headquarters](https://vercel.com/docs/ai-gateway/security-and-compliance/provider-headquarters) · [Docs: ZDR](https://vercel.com/docs/ai-gateway/zdr) · [Changelog: regional inference](https://vercel.com/changelog/regional-inference-now-available-on-ai-gateway) · [Vercel changelog](https://vercel.com/changelog.md) · Added: 2026-11-24

### Vercel Drives: storage outside the Sandbox APIs · 2026-11-23 🆕
Drives can now be created and managed with the standalone `@vercel/drives` TypeScript SDK, the `vercel drives` CLI command or the `/v1/drives` REST API, without going through Sandbox APIs.
**Why it matters:** You can prepare or inspect files that sandboxes use from your own backend or CI.
Source: [Vercel changelog](https://vercel.com/changelog.md) · Added: 2026-11-24

### Workflow SDK 5 is production-ready; Sandbox starts up to 4× faster · week of 2026-11-06 🆕
**Workflow SDK 5** (`workflow` on npm) is production-ready: plain async JavaScript with `'use workflow'` and `'use step'` that survives crashes, deploys and long waits. Runs are pinned to one region, which requires `workflow` `5.0.0-beta.33` or later; runs created on 4.x stay in `iad1`. **Vercel Sandbox** starts up to four times faster through regional caching *(self-reported)* and can now use managed npm credentials.
```bash
npm i workflow
```
**Why it matters:** Durable agent loops (`WorkflowAgent` from `@ai-sdk/workflow`, or eve) get a stable base. Upgrading doesn't move existing runs to a new region.
Sources: [Vercel Weekly, 2026-11-16](https://community.vercel.com/t/vercel-weekly-november-16-2026/1000000284) · [Vercel Workflows docs](https://vercel.com/docs/workflows) · Added: 2026-11-24

---

## 🟧 Cloudflare

<!-- newest first -->

### AI Gateway: authentication required, model aliases, stale-key review · 2026-11-03 → 11-06 🆕
- **11-03:** New gateways have authentication on and can't turn it off (sending `authentication: false` returns 400). Existing gateways keep their setting until you enable it.
- **11-04:** **Model aliases** such as `custom/support-fast` name a pool of models with ordered fallback or smart routing. Pass the alias as `model` to `/ai/run` with the `cf-aig-gateway-id` header, then change models without redeploying.
- **11-06:** The Provider Keys page shows last-used dates and flags keys with no activity for over 90 days.

**Why it matters:** Unauthenticated gateways are an open proxy to your provider keys. Aliases move model choice from code into config.
Source: [AI Gateway changelog](https://developers.cloudflare.com/ai-gateway/changelog/) · Added: 2026-11-24

### Workers AI: old models switched off 11-20; EmbeddingGemma 2 · 2026-11-05 → 11-20 🆕
The models announced for deprecation on 11-05 stopped responding on **2026-11-20** (HTTP 410, error 5028). Suggested replacements include `@cf/google/gemma-4-26b-a4b-it`, `@cf/qwen/qwen3.8-27b`, `@cf/deepseek-ai/deepseek-v4.1-flash-1017` and `@cf/zai-org/glm-5.3`. The new `@cf/google/embeddinggemma-2` (11-12) embeds text, images, video and audio into 768 dimensions at $0.0017 per million input tokens.
**Why it matters:** Calls to retired IDs now fail hard, with no fallback. If you are moving off `embeddinggemma-300m`, re-embed the whole corpus, because vectors from the two models aren't comparable.
Source: [Cloudflare changelog (AI)](https://developers.cloudflare.com/changelog/product-group/ai) · Added: 2026-11-24

### `createAI` replaces `workers-ai-provider` and `ai-gateway-provider` · 2026-10-21 🆕
The Agents SDK now exports `createAI` from `agents/models/ai-sdk` for the AI SDK (and Pi AI). It covers `@cf/` Workers AI models, AI Gateway catalog models, `dynamic/<route>` routes and vendor models, with fallback lists and gateway options (caching, retries, `byokAlias`, `zdr`). Cloudflare calls the two old packages "feature frozen and marked as deprecated", with no removal date. Migration: `createWorkersAI({ binding })` → `createAI({ binding })`; `createAiGateway(...)` → `createAI(...)` with `fallback`; AI Search moves to `createAISearchNamespace` in `ai-search-provider`.
```bash
npm i agents
```
**Why it matters:** New AI SDK features won't reach the old providers. Migrate when you next touch model wiring, and pin the old packages until then.
Source: [Cloudflare changelog (AI, page 2)](https://developers.cloudflare.com/changelog/product-group/ai/2) · Added: 2026-11-24

### Hosted MCP: `/sse` retired, step-up authorization, OAuth Provider v1 · 2026-10-01 → 10-22 🆕
Cloudflare's product MCP servers now serve only `/mcp`, and `/sse` returns 410 Gone, so clients that signed in through `/sse` must sign in again (10-22). The Cloudflare API MCP server (`https://mcp.cloudflare.com/mcp`) supports step-up authorization: grant **Minimal** scopes at consent, and it returns an `insufficient_scope` challenge only when a tool needs more (10-19). It also serves Cloudflare skills over MCP (10-10). `@cloudflare/workers-oauth-provider` 1.x splits into `OAuthAuthorizationServer` and `OAuthResourceServer` and supports MCP 2026-07-28 authorization (10-01).
**Why it matters:** Least-privilege grants for agents that use Cloudflare's own MCP servers, and an up-to-date auth library if you host your own MCP server on Workers. Spec background is in [MCP servers](../../build/mcp-servers/README.md).
Source: [Cloudflare changelog (AI, page 2)](https://developers.cloudflare.com/changelog/product-group/ai/2) · Added: 2026-11-24

---

## 📚 Reference

| Topic | Where | Notes |
|---|---|---|
| Vercel changelog | [vercel.com/changelog](https://vercel.com/changelog) | AI Gateway, Sandbox and Workflows posts |
| Vercel AI Gateway docs | [vercel.com/docs/ai-gateway](https://vercel.com/docs/ai-gateway) | Routing, BYOK, ZDR, budgets, pricing |
| Vercel Workflows | [vercel.com/docs/workflows](https://vercel.com/docs/workflows) · [workflow-sdk.dev](https://workflow-sdk.dev) | Pricing is per event, data written and data retained |
| Vercel Sandbox | [vercel.com/docs/sandbox](https://vercel.com/docs/sandbox) | SDK and CLI references |
| Cloudflare changelog (AI) | [developers.cloudflare.com/changelog/product-group/ai](https://developers.cloudflare.com/changelog/product-group/ai) | Workers AI, AI Gateway, Agents, Sandboxes, AI Search |
| Cloudflare AI Gateway changelog | [developers.cloudflare.com/ai-gateway/changelog](https://developers.cloudflare.com/ai-gateway/changelog/) | Also: Web Search API beta (2026-10-02), BYOK-only mode (2026-09-14) |
| Cloudflare Agents SDK | [github.com/cloudflare/agents](https://github.com/cloudflare/agents) | Release notes |
| Cloudflare blog | [blog.cloudflare.com](https://blog.cloudflare.com) | Launch posts |
| Gateways compared | [Architecture](../../architecture/README.md) | Cloudflare and Vercel AI Gateway against other gateways |
