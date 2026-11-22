# Successful AI projects

_Last updated: 2026-11-23 · Cadence: weekly (Mondays), plus anything exceptional_

> AI projects that **shipped and worked**, with a named owner, a measurable before/after result and a public source, and what made them succeed. The companion page [Case studies & postmortems](../case-studies/README.md) covers lessons and failures; this page is the showcase.

**Inclusion bar:** a named company or project, a specific workflow, a measured outcome with its date, and a public source. Vendor-reported numbers are marked as such, and projections ("expected to save…") are excluded.

## 🏆 Production showcase: AI in software engineering

| Project | What it is | Reported result | As of | Source |
|---|---|---|---|---|
| **Runway · software factory** | Handed its delivery pipeline to agents one stage at a time: a cloud coding agent, an AI reviewer, risk-rated AI approval (people still sign off high-risk and sensitive changes), QA agents, agents that roll back on alerts, and a coordinator | Agent share of merged PRs **0.1% (Jun) → 38% (Oct)**. Weekly merged PRs **929 → 2,235**. Median wait for first approval **2.3 h → ~5 min**. Core API ready-to-merge **~11 h → under 2 h**. AI-approved merges reverted ~0.10% vs ~0.5% for human-approved | Jun–Nov 2026 | [Runway engineering (2026-11-20)](https://runway.com/news/engineering/building-a-software-factory) |
| **Ramp · Inspect** | In-house background coding agent: one Modal sandbox per session, full dev environment, verifies its own work. Launched in Slack. | Writes about **3 of every 4 merged PRs**, up from ~30% at launch; about 1M sessions; also used by non-engineers. Ramp opened it to other companies in Oct 2026. | Oct–Nov 2026 | [Linear customer story](https://linear.app/customers/ramp) · [ZenML case study](https://www.zenml.io/llmops-database/building-an-internal-background-coding-agent-with-full-development-environment-integration) |
| **Spotify · Honk** | Background coding agent on a Claude Agent SDK harness | About **1,000 merged PRs every 10 days**; Spotify says *review*, not coding, is now the constraint | 2026 | [In-house coding agents research](https://rywalker.com/research/in-house-coding-agents) |
| **Coinbase · Forge + Mux** | Coding agent plus a multi-agent orchestration layer | 5% of merged PRs, with PR cycle time cut about 10× (~150h → ~15h). Mux: 5,068 merged PRs across 461 repos, and its users merge 3.5× more PRs per engineer | Feb–May 2026 | [Coinbase Forge research](https://rywalker.com/research/coinbase-forge) |
| **Stripe · Minions** | Internal coding agents | More than **1,000 AI-authored PRs a week** | Jun 2026 | [SoftwareSeni comparison](https://www.softwareseni.com/how-ramp-dropbox-and-stripe-measure-the-impact-of-ai-coding-agents/) |
| **Abnormal AI** | Background agents plus a Claude Code SDK planning CLI | **13% of PRs** from background agents; agents generate all design reviews company-wide | Feb–Mar 2026 | [Abnormal AI research](https://rywalker.com/research/abnormal-ai-agents) |
| **Loyola Marymount University · Kiro** | A two-person cloud team used Kiro for fleet-wide Lambda updates | 500 Lambda functions across dozens of accounts: **2 months → half a day** | 2026 | [Kiro: one year](https://kiro.dev/blog/one-year/) |
| **Cognition deployed engineering** | Devin on customers' existing backlogs | **82% reduction** in the targeted work *(vendor-reported)* | 2026 | [StartupHub summary](https://www.startuphub.ai/news/cognition-s-jia-wu-on-measuring-ai-engineering-value) |

## 🏢 Production showcase: AI in business workflows

| Project | Workflow | Reported result | Source |
|---|---|---|---|
| **StatusGator** | LLM-based parsing engine for non-standard cloud status pages | Parser onboarding **4.5 days → 12 minutes** | [SumatoSoft study of 16 rollouts](https://sumatosoft.com/blog/ai-adoption-success-cases-in-enterprises) |
| **Skylum** | AI-supported localisation | Campaign time-to-market **14 → 4 business days**; external translation costs down more than 40% | [SumatoSoft study](https://sumatosoft.com/blog/ai-adoption-success-cases-in-enterprises) |
| **Bates Electric** | Dispatcher assistance | Response time **~45 min → under 15 min** | [SumatoSoft study](https://sumatosoft.com/blog/ai-adoption-success-cases-in-enterprises) |
| **PagerDuty** | Multi-agent incident-response system in production | Shipped and running for a year; see the lessons in [details](../case-studies/README.md) | [PagerDuty engineering](https://www.pagerduty.com/eng/production-ai-agents-closing-the-gaps-between-idea-and-reality/) |

## 🔑 What the winners have in common

1. **The agent verifies its own work** with the same tools an engineer uses: tests, preview deploys, screenshots. Ramp built Inspect for exactly this, after noting that many agents do only about half the work and leave verification to reviewers.
2. **One isolated sandbox per session** with a full, realistic environment. → [Agent infrastructure](../../architecture/agent-infrastructure/README.md)
3. **Adoption was organic, not mandated**: engineers chose the tool because it saved them time.
4. **It meets people where they already work** (Slack, Jira, PR comments), not in a new UI.
5. **Review becomes the bottleneck**, so the winners invest in automated first-pass review and smaller PRs.
6. **A named workflow with a baseline**: every successful rollout in SumatoSoft's 16-case study had a named workflow, a baseline, a post-AI result, a human review point, and a reason the team accepted the change.

→ The architecture behind these: [Reference architecture C](../../architecture/README.md#c--background-coding-agent-platform-the-ramp-inspect--spotify-honk-pattern)

## 🌟 Open-source AI projects that took off

| Project | Why it succeeded | Signal |
|---|---|---|
| **OpenClaw** | Open-source personal AI assistant that developers could run and extend themselves | About 250K ⭐ in 60 days (Feb 2026), one of the fastest-growing repos in GitHub history; moving to an open-source foundation |
| **[vLLM](https://github.com/vllm-project/vllm)** | The default open serving engine; fast release cadence, broad hardware support | Among the fastest-growing projects by contributors (Octoverse); v0.33 had 389 contributors |
| **DeepSeek Harness** | Plugin-based agent harness runtime | +152K ⭐ in August 2026 alone (GitTrend) |
| **[Dify](https://github.com/langgenius/dify)** | Self-hostable platform for standing up AI apps fast | A long-running top AI repo |
| **[obra/superpowers](https://github.com/obra/superpowers)** · **[mattpocock/skills](https://github.com/mattpocock/skills)** | Agent skills that encode engineering discipline (TDD, spec-first, hand-offs) | 300K+ ⭐ each; superpowers' TDD loop showed measurable gains in controlled tests ([details](../../architecture/agentic-workflows/README.md#-latest-evidence-what-actually-moves-the-needle)) |

Sources: [ByteByteGo: top AI GitHub repositories in 2026](https://blog.bytebytego.com/p/top-ai-github-repositories-in-2026) · [What 100 trending GitHub projects tell us](https://dev.to/ji_ai/what-100-trending-github-projects-tell-us-about-where-ai-is-actually-going-4977) · [ZimaSpace: trending AI projects, Aug 2026](https://shop.zimaspace.com/blogs/tech-ai-hub/top-10-open-source-ai-projects-trending-on-github-in-2026) · Added: 2026-11-18

## 🧪 Reading success claims critically

- Prefer **merged** PRs and **cycle time** over "PRs opened" or "lines generated".
- Ask what the **baseline** was, who measured it, and over what window.
- Vendor-published customer numbers are useful but self-interested, so look for a second source.
- Org-wide claims ("one agent does the work of N employees") rarely include quality or rework data, so treat them as marketing until shown otherwise.
