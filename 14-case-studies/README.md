# 14 · Production case studies & postmortems

_Last updated: 2026-11-18 · Cadence: weekly (Mondays), plus anything exceptional_

> How real teams shipped agents and what broke. Patterns that survived real traffic are worth more than launch posts. Each entry lists the lessons that carry over to your own work.

## 📚 Learn this week

**[Anthropic: harness design for long-running apps](https://www.anthropic.com/research/harness-design-long-running-apps)**: how to keep an agent coherent across hours by decomposing the build, handing off context through structured artifacts, and using context resets where compaction isn't enough. Read it before you design any agent that runs for more than one session.

---

## 🏭 Case studies

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
