# Agent skills

> Reusable `SKILL.md` instruction packs that coding agents load when they need them. This page covers cross-language development skills. Stack-specific pages: **[Python](python.md) · [TypeScript](typescript.md) · [Java/Kotlin + Spring Boot](jvm-spring-kotlin.md)** · **[Starter skills to copy](starter-skills/)**

_Last updated: 2026-11-18_

## What a skill is (30-second version)

A skill is a folder containing a `SKILL.md`: a short description that tells the agent *when* to load it, followed by instructions and optional scripts or reference files. Skills follow the open Agent Skills format, so the same folder works in Claude Code, Codex, Cursor, Copilot and others.

```bash
# Install a skill from any GitHub repo (Vercel's skills CLI / skills.sh registry)
npx -y skills add <owner>/<repo> --skill <skill-name> --agent claude-code
# → installs into .claude/skills/ of the current project
```

**Ecosystem size:** Vercel reports that skills.sh passed 1M skills and about 280M installs within seven months of launch (Jan 2026). Most of that is noise, which is why this page is curated.

---

## ⭐ Start here: language-agnostic dev-workflow skills

### superpowers · `obra/superpowers` · methodology
A software development methodology for coding agents, built from reusable skills: clarify the spec, write failing tests first, plan, then run subagent-driven development.
**Why it matters:** In Surge AI's Nov 2026 controlled study, the clarify-spec + TDD loop gave a statistically significant gain (+2.4 points) for about 10% more cost. Few workflow plugins showed any gain at all. See [Agentic workflows](../../architecture/agentic-workflows/README.md#-latest-evidence-what-actually-moves-the-needle).
```bash
npx -y skills add obra/superpowers --skill subagent-driven-development --agent claude-code
```
Source: [github.com/obra/superpowers](https://github.com/obra/superpowers) · ~319K ⭐ (2026-11-13) · Added: 2026-11-18

### mattpocock/skills · handoff, grill-me, tdd, improve-codebase-architecture
Matt Pocock's collection is among the most-installed in the ecosystem. `handoff` compresses a session into a markdown document so you can continue in a fresh context. `grill-me` makes the agent question you before it builds. `tdd` and `improve-codebase-architecture` cover the core engineering loop.
**Why it matters:** Context hand-off and clarifying questions fix two of the most common long-session failures: context rot and building the wrong thing.
```bash
npx -y skills add mattpocock/skills --skill handoff --agent claude-code
npx -y skills add mattpocock/skills --skill grill-me --agent claude-code
```
Source: [github.com/mattpocock/skills](https://github.com/mattpocock/skills) · ~326K ⭐, `handoff` ~1.1M installs (2026-11-13) · Added: 2026-11-18

### anthropics/skills · mcp-builder, frontend-design
Anthropic's official skill repository. `mcp-builder` guides an agent through building an MCP server. `frontend-design` pushes UI work away from generic, templated output.
**Why it matters:** Official skills are a safe default to install and a reference for how to write good ones.
```bash
npx -y skills add anthropics/skills --skill mcp-builder --agent claude-code
```
Source: [github.com/anthropics/skills](https://github.com/anthropics/skills) · ~196K ⭐ (2026-11-13) · Added: 2026-11-18

### karpathy-guidelines · `forrestchang/andrej-karpathy-skills`
Coding guidelines distilled from Andrej Karpathy's advice on working with LLM coding agents.
**Why it matters:** A cheap, general "behave like a careful engineer" baseline that sits in the top 3 AI/agent-building skills by recent install copies.
```bash
npx -y skills add forrestchang/andrej-karpathy-skills --skill karpathy-guidelines --agent claude-code
```
Source: [github.com/forrestchang/andrej-karpathy-skills](https://github.com/forrestchang/andrej-karpathy-skills) · Added: 2026-11-18

### dogfood · `vercel-labs/agent-browser`
Lets the agent test what it built by driving a headless browser through the app.
**Why it matters:** Running and checking the result beats asking the model to "double-check". Self-assessment is unreliable, and execution is what catches bugs.
```bash
npx -y skills add vercel-labs/agent-browser --skill dogfood --agent claude-code
```
Source: [github.com/vercel-labs/agent-browser](https://github.com/vercel-labs/agent-browser) · Added: 2026-11-18

### task-observer · `rebelytics/one-skill-to-rule-them-all`
Ranked #1 on Claude Marketplaces' AI & agent-building chart by install copies over 90 days (as of 2026-11-13). It observes the task in progress and keeps the agent on track.
```bash
npx -y skills add rebelytics/one-skill-to-rule-them-all --skill task-observer --agent claude-code
```
Source: [claudemarketplaces.com ranking](https://claudemarketplaces.com/best/skills/ai-agents) · Added: 2026-11-18

---

## 📊 Where the rankings come from

| Source | What it measures | Link |
|---|---|---|
| skills.sh | Install counts across agents (Vercel registry) | [skills.sh](https://skills.sh) |
| Claude Marketplaces "best" lists | Install-command copies over the last 90 days, by category; bots filtered | [AI & agents](https://claudemarketplaces.com/best/skills/ai-agents) |
| Skillselion | Daily-refreshed catalogue and leaderboard (skills, MCP servers, marketplaces) | [leaderboard](https://skillselion.com/leaderboard) |
| Vercel "State of agent skills" | What the most-installed skills are used for | [vercel.com/blog](https://vercel.com/blog/state-of-agent-skills) |

## 🔒 Install hygiene

- Read the full `SKILL.md` and **audit every bundled script** before installing community skills. `anthropics/skills` and partner skills from Vercel, Trail of Bits and Remotion are reasonable defaults.
- Prefer project-scoped installs (`.claude/skills/`) so a skill only loads where it is relevant.
- Skills are context. Every always-on skill description costs tokens in every session, so prune the ones you don't use.
