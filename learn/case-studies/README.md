# Production case studies & postmortems

_Last updated: 2026-11-23 · Cadence: weekly (Mondays), plus anything exceptional_

> How real teams shipped agents and what broke. Patterns that survived real traffic are worth more than launch posts. Each entry lists the lessons that carry over to your own work.

## 📚 Learn this week

**[Anthropic: an update on recent Claude Code quality reports](https://www.anthropic.com/research/april-23-postmortem)** (2026-04-23): a postmortem of three unrelated changes that together made Claude Code seem worse for six weeks. They were a lower default reasoning effort, a caching bug that dropped prior reasoning on every turn after a session went idle, and a system-prompt line limiting verbosity. Each looked safe alone. The bug passed code review, tests and dogfooding, and concurrent experiments hid it. Read it for the fixes: per-model evals and ablations on every prompt change, soak periods and gradual rollouts for anything that trades off intelligence, and treating user reports as signal rather than noise. Added: 2026-11-23

**Previous picks:** [Anthropic: harness design for long-running apps](https://www.anthropic.com/research/harness-design-long-running-apps) (week of 2026-11-18)

---

## 🏭 Case studies

### OpenAI · Performance Factory: agents that investigate performance regressions · 2026-11-19 🆕
A cloud system of Codex workflows. A performance alert opens a task, one agent investigates the root cause, a separate adversarial session tries to disprove the diagnosis, an agent proposes a fix as a PR for an engineer to review, and an agent checks recovery after deploy. Over a little more than three months it tracked more than 1,700 investigations and root-caused more than 600. In a manual review of 100 suggestions, 70% were graded accurate *(self-reported)*.
**Lessons:**
- **Keep task state outside the agent:** findings live in a task service, so work can pass between agents and engineers.
- **Add an adversarial second session:** it caught errors that a single agent missed.
- **Backtest before changing the agent:** replay past incidents with fresh agents and stripped signals, and score timing, scope and cause separately.
- **Monitor the agents:** a daily check on agent logs turns repeated tool or access failures into repair tasks.
- **Fixes are harder than diagnoses:** proposed fixes sometimes add complexity or new bugs, so engineers keep architectural calls.
Source: [OpenAI engineering](https://openai.com/index/how-openai-performance-factory-keeps-chatgpt-fast/) · Added: 2026-11-23

### Stripe · evals for coding agents building Stripe integrations · 2026-11-19 🆕
Stripe ran 69 integration scenarios (payments, subscriptions, Connect) against 14 model-and-harness pairs, with and without its agent plugin. An LLM plays a developer with hidden needs, and each MUST/SHOULD criterion is graded separately from the transcript and the workspace. Every pair improved with the plugin, by about 3 to 8 points. Strict grading (all MUST criteria pass) dropped the average across agents from 78.1% to 29.4%. Stripe released the Forge eval harness on GitHub *(self-reported)*.
**Lessons:**
- **Grade the integration, not just the code:** tests can pass while the API usage is wrong. One example checked only `status === 'succeeded'` and could ship orders after a refund.
- **Report strict and soft scores:** averages hide last-mile failures.
- **Simulate the user's unstated needs** instead of handing the agent a complete spec.
- **Give agents authoritative docs and tools:** web searches fell 96% and outdated parameters fell from 7% to 1.3%.
- **Test each model separately and check your judge:** tool-use changes varied widely by model, and a second-judge probe found uniform leniency but no model bias.
Source: [stripe.dev](https://stripe.dev/blog/stripe-integration-evals-methodology) · Added: 2026-11-23 · → [Evals & observability](../../architecture/evals-and-observability/README.md)

### PagerDuty · multi-agent system in production · Jun 2026
A year of running a multi-agent system for incident response.
**Lessons:**
- Expect reliability work after the demo: layered validation, fallbacks and error containment are each substantial projects.
- Decide each agent's tools, state and allowed actions before writing code.
- Build tracing, evals and guardrails early, or customers find failures before you do.
- Bring designers in from the start, because showing the agent's steps is what builds enterprise trust.
- Keep DevOps discipline: staged rollouts, canaries and feature flags.
Source: [PagerDuty engineering blog](https://www.pagerduty.com/eng/production-ai-agents-closing-the-gaps-between-idea-and-reality/) · Added: 2026-11-18

### Arize · "Alex", an AI engineering agent · 2026
An in-product agent for tracing, evals and playground work.
**Lessons:**
- **Enforce planning in code:** a todo tool, the plan re-injected every call, and a finish gate.
- **Context at scale:** a structure-preserving data preview, with jq/grep-style tools and output caps for the full data.
- **Test with production data:** successful sessions become golden examples; LLM-judged decision-point and trajectory tests run in CI.
- **Debug through observability:** traces and evals are exposed to the agent as CLI skills, so it can investigate itself.
Source: [ZenML LLMOps database](https://www.zenml.io/llmops-database/building-alex-an-agent-first-ai-engineering-assistant-with-production-grade-llmops) · Added: 2026-11-18

### Replit · Replit Agent
Building and scaling a fully automated code agent.
**Lessons:** be clear about who the agent is for, since that drives every trade-off; running several attempts in parallel and picking the best (MCTS-style) markedly improves accuracy on long trajectories.
Source: [ZenML LLMOps database](https://www.zenml.io/llmops-database/building-and-scaling-production-code-agents-lessons-from-replit) · Added: 2026-11-18

### mabl · three years of agents for software testing · Jul 2026
A two-part retrospective from a testing company that has run agents in production since 2023.
Source: [Mabl engineering blog via daily.dev](https://daily.dev/posts/three-years-of-building-agents-in-production-part-2--9uvhtnda1.md) · Added: 2026-11-18

## 🗃️ Where to find more

- [ZenML LLMOps database](https://www.zenml.io/llmops-database): hundreds of summarised production case studies, searchable by industry
- Company engineering blogs: Anthropic, OpenAI, PagerDuty, Replit, Ramp, Shopify, Stripe, Atlassian
