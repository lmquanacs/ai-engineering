# Libraries · 🐍 Python

← [Back to Libraries](README.md) · _Last updated: 2026-11-28_

| Library | Latest confirmed | What it is | Pick it when |
|---|---|---|---|
| [**Pydantic AI**](https://github.com/pydantic/pydantic-ai) | 2.76.0 (2026-11-27; not yet in the upgrade guide). 2.73.0–2.75.0 change fallback, usage and instruction behaviour, see below | Type-safe agent framework from the Pydantic team. V2 has been stable since 2026-06-23 and uses a "capabilities-first" design. It supports MCP and uses OpenTelemetry tracing (Logfire). Requires Python 3.11+. MIT. | Default for new Python agents, especially if you already use Pydantic or FastAPI |
| [**LangGraph**](https://github.com/langchain-ai/langgraph) | 1.2.24 (2026-11-20) | Graph/state-machine orchestration with durable checkpoints, from LangChain. Python and TS. MIT. | You need explicit control flow, human-in-the-loop interrupts and resumable long runs |
| [**MCP Python SDK**](https://github.com/modelcontextprotocol/python-sdk) | `mcp` 2.3.0 (2026-10-02); Tier 1, supports the 2026-07-28 spec | Official SDK for building MCP servers and clients | Exposing your Python tools to any agent |
| [**Strands Agents**](https://github.com/strands-agents) (AWS) | 1.67.0 (2026-11-25; release notes not reviewed here) | AWS's open-source, model-driven agent harness SDK with behavioural middleware and sandboxing; deploys to Bedrock AgentCore or anywhere. Apache-2.0. | AWS/Bedrock-centric teams → [AWS](../../platforms/aws/README.md) |
| [**Google ADK**](https://github.com/google/adk-python) | 2.15.1 (2026-11-24; bug fixes) | Google's Agent Development Kit: agents, tools, sessions, eval CLI and live (voice) runs; works with Gemini and other models. Apache-2.0. | Gemini/Vertex-centric teams, or you want built-in `adk eval` |
| **OpenAI Agents SDK** | 0.26.0 (2026-11-24; a minor bump, which this SDK uses for breaking changes, so read the release notes before upgrading) | OpenAI's lightweight agents and handoffs SDK. 0.25.0 removed the Runloop sandbox provider. | Mostly OpenAI models, with simple triage/handoff patterns |
| **CrewAI** | — | Role-based multi-agent crews | Prototyping multi-role workflows (check the [evidence on committees](../../architecture/agentic-workflows/README.md#-latest-evidence-what-actually-moves-the-needle) first) |

## 🆕 Notable changes

### Pydantic AI 2.74.0 and 2.75.0: upgrade notes now published · 2026-11-25 🆕
The upgrade guide now lists compatibility changes for both releases.
- **2.75.0:**
  - Empty or unreadable model responses raise `ModelEmptyResponseError` or `ModelInvalidResponseError`. These subclass both `ModelAPIError` and `UnexpectedModelBehavior`, and `FallbackModel`/`ModelFallback` now fall back on them by default.
  - Gemini thinking tokens called through `OpenAIChatModel` now count as output, so cost goes up and `UsageLimits` trip sooner.
  - On the Gemini API, `thinking=False` for `gemini-2.5-flash` sends `thinking_budget=128` instead of 0. The guide says this lasts until a reroute on 2026-12-01, after which a budget of 0 returns 400.
  - Capabilities whose authority is lowered with `with_authority()`, including MCP server instructions, now send their instructions as framed data on the user channel instead of in the system prompt.
  - Durable runs that are in flight on Temporal or DBOS during the upgrade can hit nondeterminism errors.
- **2.74.0:** on GPT-6.2, static instructions go out as leading input messages. Continuing with `openai_previous_response_id` and no `message_history` now inherits them.

**Why it matters:**
- Check any `except ModelAPIError` that comes before `except UnexpectedModelBehavior`.
- Re-tune token limits if you call Gemini through the OpenAI-compatible endpoint.
- Drain durable workflows before you upgrade.
- 2.76.0 (2026-11-27) is on PyPI but not yet in the guide.

Source: [Pydantic AI upgrade guide](https://pydantic.dev/docs/ai/project/changelog/) · [PyPI](https://pypi.org/project/pydantic-ai/) · Added: 2026-11-28

### Pydantic AI 2.73.0: unsupported settings dropped, `FallbackModel` stops falling back · 2026-11-24 🆕
Pydantic AI no longer sends unified model settings that Claude, Gemini and Grok models reject; it drops them instead. Requests to models Anthropic or OpenAI have deprecated now raise a `DeprecatedModelWarning`, the `openai` dependency floor rises from 3.31.0 to 3.50.0, and OpenAI Responses `input_transformations` show up in `provider_details` and on the request span. Notes for 2.74.0 and 2.75.0 are in the entry above.
**Why it matters:** A `FallbackModel` that relied on the provider's 400 to move to a later model now stays on the first model and silently runs without the setting. If you need the setting honoured, list a model that supports it first. Also check that your lockfile allows `openai` ≥ 3.50.0.
Source: [Pydantic AI upgrade guide, v2.73.0](https://pydantic.dev/docs/ai/project/changelog/) · latest 2.75.0 on [PyPI](https://pypi.org/project/pydantic-ai/) (2026-11-25) · Added: 2026-11-26

### Google ADK 2.15.0: per-session sandboxes, pass^k evals, builder removed · 2026-11-19 🆕
`BaseEnvironment` now gets the run's context and a `scope` (`SHARED`, `USER`, `SESSION`), so sandboxes can be isolated per user or session. `adk eval` reports `pass@k` and `pass^k` across runs, and `run_live` runs tool calls in the background so voice streams keep flowing.
**Why it matters:** Breaking: the Visual Agent Builder routes and `google.adk.cli.built_in_agents` are gone; `McpInstructionProvider` no longer fills prompt arguments from `session.state` (pass `arguments=`); dynamic instruction routing is on by default (opt out with `ADK_DISABLE_DYNAMIC_INSTRUCTION_ROUTING=1`).
Source: [ADK Python CHANGELOG](https://raw.githubusercontent.com/google/adk-python/main/CHANGELOG.md) · Added: 2026-11-21

### Pydantic AI 2.71.0: renames, `PermissionRule`, `ModelRouter` · 2026-11-18
Compatibility changes: `PeerNetwork` is renamed `PeerConnection`; `StackOne`'s `api_key` is deprecated in favour of a new `auth` parameter; `DEPRECATED_ANTHROPIC_MODELS` is deprecated; pause/resume behaviour changed for deferred tools and `BackgroundTools`; the in-process `MCPToolsetClient` server is typed as a protocol rather than `FastMCP`. New: `ModelRouter`, `PermissionRule` (allow, ask or deny tool calls), harness capabilities such as `RequireVerification`, `Goal` and `WrapUpAtLimits`, secret masking with `Shell(secret_env=)`, and HTTP 408 now raises `ModelTimeoutError`.
**Why it matters:** `PermissionRule` gives Python agents a declarative allow/ask/deny layer for tools. Check for the renamed and deprecated names before upgrading.
Source: [Pydantic AI v2.71.0 release](https://github.com/pydantic/pydantic-ai/releases/tag/v2.71.0) · Added: 2026-11-20

### LangGraph 1.2.23: `Send` tool calls get typed state · 2026-11-19
Raises the `langgraph-prebuilt` minimum to 1.1.3, which makes tool calls dispatched with `Send` receive the same typed state as an edge. Not labelled breaking, but `ToolNode` code that read state in `Send` branches may see different values.
Source: [langgraph PR #9742](https://github.com/langchain-ai/langgraph/pull/9742) · [PyPI](https://pypi.org/project/langgraph/) · Added: 2026-11-20

### Pydantic AI 2.60: tool retries no longer produce `RetryPromptPart`
Since v2.60.0 (2026-10-22), a tool retry is recorded as a `ToolReturnPart` with `outcome='retried'`, and a retry that answers no tool call is a `RetryFeedbackPart`. `RetryPromptPart` is deprecated, and `result.usage()` on `RunUsage` is deprecated in favour of `result.usage`.
**Why it matters:** Code that checks `isinstance(part, RetryPromptPart)` (eval scorers, logging, dashboards) now silently finds no tool errors, with no exception or warning. Switch to `is_retry(part)` before upgrading past 2.59.
Source: [Pydantic AI upgrade guide](https://pydantic.dev/docs/ai/project/changelog/) · latest 2.70.0 on [PyPI](https://pypi.org/project/pydantic-ai/) (2026-11-17) · Added: 2026-11-19

### Pydantic AI V2: fast release cadence
It went from v2.50.0 (Sep 24) to v2.57.0 (Oct 15). The companion *Harness* is still 0.x, so its API may change.
**Why it matters:** Pin minor versions in production and read the release notes before upgrading.
Source: [Developers Digest: Pydantic AI V2 in late 2026](https://www.developersdigest.tech/blog/pydantic-ai-whats-new-2026) · Added: 2026-11-18

Comparison source: [Pydantic AI vs LangGraph, verified 2026-10-18](https://www.developersdigest.tech/agent-frameworks/compare/pydantic-ai-vs-langgraph)

Version numbers confirmed on 2026-11-28 at [PyPI](https://pypi.org/) (release upload dates).
