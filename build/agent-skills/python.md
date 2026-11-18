# Agent skills · 🐍 Python

← [Back to Agent skills](README.md) · _Last updated: 2026-11-18_

> Skills that make coding agents write, run and review Python the way a careful team would. Also see the [Python starter skill](starter-skills/python-service/SKILL.md), which you can copy into `.claude/skills/` and edit.

## ⭐ Start here

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

- Skills shipped by Python agent frameworks themselves (Pydantic AI, LangGraph). The daily job will add them when they are published.
