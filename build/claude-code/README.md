# Claude Code mastery

_Last updated: 2026-11-21_

> Tips, tricks and workflows for getting the most out of Claude Code, refreshed every day. Release notes and upgrade warnings stay in [Coding agents & IDEs](../coding-agents/README.md); this page is about *how to use it well*.

## 💡 Tip of the day

### Scope rules to the files they're about with `paths:`
Put area-specific conventions in `.claude/rules/<topic>.md` and add `paths:` frontmatter. The rule loads only when Claude reads or edits a matching file; rules without `paths` load at launch like CLAUDE.md. Globs are relative to the folder holding `.claude`, and brace expansion works (`"src/**/*.{ts,tsx}"`). If the frontmatter fails to parse, the rule loads everywhere, so check with `claude --debug`.
```markdown
---
paths:
  - "src/api/**/*.ts"
---
```
**Why it matters:** API, test or migration rules stop costing context in sessions that never touch those files, and the root CLAUDE.md stays short.
Source: [Memory: path-specific rules](https://code.claude.com/docs/en/memory#path-specific-rules) · Added: 2026-11-21

---

## ⌨️ Keys and commands worth memorising

| Key / command | What it does | Use it when |
|---|---|---|
| `Shift+Tab` | Cycles permission modes (default → accept edits → plan → others where available) | Switch to plan mode before a big change; accept edits once the plan is right |
| `Esc` | Interrupts Claude mid-turn | Claude starts drifting: stop it in the first minute, not the tenth |
| `Esc` `Esc` (empty input) or `/rewind` | Opens the rewind menu to roll back conversation and/or file edits | An approach went wrong and you want the code back too |
| `!` at the start of input | Shell mode: runs the command and adds the output to the session | Show Claude a failing test or log without asking it to run it |
| `@path` | References a file or folder in your prompt | Point Claude at exactly the files that matter |
| `Ctrl+R` | Searches your prompt history | Re-run a good prompt from earlier |
| `Ctrl+O` | Toggles the transcript viewer with full tool details | Check what Claude actually ran |
| `Ctrl+G` | Opens your prompt in your editor | Writing a long, careful prompt |
| `/clear` | Starts a fresh conversation | Between unrelated tasks, and after two failed corrections |
| `/compact <focus>` | Summarises the session, keeping what you name | A long session you want to continue, e.g. `/compact keep the API changes` |
| `/context` · `/usage` | Shows what fills the context window · where your usage went | A session feels slow, costly or confused |
| `/init` | Drafts a `CLAUDE.md` from the codebase | First session in a repo; then trim it hard |

Full lists: [Interactive mode](https://code.claude.com/docs/en/interactive-mode) · [Commands](https://code.claude.com/docs/en/slash-commands)

---

## 🧱 The building blocks, and when to use each

| Block | Lives in | Use it for | Don't use it for |
|---|---|---|---|
| **CLAUDE.md** | repo root, `~/.claude/` | Commands, conventions and gotchas Claude can't discover itself; keep it short | Describing architecture Claude can read from the code |
| **Path-scoped rules** | `.claude/rules/*.md` with `paths:` | Rules that only apply to one part of the codebase | Repo-wide rules |
| **Skills** | `.claude/skills/<name>/SKILL.md` | Team procedures and knowledge loaded on demand; add `disable-model-invocation: true` for ones with side effects (releases, deploys) | Rules that must always apply |
| **Hooks** | `.claude/settings.json` | Rules that can't have exceptions: format on edit, block a command, gate "done" on tests | Advice Claude may reasonably ignore |
| **Permissions & sandbox** | `settings.json`, `/permissions` | Pre-approving safe commands, denying dangerous ones | Replacing review of risky changes |
| **Subagents** | `.claude/agents/` | Parallel work, noisy searches, an independent reviewer | Getting a "better" answer to the same task (it isn't) |
| **MCP servers** | `claude mcp add`, `.mcp.json` | Connecting tools Claude can't reach from the shell | Things a CLI already does |
| **Plugins** | `/plugin` | Sharing a bundle of skills, agents, hooks and MCP config across a team | One-off personal tweaks |

Docs: [Memory](https://code.claude.com/docs/en/memory) · [Skills](https://code.claude.com/docs/en/skills) · [Hooks guide](https://code.claude.com/docs/en/hooks-guide) · [Subagents](https://code.claude.com/docs/en/sub-agents) · [MCP](https://code.claude.com/docs/en/mcp) · [Plugins](https://code.claude.com/docs/en/plugins) · [Settings](https://code.claude.com/docs/en/settings)

---

## ⭐ Start here: habits that pay off most

### Write the prompt Claude can't guess
Say what done looks like, which files matter, and anything Claude can't see (a ticket, a decision, a constraint). For anything non-trivial, ask Claude to brainstorm or plan first, then build.
Source: [Best practices](https://code.claude.com/docs/en/best-practices#write-a-specific-prompt) · Added: 2026-11-20

### Keep CLAUDE.md short, and push the rest into skills, rules and hooks
Run `/init`, then mostly delete. Anything procedural becomes a skill, anything area-specific a path-scoped rule, and anything that must never be broken a hook or deny rule rather than CAPITALISED text.
Source: [Best practices: keep CLAUDE.md short](https://code.claude.com/docs/en/best-practices#keep-claudemd-short) · [Memory](https://code.claude.com/docs/en/memory) · Added: 2026-11-20

### Steer early, reset rather than argue
Watch the first minute and press `Esc` when Claude drifts. If two corrections haven't fixed it, `/clear` and write one better prompt that includes what you learned; a third correction mostly adds noise.
Source: [Best practices: steer the session](https://code.claude.com/docs/en/best-practices#steer-the-session) · Added: 2026-11-20

### Drop advice that is out of date
Current models don't need ALL CAPS, "think harder" or "don't be lazy". Use the effort setting (or `ultrathink` for one turn), and give a check to pass instead of a pep talk.
Source: [Best practices: what you can stop doing](https://code.claude.com/docs/en/best-practices#what-you-can-stop-doing) · Added: 2026-11-20

### Script it with `claude -p`
`claude -p` runs once and exits, which is how Claude Code goes into CI, git hooks and loops. Pre-approve tools with `--allowedTools`, refuse everything else with `--permission-mode dontAsk`, cap work with `--max-turns`, and parse `--output-format json`. Try it on three items before running the batch.
Source: [Best practices: run Claude from a script](https://code.claude.com/docs/en/best-practices#run-claude-from-a-script) · [Headless](https://code.claude.com/docs/en/headless) · Added: 2026-11-20

### Run parallel sessions in worktrees
`claude -w <name>` starts a session in its own git worktree so edits can't collide. List the gitignored files each worktree needs (such as `.env`) in `.worktreeinclude`.
Source: [Best practices: run sessions in parallel](https://code.claude.com/docs/en/best-practices#run-sessions-in-parallel) · Added: 2026-11-20

### Automate the start: `/loop` and `/schedule`
`/loop 15m <prompt>` repeats a prompt inside the open session; `/schedule` creates a cloud task that runs while your laptop is closed. Protect `main` with a branch rule before leaving one unattended.
Source: [Best practices: start runs on a schedule or an event](https://code.claude.com/docs/en/best-practices#start-runs-on-a-schedule-or-an-event) · Added: 2026-11-20

---

## 🗞️ Latest tips

<!-- newest first: new workflows, tips from official docs and Anthropic posts, proven practitioner techniques. Each previous "Tip of the day" moves here. -->

### Let `/loop` and recurring tasks run for weeks 🆕
From 2.1.330, recurring scheduled tasks and `/loop` last up to 30 days instead of 7 while their session keeps running. Loops created before you upgrade still stop at 7 days, so recreate long-running watchers after upgrading. For anything that must outlive the session, use cloud or Desktop scheduled tasks. (The scheduled-tasks page still says seven days; the changelog is newer.)
Source: [Claude Code changelog 2.1.330](https://raw.githubusercontent.com/anthropics/claude-code/main/CHANGELOG.md) · [Scheduled tasks](https://code.claude.com/docs/en/scheduled-tasks) · Added: 2026-11-21

### Give Claude a check it can run, then enforce it with a Stop hook 🆕
Tell Claude how to verify its own work (tests, typecheck, lint). To make it non-negotiable, add a `Stop` hook in `.claude/settings.json` that runs the check and exits with code 2 on failure: the errors go back to Claude and it keeps working until the check passes.
**Why it matters:** this turns "done" from Claude's opinion into a passing command.
Source: [Best practices: enforce the check with a Stop hook](https://code.claude.com/docs/en/best-practices#enforce-the-check-with-a-stop-hook) · Added: 2026-11-20

### Add an MCP server without putting its token on the command line 🆕
`claude mcp add-json <name> -` (2.1.327+) reads the server's JSON config from stdin, so a token piped in from a secrets manager or file never lands in shell history or `ps` output. It only works from your shell, not inside a Claude Code session.
**Why it matters:** `claude mcp add ... --header "Authorization: Bearer ..."` leaves the secret in history.
Source: [Claude Code changelog 2.1.327](https://raw.githubusercontent.com/anthropics/claude-code/main/CHANGELOG.md) · [MCP docs](https://code.claude.com/docs/en/mcp) · Added: 2026-11-20

### Make unattended runs survive the stricter sandbox 🆕
Since 2.1.326, more Bash and PowerShell commands ask first, and in `-p` or scheduled runs with no one to answer they are refused. After upgrading, run the job once interactively, then add the exact commands it needs as allow rules in `.claude/settings.json`. If a sandboxed command needs to write to a home folder, add that path to `sandbox.filesystem.allowWrite` rather than turning the sandbox off.
Source: [Claude Code changelog 2.1.326](https://raw.githubusercontent.com/anthropics/claude-code/main/CHANGELOG.md) · [Settings](https://code.claude.com/docs/en/settings) · Added: 2026-11-20

## 📚 Reference

- [Claude Code docs](https://code.claude.com/docs/en/overview) · [Best practices](https://code.claude.com/docs/en/best-practices) · [Common workflows](https://code.claude.com/docs/en/common-workflows) · [CLI reference](https://code.claude.com/docs/en/cli-reference) · [Costs](https://code.claude.com/docs/en/costs) · [Checkpointing](https://code.claude.com/docs/en/checkpointing) · [GitHub Actions](https://code.claude.com/docs/en/github-actions)
- [Anthropic engineering: Claude Code best practices](https://www.anthropic.com/engineering/claude-code-best-practices)
- Skills to install: [Agent skills](../agent-skills/README.md) · MCP servers to connect: [MCP servers](../mcp-servers/README.md)
