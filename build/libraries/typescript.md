# Libraries · 🟦 TypeScript

← [Back to Libraries](README.md) · _Last updated: 2026-11-20_

| Library | Latest confirmed | What it is | Pick it when |
|---|---|---|---|
| [**Vercel AI SDK**](https://github.com/vercel/ai) (`ai`) | 7.0.177 (2026-11-18) | The most-used TS toolkit for model calls, tool loops, structured output and streaming into UIs. v6 (May 2026) made agents first-class with MCP and tool approval; v7 (Jun 25, 2026) added harness adapters. Apache-2.0. | Default for TS apps, especially web/Next.js |
| [**Mastra**](https://github.com/mastra-ai/mastra) (`@mastra/core`) | 1.85.0 (2026-11-18) | Full-stack agent framework: agents, memory, tools, workflows, evals and observability. Built on the AI SDK. Apache-2.0 (the `ee/` directory has an enterprise licence). | You want batteries included and a local dev playground |
| [**LangGraph.js**](https://github.com/langchain-ai/langgraphjs) | 1.7.5 (2026-11-17) | State-graph orchestration with checkpoints | Same reasons as Python LangGraph, or a shared Py/TS team |
| [**MCP TypeScript SDK**](https://github.com/modelcontextprotocol/typescript-sdk) | `@modelcontextprotocol/sdk` 1.32.2 / `@modelcontextprotocol/server` 2.4.0 (2026-10-23); Tier 1, supports the 2026-07-28 spec. **Upgrade to ≥ 1.32.0 / ≥ 2.3.0** for [four security fixes](../mcp-servers/README.md#-security-notes) | Official MCP SDK | Building MCP servers and clients in Node, Bun or edge runtimes |
| [**Strands Agents (TS)**](https://github.com/strands-agents) (`@strands-agents/sdk`) | 1.26.0 (2026-11-19) | TypeScript version of AWS's Strands agent SDK | Bedrock/AgentCore deployments from TS → [AWS](../../platforms/aws/README.md) |
| **OpenAI Agents SDK (JS)** | — | OpenAI's agents SDK for TS | OpenAI-centric stacks |

## 🆕 Notable changes

### AI SDK 7: harnesses, tool search, retries 🆕
There have been no minor releases since 7.0 (Jun 25), but many additions arrived in patches: **10 harness adapters** (`@ai-sdk/harness-claude-code`, `-deepagents`, `-opencode`…) through `HarnessAgent`, **tool search** for large tool sets, `toolCallConcurrency`, `streamRetries` and WebSocket chat.
**Why it matters:** You can embed a full coding agent such as Claude Code or Codex inside your own TypeScript product with a sandbox session. This is a new building block for internal dev tools.
```ts
import { HarnessAgent } from '@ai-sdk/harness/agent';
import { claudeCode } from '@ai-sdk/harness-claude-code';
```
Source: [Developers Digest: What's new in AI SDK 7](https://www.developersdigest.tech/blog/vercel-ai-sdk-whats-new-2026) · Added: 2026-11-18

Comparison source: [Mastra vs Vercel AI SDK, verified 2026-10-18](https://www.developersdigest.tech/agent-frameworks/compare/mastra-vs-vercel-ai-sdk)

Version numbers confirmed on 2026-11-19 at the [npm registry](https://www.npmjs.com/) (publish dates).
