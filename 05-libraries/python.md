# 05 · Libraries · 🐍 Python

← [Back to Libraries](README.md) · _Last updated: 2026-11-18_

| Library | Latest confirmed | What it is | Pick it when |
|---|---|---|---|
| [**Pydantic AI**](https://github.com/pydantic/pydantic-ai) | 2.57.0 (2026-10-16) | Type-safe agent framework from the Pydantic team. V2 has been stable since 2026-06-23 and uses a "capabilities-first" design. It supports MCP and uses OpenTelemetry tracing (Logfire). Requires Python 3.11+. MIT. | Default for new Python agents, especially if you already use Pydantic or FastAPI |
| [**LangGraph**](https://github.com/langchain-ai/langgraph) | 1.2.16 (2026-10-16) | Graph/state-machine orchestration with durable checkpoints, from LangChain. Python and TS. MIT. | You need explicit control flow, human-in-the-loop interrupts and resumable long runs |
| [**MCP Python SDK**](https://github.com/modelcontextprotocol/python-sdk) | Tier 1 SDK, supports the 2026-07-28 spec | Official SDK for building MCP servers and clients | Exposing your Python tools to any agent |
| [**Strands Agents**](https://github.com/strands-agents) (AWS) | 1.61.1 (2026-10-15) | AWS's open-source, model-driven agent harness SDK with behavioural middleware and sandboxing; deploys to Bedrock AgentCore or anywhere. Apache-2.0. | AWS/Bedrock-centric teams → [AWS](../16-aws/README.md) |
| **OpenAI Agents SDK** | — | OpenAI's lightweight agents and handoffs SDK | Mostly OpenAI models, with simple triage/handoff patterns |
| **CrewAI** | — | Role-based multi-agent crews | Prototyping multi-role workflows (check the [evidence on committees](../03-agentic-workflows/README.md#-latest-evidence-what-actually-moves-the-needle) first) |

## 🆕 Notable changes

### Pydantic AI V2: fast release cadence 🆕
It went from v2.50.0 (Sep 24) to v2.57.0 (Oct 15). The companion *Harness* is still 0.x, so its API may change.
**Why it matters:** Pin minor versions in production and read the release notes before upgrading.
Source: [Developers Digest: Pydantic AI V2 in late 2026](https://www.developersdigest.tech/blog/pydantic-ai-whats-new-2026) · Added: 2026-11-18

Comparison source: [Pydantic AI vs LangGraph, verified 2026-10-18](https://www.developersdigest.tech/agent-frameworks/compare/pydantic-ai-vs-langgraph)
