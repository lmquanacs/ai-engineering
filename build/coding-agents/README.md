# Coding agents & IDEs

_Last updated: 2026-11-18_

> Release notes that change how you work in Claude Code, Codex, Cursor, Copilot, Gemini CLI, Antigravity and Devin. Only items worth acting on are included.

## ⚡ Action items

| When | What | Do this |
|---|---|---|
| by **2026-11-30** | Claude Sonnet 4.5 retires | Update `model` settings, `CLAUDE.md` and CI configs that pin it |
| now | Claude Code ≥ 2.1.319 | Upgrade: it fixes a worktree sandbox escape and a Bash permission bypass |

## 🗞️ Latest releases

### Claude Code 2.1.317 → 2.1.319 · week of 2026-11-02 🆕
- **2.1.319:** auto mode now asks or denies when the server can't check a call (telemetry/flags off) instead of falling back to the local classifier. Fixes a **sandbox escape when creating worktrees** and a **Bash permission bypass** through crafted env prefixes. `CLAUDE_CODE_AUTO_MODE_SERVER=0` restores the old behaviour.
- **2.1.318:** `claude auth status` shows sign-in expiry and warns 10 days before it.
- **2.1.317:** fixes MCP servers disconnecting after the first turn in some desktop sessions; adds a prompt before web/shell tools send the account email over the network. A follow-up relaxed a rule on recreating existing games so it allows genre descriptions.
Source: [Claude Code changelog](https://code.claude.com/docs/en/changelog#2-1-319) · Added: 2026-11-18

### Codex CLI 0.167.0 · week of 2026-11-02 🆕
An **agent command center** (`codex agents --no-daemon`) marks unread results across parallel agents. A session picker switches backends while keeping drafts, and saved chats survive provider switches.
Source: [Codex changelog](https://developers.openai.com/codex/changelog/) · Added: 2026-11-18

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

[Claude Code](https://code.claude.com/docs/en/changelog) · [Codex](https://developers.openai.com/codex/changelog/) · [Cursor](https://cursor.com/changelog) · [Devin](https://docs.devin.ai/release-notes/overview) · [Weekly digest: releases.sh](https://releases.sh/collections/coding-agents)
