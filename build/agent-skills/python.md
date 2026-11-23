# Agent skills · 🐍 Python

← [Back to Agent skills](README.md) · _Last updated: 2026-11-24_

> Skills that make coding agents write, run and review Python the way a careful team would. Also see the [Python starter skill](starter-skills/python-service/SKILL.md), which you can copy into `.claude/skills/` and edit.

## ⭐ Start here

### pydantic/skills · official Pydantic, Pydantic AI and Logfire skills 🆕
Pydantic's own skill repo: `pydantic` (models, validators, unions), `building-pydantic-ai-agents` (tools, structured output, streaming, testing, multi-agent) and `logfire-instrumentation` (Python, JS/TS and Rust).
**Why it matters:** Pydantic AI V2 moves fast (see [Libraries · Python](../libraries/python.md)), so a vendor-maintained skill is the most reliable way to stop agents writing V1-era code.
```bash
npx skills add pydantic/skills --skill building-pydantic-ai-agents
# Claude Code plugin form:
claude plugin marketplace add pydantic/skills
claude plugin install pydantic@pydantic-skills
```
Source: [Pydantic: skills for Claude Code and other agents](https://pydantic.dev/articles/pydantic-ai-logfire-claude-code-skills.md) · [github.com/pydantic/skills](https://github.com/pydantic/skills) · `building-pydantic-ai-agents` ~6.6K installs on [skills.sh](https://skills.sh/pydantic/skills/building-pydantic-ai-agents) (2026-11-23) · Added: 2026-11-19

### langchain-ai/langchain-skills · official LangChain, LangGraph and Deep Agents skills, now one plugin 🆕
LangChain's official skills (Deep Agents, LangGraph, LangChain, LangSmith evals; Python and TypeScript) now ship as a single `langchain-skills` plugin that replaces the many small standalone skills such as `langgraph-fundamentals` and `langchain-rag`, and the separate `langsmith-skills` plugin. The old names still install but now only add a short redirect. The plugin also registers two documentation MCP servers (`https://docs.langchain.com/mcp` and `https://reference.langchain.com/mcp`) that need no credentials; the skills-only install adds none. The repo calls itself early development.
**Why it matters:** If you installed the old standalone skills (the most-used ones have ~17–20K installs each), remove them before installing the plugin, or your agent sees two overlapping sets of guidance.
```bash
# Claude Code (v2.1.292+), from your shell:
claude plugin install langchain-skills --marketplace langchain-ai/langchain-skills
# Skills only, no MCP servers:
npx skills add langchain-ai/langchain-skills --skill '*' --yes
```
Note: third-party marketplaces don't auto-update by default; turn it on in `/plugin` → Marketplaces, or set `"autoUpdate": true` on the `langchain-skills` entry in `~/.claude/settings.json`. The README lists the exact `npx skills remove ...` command for the retired skills.
Source: [github.com/langchain-ai/langchain-skills](https://github.com/langchain-ai/langchain-skills) · plugin 0.4.2, 279K total installs on [skills.sh](https://skills.sh/langchain-ai/langchain-skills) (2026-11-24) · Added: 2026-11-24

### adk-agent-builder · `google/adk-python` · official Google ADK skill 🆕
Google ships a skill inside the Agent Development Kit repo for building ADK Python agents: LLM agents with tools, graph workflows, conditional routing, fan-out and join, delegation between agents and human-in-the-loop pauses. It splits guidance into reference files and tells the agent to load only the one it needs, and says its APIs were checked against `google-adk` 2.14.0. The other `adk-*` skills in the repo (style, git, PR triage) are for ADK contributors, not users.
**Why it matters:** ADK's API moves quickly, and a vendor-maintained skill pinned to a stated version is safer than the model's memory.
```bash
npx skills add https://github.com/google/adk-python --skill adk-agent-builder
```
Source: [github.com/google/adk-python](https://github.com/google/adk-python) · ~767 installs on [skills.sh](https://skills.sh/google/adk-python/adk-agent-builder) (2026-11-23) · Added: 2026-11-23

### Python skills leaderboard · claudeskills.info
A ranked list of the 20 most-installed Python-specific skills, drawn from 104 qualifying skills. The top three are `python-executor` (sandboxed execution via inference.sh, ~34K installs), `python-design-patterns` and `async-python-patterns`.
**Why it matters:** It is the quickest way to see what Python developers actually install, as opposed to what gets starred.
Source: [claudeskills.info/best/python-skills](https://claudeskills.info/best/python-skills/) · Added: 2026-11-18

### python-executor · `inferen-sh`
Runs Python in a sandboxed remote environment for data analysis, scraping, image/video processing and automation.
**Why it matters:** Lets an agent *execute* Python safely when your local machine shouldn't be the sandbox.
Source: [claudeskills.info listing](https://claudeskills.info/best/python-skills/) · Added: 2026-11-18

### markitdown · `k-dense-ai/scientific-agent-skills`
Wraps Microsoft's MarkItDown to convert PDFs, Office files and HTML into clean markdown before the agent reads them.
**Why it matters:** Converting documents first saves a lot of tokens and gives better answers than handing raw files to the model.
```bash
npx -y skills add k-dense-ai/scientific-agent-skills --skill markitdown --agent claude-code
```
Source: [github.com/k-dense-ai/scientific-agent-skills](https://github.com/k-dense-ai/scientific-agent-skills) · Added: 2026-11-18

### superpowers TDD loop (language-agnostic, works well for pytest)
See [Agent skills → superpowers](README.md#superpowers--obrasuperpowers--methodology). Pair it with a project skill that names your test command (`uv run pytest -q`) so the agent runs tests rather than guessing.

## 🧩 Write your own (recommended for Python)

Public Python skills are less mature than the TypeScript and Spring ones. A small project-level skill that encodes **your** toolchain usually beats a generic one:

- Package manager and runner (`uv`, `poetry`, `pip-tools`)
- Lint, format and type-check commands (`ruff check`, `ruff format`, `mypy` / `pyright`)
- Test command and conventions (pytest fixtures, markers, coverage gate)
- Framework idioms (FastAPI dependency injection, Pydantic v2 models, async rules)

→ Template: [starter-skills/python-service/SKILL.md](starter-skills/python-service/SKILL.md)

## 🔭 Watching

- Skills shipped by other Python agent frameworks. Pydantic's, Google ADK's and LangChain's official skills are now listed above.
