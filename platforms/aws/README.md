# AWS for AI engineering

_Last updated: 2026-11-21_

> Everything on AWS that matters to AI engineers: Bedrock models, AgentCore (the agent runtime platform), Strands Agents, Kiro, AWS MCP servers, and how they connect to Spring, Python and TypeScript apps. **re:Invent 2026 runs 30 Nov – 4 Dec**, so expect a large wave of launches.

## ⚡ Action items & dates

| When | What | Do this |
|---|---|---|
| **2026-11-30 → 12-04** | **AWS re:Invent 2026**, Las Vegas | Watch the keynotes, then read the daily digests that week for the developer-relevant launches. ([event summary](https://ecorpit.com/aws-reinvent-2026-keynotes-what-to-watch/)) |
| now | Amazon Q Developer is being replaced by **Kiro**: new sign-ups blocked since 2026-05-15, end of support for plugins and subscriptions on **2027-04-30** | Plan the migration of IDE plugins and team subscriptions to Kiro. ([Enterprise DNA](https://enterprisedna.co/resources/news/aws-kiro-replaces-amazon-q-developer-spec-driven-2026)) |
| now (since 2026-11-12) | New **AgentCore runtimes default to the next-generation runtime (V2)** in 19 Regions; existing runtimes stay on V1 until you move them | Set `platformVersion` explicitly in your IaC: `V2` to migrate an existing runtime on update, `V1` to keep a new one on the old platform. ([What's New](https://aws.amazon.com/about-aws/whats-new/2026/11/new-agentcore-runtime-default/)) |
| if adopting the managed AWS MCP Server | Overlapping tools with `aws-api-mcp-server` and `aws-knowledge-mcp-server` | Remove those two from your MCP config, because duplicate tool names confuse agents. ([dev.to guide](https://dev.to/jangwook_kim_e31e7291ad98/aws-mcp-server-ga-secure-aws-api-access-for-ai-agents-2bia)) |

---

## 🧠 Amazon Bedrock: models

### OpenAI GPT-6.2 Astra and GPT-6.2 Sol on Bedrock · 2026-11-17 🆕
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

### Claude Fable 5.2 on Bedrock · 2026-11-09 🆕
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

Sources: [AgentCore release notes](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/release-notes.html) · [What's New: Marketplace agentic payments](https://aws.amazon.com/about-aws/whats-new/2026/11/marketplace-agentic-payments-agentcore/) · [What's New: Memory full session summaries](https://aws.amazon.com/about-aws/whats-new/2026/11/amazon-bedrock-agentcore-memory-full-session-summaries/) · [What's New: 10-year retention](https://aws.amazon.com/about-aws/whats-new/2026/11/amazon-bedrock-agentcore-memory-10-year-retention/) · [What's New: OAuth 2.0 discovery](https://aws.amazon.com/about-aws/whats-new/2026/11/bedrock-agentcore-oauth2-discovery/) · [What's New: next-generation runtime is the default](https://aws.amazon.com/about-aws/whats-new/2026/11/new-agentcore-runtime-default/) · [Unite.AI on Runtime V2 expansion](https://www.unite.ai/?p=516062) · [AWS ML blog, October recap](https://aws.amazon.com/blogs/machine-learning/icymi-what-landed-for-ai-builders-in-october-2026/) · Added: 2026-11-18

**JVM note:** Spring AI has an **AgentCore SDK** for deploying Spring AI agents to AgentCore Runtime (1.0 in April 2026). ([This Week in Spring, 28 Apr 2026](https://spring.io/blog/2026/04/28/this-week-in-spring-april-28-2026))

---

## 🧵 Strands Agents (AWS's open-source agent SDK)

### Strands Harness SDK + Strands harness 🆕
A model-driven agent SDK for **Python and TypeScript** (Apache-2.0), now described as an "agent harness" with behavioural middleware and sandboxed execution. **Strands harness** (released 2026-09-21) is a ready-made, general-purpose agent built on the SDK. Latest versions: `strands-agents` 1.65.0 (2026-11-13), `@strands-agents/sdk` 1.25.0 (2026-11-13) and `strands-harness` 0.4.0 (2026-11-12), checked on PyPI and npm on 2026-11-19.
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

### Kiro cloud sessions can reach your VPC; Kiro for VS Code · 2026-11-19 → 11-20 🆕
Admins can connect Kiro cloud sessions to private resources in an Amazon VPC (Enterprise plan with IAM Identity Center profiles in `us-east-1`; the profile must use Controls). Also new: IDE 1.5.11 with Remote SSH and Dev Containers, and Kiro for VS Code 1.5.0 (details in [Coding agents](../../build/coding-agents/README.md)).
**Why it matters:** Cloud agents can work against private databases and services without exposing them publicly.
Source: [Kiro changelog](https://kiro.dev/changelog/) · Added: 2026-11-21

### Kiro IDE 1.4.236: permission hook and GitLab installs · 2026-11-18 🆕
The IDE gets the CLI's Permission Request hook (answer approval prompts from a script), shows final arguments after Pre Tool Use hooks rewrite them, and supports one organization IdP sign-in across HTTP MCP servers. Powers and skills can be installed from public GitLab URLs; self-hosted GitLab hosts must be listed in `kiroAgent.powers.trustedGitLabHosts`.
**Why it matters:** IDE and CLI users can now share one hook-based policy and one MCP sign-in.
Source: [Kiro IDE 1.4.236 changelog](https://kiro.dev/changelog/ide/1-4-236/) · Added: 2026-11-20

### Kiro CLI 3.4–3.5: permission hooks and org sign-in for MCP · 2026-11-17 🆕
**CLI 3.4.0** (2026-11-16): in V3 sessions, a `PreToolUse` hook can return `updatedInput` to rewrite a tool call's inputs. A new `PermissionRequest` hook can answer `allow` or `deny` to permission prompts, and a deny from any hook overrides an allow. **CLI 3.5.0** (2026-11-17): MCP servers set to use organization sign-in share one IdP login (`kiro-cli mcp idp setup`, then sign in once from `/mcp`). Admins can set the portal that `kiro-cli login` opens with `auth.portalUrl`, or with the `AuthPortalUrl` policy. Also on 2026-11-16: IDE 1.4.215 adds conversation forking and cloud sessions in Frankfurt, and Kiro Web gains a terminal.
**Why it matters:** You can now enforce team policy on tool calls in scripts, for example denying writes outside the repo, and stop separate browser logins for every internal MCP server.
Sources: [Kiro CLI 3.4 changelog](https://kiro.dev/changelog/cli/3-4/) · [Kiro CLI 3.5 changelog](https://kiro.dev/changelog/cli/3-5/) · [Kiro changelog](https://kiro.dev/changelog/index) · Added: 2026-11-19

### Kiro bots, GA in Kiro Crew · 2026-11-05 🆕
Named, long-running agents, each with its own memory, chat and sessions. They can run sessions in parallel, follow schedules and work within per-bot permissions.
Source: [Let's Data Science](https://letsdatascience.com/news/aws-launches-kiro-bots-for-coordinating-parallel-ai-coding-a-e78ec0ae) · Added: 2026-11-18

### Kiro CLI 3.0 + October changes 🆕
November brought Kiro CLI 3.0.0–3.1.0. October added a **local command sandbox** (off by default; it blocks network access and stops the agent reading `~/.aws/credentials`), Memory, Workflows, Workspace trust and Markdown Review. Claude Opus 5.5 and Sonnet 5.5 (1M context) are now in Kiro, including GovCloud, and **Claude Sonnet 4 reached end of life in Kiro on 2026-10-14**.
**Why it matters:** Turn on the sandbox for any repo you don't fully trust.
Sources: [Kiro changelog](https://kiro.dev/changelog/dev-server-and-spec-workflows/) · [AWS Japan SA deck, Oct](https://speakerdeck.com/inariku/kiro-update-2026-10-en) · [Nov deck](https://speakerdeck.com/inariku/kiro-update-2026-11-en) · Added: 2026-11-18

## 🖥️ Self-hosted models on AWS

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
