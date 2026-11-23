# LLM APIs & structured output

_Last updated: 2026-11-24_

> The provider API features you write code against: structured outputs, tool calling, streaming, batch and files, and the breaking changes between versions. Model launches live in [LLM news](../../models/news/README.md); prices in [Inference & cost](../../models/cost-and-serving/README.md).

## 🧭 Feature map

| Feature | What to check before relying on it | Why it matters |
|---|---|---|
| **Structured outputs / JSON schema** | Is the schema *enforced* (constrained decoding) or only requested? Which schema keywords are supported? | Enforced schemas remove a whole class of parse failures and retries |
| **Tool / function calling** | Parallel calls, forced tool choice, strict argument schemas, max tools | Agents live or die on reliable tool calls; keep tool lists short |
| **Streaming** | Event format, partial JSON for tool arguments, how errors arrive mid-stream | Perceived latency and UX; error handling differs from non-streaming |
| **Batch** | Discount, turnaround window, size limits | Usually the cheapest way to run evals and backfills |
| **Files & citations** | Upload limits, retention, whether citations point at exact spans | Grounded answers without building your own RAG for small corpora |
| **Built-in tools** | Web search, code execution, computer use: pricing and data handling | Saves building infra, but check how they are billed and logged |

**Portability rule:** keep a thin internal interface (messages, tools, schema) and adapt per provider, or use a library that does it ([Libraries](../libraries/README.md)). Pin model IDs and re-run evals before switching.

**Validation libraries:** Pydantic (Python), Zod (TypeScript) and Jackson/records (JVM) define the schema once; libraries such as Instructor, Outlines and BAML add retries and constrained decoding where the provider doesn't.

---

## 🗞️ Latest

<!-- newest first: new API features, breaking changes, migration guides -->

### Anthropic: Enterprise Frontier Safeguards (beta) and storage webhooks · 2026-11-23 🆕
Enterprise Frontier Safeguards (EFS) is now in beta on Claude Platform, Claude Platform on AWS and Claude Models on Google Cloud (Anthropic managed). Eligible organizations get Zero Data Retention while encrypted copies of prompts and responses ("Sealed Safety Data") are written to a bucket in their own cloud account; workspaces left on Anthropic-managed storage are not covered. Two new organization webhook events, `external_storage.failed` and `external_storage.recovered`, fire when that bucket fails or passes Anthropic's daily check.
**Why it matters:** It is the route to ZDR-style data handling for teams that need it. If you enable it, wire up the storage webhooks, because a misconfigured bucket is now something you have to monitor.
Source: [Claude release notes](https://platform.claude.com/docs/en/release-notes/overview) · [EFS setup guide](https://platform.claude.com/docs/en/manage-claude/enterprise-frontier-safeguards/setup-console) · Added: 2026-11-24

### OpenAI: `/v1/prompts`, Evals API and Agent Builder shut down 2026-11-30 🆕
Announced on 2026-06-03 and still on the deprecations page: reusable prompt objects (`/v1/prompts`), the Evals dashboard, API and graders, and Agent Builder all stop working on 2026-11-30. OpenAI's suggested replacements are prompt text kept in your own code, Promptfoo for evals, and the Agents SDK or ChatKit for Agent Builder flows.
**Why it matters:** Code that references stored prompt IDs or calls the Evals API breaks next Monday. Grep for them now. Model retirements on the same page are in [LLM news](../../models/news/README.md#-action-items).
Source: [OpenAI deprecations](https://developers.openai.com/api/docs/deprecations) · Added: 2026-11-24

### OpenAI: standby mode for GPT-Live WebRTC sessions · 2026-11-19 🆕
GPT-Live-1 and GPT-Live-1.1 WebRTC sessions can enter a standby mode that pauses inference while the session is inactive and resumes when someone speaks. The same changelog entry adds `gpt-live-1.1`, which you select in an existing Live session configuration (`v1/live/sessions`); see [LLM news](../../models/news/README.md).
**Why it matters:** Long-open voice sessions (call centres, assistants left running) stop doing inference work while nobody is talking.
Source: [OpenAI API changelog](https://developers.openai.com/api/docs/changelog) · Added: 2026-11-22

### Google: tool retrieval for the Gemini Interactions API (preview) · 2026-11-19 🆕
Mark function or `mcp_server` tools with `defer_loading: true` and add a `{"type": "tool_search"}` tool: the model sees only each deferred tool's name and description and loads the full schema when it needs it, within the same request (`execution: "client"` lets your app run the lookup). Works with Gemini 3.6 and later, including Gemini 4. No separate fee: enabling it adds a small fixed block of input tokens, and each loaded schema is billed as input for the rest of the conversation.
**Why it matters:** Agents with large tool or MCP catalogues stop paying for every schema on every turn; it's the same deferred-loading pattern Anthropic and OpenAI already offer.
Source: [Google blog: Gemini API tool retrieval](https://blog.google/innovation-and-ai/technology/developers-tools/gemini-api-tool-retrieval/) · Added: 2026-11-21

### Google: logprobs requests to Gemini 4 now fail with 400 (user-reported) · 2026-11-20 🆕
Developers report that since about 02:00 UTC on 2026-11-20, requests asking for logprobs on `gemini-4-hydrogen`, `-argon`, `-carbon` and `-neon` return 400. There is no changelog entry, and the forum reply saying logprobs are unsupported is not from a confirmed Google account.
**Why it matters:** Confidence scoring and judge pipelines that read Gemini logprobs will break; the [Decisions API](../../models/news/README.md#-new-techniques) is Google's probability-returning alternative.
Source: [Google AI Developers Forum thread](https://discuss.ai.google.dev/t/logprobs-turned-off-without-notice-for-gemini-4-hydrogen-argon-carbon-and-neon/203009) (not a vendor announcement) · Added: 2026-11-21

### OpenAI: GPT-6.2 Responses API changes + background completion windows · 2026-11-17 🆕
- **GPT-6.2 migration:** tool calling with `gpt-6.2-astra` / `gpt-6.2-sol` requires the Responses API, reasoning effort `none` is rejected, and the handling of top-level `instructions` and of reasoning after prefix edits changes (caching details → [Context engineering](../../architecture/context-and-memory/README.md#-latest-evidence)).
- **Background completion windows** (public beta): on `v1/responses`, set `background: true`, `background_options.completion_window` to `"2h"` or `"8h"` and `service_tier: "default"`, without streaming. Collect results from the `response.completed` webhook or by polling. Supported on `gpt-6.2-astra`, `gpt-6.2-sol`, `gpt-6.1-terra` and `gpt-6-luna`. The window is a target, not a guarantee. (Discounts → [Inference & cost](../../models/cost-and-serving/README.md).)

**Why it matters:** Chat Completions tool-calling code won't carry over to GPT-6.2, and background windows are a simpler alternative to the Batch API for evals and backfills.
Sources: [OpenAI API changelog](https://developers.openai.com/api/docs/changelog) · [Migration guide](https://developers.openai.com/api/docs/guides/latest-model?model=gpt-6.2-astra#gpt-6.2-astra-migration-quickstart) · [Background mode guide](https://developers.openai.com/api/docs/guides/background#use-discounted-completion-windows) · Added: 2026-11-20

### Anthropic: linked billing (beta) · 2026-11-17 🆕
With beta header `user-profiles-billing-2026-10-01`, a `billing_policy` field on `/v1/messages` and `/v1/chat/completions` decides who pays for a request: your app, or the end customer's own Claude organization. Customers can cap or unlink your app's spend in the Console. Only customers whose organization pays Anthropic directly for API usage can be linked.
**Why it matters:** B2B apps can pass inference cost through to customers instead of re-billing it.
Source: [Claude release notes](https://platform.claude.com/docs/en/release-notes/overview) · Added: 2026-11-20

### DeepSeek: built-in web search, URL reading and file input · 2026-11-13 🆕
For `deepseek-flash`, in the Messages, Responses and Chat Completions formats: a built-in `deepseek_web_search` tool that answers with citations (also with thinking on), a `deepseek_read_url` tool for links in user messages, and file input that parses PDFs, Office files and images into context. Standalone Search/Fetch, OCR, ASR and TTS APIs shipped at the same time.
**Why it matters:** DeepSeek now runs search and document handling server-side, like Anthropic and OpenAI. Billing for these changed on 2026-11-18 → [Inference & cost](../../models/cost-and-serving/README.md).
Sources: [DeepSeek API updates](https://api-docs.deepseek.com/updates) · [Web tools guide](https://api-docs.deepseek.com/guides/web_tools) · Added: 2026-11-20

### Anthropic: thinking-block prefix check now enforced · 2026-11-09 🆕
If you edit `system`, `tools` or an earlier message and then send back a thinking block from a later turn, the request now returns **400** for all accounts. The `prefix_mismatch_behavior` parameter chooses between the error and having the API drop the failing blocks; the response's `input_transformations` lists what was dropped or let through.
**Why it matters:** Agent loops that trim or rewrite history while preserving thinking can start failing. Decide which behaviour you want and set it explicitly.
Source: [Claude docs: preserved thinking, enforcement](https://platform.claude.com/docs/en/build-with-claude/preserved-thinking#enforcement) · Added: 2026-11-20

### Anthropic: computer use moves to `computer_toolset_20260801` · 2026-11-09 🆕
Requests that declare the older `computer_20251124` tool now return 400 on every platform except Amazon Bedrock. The docs include a migration section.
**Why it matters:** Computer-use integrations stop working until migrated. → [Voice & multimodal](../voice-and-multimodal/README.md)
Source: [Claude docs: migrate from computer_20251124](https://platform.claude.com/docs/en/agents-and-tools/tool-use/computer-use-tool#migrate-from-computer-20251124) · Added: 2026-11-20

Library check (PyPI, 2026-11-24): no new releases of Instructor (1.17.0), Outlines (1.3.3) or BAML (`baml-py` 0.226.3) in the window. Gemini API and Mistral changelogs had no new entries (DeepSeek updates page could not be read); xAI retired `grok-build-0.1` on 2026-11-19.

## 📚 Reference

<!-- older or background entries -->
