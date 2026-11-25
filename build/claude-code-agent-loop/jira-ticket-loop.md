# Jira ticket agent loop (Claude Code)

A three-role loop for taking one Jira ticket from requirement to an open pull request in Claude Code. The **Tech Lead** runs as the main thread. It delegates to a **Developer** subagent (code + unit tests) and a **QA** subagent (acceptance criteria + integration tests), reviews the result, and repeats until the milestone is met. Then it opens a PR and stops.

| Role | File | Writes | Model |
|---|---|---|---|
| Tech Lead (orchestrator) | [agents/tech-lead.md](agents/tech-lead.md) | `.agent-loop/<TICKET>/` only, plus git and the PR | `opus` |
| Developer | [agents/developer.md](agents/developer.md) | Production code and unit tests | `sonnet` |
| QA | [agents/qa.md](agents/qa.md) | Integration tests and test fixtures | `sonnet` |

## The loop

```mermaid
flowchart TD
    start(["Start: claude --agent tech-lead"]) --> read["TL: read Jira ticket<br/>requirements + acceptance criteria"]
    read --> clear{"Requirements<br/>clear and testable?"}
    clear -->|no| ask(["Stop: TL asks human<br/>open questions"])
    clear -->|yes| plan["TL: plan<br/>branch, tasks, test plan, status.md"]

    plan --> dev["DEV: implement task<br/>code + unit tests"]
    dev --> unit{"Unit tests,<br/>lint green?"}
    unit -->|no| dev
    unit -->|yes| qa["QA: verify<br/>run unit tests, write + run<br/>integration tests, check every AC"]

    qa --> qav{"QA verdict"}
    qav -->|BLOCKED| blocked(["Stop: TL reports<br/>missing env or info"])
    qav -->|FAIL| triage["TL: triage defects<br/>numbered fix list"]
    qav -->|PASS| review["TL: code review<br/>diff vs ACs, design, re-run suites"]

    review --> rv{"TL review"}
    rv -->|changes requested| triage
    triage --> budget{"Fix cycles<br/>used < 5?"}
    budget -->|yes| dev
    budget -->|no| limit(["Stop: TL reports<br/>loop limit, no PR"])

    rv -->|approved| milestone{"Milestone met?<br/>all tasks done, all ACs tested,<br/>all suites green"}
    milestone -->|no, next task| dev
    milestone -->|yes| pr["TL: commit, push branch,<br/>gh pr create"]
    pr --> done(["Stop: PR opened"])

    classDef tl fill:#EEEDFE,stroke:#534AB7,color:#26215C
    classDef dv fill:#E6F1FB,stroke:#185FA5,color:#042C53
    classDef q fill:#E1F5EE,stroke:#0F6E56,color:#04342C
    classDef stop fill:#F1EFE8,stroke:#5F5E5A,color:#2C2C2A
    class read,plan,triage,review,pr,clear,rv,milestone,budget tl
    class dev,unit dv
    class qa,qav q
    class start,ask,blocked,limit,done stop
```

Purple is the Tech Lead, blue is the Developer, green is QA, and grey nodes are start and stop points. There are four ways out of the loop. Only one of them opens a PR.

## Setup

1. Copy the agents into the target repo so Claude Code can find them:
   ```bash
   mkdir -p .claude/agents
   cp <path-to>/build/claude-code-agent-loop/agents/*.md .claude/agents/
   ```
2. Give the Tech Lead access to Jira. Connect a Jira MCP server, then add its tool names (`mcp__<server>__…`) to the `tools:` line in `tech-lead.md`. Otherwise, paste the ticket into the prompt below.
3. Make sure `gh auth status` succeeds and the repo's unit and integration test commands run locally.
4. Add `.agent-loop/` to `.gitignore`. It holds the Tech Lead's status file and PR body.
5. Start the session with the Tech Lead as the main thread:
   ```bash
   claude --agent tech-lead
   ```
   With `--agent`, the main thread takes the Tech Lead's system prompt, model and tool restrictions. `Agent(developer, qa)` in its `tools` means it can spawn only those two subagents.

## Kick-off prompt

Fill in the placeholders and paste this as the first message:

```text
Ticket: <JIRA-KEY>
(If Jira tools are unavailable, the ticket text is pasted below.)

Default branch: <main>
Unit test command: <e.g. ./gradlew test | npm test | pytest -m "not integration">
Integration test command: <e.g. ./gradlew integrationTest | npm run test:int | pytest -m integration>
Lint / typecheck command: <optional>
Environment notes: <e.g. docker compose up -d db before integration tests>

Run the Jira ticket loop for this ticket:
1. Read the ticket and confirm the acceptance criteria are clear and testable. If not, list the open questions and stop.
2. Create the feature branch, plan the tasks and test plan, and start .agent-loop/<JIRA-KEY>/status.md.
3. For each task: delegate implementation to `developer`, then verification to `qa`.
   On QA FAIL or review "changes requested", send a numbered fix list back to `developer`.
   Keep at most 5 fix cycles; at the limit, stop and report without opening a PR.
4. When QA passes, review the diff against every AC and re-run both test suites yourself.
5. When the milestone is met (all tasks done, every AC covered by a passing test,
   both suites green, QA PASS, review approved), commit, push the branch, open the PR
   with `gh pr create`, print the PR URL, and stop.

Keep status.md updated after every step. Don't merge the PR.

<paste ticket text here if needed>
```

## Why it's shaped this way

- **The Tech Lead never edits code.** Review only means something when the reviewer didn't write the change. This is enforced in its prompt, and its write access is meant only for `.agent-loop/`.
- **QA works in a fresh context.** QA doesn't see the developer's reasoning, only the ACs and the changed files, so it tests the requirement and not the implementation.
- **The milestone is a checklist.** The loop ends when every box in the Tech Lead's milestone check is ticked, not when an agent says it's done.
- **There's a fix-cycle cap.** Without one, a bad ticket or a flaky environment loops forever. Five cycles, then stop and hand the problem to a human.

Sources: [Claude Code subagents](https://code.claude.com/docs/en/sub-agents) (frontmatter fields, `--agent`, `Agent(...)` allowlist) · [GitHub CLI `gh pr create`](https://cli.github.com/manual/gh_pr_create)
