# Azure for AI engineering

_Last updated: 2026-11-25_

> What matters on Azure for AI engineers: Microsoft Foundry (models, Foundry Agent Service and hosted agents, Foundry IQ, evaluation and observability), Microsoft Agent Framework for Python and .NET (the successor to Semantic Kernel and AutoGen), the Azure MCP Server, and Spring AI and LangChain4j on Azure. **Microsoft Ignite 2026 ran 17–20 Nov** in San Francisco; the developer-relevant announcements are in the section below. OpenAI model launches live in [LLM news](../../models/news/README.md), non-Azure API features in [LLM APIs](../../build/llm-apis/README.md), and GitHub Copilot in [Coding agents](../../build/coding-agents/README.md).

## ⚡ Action items & dates

Retirement dates come from Microsoft's model retirement schedule (re-checked 2026-11-25; the page shows 2026-11-18). Check the [schedule](https://learn.microsoft.com/en-sg/Azure/foundry/concepts/model-lifecycle-retirement) before you plan, because dates move.

| When | What | Do this |
|---|---|---|
| **now** | `agent-framework` 1.26.1 and 1.26.2 on PyPI were malicious (2026-11-17). The current PyPI release is 1.26.0 (2026-11-12) | Pin `agent-framework` in lockfiles and follow the cleanup steps in [AI security](../../architecture/security/README.md). |
| **now** | The npm `latest` tag of `@azure/mcp` points to **4.0.0-beta.10** (2026-11-23), so the documented `@azure/mcp@latest` config pulls a beta. The last stable release is 3.0.0 (2026-10-12) | Pin `@azure/mcp@3.0.0` in shared MCP configs unless you want the beta. ([npm](https://www.npmjs.com/package/@azure/mcp)) |
| **2026-11-30** | `claude-sonnet-4-5` (Azure Marketplace) retires; listed replacement `claude-sonnet-5-5` | Redeploy and re-run evals before the date. |
| **2026-12-03 → 12-08** | Preview retirements: `DeepSeek-V4-Flash-0731` (12-03), `MAI-Transcribe-2-Streaming` (12-04), `gpt-chat-latest` 2026-05-28 (12-08) | Pin newer versions (for example `DeepSeek-V4.1-Flash-1017`, which retires 2027-03-06) or move off. |
| **2026-12-09** | `Ministral-3B` → `ministral-ministral-4b-instruct`; `mistral-medium-2505` → `mistral-medium-3-5` (Marketplace) | Switch deployments. |
| **2026-12-15** | `whisper` 001, `tts` 001 and `tts-hd` 001 retire, plus DeepSeek-V4-Pro-0813, DeepSeek-V4.1-Flash (preview) and Cohere-parse-v5 (preview) | Move speech workloads to the `gpt-4o-*-transcribe`/`-tts` family or newer; note those retire in 2027 too (below). |
| **2027-01-14** | `gpt-4o` 2024-05-13 retires; replacement `gpt-5.1` 2025-11-13. Global Standard and Data Zone Standard deployments auto-upgrade; **Provisioned deployments do not**, and Global Batch is not auto-upgraded | Migrate provisioned and batch deployments by hand. Deployments set to `NoAutoUpgrade` stop working at retirement. |
| **2027-01-17** | Phi-4 family (Phi-4, -mini-instruct, -mini-reasoning, -multimodal-instruct, -reasoning) retires from Marketplace; listed replacement `microsoft--phi-4` on Foundry Managed Compute | Plan the move to Managed Compute. |
| **2027-01-20** | `gpt-realtime-2` 2026-05-06 (preview) → `gpt-realtime-2.1`; `gpt-4o-mini-transcribe` and `gpt-4o-mini-tts` 2025-03-20 retire | Update voice agents. |
| **2027-01-27** | `model-router` versions 2025-05-19 and 2025-08-07 (preview) retire | Move to a current model-router version. |
| **2027-02-09** | `gpt-5` and `gpt-5-nano` 2025-08-07 retire | Plan the upgrade and re-run evals. |
| **2027-02-22** | `claude-opus-4-5` (listed replacement `claude-opus-5-5`) and `claude-haiku-4-5` (→ `claude-haiku-5-5`) retire on Foundry, per the schedule. Anthropic's own notice gives **2027-01-22** for Opus 4.5 | Plan for the earlier date until Microsoft confirms. |
| **2027-04-14** | `gpt-4o` 2024-08-06 and 2024-11-20, `gpt-4o-mini` 2024-07-18, and `gpt-4.1` / `-mini` / `-nano` 2025-04-14 retire (`gpt-5.1` listed for the `gpt-4o` versions) | Inventory deployments now; fine-tuning *training* on these ends no earlier than 2027-04-01 / 04-14. |

Sources: [Model retirement schedule](https://learn.microsoft.com/en-sg/Azure/foundry/concepts/model-lifecycle-retirement) · [Azure OpenAI model retirements](https://learn.microsoft.com/en-za/azure/foundry/openai/concepts/model-retirements) · [PyPI: agent-framework](https://pypi.org/project/agent-framework/) · Added: 2026-11-24

---

## ⭐ Start here

### Microsoft Agent Framework · Python and .NET agent SDK 🆕
Microsoft's open-source framework for single agents and graph-based multi-agent workflows, from the Semantic Kernel and AutoGen teams. Python and .NET are the main SDKs; Go is in public preview. It works with Foundry, Azure OpenAI, OpenAI and other providers, and Python installs can be trimmed to `agent-framework-core` plus provider packages such as `agent-framework-foundry`. Latest versions checked 2026-11-24: `agent-framework` 1.26.0 on PyPI (2026-11-12) and `Microsoft.Agents.AI` 1.28.0 on NuGet.
```bash
pip install agent-framework                                   # Python
dotnet add package Microsoft.Agents.AI.Foundry --prerelease   # .NET
```
**Why it matters:** It is where Microsoft's new agent samples, skills and Foundry integrations land, with Foundry support in the `agent-framework-foundry` provider package. Given the 2026-11-17 PyPI compromise, pin the version and install from a lockfile.
Sources: [Agent Framework overview](https://learn.microsoft.com/en-ca/agent-framework/overview/) · [PyPI](https://pypi.org/project/agent-framework/) · [NuGet](https://www.nuget.org/packages/Microsoft.Agents.AI) · Added: 2026-11-24

### Migrating from Semantic Kernel to Agent Framework · migration guide 🆕
Microsoft calls Agent Framework the direct successor to Semantic Kernel and AutoGen. The guide maps the changes: `Microsoft.SemanticKernel(.Agents)` becomes `Microsoft.Agents.AI`; agents come straight from a chat client with no `Kernel`; threads become sessions the agent creates; plain functions passed to `tools=` replace `@kernel_function` plugins; and `invoke` becomes `run`. Existing `KernelFunction`s can be wrapped with `.as_agent_framework_tool()` (needs `semantic-kernel` 1.38 or later), so you can migrate piece by piece.
**Why it matters:** New Microsoft samples, Foundry features and skills target Agent Framework, so plan SK and AutoGen migrations now rather than building new code on them.
Sources: [Migration guide: from Semantic Kernel](https://learn.microsoft.com/en-ca/agent-framework/migration-guide/from-semantic-kernel/) · [Migration guide: from AutoGen](https://learn.microsoft.com/en-ca/agent-framework/migration-guide/from-autogen/) · Added: 2026-11-24

### Foundry Agent Service and hosted agents · managed agent runtime 🆕
Foundry's managed service for building, hosting and operating agents. **Prompt agents** are configured in Foundry (instructions, model, tools); **hosted agents** run your own agent code in VM-isolated sandboxes with network egress controls, long-running job recovery and a configurable idle timeout (2 minutes to 4 hours, default 15). Tools are shared through **toolboxes**, a managed MCP endpoint, and agents can be published into Microsoft 365. Ignite 2026 changes are below.
**Why it matters:** It is Azure's answer to AWS AgentCore ([AWS page](../aws/README.md)): agent hosting, tools, identity and tracing inside your Azure subscription and network.
Source: [What's new in Foundry Agent Service at Ignite 2026](https://devblogs.microsoft.com/foundry/whats-new-in-foundry-agent-service-at-ignite-2026/) · Added: 2026-11-24

### Azure MCP Server · Azure tools for any MCP client 🆕
Microsoft's open-source MCP server (in [microsoft/mcp](https://github.com/microsoft/mcp/tree/main/servers/Azure.Mcp.Server)) that lets agents query and manage Azure resources across many services, including listing and deploying Foundry models. Published as `@azure/mcp` (npm), `Azure.Mcp` (NuGet) and `msmcp-azure` (PyPI). It uses your local Azure sign-in (for example `az login`), supports sovereign clouds with `--cloud`, and can be self-hosted remotely on Azure Container Apps for HTTP-only clients such as Foundry and Copilot Studio. Config from the package README:
```json
{
  "mcpServers": {
    "azure-mcp-server": {
      "command": "npx",
      "args": ["-y", "@azure/mcp@latest", "server", "start"]
    }
  }
}
```
**Why it matters:** One server gives Claude Code, Copilot, Cursor and others Azure context. Note that `@latest` currently resolves to a 4.0.0 beta (see action items), and the server acts with your identity's permissions, so start with a least-privilege account. More servers: [MCP servers](../../build/mcp-servers/README.md).
Sources: [Azure MCP Server docs](https://learn.microsoft.com/en-us/azure/developer/azure-mcp-server/) · [Get started](https://learn.microsoft.com/en-us/azure/developer/azure-mcp-server/get-started) · [npm package README](https://www.npmjs.com/package/@azure/mcp) · Added: 2026-11-24

---

## 🎤 Microsoft Ignite 2026 (17–20 Nov)

### Foundry Agent Service: hosted agents to production · 2026-11-18 🆕
- **GA:** voice agents; the A2A tool; Web Search (powered by Web IQ) for prompt agents; computer use and browser automation (isolated sessions, Live View and take-control, recordings in your own storage); hosted agents with shared subnet IPs (default quota 1,000–2,000 concurrent sessions per subscription and region), network egress controls and long-running resiliency.
- **Preview:** Microsoft Copilot harness (a managed agent loop for prompt agents, authorable from the Foundry CLI `azd ai` and the VS Code toolkit); memory snapshots to cut cold starts; private CA trust for internal APIs and MCP servers; Azure Policy enforcement of egress settings; tool policies for toolboxes; Work IQ and Fabric IQ integrations; Microsoft 365 accounts (Entra Agent ID, mailbox, Teams presence) for hosted agents.
- **Coming:** deploying hosted agents to your own AKS cluster, with public preview targeted for early December.

**Why it matters:** Egress controls, private CA and policy close most of the gaps that kept hosted agents out of locked-down enterprise networks. Agents can't be switched to the Copilot harness after creation, so choose before you build.
Sources: [Foundry blog: Agent Service at Ignite 2026](https://devblogs.microsoft.com/foundry/whats-new-in-foundry-agent-service-at-ignite-2026/) · [Azure blog: continuous improvement](https://azure.microsoft.com/en-us/blog/continuous-improvement-comes-to-microsoft-foundry/) · [Visual Studio Magazine (harness caveat)](https://visualstudiomagazine.com/articles/2026/11/05/microsoft-foundry-october-recap-separates-ai-agent-previews-from-ga-releases.aspx) · Added: 2026-11-24

### Foundry observability, evaluation and optimization · 2026-11-17 🆕
**Insights** (GA) groups recurring failures in production traces, including for LangGraph, LangChain and CrewAI agents, which also get GA observability. **Multi-turn evaluation** is GA. In preview: annotations on traces, evaluation and golden datasets, safety coverage for rubric evaluators, sending insights to the agent optimizer, skill optimization (versioned, opt-in skill updates), cost optimization and Cost in Microsoft Foundry. Microsoft says the model router saves up to 65% compared with sending everything to a frontier model *(self-reported)*.
**Why it matters:** A built-in loop from traces to evals to candidate fixes, if your agents already run in Foundry. Vendor-neutral options are in [Evals & observability](../../architecture/evals-and-observability/README.md).
Sources: [Azure blog: continuous improvement comes to Foundry](https://azure.microsoft.com/en-us/blog/continuous-improvement-comes-to-microsoft-foundry/) · [Ignite 2026 Book of News](https://news.microsoft.com/events/ignite/2026/book-of-news/) · Added: 2026-11-24

### Foundry IQ, models and training · 2026-11-17 🆕
Foundry IQ (now part of Microsoft IQ) adds knowledge graphs, the **Microsoft-Retriever-1** retrieval model for iterative search and query planning, and a serverless Foundry IQ resource in every new project (all preview); the SharePoint indexed knowledge source is GA. Models: **Microsoft-Decision-1.1** is GA (also usable as an evaluation judge); MAI-Image-2.7 and -2.7-Flash are in preview; MAI-Code-2-Flash is in private preview in Foundry; fal video models (Kling, LTX, MiniMax) and Baseten on Foundry are in preview. The model router gains AI Gateway support and Messages/Responses API support. Managed Training (formerly managed fine-tuning) and **Programmed Training** (custom SFT and RL loops on supported open-weight models, preview) cover adaptation.
**Why it matters:** Foundry IQ is Microsoft's managed retrieval layer for agents; compare it with your own stack in [RAG & retrieval](../../architecture/rag-and-retrieval/README.md). Confirm deployment names in the Foundry model catalog before you code against the new models.
Sources: [Ignite 2026 Book of News](https://news.microsoft.com/events/ignite/2026/book-of-news/) · [Azure blog: continuous improvement](https://azure.microsoft.com/en-us/blog/continuous-improvement-comes-to-microsoft-foundry/) · Added: 2026-11-24

---

## 🗞️ Latest

<!-- newest first -->

### Foundry Managed Compute GA: open models on dedicated GPUs · 2026-11-20 🆕
Managed Compute, in preview since Build 2026, is now GA. Foundry provisions the GPUs and runs the serving containers for open models from the Hugging Face collection in Foundry, which has more than 150 models. Microsoft licence-reviews each model, screens it for untrusted code and stages the weights in Azure. Deployment types are Global and US or EU Data Zone. GPUs are NVIDIA A100, H100 and H200 or AMD MI300X, depending on the model, billed per accelerator-hour. A deployment template fixes context length, serving runtime and GPU count. You scale by raising `capacity` behind one endpoint, and call it with the OpenAI client at `https://<account>.services.ai.azure.com/openai/v1/`. In the blog's SDK example (`azure-mgmt-cognitiveservices`), the SKU is `GlobalManagedCompute`. LoRA adapters from Foundry fine-tuning can share a base deployment (preview), and bring-your-own-weights is in limited preview.
**Why it matters:** This is now the supported way to self-host open-weight models in Foundry, and it is the listed replacement for the Phi-4 Marketplace models that retire on 2027-01-17. You pay for GPU-hours whether or not you send traffic, so compare that with per-token serverless pricing before you move. Hosts and prices for open models are compared in [Open-weight model providers](../../models/open-model-providers/README.md).
Sources: [Foundry blog: Managed Compute GA](https://devblogs.microsoft.com/foundry/managed-compute-ga/) · [Managed compute overview](https://learn.microsoft.com/en-us/azure/foundry/concepts/managed-compute-overview) · Added: 2026-11-25

### GPT-6.2 Astra and GPT-6.2 Sol GA in Foundry · 2026-11-17 🆕
Both models are GA as `gpt-6.2-astra` and `gpt-6.2-sol`, version 2026-11-17. Each has a 1.05M context (922K input, 128K output). Parallel tool calling works only through the Responses API. Deployment types are Global Standard, Data Zone Standard (US, EU, APAC) and Global Provisioned Throughput ($1 per PTU-hour). Short-context Global Standard prices per 1M tokens (input / cached / output):

| | Astra | Sol |
|---|---|---|
| Global Standard | $8 / $0.40 / $40 | $2 / $0.10 / $10 |
| Data Zone US | $8.80 / $0.44 / $44 | $2.20 / $0.11 / $11 |
| Data Zone EU / APAC | $9.60 / $0.48 / $48 | $2.40 / $0.12 / $12 |

Long-context requests cost more (Astra $16 / $60, Sol $4 / $15 input / output on Global Standard). The default cache TTL is 30 minutes; you can opt into a 12-hour cache write with `prompt_cache_options.ttl: "12h"` on the Responses API, which costs more to write.
**Why it matters:** Prices match OpenAI's and Bedrock's Global prices, so you can choose between clouds on data residency and quota. Commenters on the announcement report they can't deploy in East US 2, so check regional availability before you plan. Migration notes for GPT-6.2 are in [LLM APIs](../../build/llm-apis/README.md).
Sources: [Foundry blog: GPT-6.2 GA](https://techcommunity.microsoft.com/blog/azure-ai-foundry-blog/gpt-6-2-astra-and-gpt-6-2-sol-now-generally-available-in-microsoft-foundry/4574122) · [Foundry Models sold by Azure](https://learn.microsoft.com/en-us/azure/foundry/foundry-models/concepts/models-sold-directly-by-azure) · Added: 2026-11-25

### `@azure/mcp` 4.0.0 betas now on the npm `latest` tag · 2026-11-23 🆕
The npm registry's `latest` dist-tag for `@azure/mcp` points to 4.0.0-beta.10, published 2026-11-23 after weekly betas through November. The last non-beta release is 3.0.0 (2026-10-12). PyPI's `msmcp-azure` keeps 3.0.0 as its latest.
**Why it matters:** Every config that follows the docs' `@azure/mcp@latest` pattern now runs a beta major version. Pin the version for team and CI configs.
Source: [npm: @azure/mcp](https://www.npmjs.com/package/@azure/mcp) · [PyPI: msmcp-azure](https://pypi.org/project/msmcp-azure/) · Added: 2026-11-24

### `agent-framework` PyPI compromise · 2026-11-17 🆕
Two malicious releases of the Python meta-package (1.26.1 and 1.26.2) stole cloud credentials and Azure managed-identity and DevOps OIDC tokens; they were pulled within about an hour, and PyPI's latest is back to 1.26.0. Full details and cleanup steps are in [AI security](../../architecture/security/README.md).
**Why it matters:** Treat any host that resolved an unpinned `agent-framework` on 2026-11-17 as compromised, and review Entra ID federated credentials, not just stored secrets.
Sources: [Wiz](https://www.wiz.io/blog/malicious-version-of-microsofts-agent-framework-published-to-pypi) · [StepSecurity](https://www.stepsecurity.io/blog/microsoft-agent-framework-pypi-package-compromised) · Added: 2026-11-24

### Foundry October 2026 recap: browser automation GA, Copilot harness preview · 2026-11-05 🆕
Microsoft's monthly recap covers October: browser automation GA (19 Oct), long-running hosted-agent resilience GA (28 Oct), the Microsoft Copilot harness in public preview (28 Oct), the Decisions API GA (structured predicates, choices or scores instead of prose), GPT-6.1 Terra among GA model changes and MAI Image 2.6 in regional preview. The recap flags SDK and CLI changes that need compatibility checks before upgrading.
**Why it matters:** Use checkpoints and idempotent steps so resumed long-running agents don't repeat side effects, and keep human approval on browser tools.
Sources: [What's new in Microsoft Foundry, October 2026](https://devblogs.microsoft.com/foundry/whats-new-in-microsoft-foundry-october-2026/) · [Visual Studio Magazine summary](https://visualstudiomagazine.com/articles/2026/11/05/microsoft-foundry-october-recap-separates-ai-agent-previews-from-ga-releases.aspx) · Added: 2026-11-24

### Agent Framework builder skills for coding agents · 2026-11-04 🆕
Microsoft published two Agent Skills, `agent-framework-builder-python` and `agent-framework-builder-dotnet`, in the repo's `skills/` folder. They teach coding agents how to choose patterns, tools, sessions, workflows and hosting when they write Agent Framework code; they are development aids, not runtime dependencies.
```bash
npx skills add microsoft/agent-framework --skill agent-framework-builder-python
gh skill install microsoft/agent-framework agent-framework-builder-dotnet@main
```
**Why it matters:** Fewer hallucinated SK-era APIs when an agent writes Agent Framework code. Pin a tag or commit instead of `@main` for reproducible guidance. More skills: [Agent skills](../../build/agent-skills/README.md).
Source: [Agent Framework blog](https://devblogs.microsoft.com/agent-framework/give-your-coding-agent-a-head-start-with-microsoft-agent-framework-skills-for-net-and-python/) · Added: 2026-11-24

---

## ☕ Spring & JVM on Azure

### Spring AI 2.x: use the OpenAI module for Azure OpenAI / Foundry 🆕
Spring AI's Azure OpenAI page says that, as of 2.0.0-M5, models deployed on Azure / Microsoft Foundry should be reached through the **OpenAI Chat** support. On Maven Central the separate `spring-ai-starter-model-azure-openai` stops at 2.0.0-M4, while `spring-ai-starter-model-openai` is at 2.1.0. For keyless auth, pass an Entra ID `TokenCredential` (for example a managed identity via `DefaultAzureCredentialBuilder`, from `com.azure:azure-identity`) as `AzureOpenAiCredentials` in `OpenAiChatOptions`. Azure AI Search as a vector store: `spring-ai-starter-vector-store-azure` (2.1.0).
**Why it matters:** Spring AI 1.x apps on the Azure starter must switch modules when they move to 2.x. Release details: [JVM libraries](../../build/libraries/jvm.md).
Sources: [Spring AI 2.1 docs: Azure OpenAI chat](https://docs.spring.io/spring-ai/reference/2.1/api/chat/azure-openai-chat.html) · [Maven Central](https://repo1.maven.org/maven2/org/springframework/ai/) · Added: 2026-11-24

### LangChain4j on Azure 🆕
`dev.langchain4j:langchain4j-azure-open-ai` is at 1.24.0 and `langchain4j-azure-ai-search` at 1.24.0-beta34 (both 2026-11-18, Maven Central).
**Why it matters:** The non-Spring route (Quarkus, Micronaut, plain Java) to Azure OpenAI and Azure AI Search.
Source: [Maven Central: dev.langchain4j](https://repo1.maven.org/maven2/dev/langchain4j/) · Added: 2026-11-24

---

## 🗺️ Picking an Azure path

```
"I want OpenAI/Claude/open models inside my Azure tenant"   → Foundry Models (check the retirement schedule)
"I'm writing the agent code"                                → Agent Framework (Py/.NET) · Spring AI 2.x / LangChain4j (JVM)
"I want to host agents without running servers"             → Foundry Agent Service hosted agents (+ toolboxes, egress controls)
"My agents need enterprise knowledge"                       → Foundry IQ / Azure AI Search
"My coding agent should operate my Azure subscription"      → Azure MCP Server, least-privilege identity, pinned version
"I'm on Semantic Kernel or AutoGen"                         → Follow the Agent Framework migration guide
```

## 📚 Reference

[Foundry blog](https://devblogs.microsoft.com/foundry/) and its [monthly "What's new"](https://devblogs.microsoft.com/foundry/category/whats-new/) · [Agent Framework blog](https://devblogs.microsoft.com/agent-framework/) · [Agent Framework docs](https://learn.microsoft.com/en-ca/agent-framework/overview/) · [Model retirement schedule](https://learn.microsoft.com/en-sg/Azure/foundry/concepts/model-lifecycle-retirement) · [Azure OpenAI model retirements](https://learn.microsoft.com/en-za/azure/foundry/openai/concepts/model-retirements) · [Azure MCP Server docs](https://learn.microsoft.com/en-us/azure/developer/azure-mcp-server/) · [microsoft/mcp](https://github.com/microsoft/mcp) · [microsoft/agent-framework](https://github.com/microsoft/agent-framework) · [Ignite 2026 Book of News](https://news.microsoft.com/events/ignite/2026/book-of-news/)
