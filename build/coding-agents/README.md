# Coding agents & IDEs

_Last updated: 2026-11-25_

> Release notes that change how you work in Claude Code, Codex, Cursor, Copilot, Gemini CLI, Antigravity, Devin and Kiro. Only items worth acting on are included.

## ⚡ Action items

| When | What | Do this |
|---|---|---|
| now | Claude Code ≥ 2.1.325 | Upgrade: 2.1.321–2.1.325 fix an MCP OAuth refresh-token leak on redirect, several sandbox and Bash permission bypasses, and zstd decoding. Sandboxed Bash now prompts by default; set `sandbox.autoAllowBashIfSandboxed: true` to keep the old behaviour |
| now | Claude Code: unknown model IDs assume a 1M context (2.1.323) | If you route to a gateway or custom model with a smaller window, set `CLAUDE_CODE_DISABLE_1M_CONTEXT=1` or `CLAUDE_CODE_MAX_CONTEXT_TOKENS` |
| now | Claude Code 2.1.326–2.1.329 tighten the sandbox and bypass mode | Re-test unattended and `-p` jobs: more Bash/PowerShell commands now ask (or are refused when no one can answer), even in bypass mode; sandboxed commands no longer write to some sensitive home folders (allow with `sandbox.filesystem.allowWrite`) |
| next release | Claude Code auto mode: the billed classifier fallback is being removed (2.1.327 notice) | Actions it would have checked will be asked about or denied, so check auto-mode runs with telemetry off |
| now | Codex CLI ≥ 0.169.0: `codex exec` ignores project config and MCP servers in untrusted folders | Add `--trust` to CI jobs that rely on repo-level Codex config or MCP servers |
| now | Claude Code 2.1.330: `deniedMcpServers` entries by name now hide only that claude.ai connector, not others at the same URL | To block every connector at a server, deny its URL |
| now | Claude Code 2.1.330: more `rm` commands aimed at root, home, a top-level folder or the working folder now ask, and are refused when no one can answer | Re-run `-p` and scheduled jobs that clean up broad paths |
| now | Codex CLI 0.171.0 makes GPT-6.2 Sol the default catalog selection | Pin `model` in CI and config if you depend on a specific model |
| now | Gemini CLI 0.70.0: `commandPrefix`/`commandRegex` policy rules match top-level command arguments only | Re-test policy rules written for nested or wrapped commands |
| now | Antigravity App < 2.33.0 sends MCP headers on cross-origin redirects and can let hooks/wildcard rules bypass enforced command review | Update managed installs to 2.33.0+ |
| now | Kiro Crew 0.13.0 turns usage data on by default | Opt out with `telemetry.enabled: false`, `KIROCREW_TELEMETRY=0` or `DO_NOT_TRACK=1` if policy requires |
| when enabled | Devin Access and Sharing: Slack-started sessions take instructions only from people they're shared with | Agree group sharing defaults before your Cognition rep turns it on |
| now | Cursor CLI < v2026.11.17: team-dashboard prompt hooks never ran in the CLI, and MCP resource downloads skipped file-write rules | Update the CLI; re-check any guardrail you set as a dashboard prompt hook |
| now | Claude Code 2.1.331 (VS Code): wrappers, hooks or MCP servers that run VS Code as Node must set `ELECTRON_RUN_AS_NODE=1` | Add the variable to those scripts |
| now | Antigravity CLI 1.5.16 / App 2.35.0: Auto mode now writes files outside the workspace inside any Git/Jujutsu/Mercurial repo, and reads outside the project, without asking | Add `ask` or `deny` rules for sibling repos and paths it shouldn't touch |
| now | Copilot CLI 1.0.115: `--available-tools=` with an empty value now gives the model no tools (before: all tools) | Check scripts that pass an empty or computed `--available-tools` |
| now | Codex CLI 0.172.0: optional stdio MCP servers with cached tool lists start on first tool call | If a job expects a server to be up at session start, mark it required |
| **2026-11-26** | Kiro enterprise daily metrics move to 00:30 UTC | Shift any job that reads the daily metrics export |
| on/after **2026-11-30** | Claude Code: marketplaces in managed `extraKnownMarketplaces` start auto-updating by default (2.1.331 notice) | Set `"autoUpdate": false` on any managed marketplace you want to keep pinned |
| by **2026-11-30** | Claude Sonnet 4.5 retires | Update `model` settings, `CLAUDE.md` and CI configs that pin it |
| **2026-12-14** | Copilot retires Claude Fable 5, Claude Haiku 4.5, Gemini 3.8 Flash, Gemini 4 Argon, Grok 4.6 and Kimi K3 | Move to Fable 5.2, Haiku 5.5, Gemini 4 Hydrogen, Gemini 4 Carbon and Grok 4.7 (no Kimi replacement announced yet) |
| **2026-12-18** | Copilot retires MAI-Code-1.1-Flash | Switch to the latest MAI Code Flash model (MAI-Code-2-Flash is in the Copilot CLI picker from 1.0.115) |
| **Feb 2027** | Copilot in VS Code: the Local harness is removed | Move remaining workflows to the Copilot harness (already the default for new sessions) |

## 🗞️ Latest releases

### Antigravity CLI 1.5.16 + App 2.35: Auto mode asks less, `~/.agents/skills` · 2026-11-23 → 11-24 🆕
**CLI 1.5.16** (11-24): Auto mode, the default agent mode, no longer asks before creating or editing files outside the workspace when they sit inside a version-controlled repo, or when the change only adds content. Overwrites outside a repo, hidden paths, `.git` and hook metadata, and system folders still ask. Skills in `~/.agents/skills` are now discovered (those in `~/.gemini` win on name clashes), `agy -r <id>` resumes a conversation, and `pluginControls.pluginsDisabled` now leaves built-in plugins on. **CLI 1.5.15** (11-23) adds `AGY_CLI_AUTO_COMPACT_OVERRIDE` for all eligible models (token count, `800K` or `80%`) and stops pruning saved conversations after 500. **App 2.35.0** (11-23): Auto mode now reads files outside the project without asking (sensitive config folders stay protected), and a Conversation Management API lets agents and scripts create, list and delete local conversations.
**Why it matters:** Auto mode can now write into sibling repos on your machine without a prompt; add explicit `ask`/`deny` rules if that matters to you.
Source: [Antigravity changelog](https://antigravity.google/docs/changelog) · Added: 2026-11-25

### Codex CLI 0.172.0: lazy MCP start, `codex exec resume` keeps sandbox settings · 2026-11-24 🆕
Optional stdio MCP servers with cached tool lists now start on their first tool call by default. `codex exec resume` restores the saved sandbox permissions, working directory and workspace roots unless you override them, and `config.toml` can set an approval reviewer for individual connected-app tools. Also: Tab-completion for slash-command arguments, Amazon Bedrock Runtime selectable during app-server setup, and spend-limit errors that name which limit was hit. `code_mode_host_grpc` is deprecated (Code Mode always uses gRPC now).
**Why it matters:** Sessions start faster with many MCP servers, and resumed `exec` jobs no longer fall back to default sandbox settings.
```bash
npm install -g @openai/codex@0.172.0
```
Source: [Codex changelog](https://developers.openai.com/codex/changelog/) · Added: 2026-11-25

### Kiro CLI 3.6.0 + Claude Fable 5.2 preview for Kiro Enterprise · 2026-11-23 → 11-24 🆕
**CLI 3.6.0** (11-24): in V3 sessions a `SubagentStop` hook runs when a subagent finishes and can send it one more instruction before its result returns; hook output over 3,000 characters is saved to a file and the agent gets the start plus the path; `/compact <instructions>` steers that one summary. **Claude Fable 5.2** (11-23) is rolling out in preview to Kiro Enterprise orgs: admins enable it in model governance; it has a 1M context window and a 6x credit multiplier, runs only in the US geography, and its traffic is kept up to 30 days for abuse detection. Kiro Enterprise for iPhone is on the App Store (iOS 26+, organisation sign-in only).
**Why it matters:** Check the 6x multiplier and 30-day retention against your budget and data policy before you enable Fable 5.2.
Source: [Kiro CLI 3.6](https://kiro.dev/changelog/cli/3-6/) · [Fable 5.2 for Kiro Enterprise](https://kiro.dev/changelog/models/claude-fable-5-2-for-enterprise/) · [Kiro changelog](https://kiro.dev/changelog/) · Added: 2026-11-25

### Copilot CLI 1.0.115: tighter shell-read checks, MAI-Code-2-Flash, Gemini 4 Hydrogen · 2026-11-23 🆕
Shell reads that reach outside approved folders through `~`, `~user`, an unset variable, PowerShell `FileSystem::` paths or a glob that matches a symlink now ask first. ACP clients now honour `permissions.disableBypassPermissionsMode`, `copilot -p` honours trusted-repo settings (denied URLs, disabled skills, model), and an empty `--available-tools=` now gives the model no tools instead of all of them. Saying No to a foreground subagent's request now stops the main turn. Windows sandbox package queries are on by default (`sandbox.userPolicy.capabilities: []` opts out). Gemini 4 Hydrogen, GPT-6.2 Astra and MAI-Code-2-Flash join the model picker.
**Why it matters:** Closes several ways a shell read could slip past directory approvals; scripts relying on the old empty `--available-tools` behaviour change.
Source: [Copilot CLI changelog](https://raw.githubusercontent.com/github/copilot-cli/main/changelog.md) · Added: 2026-11-25

### Claude Code 2.1.331: Code Mode on cloud providers, plugin optional dependencies · 2026-11-23 🆕
Experimental Code Mode now works in terminal sessions on Amazon Bedrock, Google Cloud's Agent Platform, Microsoft Foundry and Claude Platform on AWS. Plugin manifests gain `optionalDependencies` (installed with the parent plugin, but each can be disabled or removed on its own). `claude doctor` now reports whether the API is reachable, and `claude_code.llm_request` trace spans carry OpenTelemetry `gen_ai.usage.*`, `gen_ai.response.model` and `gen_ai.operation.name` (input tokens include prompt-cache tokens). New `CLAUDE_CODE_DISABLE_RESPONSE_COMPRESSION` helps behind proxies that cut compressed replies off. Fixes include MCP tool calls hanging up to 30 minutes on malformed replies, compaction dropping part of its summary, a rewind deleting files after a failed restore, and interrupted plugin updates leaving half-installed plugins. The VS Code extension adds "Fix with Claude Code" quick fixes and "Resolve Merge Conflicts".
**Why it matters:** Not a security release, but admins should decide before 30 Nov whether managed marketplaces may auto-update, and OTel dashboards can now read token usage from standard `gen_ai.*` attributes.
Source: [Claude Code CHANGELOG](https://raw.githubusercontent.com/anthropics/claude-code/main/CHANGELOG.md) · release date from [npm](https://www.npmjs.com/package/@anthropic-ai/claude-code?activeTab=versions) · Added: 2026-11-24

### Cursor CLI v2026.11.17: credential and plan-mode hardening · 2026-11-17 🆕
Missed earlier. On Linux, other processes running as you (including commands the agent runs) can no longer read the CLI's memory, environment or open files, or attach a debugger (`CURSOR_AGENT_ALLOW_PROCESS_INSPECTION=1` re-allows it). MCP resources saved to disk now go through normal file-write approvals and must land in the workspace. Plan mode can no longer write outside its canvases folder through symlinks or hard links, and saving a login to the macOS keychain no longer exposes the token in the process list. Prompt hooks set in the team dashboard now actually run in the CLI; before, they ran as empty commands. Also new: `"privateTmp": true` in `sandbox.json` (Linux) and `CURSOR_LOGIN_SHELL=0`. Cursor SDK 1.4.0 adds `run.steer()` for cloud runs and per-model-call token usage in local runs.
**Why it matters:** If your team relies on dashboard prompt hooks as a guardrail, CLI sessions were bypassing them until this release.
Source: [Cursor release notes](https://cursor.com/docs/release-notes) · Added: 2026-11-24

### Devin: Access and Sharing, Devin Bots · 2026-11-19 → 11-20 🆕
**Access and Sharing** (gradual rollout, off by default, enabled through your Cognition rep) adds user groups: secrets, environments, sessions, automations, playbooks, skills, MCP servers and knowledge can be shared with a group, and each session has its own sharing setting. Sessions started from Slack still reply in the channel, but only people the session is shared with can instruct it. Service users and bots now use only resources explicitly granted to them. **Devin Bots** (Nov 19) are always-on Devins with their own identity, memory and permissions that split a goal into parallel cloud sessions and drive each to a mergeable PR, starting from templates such as QA engineer, reviewer or on-call.
**Why it matters:** Once sharing is on, teammates' Slack instructions are ignored until a session is shared with them; audit what bots and service users are granted.
Source: [Devin release notes](https://docs.devin.ai/release-notes/overview) · Added: 2026-11-22

### Google Antigravity App 2.34.0: MCP Apps, Gemini 4 Neon for API-key users · 2026-11-20 🆕
Gemini 4 Neon and the Neon Orchestrator now work on eligible paid consumer plans, with Gemini API keys and with Application Default Credentials; MCP App support arrives. Also: choose Enter or Ctrl/Cmd+Enter to send, side questions from selected terminal output, and new marketplace plugins. Fixes include skills without a frontmatter `name` colliding (they now take their folder name), plugins whose manifest starts with a UTF-8 BOM silently failing to load, and staged updates corrupting Windows installs.
**Why it matters:** Not a security release, but skill authors who relied on folder names should re-check that their skills load.
Source: [Antigravity changelog](https://antigravity.google/docs/changelog) · Added: 2026-11-22

### Claude Code 2.1.330 · 2026-11-20 🆕
Signing in to an organization managed in Anthropic's Enterprise Admin Console now applies that org's settings and its cloud provider or gateway after `claude auth login`. A built-in mod, **easel**, draws charts on request and under MCP metrics results (turn automatic charts off in `/config`). Recurring scheduled tasks and `/loop` now last up to 30 days instead of 7. Behaviour changes: more broad `rm` commands now ask, and `deniedMcpServers` name entries hide only the named claude.ai connector. Fixes include `ExitWorktree` deleting a worktree another running session was using, settings lost on concurrent saves, and freezes after compaction and in WebFetch.
**Why it matters:** If you block claude.ai connectors by name, you may now be blocking less than you think; unattended jobs that `rm` broad paths will stop.
Source: [Claude Code changelog](https://raw.githubusercontent.com/anthropics/claude-code/main/CHANGELOG.md) · Added: 2026-11-21

### Codex CLI 0.171.0: GPT-6.2 Sol by default, `codex exec --remote` · 2026-11-20 🆕
GPT-6.2 Sol and Astra join the model catalog, with Sol as the default selection. The side-by-side TUI workspace is on by default, and `codex exec --remote <ADDR>` starts or resumes non-interactive sessions on an existing app server. Fixes cover enterprise MCP sign-in with identity providers that issue no refresh token and permission profiles lost on directory change, plus Linux sandbox hardening.
**Why it matters:** Unpinned CI jobs may silently move to a new model.
Source: [Codex changelog](https://developers.openai.com/codex/changelog/) · Added: 2026-11-21

### Kiro: Remote SSH and Dev Containers, Kiro for VS Code · 2026-11-19 → 11-20 🆕
**IDE 1.5.11** connects to a Linux machine over SSH (files, terminals and the agent run remotely and keep going after you disconnect) and can reopen a project in its Dev Container. **Kiro for VS Code 1.5.0** is on the VS Code Marketplace and Open VSX for every Kiro plan; it reads the workspace `.kiro` folder (specs, steering, skills, hooks, Powers, MCP) and needs VS Code 1.145+. **Kiro Crew 0.13.0** enables conductor mode in standard builds and turns usage data on by default. VPC connections for cloud sessions are on the [AWS page](../../platforms/aws/README.md#-kiro-awss-agentic-ide-replacing-q-developer).
**Why it matters:** You can use Kiro's specs and hooks without leaving VS Code, and run its agent on a remote dev box.
Source: [Kiro changelog](https://kiro.dev/changelog/) · Added: 2026-11-21

### GitHub Copilot: Gemini 4 Neon, team plugin defaults, December retirements · 2026-11-13 → 11-18 🆕
Gemini 4 Neon is GA for Pro+, Max, Business and Enterprise. Team maintainers and org owners can now pick approved Agent Plugins as team defaults (Business and Enterprise; VS Code, Copilot app and CLI). Seven models retire on 14 and 18 December (see Action items). `gh event listen` (gh v2.105.0, preview behind the Event Streams waitlist) waits for PR events instead of polling, which suits agent loops.
**Why it matters:** Workflows pinned to retiring models break in December.
Source: [Gemini 4 Neon](https://github.blog/changelog/2026-11-18-gemini-4-neon-in-github-copilot) · [Team customizations](https://github.blog/changelog/2026-11-18-customize-github-copilot-for-your-team) · [December deprecations](https://github.blog/changelog/2026-11-13-upcoming-deprecation-of-selected-github-copilot-models-in-december) · [MAI-Code-1.1-Flash](https://github.blog/changelog/2026-11-17-upcoming-deprecation-of-mai-code-1-1-flash-in-december) · [gh event listen](https://github.blog/changelog/2026-11-18-wait-for-pull-request-events-with-github-cli) · Added: 2026-11-21

### Google Antigravity App 2.33.0: SSH hosts and security fixes; Gemini 4 Neon default · 2026-11-17 → 11-19 🆕
Gemini 4 Neon becomes the default model where none is chosen. App 2.33.0 adds SSH connections to remote Linux machines and lets device-management policies in `admin_settings.json` enforce permission ceilings and restrict plugins. It fixes MCP headers sent on cross-origin redirects, a local debug port opened at startup, and hooks or wildcard rules bypassing enforced command review. CLI 1.5.12 adds Neon with `GEMINI_API_KEY`.
**Why it matters:** The fixes close a credential-leak path and a policy bypass, so update managed installs.
Source: [Antigravity changelog](https://antigravity.google/docs/changelog) · Added: 2026-11-21

### Gemini CLI 0.69.0 → 0.70.0: policy-engine hardening · 2026-11-19 🆕
0.70.0 runs policy regexes on `re2js` (linear time, against ReDoS), matches `commandPrefix`/`commandRegex` against top-level command arguments only, asks before shell commands with unresolved variable expansions, and skips system MCP servers whose command files have insecure permissions. 0.69.0 adds `/stats heatmap` and standalone `theme.json` themes.
**Why it matters:** Policy rules aimed at nested or wrapped commands may now behave differently.
Source: [Gemini CLI release notes](https://raw.githubusercontent.com/google-gemini/gemini-cli/main/docs/changelogs/latest.md) · Added: 2026-11-21

### Claude Code 2.1.326 → 2.1.329 · 2026-11-16 → 11-19 🆕
- **2.1.326:** a large permission and sandbox hardening pass. Sandboxed commands on macOS, Linux and WSL no longer write to some sensitive home folders by default (`sandbox.filesystem.allowWrite` re-allows some); file tools refuse writes to sign-in files such as `.credentials.json`; more Bash and PowerShell commands ask first, some even in bypass mode, and are refused where no one can answer. Self-hosted runners without `gh` get a built-in `gh api` routed via Anthropic (`--use-anthropic-gh false` turns it off). Adds `OTEL_RESOURCE_INCLUDE_HOST`.
- **2.1.327:** `claude mcp add-json <name> -` reads server JSON from stdin so tokens stay off the command line; `ExitWorktree` asks before removing a worktree that may hold unsaved work; `permissions.blockReadsOutsideWorkingDirectories` covers more Bash commands; project-scope `claude mcp add/remove` no longer deletes other keys in `.mcp.json`. Auto mode now warns that an upcoming release removes the billed classifier fallback.
- **2.1.328:** auto mode for Claude Opus 4.6 and Sonnet 4.6 on Bedrock, Google Cloud, Microsoft Foundry and the Claude apps gateway. Self-hosted runners turn the built-in `gh api` **off** by default where settings guard GitHub tools by name.
- **2.1.329:** the trust dialog now says where a folder's hooks are declared; warns when managed-settings hooks fail to load; fixes `~/.claude.json` sometimes being reset to defaults.

**Why it matters:** CI, `-p` and scheduled runs that worked under 2.1.325 may now stop at a prompt or get refused. Run them once after upgrading and add explicit allow rules where needed.
Source: [Claude Code CHANGELOG](https://raw.githubusercontent.com/anthropics/claude-code/main/CHANGELOG.md) · release dates from [npm](https://www.npmjs.com/package/@anthropic-ai/claude-code?activeTab=versions) · Added: 2026-11-20

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
- **Copilot CLI 1.0.113** (2026-11-17): admins can switch off the built-in Browser Use with the managed setting `features.browserUse`, which also applies to running sessions.

**Why it matters:** Org admins need to flip a policy before developers can use Fable 5.2, and teams on the Local harness have a migration deadline.
Source: [GitHub changelog: Copilot weekly releases, November 9](https://github.blog/changelog/2026-11-16-github-copilot-weekly-releases-november-9) · [Copilot CLI changelog](https://raw.githubusercontent.com/github/copilot-cli/main/changelog.md) · Added: 2026-11-19 · Updated: 2026-11-20

### Kiro: admin-enforced sandboxing and org sign-in for MCP · 2026-11-16 → 11-18 🆕
- **Local Sandbox Controls:** admins can require sandboxing for commands and local stdio MCP servers, and developers can't turn it off in client settings.
- **CLI 3.5.0:** organisation sign-in for MCP servers, so one identity-provider login covers every server set to use it.
- **CLI 3.4.0:** hooks can rewrite tool inputs and answer permission prompts; a `deny` from any hook overrides an `allow`.
- **IDE 1.4.236** (2026-11-18): a Permission Request hook answers approval prompts from a script, prompts show the final arguments after Pre Tool Use hooks rewrite them, org sign-in comes to HTTP MCP servers in the IDE, and powers and skills install from public GitLab URLs (self-hosted GitLab hosts go in `kiroAgent.powers.trustedGitLabHosts`).
- Enterprise admins can stream LLM requests and tool calls as OpenTelemetry events (exports exclude prompts, responses and code). Daily metrics move to 00:30 UTC on 2026-11-26.

**Why it matters:** Platform teams can now enforce a sandbox and central MCP auth for Kiro rather than relying on each developer's settings.
Source: [Kiro changelog](https://kiro.dev/changelog/index) · [IDE 1.4.236](https://kiro.dev/changelog/ide/1-4-236/) · Added: 2026-11-19 · Updated: 2026-11-20

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
