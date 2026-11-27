# Claude Code mastery

_Last updated: 2026-11-28_

> Tips, tricks and workflows for getting the most out of Claude Code, refreshed every day. Release notes and upgrade warnings stay in [Coding agents & IDEs](../coding-agents/README.md); this page is about *how to use it well*.

## 💡 Tip of the day

### Get JSON your script can trust from `claude -p --json-schema`
For a CI step or build script that acts on Claude's answer, pass a JSON Schema with `--output-format json`. The answer comes back validated in the `structured_output` field, next to the session ID and usage, instead of as prose you have to parse. Cap the run with `--max-turns` and `--max-budget-usd` so a confused run can't loop or overspend.
```bash
claude -p "Extract the main function names from auth.py" \
  --output-format json \
  --json-schema '{"type":"object","properties":{"functions":{"type":"array","items":{"type":"string"}}},"required":["functions"]}' \
  | jq '.structured_output'
```
```bash
claude -p --max-turns 3 "query"
claude -p --max-budget-usd 5.00 "query"
```
Gotchas: if a run ends without valid structured output (for example Claude declined), the response has **no** `structured_output` field, so check it is present before using it. An invalid schema exits with `Error: --json-schema is not a valid JSON Schema`; `format` (such as `"email"`) is accepted but not enforced. `--json-schema`, `--max-turns` and `--max-budget-usd` are print-mode only. The budget cap uses Claude Code's client-side cost estimate, counts subagents, and spend can pass it, so leave headroom. Piped stdin is capped at 10MB; write bigger inputs to a file and name the path. Without `--bare`, `-p` runs a project's `.claude/settings.json` hooks and connects its `.mcp.json` servers even in a folder you never trusted, with no trust dialog; the docs recommend `--bare` for scripted calls, which skips that discovery (and CLAUDE.md, skills and plugins) but needs `ANTHROPIC_API_KEY` instead of your subscription login.
**Why it matters:** "summarise the diff" becomes a step that returns fields a script can gate on (a list of risky files, a pass/fail verdict) without regex over free text.
Source: [Headless: get structured output](https://code.claude.com/docs/en/headless#get-structured-output) · [CLI reference: flags](https://code.claude.com/docs/en/cli-reference#cli-flags) · Added: 2026-11-28

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

### Decide which MCP servers may hand Claude skills: `Skill(mcp__<server>__*)` rules 🆕
From 2.1.331, an MCP server can serve skills as well as tools (public beta). They show up in `/` and `/skills` as `<server>:<skill>`, for example `/docs:pdf report.pdf` for a `pdf` skill on a server named `docs`; connector and plugin servers get a prefix such as `claude_ai_Docs:pdf`. In auto mode the classifier decides whether a skill loads without you seeing it, and the server can change the skill at any time, so set a rule per server. Run `/permissions`, or add to settings:
```json
{
  "permissions": {
    "allow": ["Skill(mcp__docs__*)"],
    "ask":   ["Skill(mcp__vendor__*)"],
    "deny":  ["Skill(mcp__scratch__*)", "Skill(docs:pdf)"]
  }
}
```
`allow` approves every version of a server's skills, but only works in user or managed settings and only for servers you added at user or local scope or managed servers (not connectors, `.mcp.json` or plugin servers). `ask` prompts each time, even in auto and `bypassPermissions` mode. `deny` also blocks typed commands; deny `mcp__<server>` to block its tools too. Org admins turn skills on for other servers with `disableDirectMcpSkills: false` in managed settings, or keep them off with `true`.
Gotchas: MCP skills don't load in `claude -p`, cloud sessions, GitHub Actions, the Agent SDK, or through cloud providers, a custom `ANTHROPIC_BASE_URL`, `apiKeyHelper` or `ANTHROPIC_AUTH_TOKEN`. They get no `allowed-tools` grant, and a `deny` rule still lets Claude read the server's resources (deny `ReadMcpResourceTool` for that). If a skill is missing, check `claude --debug=mcp`.
**Why it matters:** a skill is instructions plus code that can steer Claude, coming from a server that can change it without telling you. One line per server decides whether that happens silently, with a prompt, or never. Pair it with the `PreSkillShellCommand` hook, below.
Source: [MCP: use skills from MCP servers](https://code.claude.com/docs/en/mcp#use-skills-from-mcp-servers) · [Skills: skills from MCP servers](https://code.claude.com/docs/en/skills#skills-from-mcp-servers) · Added: 2026-11-27

### Guard the shell commands skills run as they load, with a `PreSkillShellCommand` hook 🆕
A skill's `` !`command` `` lines run while the skill loads, and `PreToolUse` hooks never see them. From 2.1.332, a `PreSkillShellCommand` hook does: it gets each command after the permission check, even in `bypassPermissions` mode, and can block it. Reuse the script you already run on `PreToolUse` (this one reads `tool_input.command` and denies `rm -rf`), match both tools that run injected commands, and set `onFailure: "block"` so a crashed or slow hook doesn't let the command through.
```json
{
  "hooks": {
    "PreSkillShellCommand": [
      {
        "matcher": "Bash|PowerShell",
        "hooks": [
          { "type": "command", "command": "${CLAUDE_PROJECT_DIR}/.claude/hooks/block-rm.sh", "args": [], "onFailure": "block" }
        ]
      }
    ]
  }
}
```
```bash
#!/bin/bash
# .claude/hooks/block-rm.sh
COMMAND=$(jq -r '.tool_input.command')

if echo "$COMMAND" | grep -q 'rm -rf'; then
  jq -n '{
    hookSpecificOutput: {
      hookEventName: "PreToolUse",
      permissionDecision: "deny",
      permissionDecisionReason: "Destructive command blocked by hook"
    }
  }'
else
  exit 0  # no decision; normal permission flow applies
fi
```
Test it with `.claude/skills/hook-test/SKILL.md` containing only `` !`echo 'rm -rf'` ``, then type `/hook-test`: you should see `Not run in /hook-test: echo 'rm -rf' (blocked by hook: ...)`. A blocked command doesn't stop the skill; Claude reads `[not run: blocked by hook: <reason>]` in place of its output.
Gotchas: upgrade first, because 2.1.331 and older run injected commands without calling the hook and show an `Unknown hook event` dialog at the start of every interactive terminal session (`requiredMinimumVersion` can enforce the version). The hook can only block: `ask`, `defer` or an `updatedInput` also block. Put it in a settings file or plugin, not in the skill's own frontmatter, which is skipped on first load and in subagents. Keep the script on `PreToolUse` too, since in auto mode a command that needs approval is skipped at load and Claude may run it afterwards as a normal tool call. Use a non-async `command`, `http` or `mcp_tool` hook: a `prompt` or `agent` hook on this event blocks every command it matches.
**Why it matters:** skills from plugins and teammates can run shell commands before Claude reads a word of them, and this is the one place to log or veto those commands.
Source: [Hooks: PreSkillShellCommand](https://code.claude.com/docs/en/hooks#preskillshellcommand) · [How a hook resolves](https://code.claude.com/docs/en/hooks#how-a-hook-resolves) · [Skills: inject dynamic context](https://code.claude.com/docs/en/skills#inject-dynamic-context) · [Changelog 2.1.332](https://raw.githubusercontent.com/anthropics/claude-code/main/CHANGELOG.md) · Added: 2026-11-26

### Keep secrets out of Claude's reach with `Read` deny rules 🆕
Add `permissions.deny` rules for the files that hold keys and environment values. Claude Code then leaves them out of file discovery and search results, refuses to read them, and also blocks Edit and Write on those paths. The rules cover the built-in file tools, Bash commands it recognises (`cat`, `head`, `tail`, `sed`, `tee`) and redirection targets like `< .env`. Commit them to `.claude/settings.json` so the whole team gets them.
```json
{
  "permissions": {
    "deny": [
      "Read(./.env)",
      "Read(./.env.*)",
      "Read(./secrets/**)",
      "Read(./config/credentials.json)",
      "Bash(curl *)"
    ]
  }
}
```
Gotchas: deny is checked before ask and allow, and an allow rule can't carve an exception out of it. Patterns use gitignore syntax, and a single leading `/` anchors at the settings source: `Read(/secrets/**)` in `~/.claude/settings.json` means `~/.claude/secrets/**`, so use `//abs/path` or `~/path` in user settings. A `.claudeignore` file does nothing; move its entries into `Read` deny rules. These rules don't stop `grep -r pattern .`, other subprocesses, or `curl` called by full path or through `sh -c`, so turn on the [sandbox](https://code.claude.com/docs/en/sandboxing) when the boundary must hold.
**Why it matters:** `.env` contents stop turning up in transcripts, search results and the logs you share, without anyone remembering to say "don't read that".
Source: [Settings reference: permissions.deny](https://code.claude.com/docs/en/settings-reference#permissions-deny) · [Permissions: Read and Edit](https://code.claude.com/docs/en/permissions#read-and-edit) · [How path patterns match](https://code.claude.com/docs/en/permissions#how-path-patterns-match) · Added: 2026-11-25

### Ship your team's plugins with the repo: `extraKnownMarketplaces` + `enabledPlugins` 🆕
Commit both keys to `.claude/settings.json`. `extraKnownMarketplaces` registers your marketplace for everyone who opens the repo and trusts the folder; `enabledPlugins` (keyed `plugin-name@marketplace-name`) turns the plugins on for the project. Enabling does **not** download a plugin, so each teammate runs the install once per clone (or `--scope user` for all projects), then `/reload-plugins`.
```json
{
  "extraKnownMarketplaces": {
    "acme-tools": {
      "source": { "source": "github", "repo": "acme-corp/claude-plugins" },
      "autoUpdate": true
    }
  },
  "enabledPlugins": {
    "code-formatter@acme-tools": true
  }
}
```
```shell
claude plugin install code-formatter@acme-tools --scope project
```
Gotchas: in an untrusted folder, including a `-p` run there, the marketplace entry is ignored without a message. Third-party marketplaces don't auto-update unless you set `"autoUpdate": true` (official Anthropic ones default to on). Project settings beat user settings, so a teammate who wants a plugin off sets it to `false` in `.claude/settings.local.json`; a `false` in managed settings blocks it everywhere. From a release on or after 2026-11-30, marketplaces listed in *managed* `extraKnownMarketplaces` will auto-update by default (2.1.331 notice), so add `"autoUpdate": false` to any you want pinned.
**Why it matters:** the team's skills, hooks, agents and MCP config arrive with `git clone` instead of a wiki page of setup steps.
Source: [Settings reference: extraKnownMarketplaces](https://code.claude.com/docs/en/settings-reference#extraknownmarketplaces) · [enabledPlugins](https://code.claude.com/docs/en/settings-reference#enabledplugins) · [Enabled in project settings but not installed](https://code.claude.com/docs/en/plugins/loading#enabled-in-project-settings-but-not-installed) · [Changelog 2.1.331](https://raw.githubusercontent.com/anthropics/claude-code/main/CHANGELOG.md) · Added: 2026-11-24

### Feed live data into a skill with `` !`command` `` 🆕
In a skill's `SKILL.md`, a line with `` !`<command>` `` runs that shell command before Claude sees the skill, and the output replaces the line. Claude starts with the real diff, PR comments or test output already in its prompt instead of spending turns fetching them. Use a fenced ` ```! ` block for several commands. Add `context: fork` to run the skill in its own subagent so the bulky output stays out of your main conversation.
```yaml
---
name: pr-summary
description: Summarize changes in a pull request
context: fork
agent: Explore
allowed-tools: Bash(gh *)
---

## Pull request context
- PR diff: !`gh pr diff`
- PR comments: !`gh pr view --comments`
- Changed files: !`gh pr diff --name-only`

## Your task
Summarize this pull request...
```
Gotchas: if any injected command fails (non-zero exit, apart from exit 1 from search and compare commands), the whole skill invocation stops and Claude never sees the skill. `!` only counts at the start of a line or after whitespace. Each command gets the Bash tool's 2-minute timeout and runs in the session's current folder, so use `${CLAUDE_SKILL_DIR}` or `${CLAUDE_PROJECT_DIR}` in paths. Admins can turn the feature off with `"disableSkillShellExecution": true` (bundled and managed skills keep it).
**Why it matters:** skills like "review my diff" or "summarise this PR" start from the real data on the first turn, and the result is the same every time.
Source: [Skills: inject dynamic context](https://code.claude.com/docs/en/skills#inject-dynamic-context) · Added: 2026-11-23

### Give an MCP server to one subagent only, with `mcpServers:` 🆕
Define a heavy server (Playwright, a database) inline in a subagent's frontmatter instead of in `.mcp.json`: it connects when that subagent starts and disconnects when it finishes, so its tool descriptions never load into the main conversation. A bare name in the list (such as `github`) reuses a server already configured in the session.
```yaml
---
name: browser-tester
description: Tests features in a real browser using Playwright
mcpServers:
  # Inline definition: scoped to this subagent only
  - playwright:
      type: stdio
      command: npx
      args: ["-y", "@playwright/mcp@latest"]
  # Reference by name: reuses an already-configured server
  - github
---

Use the Playwright tools to navigate, screenshot, and interact with pages.
```
Gotchas: inline servers in a project's `.claude/agents/` load only after you accept the trust dialog for that folder (otherwise they're skipped; `~/.claude/agents/` skips the check), and managed allow/deny lists still apply. Upgrade to 2.1.330 first if several subagents share a server: it fixed one subagent finishing shutting the server down for the others.
**Why it matters:** browser and database tools stop costing context in every session that doesn't need them.
Source: [Subagents: scope MCP servers to a subagent](https://code.claude.com/docs/en/sub-agents#scope-mcp-servers-to-a-subagent) · Added: 2026-11-22

### Scope rules to the files they're about with `paths:` 🆕
Put area-specific conventions in `.claude/rules/<topic>.md` and add `paths:` frontmatter. The rule loads only when Claude reads or edits a matching file; rules without `paths` load at launch like CLAUDE.md. Globs are relative to the folder holding `.claude`, and brace expansion works (`"src/**/*.{ts,tsx}"`). If the frontmatter fails to parse, the rule loads everywhere, so check with `claude --debug`.
```markdown
---
paths:
  - "src/api/**/*.ts"
---
```
**Why it matters:** API, test or migration rules stop costing context in sessions that never touch those files, and the root CLAUDE.md stays short.
Source: [Memory: path-specific rules](https://code.claude.com/docs/en/memory#path-specific-rules) · Added: 2026-11-21

### Let `/loop` and recurring tasks run for weeks 🆕
From 2.1.330, recurring scheduled tasks and `/loop` last up to 30 days instead of 7 while their session keeps running. Loops created before you upgrade still stop at 7 days, so recreate long-running watchers after upgrading. For anything that must outlive the session, use cloud or Desktop scheduled tasks. (The scheduled-tasks page still says seven days; the changelog is newer.)
Source: [Claude Code changelog 2.1.330](https://raw.githubusercontent.com/anthropics/claude-code/main/CHANGELOG.md) · [Scheduled tasks](https://code.claude.com/docs/en/scheduled-tasks) · Added: 2026-11-21

### Give Claude a check it can run, then enforce it with a Stop hook
Tell Claude how to verify its own work (tests, typecheck, lint). To make it non-negotiable, add a `Stop` hook in `.claude/settings.json` that runs the check and exits with code 2 on failure: the errors go back to Claude and it keeps working until the check passes.
**Why it matters:** this turns "done" from Claude's opinion into a passing command.
Source: [Best practices: enforce the check with a Stop hook](https://code.claude.com/docs/en/best-practices#enforce-the-check-with-a-stop-hook) · Added: 2026-11-20

### Add an MCP server without putting its token on the command line
`claude mcp add-json <name> -` (2.1.327+) reads the server's JSON config from stdin, so a token piped in from a secrets manager or file never lands in shell history or `ps` output. It only works from your shell, not inside a Claude Code session.
**Why it matters:** `claude mcp add ... --header "Authorization: Bearer ..."` leaves the secret in history.
Source: [Claude Code changelog 2.1.327](https://raw.githubusercontent.com/anthropics/claude-code/main/CHANGELOG.md) · [MCP docs](https://code.claude.com/docs/en/mcp) · Added: 2026-11-20

### Make unattended runs survive the stricter sandbox
Since 2.1.326, more Bash and PowerShell commands ask first, and in `-p` or scheduled runs with no one to answer they are refused. After upgrading, run the job once interactively, then add the exact commands it needs as allow rules in `.claude/settings.json`. If a sandboxed command needs to write to a home folder, add that path to `sandbox.filesystem.allowWrite` rather than turning the sandbox off.
Source: [Claude Code changelog 2.1.326](https://raw.githubusercontent.com/anthropics/claude-code/main/CHANGELOG.md) · [Settings](https://code.claude.com/docs/en/settings) · Added: 2026-11-20

## 📚 Reference

- [Claude Code docs](https://code.claude.com/docs/en/overview) · [Best practices](https://code.claude.com/docs/en/best-practices) · [Common workflows](https://code.claude.com/docs/en/common-workflows) · [CLI reference](https://code.claude.com/docs/en/cli-reference) · [Costs](https://code.claude.com/docs/en/costs) · [Checkpointing](https://code.claude.com/docs/en/checkpointing) · [GitHub Actions](https://code.claude.com/docs/en/github-actions)
- [Anthropic engineering: Claude Code best practices](https://www.anthropic.com/engineering/claude-code-best-practices)
- Skills to install: [Agent skills](../agent-skills/README.md) · MCP servers to connect: [MCP servers](../mcp-servers/README.md)
