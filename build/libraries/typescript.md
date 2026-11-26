# Libraries · 🟦 TypeScript

← [Back to Libraries](README.md) · _Last updated: 2026-11-27_

| Library | Latest confirmed | What it is | Pick it when |
|---|---|---|---|
| [**Vercel AI SDK**](https://github.com/vercel/ai) (`ai`) | 7.0.183 (2026-11-26); also 6.0.338 and 5.0.294. Use these rather than 7.0.182 / 6.0.337 / 5.0.293 if you generate images through Responses, see below | The most-used TS toolkit for model calls, tool loops, structured output and streaming into UIs. v6 (May 2026) made agents first-class with MCP and tool approval; v7 (Jun 25, 2026) added harness adapters. Apache-2.0. | Default for TS apps, especially web/Next.js |
| [**Mastra**](https://github.com/mastra-ai/mastra) (`@mastra/core`) | 1.86.0 (2026-11-25; adds durable experiments and an `interrupted` thread run status) | Full-stack agent framework: agents, memory, tools, workflows, evals and observability. Built on the AI SDK. Apache-2.0 (the `ee/` directory has an enterprise licence). | You want batteries included and a local dev playground |
| [**LangGraph.js**](https://github.com/langchain-ai/langgraphjs) | 1.7.5 (2026-11-17) | State-graph orchestration with checkpoints | Same reasons as Python LangGraph, or a shared Py/TS team |
| [**MCP TypeScript SDK**](https://github.com/modelcontextprotocol/typescript-sdk) | `@modelcontextprotocol/sdk` 1.32.2 / `@modelcontextprotocol/server` 2.4.0 (2026-10-23); Tier 1, supports the 2026-07-28 spec. **Upgrade to ≥ 1.32.0 / ≥ 2.3.0** for [four security fixes](../mcp-servers/README.md#-security-notes) | Official MCP SDK | Building MCP servers and clients in Node, Bun or edge runtimes |
| [**Strands Agents (TS)**](https://github.com/strands-agents) (`@strands-agents/sdk`) | 1.26.0 (2026-11-19) | TypeScript version of AWS's Strands agent SDK | Bedrock/AgentCore deployments from TS → [AWS](../../platforms/aws/README.md) |
| **OpenAI Agents SDK (JS)** | — | OpenAI's agents SDK for TS | OpenAI-centric stacks |

## 🆕 Notable changes

### AI SDK: the new 64 MiB event cap broke multi-image Responses streams; fixed next day · 7.0.183 / 6.0.338 / 5.0.294 (2026-11-26) 🆕
Yesterday's per-event cap was too small for OpenAI and xAI Responses streams: their `response.completed` event repeats every output item, including base64 generated images, so a stream with several large images failed after all of them had arrived. In `@ai-sdk/provider-utils` 5.0.85, `createEventSourceResponseHandler` takes a `maxEventSize` option, and the OpenAI and xAI Responses models use it to accept events of up to 512 MiB.
**Why it matters:** if you upgraded for the memory fix and use image generation through Responses, upgrade again, including the provider packages (`@ai-sdk/openai`, `@ai-sdk/xai`) that were republished the same day.
Source: [`@ai-sdk/provider-utils` CHANGELOG](https://raw.githubusercontent.com/vercel/ai/main/packages/provider-utils/CHANGELOG.md) · [npm: ai](https://www.npmjs.com/package/ai?activeTab=versions) · Added: 2026-11-27

### AI SDK: a single streamed event is now capped at 64 MiB · 7.0.182 / 6.0.337 / 5.0.293 (2026-11-25) 🆕
`@ai-sdk/provider-utils` buffered a server-sent event until it was complete, with no limit, so a streaming response that never finished an event could use up memory and crash the process. `parseJsonEventStream` and `createEventSourceResponseHandler` now stop at 67,108,864 characters per event, fail the stream and cancel the body; the cap also covers what `useChat` and `useCompletion` read, and a new `maxEventSize` option changes it. The fix ships in provider-utils 5.0.84, 4.0.68 and 3.0.47, which `ai` 7.0.182, 6.0.337 and 5.0.293 depend on.
**Why it matters:** Upgrade on whichever major line you run, especially if your app streams from a gateway or endpoint you don't control. If you legitimately stream very large single events, raise `maxEventSize` rather than seeing new stream errors.
Source: [`@ai-sdk/provider-utils` 5.0.84 CHANGELOG](https://unpkg.com/@ai-sdk/provider-utils@5.0.84/CHANGELOG.md) · [`ai` 7.0.182 CHANGELOG](https://unpkg.com/ai@7.0.182/CHANGELOG.md) · Added: 2026-11-26

### AI SDK 6.x: Google MCP connector credentials leaked into telemetry · 6.0.336 (2026-11-22) 🆕
In the v6 line, `google.mcp_server` tool definitions (the Gemini Interactions MCP connector) can carry headers such as `Authorization`, and telemetry redaction only recognised OpenAI tool ids, so those credentials were written to the `ai.prompt.tools` span attribute of `generateText` and `streamText`. The changelog lists the fix under 6.0.335; the first v6 release on npm that contains it is 6.0.336.
**Why it matters:** If you stay on AI SDK 6 with telemetry on and pass headers to Google's MCP connector, upgrade, then rotate those tokens and check your tracing backend for stored spans.
Source: [`ai` 6.0.336 CHANGELOG](https://unpkg.com/ai@6.0.336/CHANGELOG.md) · [`ai` on npm](https://www.npmjs.com/package/ai?activeTab=versions) · Added: 2026-11-23

### AI SDK 7.0.178: signed tool approvals could be replayed for auto-denied calls 🆕
With `experimental_toolApprovalSecret` set, `generateText` and `streamText` also signed the approval request for tool calls the approval policy had denied automatically, so a client that controls message history could send it back as approved and run the denied tool. 7.0.178 stops signing those requests; it also copies `prepareStep` message arrays per step and forwards the `preliminary` flag on provider-executed tool results. 7.0.179 lets `gateway.experimental_realtime()` use `openai/gpt-live-1` and `openai/gpt-live-1.1`.
**Why it matters:** If you use signed tool approvals, upgrade **and rotate the secret**: signatures issued earlier for automatic denials stay valid until you do (pending approvals must then be re-requested).
Source: [`ai` CHANGELOG (npm 7.0.179)](https://www.npmjs.com/package/ai?activeTab=versions) · [vercel/ai releases](https://github.com/vercel/ai/releases) · Added: 2026-11-22

### AI SDK 7: harnesses, tool search, retries
There have been no minor releases since 7.0 (Jun 25), but many additions arrived in patches: **10 harness adapters** (`@ai-sdk/harness-claude-code`, `-deepagents`, `-opencode`…) through `HarnessAgent`, **tool search** for large tool sets, `toolCallConcurrency`, `streamRetries` and WebSocket chat.
**Why it matters:** You can embed a full coding agent such as Claude Code or Codex inside your own TypeScript product with a sandbox session. This is a new building block for internal dev tools.
```ts
import { HarnessAgent } from '@ai-sdk/harness/agent';
import { claudeCode } from '@ai-sdk/harness-claude-code';
```
Source: [Developers Digest: What's new in AI SDK 7](https://www.developersdigest.tech/blog/vercel-ai-sdk-whats-new-2026) · Added: 2026-11-18

Comparison source: [Mastra vs Vercel AI SDK, verified 2026-10-18](https://www.developersdigest.tech/agent-frameworks/compare/mastra-vs-vercel-ai-sdk)

Version numbers confirmed on 2026-11-26 at the [npm registry](https://www.npmjs.com/) (publish dates).
