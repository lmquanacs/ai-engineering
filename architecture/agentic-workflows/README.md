# Agentic workflows: patterns and breakthroughs

_Last updated: 2026-11-25_

> How to structure agent systems, and what the evidence says actually works. Patterns are stable; the "latest evidence" section changes fastest.

## 🧭 Pattern cheat-sheet (start simple)

| Pattern | Shape | Use when | Breaks when |
|---|---|---|---|
| **Single agent loop** | One model + tools + memory, looping | Default. Most tasks. | The context window fills with unrelated work |
| **Router / triage** | A classifier agent hands off to a specialist | Distinct request types with different tools | Routing errors cascade silently |
| **Sequential pipeline** | Fixed stages (plan → build → review) | The process is known and auditable | Upstream errors flow downstream unchecked |
| **Orchestrator–workers / supervisor** | A lead agent delegates subtasks in parallel | Wide, parallelisable work (research, multi-file changes) | Workers share the lead's flawed plan |
| **Evaluator–optimizer** | Generate → critique → revise loop | Clear quality criteria exist | The critic is the same model with the same blind spots |
| **Hierarchical** | A router at the top, supervisors below | Large orgs, many domains | Latency, cost and debugging depth |
| **Swarm / peer-to-peer** | Agents coordinate through a shared bus | Exploration, debate | Hard to predict and debug; needs time limits |

**Rule of thumb from 2026 practitioner guides:** start with one agent and one workflow. Add structure only for parallelism, separation of duties, reliability or permission boundaries. Most teams overshoot by one tier. ([StackAI guide](https://www.stackai.com/blog/the-2026-guide-to-agentic-workflow-architectures) · [Arahi guide](https://bump.arahi.ai/blog/ai-agent-orchestration))

Production guardrails that apply to every pattern: an iteration cap, deadlock detection that escalates to a human, checkpointing so a run survives restarts, and validated contracts at every hand-off.

---

## 🔬 Latest evidence: what actually moves the needle

### When tools fail, agents make things up · RetryRealistic · arXiv 2611.28341 · 2026-11-20 🆕
The authors injected 9 fault types into 8 real tools (filesystem with real permissions, SQLite, a local HTTP server, a shell) across 30 multi-step tasks and 2,100 runs. Four agents recovered correctly only 19–68% of the time, and 6–26% of runs ended in a confidently stated wrong answer. The fault type mattered more than the model: partial-data faults drove fabrication (up to 38%), while outright denials led to honest failures. A verification-first monitor that checks answers against structured tool output and sends corrective instructions instead of hard blocks raised correct recovery from 45.6% to 56.3% and cut fabrication from 17.3% to 10.8%. Removing chain-of-thought made fabrication worse *(self-reported)*. Toolkit and traces: `Kingsford-Group/RetryRealistic`.
**Why it matters:** Make tools fail loudly. Return explicit error or truncation flags instead of partial results that look complete, and add fault-injection cases (timeouts, partial pages, permission errors) to your agent evals.
Source: [arXiv 2611.28341](https://arxiv.org/abs/2611.28341) · Added: 2026-11-25

### Lead agents rubber-stamp their subagents · RI-Bench · arXiv 2611.27139 · 2026-11-20 🆕
RI-Bench tests whether a "senior" agent actually weighs, verifies and relays its subordinates' reports, by perturbing that material in controlled ways and watching how the output changes. Across eight LLMs and more than 12,000 episodes, planted procedural errors were rarely adopted (2.9%), but senior agents went with a majority of low-value generic reviews in up to 71% of decisions and dropped sources' stated limitations in up to 65% of cited claims. Prompts that spell out the senior agent's obligations helped without fixing it, and changed behaviour in control runs *(self-reported)*. Code and data: `jxtse/ri-bench`.
**Why it matters:** In orchestrator–worker and reviewer-committee setups, a good final answer can hide poor aggregation. Test the lead's weighing and caveat-passing directly, and don't let it count votes. → [Research](../../learn/research/README.md)
Source: [arXiv 2611.27139](https://arxiv.org/abs/2611.27139) · Added: 2026-11-24

### Evolve the harness before the weights · arXiv 2611.25380 · 2026-11-19 🆕
The authors optimise the system prompt, tool schemas, skill library and planning scaffold with GEPA while the model stays frozen, on SWE-bench Verified, OfficeBench and Terminal-Bench with a Claude Code-style agent. Weight updates gave the biggest single gains, harness evolution recovered most of them for a small fraction of the compute, and both together did best. Hugging Face's same-week [harness adapters](../../models/fine-tuning/README.md#-releases) point the same way from the training side *(both self-reported)*.
**Why it matters:** If you can't fine-tune, optimising prompts and tool schemas inside your own harness is the cheap way to get most of the gain.
Source: [arXiv 2611.25380](https://arxiv.org/abs/2611.25380) · Added: 2026-11-21

### Agent teams cost 1.8–5.1× more for little gain · Vals AI, 2026-10-09 🆕
On Vibe Code Bench (50 full-stack apps), Vals compared one agent against a lead with up to five subagents, using GPT 6 Sol and Claude Opus 5.5 at medium and max effort. Teams cost 1.8–5.1× as much; the only statistically significant team gain was Sol at medium effort (+7.3 points), while simply raising a single Sol agent to max effort gave +11.4 *(self-run, one run per setup)*.
**Takeaway:** Try more effort on one agent before adding subagents.
Source: [Vals AI: Do agent teams pay off?](https://www.vals.ai/blog/multi-agent-vibe-code-bench) · Added: 2026-11-20

### Best harness depends on the model · FrontierHarness Eval v1.1, 2026-11-17 🆕
In 27,280 runs (22 harness configurations × 5 open models), the model explained most of the cost, but with the model fixed the harness still changed cost per task by about 1.8–5×. Rankings reshuffled between models, and 64.5% of spend went to failed runs. Steps per pass, not prompt size or tool count, tracked cost.
**Takeaway:** A harness choice is only valid for the model you tested it with. Cutting wasted steps on doomed runs matters more than trimming the prompt. → [Evals & observability](../evals-and-observability/README.md#frontierharness-eval-v11--harness--model-leaderboard--2026-11-17-)
Source: [Runta](https://runta.com/blog/introducing-frontierharness-eval-v1-1/) · Added: 2026-11-19

### Controlled studies of harness tricks · Surge AI + FireFlash (UCLA), Nov 2026 🆕
Two independent reports dismantled popular workflow plugins and harness techniques on real engineering tasks. As summarised by [yage.ai](https://yage.ai/share/agent-harness-tricks-benchmark-en-20261109.html):

| Technique | Effect | Cost |
|---|---|---|
| Higher reasoning effort (Opus 5.5, medium → xhigh) | **+11.3** (31.1 → 42.4) | 3.5× |
| End-of-turn goal checks (`/goal` + review plugin) | **+3.3** | 1.8× |
| Clarify-spec + TDD loop (Superpowers) | **+2.4**, statistically significant | ~1.1× |
| Low-level harness plumbing (background slow commands, file-backed output previews, cache-preserving summaries) | **+4.4** on Terminal-Bench 4.0 | about ⅓ cheaper |
| Anti-waste rules (no `sleep` polling, in-place edits, single-pass writes) | — | a further 16% cheaper |
| Multi-subagent "committee" (37 skills, 17 subagents) | +1.8, **within noise** | up to **8×** |
| Heavyweight harnesses vs a 100-line harness (HarnessTax, 492 problems) | under 2% accuracy difference | 3–5× more expensive |

**Takeaway:** Make the control layer as light as you can. Spend on reasoning effort, real verification (tests, goal checks) and cache-friendly context. Avoid committees that all review the same flawed plan.
_Added: 2026-11-18_

### Harness engineering is now a discipline
*Agent = Model + Harness*: the harness is all the code, config and runtime around the model. Anthropic's write-up on harnesses for long-running apps covers decomposing builds into chunks, handing context between sessions through structured artifacts, and using **context resets** when compaction alone isn't enough. Addy Osmani's guide adds the key habit: treat every agent mistake as a permanent signal and fix the harness, not just the output.
Sources: [Anthropic: harness design for long-running apps](https://www.anthropic.com/research/harness-design-long-running-apps) · [Addy Osmani: Agent harness engineering](https://addyosmani.com/blog/agent-harness-engineering/) · Added: 2026-11-18

---

## 🛠️ New orchestration features in tools

| Tool | Feature | Why it matters | Source |
|---|---|---|---|
| Google Antigravity | `/swarm` multi-agent command + orchestrator mode for planning parallel work (Nov 12) | First-class parallel agents in an IDE | [ThursdAI Nov](https://thursdai.news/releases/2026-11) |
| Codex CLI 0.167 | `codex agents` command center that marks unread results | Managing many background agents from one place | [Codex changelog](https://developers.openai.com/codex/changelog/) |
| Claude Code | Workflow tool for deterministic multi-agent orchestration (May 2026, behind `CLAUDE_CODE_WORKFLOWS=1`) | Scripted fan-out with predictable control flow | [releases.sh digest](https://releases.sh/collections/coding-agents/digest/2026-05-18) |
| Vercel AI SDK 7 | `HarnessAgent` adapters that run Claude Code, Codex, Deep Agents, OpenCode and others from TypeScript | Embed a full coding harness in your own product | [What's new in AI SDK 7](https://www.developersdigest.tech/blog/vercel-ai-sdk-whats-new-2026) |

## ☕ JVM: Spring AI agentic patterns series

Spring AI publishes a pattern series with runnable code: Agent Skills, AskUserQuestion (clarify before acting), TodoWrite (task tracking), task subagents, A2A interop, AutoMemoryTools (persistent memory), and the Session API (event-sourced short-term memory with compaction). Spring AI Agents (wrapping CLIs such as Claude Code and Codex) was planned for November 2026 as a Spring Projects Experimental project.
Sources: [Spring AI agentic patterns posts](https://spring.io/team/tzolov) · [Spring AI 2.1.0-M1 roadmap](https://spring.io/blog/2026/09/25/spring-ai-2-1-0-M1-available-now/) · Added: 2026-11-18

## 🔌 Interop protocols to know

- **MCP**: agent ↔ tools/data. → [MCP servers](../../build/mcp-servers/README.md)
- **A2A** (Agent2Agent): agent ↔ agent discovery and messaging (supported by Spring AI, Google ADK, Koog).
- **ACP** (Agent Client Protocol): editor ↔ coding agent (JetBrains, Zed, Gemini CLI; Cursor joined the ACP registry in March 2026).
