# Google Cloud for AI engineering

_Last updated: 2026-11-24_

> What matters on Google Cloud if you build AI systems: **Gemini Enterprise Agent Platform** (formerly Vertex AI), with model availability and retirements, Model Garden's third-party and open models, Agent Runtime (formerly Agent Engine), sessions and Memory Bank, plus the Agent Development Kit (ADK), Google Cloud MCP servers and Spring AI on Google Cloud. New Gemini models are covered in [LLM news](../../models/news/README.md), Gemini Developer API features in [LLM APIs](../../build/llm-apis/README.md), and Gemini CLI and Antigravity in [Coding agents](../../build/coding-agents/README.md).

## ⚡ Action items & dates

| When | What | Do this |
|---|---|---|
| **2026-12-01** | Gemini 4 Carbon and Argon prices double when introductory pricing ends | Re-budget December. Details are on [Inference, cost & serving](../../models/cost-and-serving/README.md). |
| **2026-12-13** | `gemini-live-2.5-flash-native-audio` retires on the platform | Move live voice agents to `gemini-3.8-live`. See [Voice & multimodal](../../build/voice-and-multimodal/README.md). ([model versions](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/learn/model-versions)) |
| **2027-01-12** | Cache writes start being billed for Gemini 4 Hydrogen and later models | Check how often you write to the context cache. ([release notes, 2026-11-18](https://docs.cloud.google.com/gemini-enterprise-agent-platform/release-notes)) |
| **2027-01-28** | `gemini-3.7-flash` retires | Pin `gemini-3.8-flash` and re-run your evals. ([model versions](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/learn/model-versions)) |
| **2027-03-15** | `gemini-2.5-flash-image` retires | Move to `gemini-3.1-flash-lite-image`, the recommended upgrade. ([model versions](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/learn/model-versions)) |
| **2027-04-01** | `text-embedding-005`, `text-embedding-004`, `text-multilingual-embedding-002` and `multimodalembedding@001` retire. The table names no replacement | Vectors from different models don't mix, so plan a full re-embed and reindex of affected vector stores. ([model versions](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/learn/model-versions)) |

Retirement dates come from the model versions page (last updated 2026-11-19). It also lists `veo-3.1-*`, `gemini-3.1-flash-lite`, `gemini-3.5-flash` and several image models as retiring "on or after" dates from May to June 2027.

---

## ⭐ Start here

### Vertex AI is now Gemini Enterprise Agent Platform: what changes in your code · migration 🆕
Google announced Agent Platform on 2026-04-22 as the successor to Vertex AI. All Vertex AI services and future roadmap now ship through Agent Platform. Agent Engine is now **Agent Runtime**, but the API resource is still `ReasoningEngine` for backward compatibility. In the Python SDK (2.0.1 onward), `vertexai.agent_engines` becomes `client.runtimes` on a standalone `agentplatform` package (`agentplatform.Client(project=..., location=...)`). Sessions move to `client.sessions.*` and Memory Bank to `client.memory_banks.memories.*`. No removal date has been given for the legacy namespaces yet. Separately, the generative modules in the old Vertex AI SDK (`vertexai.generative_models`, `@google-cloud/vertexai`, `com.google.cloud:google-cloud-vertexai`, and the Go `vertexai/genai`) are no longer available after **2026-06-24**. Their replacement is the Google Gen AI SDK (`google-genai`, `@google/genai`, `com.google.genai:google-genai`, `google.golang.org/genai`).
**Why it matters:** Code that still imports `vertexai.generative_models` stops getting fixes, and new runtime features land only in the `agentplatform` client. Migrate both before you build anything new.
Sources: [Google Cloud blog: introducing Agent Platform](https://cloud.google.com/blog/products/ai-machine-learning/introducing-gemini-enterprise-agent-platform) · [Agent Runtime SDK migration guide](https://docs.cloud.google.com/gemini-enterprise-agent-platform/build/runtime/sdk-migration) · [Vertex AI SDK migration guide](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/deprecations/genai-vertexai-sdk) · Added: 2026-11-24

### Agent Development Kit (ADK) · Google's agent framework 🆕
ADK is Google's open-source, code-first agent framework, available for Python, Java, TypeScript/JS and Go. It is the framework most tightly integrated with Agent Runtime: Python agents deploy with the `adk` CLI and Go agents with `adkgo`. The Python package is at **2.15.0**, released 2026-11-20 on PyPI. The breaking changes in that release are covered on the [Python libraries](../../build/libraries/python.md) page, and the Java version is listed under [JVM libraries](../../build/libraries/jvm.md).
```bash
pip install google-adk
```
**Why it matters:** If you are deploying to Google Cloud, ADK gives you managed sessions, Memory Bank, tracing and the new Deferred tier without glue code. Pin the version, because the API moves quickly.
Sources: [PyPI: google-adk](https://pypi.org/project/google-adk/) · [Agent Runtime docs](https://docs.cloud.google.com/gemini-enterprise-agent-platform/build/runtime) · [google/adk-python](https://github.com/google/adk-python) · Added: 2026-11-24

### Agent Runtime (formerly Agent Engine) · managed agent hosting 🆕
A fully managed runtime for deploying and scaling agents. It runs any containerised agent that meets the runtime contract, and you can deploy from an Artifact Registry image or a Dockerfile. ADK has full integration; LangChain, LangGraph, AG2 and LlamaIndex work through SDK templates; CrewAI and other frameworks use a custom template. A2A support is in Preview. Other features include VPC-SC, IAM, OpenTelemetry tracing to Cloud Trace, and an Agents CLI with templates, Terraform and Cloud Build CI/CD. Sessions and Memory Bank are separate services alongside it.
**Why it matters:** This is Google's equivalent of AWS's AgentCore Runtime (see [AWS](../aws/README.md)). Compare the two on cold start, identity and memory before you commit to either.
Source: [Agent Runtime docs](https://docs.cloud.google.com/gemini-enterprise-agent-platform/build/runtime) · Added: 2026-11-24

### Google Cloud MCP servers · remote, IAM-governed 🆕
Google hosts remote MCP endpoints for dozens of Google Cloud products, including BigQuery, Cloud Run, Cloud SQL, Spanner, GKE, Cloud Logging and Monitoring, IAM, Pub/Sub and Agent Platform itself. Many are still in Preview. The usual endpoint is `https://SERVICE.googleapis.com/mcp`; Agent Platform exposes toolsets such as `https://aiplatform.googleapis.com/mcp/generate`. An endpoint is live as soon as you enable that service's API. Callers need `roles/mcp.toolUser` plus permissions on the underlying service. You can limit tools by toolset, manage servers in Agent Registry, and have Model Armor scan requests and responses for prompt injection and tool poisoning.
```bash
gcloud projects add-iam-policy-binding PROJECT_ID \
    --member="PRINCIPAL" \
    --role="roles/mcp.toolUser"
```
**Why it matters:** These servers give you managed, audited MCP access to Google Cloud without running your own servers. Enabling a service API also exposes its MCP endpoint, so check who holds `roles/mcp.toolUser`. See [MCP servers](../../build/mcp-servers/README.md) and [AI security](../../architecture/security/README.md).
Sources: [MCP overview](https://docs.cloud.google.com/mcp/overview) · [Supported products](https://docs.cloud.google.com/mcp/supported-products) (updated 2026-11-12) · [Manage MCP servers](https://docs.cloud.google.com/mcp/manage-mcp-servers) · Added: 2026-11-24

---

## 🗞️ Latest

<!-- newest first -->

### Deferred tier for agents and the Interactions API · 2026-11-16 🆕
Background work can now opt into a cheaper Deferred service tier, now GA. In ADK, set `ServiceTier.DEFERRED` in `RunConfig` (this needs `google-adk` v2.10.0 or later). In the Interactions API, pass `service_tier="deferred"` on the `global` endpoint. It covers `gemini-4-carbon`, `gemini-4-argon`, the Gemini 3.x Flash models and `gemini-3.1-pro-preview`. The release notes say Deferred is billed at a 50% discount.
**Why it matters:** Batch-like agent jobs such as nightly triage, backfills and evals can run at half price without being rewritten for a batch API.
Source: [Agent Platform release notes](https://docs.cloud.google.com/gemini-enterprise-agent-platform/release-notes) · Added: 2026-11-24

### Agent Gateway: cross-cloud and GKE previews · 2026-11-11 → 12 🆕
Agent Gateway enforces connectivity and security policies, including Model Armor, between agents and tools. It entered a cross-cloud Limited Preview on 2026-11-11. **Agent Gateway for GKE** reached Preview on 2026-11-12; it needs GKE 1.37.2-gke.1042000 or later and runs in `europe-west1` and `us-central1`.
**Why it matters:** You can put one policy point in front of agents running on GKE or on other clouds, instead of adding auth and filtering to each agent.
Source: [Agent Platform release notes](https://docs.cloud.google.com/gemini-enterprise-agent-platform/release-notes) · Added: 2026-11-24

### Model Garden: Claude Fable 5.2 with Fast mode, plus new partner and open models · 2026-10-27 → 11-16 🆕
`claude-fable-5-2` went GA on 2026-11-09, alongside GA of Fast mode for Claude (`"speed": "fast"`), with Fable 5.2 as the first supported model. Other partner and open models added in this period:

| Date | Model | Status |
|---|---|---|
| 2026-10-27 | Grok 4.7 | GA on `global` and the US multi-region |
| 2026-11-09 | Meta Muse: `meta/muse-wonder-1.0`, `meta/muse-ember-1.0`, `meta/muse-spark-1.3` | Preview on `global` |
| 2026-11-16 | DeepSeek-V4.1-Flash-1017 (managed API, up to 1M context) | Public Preview |

**Why it matters:** You can call Anthropic, xAI, Meta and DeepSeek models under the same IAM, billing and VPC-SC as Gemini. Compare with [Bedrock](../aws/README.md) if you run on both clouds. Model details are in [LLM news](../../models/news/README.md).
Source: [Agent Platform release notes](https://docs.cloud.google.com/gemini-enterprise-agent-platform/release-notes) · Added: 2026-11-24

### Tuned Gemini 3.x models: global serving and Provisioned Throughput · 2026-10-19 → 11-04 🆕
Supervised fine-tuning went GA for `gemini-3.5-flash-lite`, `gemini-3.5-flash` and `gemini-3.1-flash-lite` on 2026-10-19 (in the `us` and `eu` multi-regions, with CMEK). Tuned Gemini 3.x models can be served on `global` endpoints from 2026-11-02, after you copy them with Model Registry `models:copy`. Provisioned Throughput for fine-tuned models went GA on 2026-11-04.
**Why it matters:** A tuned model can now run in production with reserved capacity and global routing, which removes the main reason to avoid tuning for latency-critical paths. Note that `gemini-3.5-flash` and `gemini-3.1-flash-lite` are scheduled to retire on or after May 2027. See [Fine-tuning](../../models/fine-tuning/README.md).
Source: [Agent Platform release notes](https://docs.cloud.google.com/gemini-enterprise-agent-platform/release-notes) · Added: 2026-11-24

---

## ☕ Spring & JVM on Google Cloud

- **Spring AI 2.1.0:** use the `spring-ai-starter-model-google-genai` starter. Set `spring.ai.google.genai.project-id` and `spring.ai.google.genai.location` and leave `api-key` unset to call Agent Platform (Vertex mode); setting `api-key` switches to the Gemini Developer API. The old `spring-ai-vertex-ai-gemini` module **has been removed**. To migrate, change the package `org.springframework.ai.vertexai.gemini` to `org.springframework.ai.google.genai` and the property prefix `spring.ai.vertex.ai.gemini` to `spring.ai.google.genai`. ([Spring AI: Google GenAI Chat](https://docs.spring.io/spring-ai/reference/api/chat/google-genai-chat.html))
- **Plain Java:** the generative classes in `com.google.cloud:google-cloud-vertexai` are gone from SDK releases after 2026-06-24; use `com.google.genai:google-genai`. ([migration guide](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/deprecations/genai-vertexai-sdk))
- **ADK for Java:** see [JVM libraries](../../build/libraries/jvm.md) and [google/adk-java](https://github.com/google/adk-java).

---

## 📚 Reference

- [Agent Platform release notes](https://docs.cloud.google.com/gemini-enterprise-agent-platform/release-notes): the primary feed for this page
- [Model versions and retirement dates](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/learn/model-versions)
- [Agent Platform docs](https://docs.cloud.google.com/gemini-enterprise-agent-platform) · [Agent Runtime](https://docs.cloud.google.com/gemini-enterprise-agent-platform/build/runtime)
- [Google Cloud MCP servers](https://docs.cloud.google.com/mcp/overview)
- [ADK docs](https://google.github.io/adk-docs/) · GitHub: [adk-python](https://github.com/google/adk-python) · [adk-java](https://github.com/google/adk-java) · [adk-js](https://github.com/google/adk-js) · [adk-go](https://github.com/google/adk-go)
- [Google Cloud blog: AI & Machine Learning](https://cloud.google.com/blog/products/ai-machine-learning)
