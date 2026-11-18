# Agent skills · 🐍 Python

← [Back to Agent skills](README.md) · _Last updated: 2026-11-19_

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
Source: [Pydantic: skills for Claude Code and other agents](https://pydantic.dev/articles/pydantic-ai-logfire-claude-code-skills.md) · [github.com/pydantic/skills](https://github.com/pydantic/skills) · `building-pydantic-ai-agents` ~6.3K installs on [skills.sh](https://skills.sh/pydantic/skills/building-pydantic-ai-agents) (2026-11-19) · Added: 2026-11-19

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

- Skills shipped by other Python agent frameworks (LangGraph). Pydantic's official skills are now listed above.
