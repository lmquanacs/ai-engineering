# AWS for AI engineering

_Last updated: 2026-11-27_

> Everything on AWS that matters to AI engineers: Bedrock models, AgentCore (the agent runtime platform), Strands Agents, Kiro, AWS MCP servers, and how they connect to Spring, Python and TypeScript apps. **re:Invent 2026 runs 30 Nov – 4 Dec**, so expect a large wave of launches.

## ⚡ Action items & dates

| When | What | Do this |
|---|---|---|
| **2026-11-30 → 12-04** | **AWS re:Invent 2026**, Las Vegas | Watch the keynotes, then read the daily digests that week for the developer-relevant launches. ([event summary](https://ecorpit.com/aws-reinvent-2026-keynotes-what-to-watch/)) |
| now | Amazon Q Developer is being replaced by **Kiro**: new sign-ups blocked since 2026-05-15, end of support for plugins and subscriptions on **2027-04-30** | Plan the migration of IDE plugins and team subscriptions to Kiro. ([Enterprise DNA](https://enterprisedna.co/resources/news/aws-kiro-replaces-amazon-q-developer-spec-driven-2026)) |
| now (since 2026-11-12) | New **AgentCore runtimes default to the next-generation runtime (V2)** in 19 Regions; existing runtimes stay on V1 until you move them | Set `platformVersion` explicitly in your IaC: `V2` to migrate an existing runtime on update, `V1` to keep a new one on the old platform. ([What's New](https://aws.amazon.com/about-aws/whats-new/2026/11/new-agentcore-runtime-default/)) |
| **2027-04-08** | **Claude Sonnet 4.5 on Bedrock** (`anthropic.claude-sonnet-4-5-20250929-v1:0` and its `us.`/`eu.`/`au.`/`jp.`/`global.` profiles) reaches end of life; Legacy since 2026-10-08, public extended access from 2027-01-08 (GovCloud: 2027-04-27). Anthropic's own API retires it on 2026-11-30, but Bedrock calls keep working until then | Move to Sonnet 5.5 at your own pace; after end of life calls fail with `ResourceNotFoundException`. ([legacy models](https://docs.aws.amazon.com/bedrock/latest/userguide/model-lifecycle-legacy.html)) |
| if adopting the managed AWS MCP Server | Overlapping tools with `aws-api-mcp-server` and `aws-knowledge-mcp-server` | Remove those two from your MCP config, because duplicate tool names confuse agents. ([dev.to guide](https://dev.to/jangwook_kim_e31e7291ad98/aws-mcp-server-ga-secure-aws-api-access-for-ai-agents-2bia)) |

---

## 🧠 Amazon Bedrock: models

### Bedrock Trusted Access API (GA) + Anthropic Enterprise Frontier Safeguards / Enterprise Data Controls (preview) · 2026-11-23 🆕
A new API lists the model-provider programs your account can join and their status (`aws bedrock list-trusted-access-programs`); "eligible" means you can enroll, "requestable" means you need approval first. The first two programs are in public preview for customers already on Anthropic's EFS zero data retention. **Enterprise Frontier Safeguards** keeps retained prompts and responses in your own S3 bucket, encrypted with your KMS key. **Enterprise Data Controls** keeps them in Amazon-managed storage instead. Both turn ZDR off for the accounts or projects you enroll, set the retention mode to `aws_review`, and raise flagged content as review cases. Under EFS, these arrive as files in `review-cases/`, and you must answer within 7 days. Covered models are Claude Fable 5–5.2 and Mythos 5–5.2, plus Opus 5.5 and Sonnet 5.5 used through the Cyber Verification Program, called through `bedrock-runtime` on US, EU or Global CRIS profiles. You need a key and bucket in every Region you call from. AWS and Anthropic charge nothing extra beyond S3 and KMS.
**Why it matters:** This is how Fable and Mythos stay usable for teams that can't let a vendor keep their data. It is also a new outage path: Bedrock stops serving covered models 24 hours after it loses access to your key or bucket, so monitor both. Preview only: no console yet, no condition keys to enforce it with SCPs, and test traffic only. The Claude API side is covered in [LLM APIs](../../build/llm-apis/README.md).
Sources: [AWS ML blog](https://aws.amazon.com/blogs/machine-learning/introducing-the-amazon-bedrock-trusted-access-api-with-anthropics-enterprise-frontier-safeguards-and-enterprise-data-controls/) · [Bedrock user guide: EFS and EDC](https://docs.aws.amazon.com/bedrock/latest/userguide/anthropic-efs-enterprise-data-controls.html) · Added: 2026-11-25

### OpenAI GPT-6.2 Astra and GPT-6.2 Sol on Bedrock · 2026-11-17
AWS made both models generally available on Bedrock. Astra is the frontier reasoning model and has an Ultrafast mode for latency-sensitive calls. Sol targets recurring coding and agentic work where speed and cost per task matter. The model cards give the details:

| | Astra | Sol |
|---|---|---|
| `bedrock-mantle` (in-Region, us-east-1 only) | `openai.gpt-6.2-astra` | `openai.gpt-6.2-sol` |
| `bedrock-runtime` Geo profile | `us.openai.gpt-6.2-astra` | `us.openai.gpt-6.2-sol` |
| `bedrock-runtime` Global profile | `global.openai.gpt-6.2-astra` | `global.openai.gpt-6.2-sol` |
| Global price ≤272K context (in / cached / out per 1M) | $8 / $0.40 / $40 | $2 / $0.10 / $10 |
| Geo / in-Region price ≤272K context | $8.80 / $0.44 / $44 | $2.20 / $0.11 / $11 |
| Service tiers | Standard, Ultrafast (`service_tier: "ultrafast"`) | Standard |

Both have a 1.05M context and 128K output. `bedrock-runtime` has no in-Region option; Geo sources are us-east-1/2, us-west-1/2, ca-central-1 and ca-west-1. Converse on `bedrock-runtime` rejects `document` blocks, so use `input_file` with the Responses API. Output tokens count 10× against quota.
**Why it matters:** You can run OpenAI's newest models behind your existing Bedrock IAM, logging and billing. Re-run your evals before you switch any GPT-6 workloads.
Sources: [AWS What's New](https://aws.amazon.com/about-aws/whats-new/2026/11/openai-gpt-6-2-astra-sol-amazon-bedrock/) · [Model card: GPT-6.2 Astra](https://docs.aws.amazon.com/bedrock/latest/userguide/model-card-openai-gpt-6-2-astra.html) · [Model card: GPT-6.2 Sol](https://docs.aws.amazon.com/bedrock/latest/userguide/model-card-openai-gpt-6-2-sol.html) · Added: 2026-11-19 · Updated: 2026-11-20

### Claude Fable 5.2 on Bedrock · 2026-11-09
Available through **US Geo and Global cross-region inference profiles**; the Global profile ID is `global.anthropic.claude-fable-5-2`. The `bedrock-runtime` endpoint supports server-side compaction (betas `compact-2026-09-04`, `compact-2026-01-12`). Classmethod reports Global pricing 20% below Fable 5.1. The AWS ML blog (as summarised) says zero data retention is offered through 2027-06-30. Earliest EOL is 2027-11-09.
**Why it matters:** You can use the top Anthropic model inside your AWS account boundary and IAM. Call it with the Converse API or the Anthropic Messages API on Bedrock.
Sources: [Bedrock model card](https://docs.aws.amazon.com/bedrock/latest/userguide/model-card-anthropic-claude-fable-5-2.html) · [Classmethod hands-on](https://dev.classmethod.jp/en/articles/bedrock-claude-fable-5-2/) · [TechBytes summary of AWS ML blog](https://techbytes.app/posts/introducing-claude-fable-52-on-aws/) · Added: 2026-11-18

### Bedrock Guardrails: contextual grounding checks, Standard tier · Oct 2026
Checks that answers stay faithful to their retrieved sources. The new Standard tier costs the same as Classic.
Source: [AWS ML blog: what landed in October 2026](https://aws.amazon.com/blogs/machine-learning/icymi-what-landed-for-ai-builders-in-october-2026/) · Added: 2026-11-18

---

## 🤖 Amazon Bedrock AgentCore: the agent platform

A managed platform for running agents in production: **Runtime** (serverless agent hosting), **Gateway** (tools, MCP and model routing), **Memory**, **Identity**, **Policy**, **Evaluations**, **Observability** and the **Agent Registry**. It is framework-agnostic and runs Strands, LangGraph, CrewAI, Spring AI and others.

| Date | What shipped | Why it matters |
|---|---|---|
| Nov 2026 (in the window) | **Agent Registry search types:** `searchType` takes `KEYWORD`, `SEMANTIC` or `HYBRID` (default); keyword search pages up to 1,000 results with `nextToken`. The Runtime identity service-linked policy now scopes the `GetWorkloadAccessToken*` actions to all resources | Use `KEYWORD` for exact tool or agent names, where semantic search can miss ([release notes](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/release-notes.html)) |
| 2026-11-23 | **Runtime Instances in AWS GovCloud (US-West):** instances, volumes and session data stay in GovCloud | Agents on EC2-backed sessions for regulated US workloads |
| 2026-11-20 | **Gateway streaming response interceptors:** set `responseInterceptionMode: STREAM` and your interceptor Lambda gets each batch of SSE or event-stream events (batch size via `responseStreamingConfiguration.maxEventsPerInvocation`) to redact, change or drop | PII filtering on model output without losing streaming |
| 2026-11-20 | **Runtime Instances on EC2 G7** (`g7.2xlarge`–`g7.48xlarge`, NVIDIA RTX PRO 4500 Blackwell): add them to the capacity provider's allowed types; drivers are installed, sessions up to 14 days; 8 Regions incl. ap-southeast-2 | A GPU per agent session for vision models or rendering |
| 2026-11-20 | **Agent Registry:** verify a domain and publish agents and tools for discovery by any AWS-authenticated user (no extra charge for now); new WebBotAuth record type that works with WAF Bot Control | Check who owns an agent before yours connects to it |
| 2026-11-21 | **Web Search:** Spanish, French, German, Italian, Japanese and non-US English, plus an optional `country` field (ISO 3166-1 alpha-2) to bias sources; AgentCore in 6 Regions incl. Sydney, Bedrock in US Regions | Local sources for non-US users with no code change |
| 2026-11-19 | **Runtime Instances:** nested virtualization (KVM) lets agents run their own VMs, such as an Android emulator, inside a session; a separate opt-in lets agents on Instances run with elevated privileges (off by default; read the security considerations first) | Mobile-app testing and VM-based sandboxes inside managed agent sessions |
| 2026-11-19 | **Agentic payments:** agents can find and buy selected AWS Marketplace products and pay per request in USD over x402 through AgentCore payments, billed to the AWS account; discovery via the Gateway Marketplace connector (`connectorId: "aws-marketplace"`) | Agents can buy paid tools and data under spending limits; set limits and approved sellers before enabling |
| Nov 2026 | **Governance:** Organizations resource control policies cover AgentCore; Gateway `bedrock-agentcore:InboundJwtClaim/*` condition keys filter `InvokeGateway` by `iss`, `sub`, `aud`, `scope`, `client_id`. **Runtime V2:** `s3BucketMount` mounts your S3 bucket (use `{runtimeSessionId}` in the prefix for per-session folders). **Agent Registry:** stores skill packages (`.zip` with `SKILL.md`), synced from S3 or GitHub, with keyword, semantic or hybrid search | Org-wide limits, per-caller JWT rules and versioned shared skills |
| 2026-11-17 | **Memory:** automatic **full session summaries** for every memory using the summary strategy (existing sessions included), stored as long-term records you can filter by type; short-term event retention up to **10 years** (was 1 year) | Long-lived assistants keep history without your own archive store |
| Nov 2026 | **Evaluations:** managed dataset-evaluation batch jobs and Insights via the `Builtin.FailureAnalysis` evaluator (enable the Insight Store first). **Gateway:** `domainOverride` for JWT gateways behind a proxy. **Identity:** OAuth 2.0 discovery URLs for non-OIDC authorization servers (2026-11-13) | Batch regression evals and failure clustering without your own pipeline |
| Nov 2026 | **Web search:** the first 5,000 queries per month are free for each account, shared across an organization (not GovCloud). A new `InvokeWebSearch` API lets apps search without a gateway, in six Regions | Cheap grounding for agents with no third-party search key |
| Nov 2026 | **Harness:** IAM authentication to remote MCP servers. Managed defaults now run on the Strands Harness (recommended model: Claude Opus 5 in commercial Regions, plus summarization, prompt caching and built-in tools) | Call IAM-protected MCP servers without separate credentials. Explicit settings still override the defaults |
| Nov 2026 | **Runtime:** MCP protocol version 2026-07-28, with HTTP status codes aligned to the spec. V2 also gets 10 GB container images (up from 2 GB), a build warmup hook (`hooksConfiguration`) and more Regions | Implement `GET /ping` on MCP servers for reliable health checks |
| 2026-11-12 | **Runtime V2 becomes the default for new runtimes** (existing ones stay on V1 until you set `platformVersion` to V2). Sessions scale to 8 vCPU/32 GB; AWS reports P75 starts under 2 s on a 2 GB image, versus 29.7 s before *(self-reported)*. Also adds committed-baseline billing and dynamic filesystem mounts | Faster cold starts and predictable cost for long-running agents, but check IaC that assumed V1 |
| Nov 2026 | **Gateway Web Answer connector** (GA in us-east-1): cited web answers as a built-in tool | Web search without bringing your own search API |
| Nov 2026 | Runtime: higher concurrent-connection limit for V2; new `OverheadLatency` CloudWatch metric | Separates platform latency from your agent's latency |
| Oct 2026 | **AgentCore CLI 1.0 GA**: faster start-up, consistent commands | Scriptable deploys and CI |
| Oct 2026 | **Gateway model fallback** + Bedrock `InvokeModel` wire format on `/inference` | Agents keep working when a model is throttled |
| 2026-09-18 | **Runtime V2:** snapshot-based starts, memory reclamation | Faster cold starts |
| Sep 2026 | Evaluations support **TypeScript** frameworks as well as Python | Eval TS agents natively |
| Aug 2026 | **Amazon Agent Registry GA** (auto-detection, CMK encryption) | A catalogue of every agent in the organisation |

Sources: [AgentCore release notes](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/release-notes.html) · [What's New: Instances in GovCloud](https://aws.amazon.com/about-aws/whats-new/2026/11/agentcore-runtime-instances-govcloud) · [What's New: Marketplace agentic payments](https://aws.amazon.com/about-aws/whats-new/2026/11/marketplace-agentic-payments-agentcore/) · [What's New: Memory full session summaries](https://aws.amazon.com/about-aws/whats-new/2026/11/amazon-bedrock-agentcore-memory-full-session-summaries/) · [What's New: 10-year retention](https://aws.amazon.com/about-aws/whats-new/2026/11/amazon-bedrock-agentcore-memory-10-year-retention/) · [What's New: OAuth 2.0 discovery](https://aws.amazon.com/about-aws/whats-new/2026/11/bedrock-agentcore-oauth2-discovery/) · [What's New: next-generation runtime is the default](https://aws.amazon.com/about-aws/whats-new/2026/11/new-agentcore-runtime-default/) · [Unite.AI on Runtime V2 expansion](https://www.unite.ai/?p=516062) · [AWS ML blog, October recap](https://aws.amazon.com/blogs/machine-learning/icymi-what-landed-for-ai-builders-in-october-2026/) · Added: 2026-11-18

**JVM note:** Spring AI has an **AgentCore SDK** for deploying Spring AI agents to AgentCore Runtime (1.0 in April 2026). ([This Week in Spring, 28 Apr 2026](https://spring.io/blog/2026/04/28/this-week-in-spring-april-28-2026))

---

## 🧵 Strands Agents (AWS's open-source agent SDK)

### Strands Decider v2 + Box CLI · 2026-11-23 🆕
**Decider v2** is a family of five open "decision models" (Apache-2.0, fine-tuned from Gemma 4 E2B, E4B, 12B, 26B-A4B and 31B) that pick one of a fixed set of answers in a single forward pass and return calibrated confidence: which model or tool to use, whether tool arguments look right, whether an answer is grounded, which team owns a ticket. They are not for free-text generation. Strands reports the 31B averaging 82.1 on six text benchmarks (v1 26B-A4B: 70.0), and a Haiku 5.5 → Sonnet 5.5 router solving 94% as many tasks as Sonnet alone at 44% of the cost *(self-reported)*. Weights are under `StrandsAgents` on Hugging Face (e.g. `StrandsAgents/strands-decider-E4B-gemma4-v2-2611`); the Harness SDK exposes them as decision models. Also launched: the **Strands Box CLI**, which sandboxes Claude Code, Codex or Kiro CLI under Dogwood policies (see [Agent infrastructure](../../architecture/agent-infrastructure/README.md)).
```bash
pip install strands-decider
strands-decider serve StrandsAgents/strands-decider-E4B-gemma4-v2-2611 --port 8000   # POST /v1/systemone
```
**Why it matters:** Cheap, self-hostable routing and guard checks inside an agent loop, instead of asking a frontier model to choose. Validate the router's cost/quality trade-off on your own traffic.
Sources: [Strands blog: Decider v2](https://strandsagents.com/blog/introducing-strands-decider-v2/) · [SiliconANGLE](https://siliconangle.com/2026/11/23/aws-is-making-ai-agents-more-decisive-and-secure-with-its-latest-strands-updates/) · Added: 2026-11-24

### Strands Harness SDK + Strands harness
A model-driven agent SDK for **Python and TypeScript** (Apache-2.0), now described as an "agent harness" with behavioural middleware and sandboxed execution. **Strands harness** (released 2026-09-21) is a ready-made, general-purpose agent built on the SDK. Latest versions: `strands-agents` 1.67.0 (2026-11-25), `@strands-agents/sdk` 1.26.0 (2026-11-19), `strands-harness` 0.5.0 (2026-11-23) and `strands-decider` 0.4.0 (2026-11-20), checked on PyPI and npm on 2026-11-26.
```bash
pip install strands-agents strands-agents-tools   # SDK
pip install strands-harness                       # assembled agent
npm install @strands-agents/sdk                   # TypeScript
```
**Why it matters:** It is the shortest path to agents on Bedrock and AgentCore, but it is model-agnostic and runs anywhere.
Sources: [Developers Digest (verified install commands)](https://www.developersdigest.tech/agent-frameworks/strands-agents) · [Carly: what is Strands](https://www.usecarly.com/blog/strands-agents/) · [PyPI](https://pypi.org/project/strands-agents/) · Added: 2026-11-18

### Strands Labs
Experimental projects: **AI Functions**, which generate code at runtime from natural-language specs, and **Strands Robots**, which connects LLMs to hardware through vision-language-action models.
Source: [The New Stack](https://thenewstack.io/aws-strands-labs-launch/) · Added: 2026-11-18

---

## 🛠️ Kiro (AWS's agentic IDE, replacing Q Developer)

### Kiro Enterprise: GPT 6.2 Astra preview and credit-pool limits · 2026-11-25 🆕
GPT 6.2 Astra is starting to roll out in preview to Kiro Enterprise organisations, with limited access. It has a 1M context window, runs inference in the US only, and costs a 7.2× credit multiplier, rising to 14.4× for requests over 272K tokens. Admins enable it through model governance. Separately, admins can now cap pooled credits per user per billing cycle with `credit_pool.usage_limit` in Controls, set on the profile (default), a group or a user. A user's own limit wins, then the highest group limit, then the profile's. An account-wide overage switch sits in the same Controls. Enterprise Management is in preview in `us-east-1` and `eu-central-1`. Kiro is also now in scope for AWS SOC reports.
**Why it matters:** one long Astra session can burn a large share of a team's pool, so set limits before you turn the model on.
Sources: [GPT 6.2 Astra for Enterprise](https://kiro.dev/changelog/models/gpt-6-2-astra-for-enterprise/) · [Credit pooling limits and overages](https://kiro.dev/changelog/general/enterprise-management-credit-pooling-controls/) · [SOC scope](https://kiro.dev/changelog/general/kiro-is-now-in-scope-for-aws-soc-reports/) · Added: 2026-11-27

### Kiro CLI 3.6.0: SubagentStop hook and guided compaction · 2026-11-24 🆕
In V3 sessions, a new **SubagentStop** hook runs when a dispatched subagent finishes and can send it one more instruction before its result goes back. Hook output over 3,000 characters is saved to a file, and the agent gets the start of the output plus the file path. `/compact <instructions>` shapes a single compaction, for example telling it to keep migration decisions. The release also adds conversation recaps, notification controls, managed V2 controls and an all-users Windows installer.
**Why it matters:** A SubagentStop hook can make each subagent run its checks (tests, lint) before it reports back, instead of relying on the parent agent to remember.
Sources: [Kiro CLI 3.6 changelog](https://kiro.dev/changelog/cli/3-6/) · [Hook types](https://kiro.dev/docs/hooks/types/#subagent-stop-cli-v3-only) · Added: 2026-11-25

### Kiro cloud sessions can reach your VPC; Kiro for VS Code · 2026-11-19 → 11-20 🆕
Admins can connect Kiro cloud sessions to private resources in an Amazon VPC (Enterprise plan with IAM Identity Center profiles in `us-east-1`; the profile must use Controls). Also new: IDE 1.5.11 with Remote SSH and Dev Containers, and Kiro for VS Code 1.5.0 (details in [Coding agents](../../build/coding-agents/README.md)).
**Why it matters:** Cloud agents can work against private databases and services without exposing them publicly.
Source: [Kiro changelog](https://kiro.dev/changelog/) · Added: 2026-11-21

### Kiro IDE 1.4.236: permission hook and GitLab installs · 2026-11-18 🆕
The IDE gets the CLI's Permission Request hook (answer approval prompts from a script), shows final arguments after Pre Tool Use hooks rewrite them, and supports one organization IdP sign-in across HTTP MCP servers. Powers and skills can be installed from public GitLab URLs; self-hosted GitLab hosts must be listed in `kiroAgent.powers.trustedGitLabHosts`.
**Why it matters:** IDE and CLI users can now share one hook-based policy and one MCP sign-in.
Source: [Kiro IDE 1.4.236 changelog](https://kiro.dev/changelog/ide/1-4-236/) · Added: 2026-11-20

### Kiro CLI 3.4–3.5: permission hooks and org sign-in for MCP · 2026-11-17
**CLI 3.4.0** (2026-11-16): in V3 sessions, a `PreToolUse` hook can return `updatedInput` to rewrite a tool call's inputs. A new `PermissionRequest` hook can answer `allow` or `deny` to permission prompts, and a deny from any hook overrides an allow. **CLI 3.5.0** (2026-11-17): MCP servers set to use organization sign-in share one IdP login (`kiro-cli mcp idp setup`, then sign in once from `/mcp`). Admins can set the portal that `kiro-cli login` opens with `auth.portalUrl`, or with the `AuthPortalUrl` policy. Also on 2026-11-16: IDE 1.4.215 adds conversation forking and cloud sessions in Frankfurt, and Kiro Web gains a terminal.
**Why it matters:** You can now enforce team policy on tool calls in scripts, for example denying writes outside the repo, and stop separate browser logins for every internal MCP server.
Sources: [Kiro CLI 3.4 changelog](https://kiro.dev/changelog/cli/3-4/) · [Kiro CLI 3.5 changelog](https://kiro.dev/changelog/cli/3-5/) · [Kiro changelog](https://kiro.dev/changelog/index) · Added: 2026-11-19

### Kiro bots, GA in Kiro Crew · 2026-11-05
Named, long-running agents, each with its own memory, chat and sessions. They can run sessions in parallel, follow schedules and work within per-bot permissions.
Source: [Let's Data Science](https://letsdatascience.com/news/aws-launches-kiro-bots-for-coordinating-parallel-ai-coding-a-e78ec0ae) · Added: 2026-11-18

### Kiro CLI 3.0 + October changes
November brought Kiro CLI 3.0.0–3.1.0. October added a **local command sandbox** (off by default; it blocks network access and stops the agent reading `~/.aws/credentials`), Memory, Workflows, Workspace trust and Markdown Review. Claude Opus 5.5 and Sonnet 5.5 (1M context) are now in Kiro, including GovCloud, and **Claude Sonnet 4 reached end of life in Kiro on 2026-10-14**.
**Why it matters:** Turn on the sandbox for any repo you don't fully trust.
Sources: [Kiro changelog](https://kiro.dev/changelog/dev-server-and-spec-workflows/) · [AWS Japan SA deck, Oct](https://speakerdeck.com/inariku/kiro-update-2026-10-en) · [Nov deck](https://speakerdeck.com/inariku/kiro-update-2026-11-en) · Added: 2026-11-18

## 🖥️ Self-hosted models on AWS

### Lambda durable functions can drive Lambda MicroVMs (developer preview) · 2026-11-25 🆕
A new extension to the AWS Durable Execution SDK (TypeScript and Python) adds durable operations that run tasks in Lambda MicroVMs, one per task or as a session where tasks share files and memory. The durable function owns the MicroVM lifecycle: it checkpoints each task, retries failures, refreshes MicroVM tokens and can run several MicroVMs in parallel, triggered from SQS or EventBridge. An optional worker library inside your MicroVM image receives tasks and reports results. AWS says not to use the preview in production.
**Why it matters:** it is a serverless way to run agent-generated or untrusted code in VM-isolated sandboxes, with workflows that can last up to a year. Compare it with the sandboxes in [Agent infrastructure](../../architecture/agent-infrastructure/README.md) before you build your own orchestration.
Source: [AWS What's New](https://aws.amazon.com/about-aws/whats-new/2026/11/lambda-durable-microvm/) · Added: 2026-11-27

### Amazon Transcribe Turbo (preview): semantic turn-taking and per-turn hints for voice agents · 2026-11-25 🆕
A new speech-to-text model. Streaming is in preview in us-east-2 for English, Portuguese, French, Italian, German and Spanish; English batch is GA in most Regions. For voice agents, `EndOfTurnDetection` decides a caller has finished from their words and prosody rather than silence alone, and a `ConfigureEvent` can send hints before each turn (menu options, expected names, the entity type you expect). Both are English-only at launch and cost nothing extra. AWS reports about 14% lower word error rate in English, about 615 ms end-of-turn response with a 5% interruption rate, and menu routing up from 87% to 97% with hints *(self-reported)*.
**Why it matters:** cutting callers off mid-sentence is the most common voice-agent complaint, and this fixes it at the speech-to-text layer without changing your agent. More voice tooling: [Voice & multimodal](../../build/voice-and-multimodal/README.md).
Source: [AWS What's New](https://aws.amazon.com/about-aws/whats-new/2026/11/transcribe-turbo-preview/) · Added: 2026-11-27

### CloudWatch Container Insights: built-in vLLM, SGLang, KServe and Ray dashboards on EKS · 2026-11-20 🆕
Turning on OTel Container Insights for EKS (add-on/Helm chart 8.0.0 or later) now also monitors vLLM, SGLang, KServe, Ray, Karpenter, KEDA and Knative Serving with no Prometheus or Grafana to run. For model servers you get queued requests, time to first token and KV-cache usage, tagged by pod, workload and node. Metrics are billed at the EKS OpenTelemetry ingestion rate ($0.08 per GB).
**Why it matters:** Quick TTFT and KV-cache visibility for self-hosted LLMs on EKS, useful alongside the ElastiCache KV tier below. Estimate ingestion volume first on busy clusters.
Source: [AWS What's New](https://aws.amazon.com/about-aws/whats-new/2026/11/cloudwatch-eks-kubernetes-tools/) · Added: 2026-11-24

### ElastiCache distributed KV caching for vLLM/SGLang + an agent skill to set it up · 2026-11-18 → 11-21 🆕
ElastiCache for Valkey can now act as a shared KV-cache tier beside your GPU fleet (GA 2026-11-18): engines such as vLLM, SGLang and TensorRT-LLM connect through the open-source LMCache connector with a config change, so any server can reuse prefill state across sessions, re-routes and server failures. AWS claims up to 40% lower inference cost and up to 80% lower time to first token *(self-reported)*. On 2026-11-21 AWS added a **distributed KV caching skill** to the Agent Toolkit for AWS: it checks fit first (EFA-capable GPUs such as p5, LMCache 0.5.8rc1+, vLLM 0.11.1+ or SGLang 0.5.13+, Valkey 9.1+ on `cache.i8ge.48xlarge`), estimates savings from your own traffic with the free KVTrace tool, then configures the connector.
**Why it matters:** Long-context agents that come back after a break stop paying for full prefill on whichever GPU picks them up. Check the multi-tenant guidance first: a shared cache can leak via timing, so isolate tenants or add a tenant ID to the KV hash.
Sources: [AWS Database blog: announcement](https://aws.amazon.com/blogs/database/announcing-distributed-kv-caching-for-self-hosted-llms-with-amazon-elasticache/) · [AWS ML blog: the agent skill](https://aws.amazon.com/blogs/machine-learning/cut-self-hosted-llm-cost-and-latency-with-the-distributed-kv-caching-agent-skill/) · [Skill on GitHub](https://github.com/aws/agent-toolkit-for-aws/tree/main/skills/specialized-skills/database-skills/distributed-kv-caching) · Added: 2026-11-23

### SageMaker HyperPod Global Inference Gateway: one endpoint across clusters and Regions · 2026-11-20 🆕
A SageMaker-managed gateway that routes requests across every HyperPod cluster you register (same or other Regions), choosing by KV-cache headroom, queue depth, proximity and error rate, and failing over automatically; a failed request is retried once on another cluster unless it has started streaming. You enable `spec.globalRouting` in each cluster's `InferenceGatewayConfig`, then call `CreateGlobalInferenceGateway`. Calls are SigV4/IAM-signed (`sagemaker:InvokeGlobalInferenceGateway`, plus `...WithResponseStream` for streaming) and reach clusters only over PrivateLink. 13 Regions, including Sydney.
**Why it matters:** Cross-Region overflow and failover for self-hosted LLMs on HyperPod without your own load balancers or DNS. Note that each published cluster's Network Load Balancer is billed even when no gateway uses it.
Source: [AWS ML blog](https://aws.amazon.com/blogs/machine-learning/introducing-amazon-sagemaker-hyperpod-global-inference-gateway-one-endpoint-across-regions-and-clusters/) · Added: 2026-11-23

### Vector filters: S3 Vectors 40 KB metadata, DynamoDB `SearchVectors` filters · 2026-11-20 🆕
S3 Vectors raises filterable metadata per vector from 2 KB to 40 KB (default for new vector buckets; existing indexes need `UpdateIndexMode` to switch to enhanced index mode; no extra cost). DynamoDB `SearchVectors` filters now accept range comparisons and `BETWEEN` on numbers, `IN`, `attribute_exists`/`attribute_not_exists` and `AND`/`OR`/`NOT`, applied during the search so every result matches.
**Why it matters:** Permission, tenant and date filters can live in the vector store instead of post-filtering, which also fixes short result pages. Patterns: [RAG & retrieval](../../architecture/rag-and-retrieval/README.md).
Source: [S3 Vectors 40 KB metadata](https://aws.amazon.com/about-aws/whats-new/2026/11/amazon-s3-vectors-raises-filterable-metadata-40kb-per-vector/) · [DynamoDB vector filters](https://aws.amazon.com/about-aws/whats-new/2026/11/dynamodb-vector-filters/) · Added: 2026-11-22

### Amazon OpenSearch Memory GA: managed cross-session memory for agents · 2026-11-18 🆕
A serverless memory store on OpenSearch Serverless: you write conversation turns as events (`CreateEvent`), it derives facts, preferences and summaries, and you recall them with hybrid keyword + semantic `SearchMemories` (or search raw turns with `SearchEvents`). Data lives in a *space*, scoped by actor and optional session ID. Boto3 client `opensearchmemory` (boto3 1.44.4 or later); extraction and embedding are included in the price. Regions: us-east-1, us-west-2, ap-northeast-1, eu-central-1. An AWS MCP server and skills for Kiro, Claude Code and Codex are offered.
**Why it matters:** An alternative to AgentCore Memory if your retrieval already runs on OpenSearch. Not yet in Sydney. Patterns: [Context engineering & memory](../../architecture/context-and-memory/README.md).
Source: [AWS Big Data blog](https://aws.amazon.com/blogs/big-data/introducing-amazon-opensearch-memory-persistent-memory-for-ai-agents/) · Added: 2026-11-23

### Amazon Textract Insights GA: schema-driven extraction with page grounding · 2026-11-20 🆕
A new asynchronous Textract API (`StartDocumentInsights`): you describe fields in a JSON Schema "blueprint" (AWS ships public ones for W-2, 1040, passports and others), submit a single document or a mixed packet of up to 3,000 pages from S3, and it splits the packet, matches each part to a blueprint and returns every value with a confidence score plus page and bounding box. Priced per page; PDF, PNG, JPEG, TIFF; English, French, German, Italian, Portuguese and Spanish. It uses cross-Region inference within your geography. Textract Core also gets better tables and handwriting and 40 languages, with no API change.
**Why it matters:** Grounded, auditable extraction for document pipelines and RAG ingestion without building OCR, splitting and LLM prompting yourself. Set your auto-accept threshold on a sample of your own documents. More on parsers: [RAG & retrieval](../../architecture/rag-and-retrieval/README.md).
Source: [AWS ML blog](https://aws.amazon.com/blogs/machine-learning/announcing-amazon-textract-insights-verifiable-generative-ai-for-documents/) · Added: 2026-11-23

### SageMaker AI inference routers: cross-Region failover for your own endpoints · 2026-11-18 🆕
An inference router is a Regional resource you call instead of an endpoint; it sends each request to a healthy endpoint or inference component for the same model, in another Region or account, preferring local destinations and shifting traffic when they throttle or return 5xx. The response header `X-Amzn-SageMaker-Invoked-Routing-Reason` says where it went. Limits: no response streaming, 60 s per real-time request (use `InvokeInferenceRouterAsync` for longer), 5 routers per account per Region; calls use the `sagemaker-inference-router-runtime` client. No extra charge.
**Why it matters:** Bedrock-style cross-Region failover for self-hosted LLMs; only add destinations where your data may go.
Source: [SageMaker docs: inference router](https://docs.aws.amazon.com/sagemaker/latest/dg/inference-router.html) · Added: 2026-11-21

---

## 🔌 AWS MCP servers

| Option | What it is | Use when |
|---|---|---|
| **AWS MCP Server (managed)**, GA 2026-05-06 | A remote MCP server giving agents authenticated access to AWS APIs through a few tools. Auth is IAM + SigV4 through a local proxy (`pip install awslabs-mcp-proxy`). IAM condition keys tell MCP-initiated calls apart from human ones. | The default for general AWS work from Claude Code, Codex, Cursor or Kiro |
| **[awslabs/mcp](https://github.com/awslabs/mcp)** (open source, 45–60+ servers) | Focused servers for CloudWatch, IAM, EKS, CDK, Bedrock Knowledge Bases, Cost Explorer and more | You need a specialised capability, such as CloudWatch anomaly analysis |
| **Agent Toolkit for AWS** | AWS skills and plugins for coding agents | Teaching agents AWS best practices |

```bash
uvx awslabs.cloudwatch-mcp-server@latest
uvx awslabs.iam-mcp-server@latest
```
**Guardrail:** give the MCP role read-only IAM permissions first, and use the MCP condition keys to block mutating calls that an agent starts.
Sources: [MCP Directory: AWS MCP Server guide](https://mcp.directory/blog/aws-mcp-server-complete-guide-2026) · [dev.to: CloudWatch + IAM via MCP](https://dev.to/jangwook_kim_e31e7291ad98/aws-mcp-server-ga-practical-guide-connecting-cloudwatch-iam-to-your-ai-coding-agent-3d79) · [Developers Digest](https://www.developersdigest.tech/mcp-servers/aws-mcp-server) · Added: 2026-11-18

### AWS WAF AI Security: find and guard LLM, MCP and A2A endpoints · 2026-11-23 🆕
Two pieces (missed earlier). The API Gateway **API Portal** finds AI endpoints across your AWS Organization from traffic logs and service configuration, including undocumented public MCP servers, with no agents or log forwarding; it covers endpoints behind API Gateway, Application Load Balancers and CloudFront. The new **AWS WAF AI Security** managed rule group blocks malformed MCP and A2A messages. With content inspection turned on, it calls the Bedrock Guardrails `InvokeGuardrailsCheck` API to check requests for prompt injection, jailbreaks and harmful content, and responses for sensitive data. AI Security runs in us-east-1, us-east-2, us-west-2, London, Stockholm, Tokyo and Sydney; the API Portal is in 32 Regions. WAF fees apply, and Bedrock bills the inspection calls separately.
**Why it matters:** A quick way to find shadow MCP servers your teams exposed and put a protocol-aware filter in front of them without writing rules. Guardrails calls on every request add cost and latency, so measure both before you turn on content inspection everywhere. Patterns: [AI security](../../architecture/security/README.md).
Source: [AWS What's New](https://aws.amazon.com/about-aws/whats-new/2026/11/waf-ai-endpoint-discovery-protection/) · Added: 2026-11-26

### Amazon Cognito: client ID metadata documents (CIMD) for MCP clients · 2026-11-19 🆕
A client can use an HTTPS URL as its client ID and publish a JSON metadata document there; Cognito validates it at sign-in, and CIMD policies map URL patterns to your app clients, limiting scopes and grant types to what both allow. Needs the Essentials or Plus plan.
**Why it matters:** An MCP server behind Cognito can accept AI assistants by allow-listing their metadata URL instead of registering an app client per assistant.
Source: [AWS What's New](https://aws.amazon.com/about-aws/whats-new/2026/11/cognito-client-id-metadata-documents/) · Added: 2026-11-21

**Security:** `awslabs.document-loader-mcp-server` 1.0.10–1.0.20 has a path traversal when `DOCUMENT_BASE_DIR` is unset (CVE-2026-130901); upgrade to 1.0.21 or later. ([AWS bulletin 2026-195](https://aws.amazon.com/security/security-bulletins/2026-195-aws/))

---

## 🗺️ Picking an AWS path

```
"I want Claude/frontier models inside my AWS account"   → Bedrock (Converse / Messages API, CRIS profiles)
"I want to host agents without running servers"         → AgentCore Runtime (+ Gateway for tools, Memory, Policy)
"I'm writing the agent code"                            → Strands (Py/TS) · Spring AI + AgentCore SDK (JVM) · LangGraph
"My coding agent should operate my AWS account"         → AWS MCP Server (managed) + awslabs servers, read-only IAM first
"Team AI IDE with AWS SSO and billing"                   → Kiro (replacing Q Developer)
```

## 🔗 Bookmarks
[What's New: AI/ML](https://aws.amazon.com/about-aws/whats-new/) · [AWS ML blog monthly "ICYMI"](https://aws.amazon.com/blogs/machine-learning/) · [AgentCore release notes](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/release-notes.html) · [Kiro changelog](https://kiro.dev/changelog/) · [Strands](https://strandsagents.com)
