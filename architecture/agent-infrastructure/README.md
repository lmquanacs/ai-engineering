# Agent infrastructure & runtimes

_Last updated: 2026-11-23_

> Where agents actually run: sandboxes for untrusted code, durable execution for long runs, hosting, and identity and permissions. This is the layer between "I wrote an agent" and "it runs safely in production".

## 🧭 The four jobs (most stacks combine 2–3)

| Job | What it solves | Typical picks |
|---|---|---|
| **Sandboxed execution** | Running model-generated code and commands safely | E2B, Daytona, Vercel Sandbox, Modal Sandboxes, Cloudflare Sandbox, Northflank |
| **GPU / serverless compute** | Inference, batch jobs, bursty tools | Modal |
| **Durable orchestration** | Long, multi-step runs that survive crashes, retries and human waits | Temporal, Trigger.dev, LangGraph Platform |
| **Hosting app + data** | The agent service, its DB, secrets and data residency | Northflank, Fly.io, TrueFoundry, Qovery |

Source: [Qovery: infrastructure platforms for agentic workloads](https://www.qovery.com/blog/best-infrastructure-platforms-for-agentic-workloads) · Added: 2026-11-18

## 🔒 Isolation: know what you're getting (as of 2026-11-11)

| Provider | Default isolation |
|---|---|
| E2B · Vercel Sandbox · Fly.io | Firecracker microVM per sandbox |
| Modal | gVisor |
| Daytona | Linux container (a VM class is available) |
| Cloudflare Containers | Each instance in its own VM, behind a Durable Object |
| Northflank | microVMs and gVisor |
| AWS Nitro Sandboxes (EKS, ECS, EC2) | Firecracker microVM per pod or task under the Nitro hypervisor (added 2026-11-23) |

Shared-kernel containers (plain Docker/runc) are no longer considered enough for untrusted agent code. Prefer microVM or gVisor isolation when the agent runs code it wrote itself.
Sources: [Agentpedia sandbox comparison](https://agentpedia.codes/blog/best-ai-agent-sandboxes-2026) · [Sandboxing guide](https://manveerc.substack.com/p/ai-agent-sandboxing-guide) · Added: 2026-11-18

---

## ⭐ Start here

### E2B · sandboxes built for agents
Firecracker microVMs with pause and resume of memory plus filesystem, and 24-hour sessions on Pro. The runtime is Apache-2.0 and self-hostable; **E2B Embed** (Sep 2026) packages it for a single machine.
**Why it matters:** It is the default choice for agents that need to run code: ephemeral, fast and strongly isolated.
Source: [Agentpedia comparison](https://agentpedia.codes/blog/best-ai-agent-sandboxes-2026) · [e2b.dev](https://e2b.dev) · Added: 2026-11-18

### Daytona · persistent sandboxes
Persistent sandboxes and dev environments. Teams use them for long-lived, stateful coding agents where the working tree must survive. **No longer open source:** since 2026-06-11 the production code is closed and the old public repository is unmaintained, so self-hosting it means no fixes from Daytona. The SDKs live under github.com/daytona (the Python SDK is Apache-2.0).
Source: [ZenML: choosing a sandbox runtime for long-lived coding agents](https://www.zenml.io/blog/choosing-a-sandbox-runtime-for-long-lived-coding-agents) · [Daytona: going closed source](https://daytona.io/dotfiles/updates/daytona-is-going-closed-source) · Added: 2026-11-18 · Updated: 2026-11-23

### Temporal Sandbox Orchestration Harness · May 2026
Runs the agent as a Temporal Workflow, so state survives failures and waits, and orchestrates sandboxes (Modal, E2B, Daytona, GKE Agent Sandbox, Bedrock AgentCore) as activities.
**Why it matters:** It combines durable execution with isolated compute, the two pieces most homegrown agent backends lack.
Source: [Temporal blog](https://temporal.io/blog/temporal-sandbox-orchestration-harness-the-missing-layer-for-running-agents) · Added: 2026-11-18

### Modal Sandboxes · coding agents at scale
Used by Ramp for background coding agents that write commits and PRs, and by Imbue to orchestrate hundreds of isolated coding agents.
Source: [Modal](https://modal.com/resources/best-code-execution-sandboxes-tool-calling-ai-agents) · Added: 2026-11-18

### Upstash Box · a coding agent in a box
A TypeScript API that starts a sandbox with a coding-agent harness (for example Claude Code), a model and Git credentials in a few lines.
Source: [Upstash: sandbox providers for AI agents](https://upstash.com/blog/best-sandbox-providers-for-ai-agents) · Added: 2026-11-18

## 📰 Recent releases

### Cloudflare Agents SDK 0.34.0: Pi 1.6 tools that wait while the agent sleeps · 2026-11-20 🆕
`PiHarness` moves to Pi 1.6: a tool can "park" instead of returning, and Pi reruns it when a signal arrives (`harness.signal()`) or a deadline passes, while the Durable Object hibernates. A `beforeTool` hook can park a call for human approval, and sessions can start from an existing history via `init`. **Breaking:** signals go through `harness.signal()` instead of `(await harness.pi()).signal()`, call `harness.root()` before reaching the root session, Pi Durable's `RunEndTask` is now `HookTask`, failed requests return a generic `500` (customise with `onFetchError()`), and MCP clients must catch `MCPAuthorizationRequiredError`. Conversations that ran on Pi 1.6 can't go back to Pi 1.5.
**Why it matters:** Human-in-the-loop and wait-for-event tools no longer keep a paid instance awake. Because rollback is one-way, test the upgrade on a staging deployment and plan to roll forward.
Source: [Cloudflare changelog](https://developers.cloudflare.com/changelog/post/2026-11-20-pi-harness-pi-1-6/) · `agents` 0.34.0 on npm (2026-11-20) · Added: 2026-11-23

### AWS Nitro Sandboxes: a hardware-isolated VM per pod, task or agent · 2026-11-09 🆕
Each EKS pod or ECS task (or your own VMs on EC2) can run in its own lightweight VM, a Firecracker microVM managed by the Nitro hypervisor, on your existing instances. On EKS you opt in per pod with `runtimeClassName: isolated-sandbox` (or `confidential-sandbox`, which adds attestation so KMS releases keys only to approved images and policies); every pod gets a Cedar policy governing image admission, exec and logs. It needs Kubernetes 1.36 or later and supported Nitro instance types, and is in all commercial Regions at no extra charge beyond EC2.
**Why it matters:** microVM isolation for agent-generated code inside your own VPC and IAM, at EC2 prices. Unlike hosted sandboxes you run warm pools, cleanup and quotas yourself, and the sandbox keeps whatever IAM role the pod has, so scope it tightly.
Sources: [AWS What's New](https://aws.amazon.com/about-aws/whats-new/2026/11/nitro-sandboxes-eks-ecs-ec2/) · [EKS User Guide: sandboxing](https://docs.aws.amazon.com/eks/latest/userguide/sandboxing.html) · Added: 2026-11-23

### Daytona Python SDK 2.x is now the default `pip install daytona` · 2026-11-13 → 11-20 🆕
`daytona` 2.0.0 (Nov 13) and 2.1.0 (Nov 20) put every call behind a version namespace (`Daytona().v2` / `.v0`), and importing resource types such as `Sandbox` or `Image` from the package root now raises `ImportError`. The old API needs the `daytona[v0-sdk]` extra; the legacy `daytona-sdk` package stays on 0.x, and npm `@daytonaio/sdk` is still 0.x.
**Why it matters:** Unpinned installs break existing integrations; pin `daytona<1` until you migrate.
Source: [daytona on PyPI](https://pypi.org/project/daytona/) · Added: 2026-11-22

### External sandboxes for local coding agents · Prime Radiant · 2026-11-16 🆕
The agent (Claude Code, Codex or Pi) stays on your machine but sends every command to a separate Linux sandbox over a localhost API. Three implementations share one protocol (v86/WebAssembly, Apple Containers, Microsoft Quicksand/QEMU), each with mounted folders only, no network by default, an allow-list proxy, and credential substitution so the agent never sees real API keys.
**Why it matters:** A practical way to run less-trusted or local models without handing them your laptop; keys injected at the proxy are out of reach of prompt injection.
Source: [Prime Radiant blog](https://blog.primeradiant.com/external-sandboxes-for-coding-agents/) · [Simon Willison](https://simonwillison.net/2026/Nov/17/external-sandboxes-for-coding-agents/) · Added: 2026-11-21

### Per-session runtimes run out of sessions, not CPU · arXiv 2611.26480 · 2026-11-19 🆕
Measured on Bedrock AgentCore: agents waited a median 2.7 s per model reply and computed for an estimated 5–40 ms, yet each conversation holds its own VM, which stayed reserved about 15 minutes after a 33-second conversation unless the client closed it *(as reported)*.
**Why it matters:** Close sessions explicitly when a conversation ends, and size quotas by concurrent conversations. More in [Research](../../learn/research/README.md).
Source: [arXiv 2611.26480](https://arxiv.org/abs/2611.26480) · Added: 2026-11-21

### Daytona macOS Sandboxes · 2026-11-17 🆕
Full macOS VMs on dedicated Apple silicon reserved for your organization. The base image ships macOS 26.6.2 with Xcode 26.6 and the iPhone simulator. Create one with `daytona sandbox create-macos --region macos-1 --image base-macos` or from the SDK; SSH uses short-lived tokens scoped to one sandbox, and computer-use (screenshots, input, accessibility tree) and filesystem snapshots are supported. Pricing and preview/GA status aren't stated.
**Why it matters:** Agents that build iOS/macOS apps or drive macOS GUIs get a managed sandbox instead of a Mac farm.
Source: [Daytona: macOS Sandboxes](https://www.daytona.io/dotfiles/macos-sandboxes) · Added: 2026-11-20

### Vercel eve 1.0 GA + Sandbox Python SDK 1.0 · 2026-11-16 → 11-17 🆕
**eve** is Vercel's open-source TypeScript agent framework: durable workflows that resume after a crash, approvals answerable in Slack, and Vercel Sandbox for code execution. It needs Node.js 24+ (`npx eve@latest init my-agent`); stable APIs follow semver. Vercel puts a 50-turn session on Vercel Workflows at 1.3¢ *(self-reported)*. Separately, **`vercel-sandbox` 1.0** for Python stabilises the API to match the TS SDK (context-manager cleanup, async on AnyIO, sync calls); **breaking:** command input and output are now bytes.
**Why it matters:** A durable agent runtime and a stable Python sandbox client from one vendor. Python users upgrading from 0.x must handle bytes I/O.
Sources: [Vercel: eve is GA](https://vercel.com/blog/eve-is-now-generally-available) · [Vercel changelog: Sandbox Python SDK 1.0](https://vercel.com/changelog/vercel-sandbox-python-sdk-1-0-is-now-available) · Added: 2026-11-20

### Temporal Cloud on Azure · public preview · 2026-11-17 🆕
Temporal Cloud now runs on Azure in public preview, with production workloads supported in **Central US and Australia East**. Access needs approval so Temporal can plan capacity.
**Why it matters:** Azure-first teams, and teams with Australian data-residency needs, can run durable agent workflows on managed Temporal next to their other workloads instead of self-hosting.
Source: [Temporal changelog](https://temporal.io/changelog/temporal-cloud-on-azure-is-in-public-preview) · Added: 2026-11-19

## 🪪 Identity & permissions for agents

- **MCP auth:** remote MCP servers are OAuth 2.1 resource servers under the 2026-07-28 spec, so prefer scoped tokens to static keys. → [MCP servers](../../build/mcp-servers/README.md)
- **Fail closed:** Claude Code 2.1.319 auto mode now asks or denies when its server-side check is unavailable. → [Coding agents](../../build/coding-agents/README.md)
- **Default-deny PATs:** Devin now requires approval for personal access tokens by default in enterprises without a policy.
- **Rule of Two:** limit any session to two of: untrusted input, sensitive access, external side effects. → [AI security](../security/README.md)
