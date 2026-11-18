# Coding agents & IDEs

_Last updated: 2026-11-19_

> Release notes that change how you work in Claude Code, Codex, Cursor, Copilot, Gemini CLI, Antigravity, Devin and Kiro. Only items worth acting on are included.

## ⚡ Action items

| When | What | Do this |
|---|---|---|
| now | Claude Code ≥ 2.1.325 | Upgrade: 2.1.321–2.1.325 fix an MCP OAuth refresh-token leak on redirect, several sandbox and Bash permission bypasses, and zstd decoding. Sandboxed Bash now prompts by default; set `sandbox.autoAllowBashIfSandboxed: true` to keep the old behaviour |
| now | Claude Code: unknown model IDs assume a 1M context (2.1.323) | If you route to a gateway or custom model with a smaller window, set `CLAUDE_CODE_DISABLE_1M_CONTEXT=1` or `CLAUDE_CODE_MAX_CONTEXT_TOKENS` |
| now | Codex CLI ≥ 0.169.0: `codex exec` ignores project config and MCP servers in untrusted folders | Add `--trust` to CI jobs that rely on repo-level Codex config or MCP servers |
| **2026-11-26** | Kiro enterprise daily metrics move to 00:30 UTC | Shift any job that reads the daily metrics export |
| by **2026-11-30** | Claude Sonnet 4.5 retires | Update `model` settings, `CLAUDE.md` and CI configs that pin it |
| **Feb 2027** | Copilot in VS Code: the Local harness is removed | Move remaining workflows to the Copilot harness (already the default for new sessions) |

## 🗞️ Latest releases

### Claude Code 2.1.317 → 2.1.325 · 2026-11-02 → 11-13 🆕
- **2.1.325:** security fixes for zstd response decoding, a Bash allow rule that could run a different program than the one it names, compound commands that ran without asking, and subagents changing external artifacts without asking. **Behaviour change:** sandboxed Bash commands now go through the normal permission prompt (`sandbox.autoAllowBashIfSandboxed: true` restores the old behaviour). Scheduled tasks and `/loop` ask before running skills that declare `allowed-tools` or hooks, and `-p`/SDK runs only apply `.claude/settings.local.json` allow rules in trusted folders.
- **2.1.323:** experimental opt-in **Code Mode** (Claude writes JavaScript to call its tools); `engines["claude-code"]` in `plugin.json` pins plugins to a version range. Fixes Bash deny/ask rules missed through `sudo`/`env` wrappers and Write/Edit ignoring `Read` deny rules. Unrecognised model IDs now assume a 1M context window (`CLAUDE_CODE_DISABLE_1M_CONTEXT=1` keeps 200K).
- **2.1.321:** **Claude Fable 5.2** (`claude-fable-5-2`) becomes the default Fable model; saved Fable 5.1 selections move to `fable` (`/model claude-fable-5-1` to switch back). Fixes MCP OAuth sending refresh tokens to another host on redirect, read-only Bash running outside the sandbox without a prompt, and deny rules not covering `cp`/`mv` destinations.
- **2.1.319:** auto mode now asks or denies when the server can't check a call (telemetry/flags off) instead of falling back to the local classifier. Fixes a **sandbox escape when creating worktrees** and a **Bash permission bypass** through crafted env prefixes. `CLAUDE_CODE_AUTO_MODE_SERVER=0` restores the old behaviour.
- **2.1.318:** `claude auth status` shows sign-in expiry and warns 10 days before it.
- **2.1.317:** fixes MCP servers disconnecting after the first turn in some desktop sessions; adds a prompt before web/shell tools send the account email over the network.

**Why it matters:** Three releases in a row close permission and sandbox gaps, and 2.1.325 changes a sandbox default that unattended runs may depend on.
Source: [Claude Code CHANGELOG (v2.1.325 tag)](https://raw.githubusercontent.com/anthropics/claude-code/v2.1.325/CHANGELOG.md) · Added: 2026-11-18 · Updated: 2026-11-19

### Codex CLI 0.167 → 0.170 + GPT-6.2 Astra/Sol · 2026-11-17 → 11-18 🆕
- **GPT-6.2 Astra and GPT-6.2 Sol** (2026-11-17) are available in Codex: Astra for the hardest projects, Sol for everyday coding. OpenAI says Sol completes more tasks than GPT-6.1 Sol on the same paid plan *(self-reported)*.
- **0.170.0** (2026-11-18): MCP OAuth credential race fixes, experimental support for identically named MCP servers across environments, and an HTTP fallback for oversized WebSocket requests.
- **0.169.0** (2026-11-13): `codex exec` keeps project config and MCP servers disabled in untrusted directories unless you pass `--trust`. Adds multiple side-chat tabs and custom model providers configurable from the terminal.
- **0.168.0** (2026-11-13): side-by-side conversation panes (`features.tui_workspace`) and a default model provider for new chats.
- **0.167.0:** an **agent command center** (`codex agents --no-daemon`) marks unread results across parallel agents.

**Why it matters:** CI jobs that run `codex exec` in a fresh checkout may silently lose repo config and MCP servers after 0.169.0.
Source: [Codex changelog](https://learn.chatgpt.com/codex/changelog) · Added: 2026-11-18 · Updated: 2026-11-19

### GitHub Copilot: Fable 5.2, Gemini 4 Carbon, Local harness retiring · 2026-11-16 🆕
- **Claude Fable 5.2** and **Gemini 4 Carbon** are available on Copilot Pro+, Max, Business and Enterprise. Fable 5.2's policy is **off by default** for Business and Enterprise, so an admin must enable it.
- The Copilot app re-authenticates MCP servers in place when they require sign-in again, and GitHub Enterprise Server support is GA in the app (cloud sessions are not supported for GHES).
- VS Code 1.146: the **Local harness is scheduled for removal in February 2027**; the Copilot harness is already the default for new sessions.

**Why it matters:** Org admins need to flip a policy before developers can use Fable 5.2, and teams on the Local harness have a migration deadline.
Source: [GitHub changelog: Copilot weekly releases, November 9](https://github.blog/changelog/2026-11-16-github-copilot-weekly-releases-november-9) · Added: 2026-11-19

### Kiro: admin-enforced sandboxing and org sign-in for MCP · 2026-11-16 → 11-17 🆕
- **Local Sandbox Controls:** admins can require sandboxing for commands and local stdio MCP servers, and developers can't turn it off in client settings.
- **CLI 3.5.0:** organisation sign-in for MCP servers, so one identity-provider login covers every server set to use it.
- **CLI 3.4.0:** hooks can rewrite tool inputs and answer permission prompts; a `deny` from any hook overrides an `allow`.
- Enterprise admins can stream LLM requests and tool calls as OpenTelemetry events (exports exclude prompts, responses and code). Daily metrics move to 00:30 UTC on 2026-11-26.

**Why it matters:** Platform teams can now enforce a sandbox and central MCP auth for Kiro rather than relying on each developer's settings.
Source: [Kiro changelog](https://kiro.dev/changelog/index) · Added: 2026-11-19

### Cursor: voice chat + live app hosting · week of 2026-11-02 🆕
- **Realtime voice** with coding agents in the Agents Window, IDE, web and iOS; zero data retention in Privacy Mode.
- **Build live apps:** cloud agents scaffold a web app, provision Postgres, add Cursor SSO and deploy to your domain. Exposed-secret checks must pass first.
Sources: [voice chat](https://cursor.com/changelog/voice-chat) · [build live apps](https://cursor.com/changelog/build-live-apps) · Added: 2026-11-18

### Google Antigravity `/swarm` · 2026-11-12 🆕
A multi-agent `/swarm` command and an orchestrator mode for planning parallel work.
Source: [ThursdAI November releases](https://thursdai.news/releases/2026-11) · Added: 2026-11-18

### Devin: enterprise governance · 2026-10-30 → 11-06 🆕
Self-serve SSO, hierarchical budgets, default PAT approval, session-sharing controls, sign-out everywhere, a 1,000-repo multi-repo scan cap, and OAuth discovery when an MCP server returns 401 mid-session.
Source: [Devin release notes](https://docs.devin.ai/release-notes/overview#november-6-2026) · Added: 2026-11-18

### DeepSeek Harness: Creator Mode · 2026-11-05 🆕
Turns chat prompts into installable coding-harness plugins.
Source: [deepseek-ai/deepseek-harness](https://github.com/deepseek-ai/deepseek-harness) · Added: 2026-11-18

## 📐 Big picture: the stack is layering, not consolidating

Through 2026 the tools have composed rather than merged. Cursor and IDEs act as the **orchestration** layer, while Claude Code and Codex act as **executors** and reviewers. OpenAI even ships an official Codex plugin that runs inside Claude Code, and Cursor joined the ACP registry so it can run as an agent inside JetBrains IDEs. Plan your setup around which layer each tool fills.
Source: [The New Stack](https://thenewstack.io/ai-coding-tool-stack/) · Added: 2026-11-18

## 🔗 Changelogs (bookmarks)

[Claude Code](https://code.claude.com/docs/en/changelog) · [Codex](https://developers.openai.com/codex/changelog/) · [Cursor](https://cursor.com/changelog) · [Devin](https://docs.devin.ai/release-notes/overview) · [Copilot](https://github.blog/changelog/) · [Kiro](https://kiro.dev/changelog/index) · [Weekly digest: releases.sh](https://releases.sh/collections/coding-agents)
