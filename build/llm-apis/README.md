# LLM APIs & structured output

_Last updated: 2026-11-20_

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

## 📚 Reference

<!-- older or background entries -->
