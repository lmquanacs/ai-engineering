# Libraries · 🐍 Python

← [Back to Libraries](README.md) · _Last updated: 2026-11-25_

| Library | Latest confirmed | What it is | Pick it when |
|---|---|---|---|
| [**Pydantic AI**](https://github.com/pydantic/pydantic-ai) | 2.73.0 (2026-11-24; release notes not yet reviewed here) | Type-safe agent framework from the Pydantic team. V2 has been stable since 2026-06-23 and uses a "capabilities-first" design. It supports MCP and uses OpenTelemetry tracing (Logfire). Requires Python 3.11+. MIT. | Default for new Python agents, especially if you already use Pydantic or FastAPI |
| [**LangGraph**](https://github.com/langchain-ai/langgraph) | 1.2.24 (2026-11-20) | Graph/state-machine orchestration with durable checkpoints, from LangChain. Python and TS. MIT. | You need explicit control flow, human-in-the-loop interrupts and resumable long runs |
| [**MCP Python SDK**](https://github.com/modelcontextprotocol/python-sdk) | `mcp` 2.3.0 (2026-10-02); Tier 1, supports the 2026-07-28 spec | Official SDK for building MCP servers and clients | Exposing your Python tools to any agent |
| [**Strands Agents**](https://github.com/strands-agents) (AWS) | 1.66.0 (2026-11-23) | AWS's open-source, model-driven agent harness SDK with behavioural middleware and sandboxing; deploys to Bedrock AgentCore or anywhere. Apache-2.0. | AWS/Bedrock-centric teams → [AWS](../../platforms/aws/README.md) |
| [**Google ADK**](https://github.com/google/adk-python) | 2.15.0 (2026-11-19) | Google's Agent Development Kit: agents, tools, sessions, eval CLI and live (voice) runs; works with Gemini and other models. Apache-2.0. | Gemini/Vertex-centric teams, or you want built-in `adk eval` |
| **OpenAI Agents SDK** | 0.26.0 (2026-11-24; a minor bump, which this SDK uses for breaking changes, so read the release notes before upgrading) | OpenAI's lightweight agents and handoffs SDK. 0.25.0 removed the Runloop sandbox provider. | Mostly OpenAI models, with simple triage/handoff patterns |
| **CrewAI** | — | Role-based multi-agent crews | Prototyping multi-role workflows (check the [evidence on committees](../../architecture/agentic-workflows/README.md#-latest-evidence-what-actually-moves-the-needle) first) |

## 🆕 Notable changes

### Google ADK 2.15.0: per-session sandboxes, pass^k evals, builder removed · 2026-11-19 🆕
`BaseEnvironment` now gets the run's context and a `scope` (`SHARED`, `USER`, `SESSION`), so sandboxes can be isolated per user or session. `adk eval` reports `pass@k` and `pass^k` across runs, and `run_live` runs tool calls in the background so voice streams keep flowing.
**Why it matters:** Breaking: the Visual Agent Builder routes and `google.adk.cli.built_in_agents` are gone; `McpInstructionProvider` no longer fills prompt arguments from `session.state` (pass `arguments=`); dynamic instruction routing is on by default (opt out with `ADK_DISABLE_DYNAMIC_INSTRUCTION_ROUTING=1`).
Source: [ADK Python CHANGELOG](https://raw.githubusercontent.com/google/adk-python/main/CHANGELOG.md) · Added: 2026-11-21

### Pydantic AI 2.71.0: renames, `PermissionRule`, `ModelRouter` · 2026-11-18 🆕
Compatibility changes: `PeerNetwork` is renamed `PeerConnection`; `StackOne`'s `api_key` is deprecated in favour of a new `auth` parameter; `DEPRECATED_ANTHROPIC_MODELS` is deprecated; pause/resume behaviour changed for deferred tools and `BackgroundTools`; the in-process `MCPToolsetClient` server is typed as a protocol rather than `FastMCP`. New: `ModelRouter`, `PermissionRule` (allow, ask or deny tool calls), harness capabilities such as `RequireVerification`, `Goal` and `WrapUpAtLimits`, secret masking with `Shell(secret_env=)`, and HTTP 408 now raises `ModelTimeoutError`.
**Why it matters:** `PermissionRule` gives Python agents a declarative allow/ask/deny layer for tools. Check for the renamed and deprecated names before upgrading.
Source: [Pydantic AI v2.71.0 release](https://github.com/pydantic/pydantic-ai/releases/tag/v2.71.0) · Added: 2026-11-20

### LangGraph 1.2.23: `Send` tool calls get typed state · 2026-11-19 🆕
Raises the `langgraph-prebuilt` minimum to 1.1.3, which makes tool calls dispatched with `Send` receive the same typed state as an edge. Not labelled breaking, but `ToolNode` code that read state in `Send` branches may see different values.
Source: [langgraph PR #9742](https://github.com/langchain-ai/langgraph/pull/9742) · [PyPI](https://pypi.org/project/langgraph/) · Added: 2026-11-20

### Pydantic AI 2.60: tool retries no longer produce `RetryPromptPart` 🆕
Since v2.60.0 (2026-10-22), a tool retry is recorded as a `ToolReturnPart` with `outcome='retried'`, and a retry that answers no tool call is a `RetryFeedbackPart`. `RetryPromptPart` is deprecated, and `result.usage()` on `RunUsage` is deprecated in favour of `result.usage`.
**Why it matters:** Code that checks `isinstance(part, RetryPromptPart)` (eval scorers, logging, dashboards) now silently finds no tool errors, with no exception or warning. Switch to `is_retry(part)` before upgrading past 2.59.
Source: [Pydantic AI upgrade guide](https://pydantic.dev/docs/ai/project/changelog/) · latest 2.70.0 on [PyPI](https://pypi.org/project/pydantic-ai/) (2026-11-17) · Added: 2026-11-19

### Pydantic AI V2: fast release cadence 🆕
It went from v2.50.0 (Sep 24) to v2.57.0 (Oct 15). The companion *Harness* is still 0.x, so its API may change.
**Why it matters:** Pin minor versions in production and read the release notes before upgrading.
Source: [Developers Digest: Pydantic AI V2 in late 2026](https://www.developersdigest.tech/blog/pydantic-ai-whats-new-2026) · Added: 2026-11-18

Comparison source: [Pydantic AI vs LangGraph, verified 2026-10-18](https://www.developersdigest.tech/agent-frameworks/compare/pydantic-ai-vs-langgraph)

Version numbers confirmed on 2026-11-25 at [PyPI](https://pypi.org/) (release upload dates).
