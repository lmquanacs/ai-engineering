# 05 · Libraries: Python · TypeScript · JVM

_Last updated: 2026-11-18_

> Agent and LLM application libraries, with the latest version we confirmed and when to choose each one.

| Stack | Page | Default pick | When to pick something else |
|---|---|---|---|
| 🐍 Python | [python.md](python.md) | **Pydantic AI v2**: typed agents, MCP, evals | **LangGraph** when you need an explicit state graph and durable checkpoints |
| 🟦 TypeScript | [typescript.md](typescript.md) | **Vercel AI SDK 7**: model calls, tool loops, streaming UI, harness adapters | **Mastra** for the full stack (agents, memory, workflows, evals) in one framework |
| ☕ JVM | [jvm.md](jvm.md) | **Spring AI 2.0**: Spring-native ChatClient, tools, MCP, RAG | **Embabel** (typed GOAP planning on top of Spring AI), **Koog** (Kotlin Multiplatform), **LangChain4j** (framework-agnostic) |

**General advice:** Write the agent loop without a framework first. Adopt a framework when it removes code you would otherwise maintain, such as memory, tracing, retries or MCP plumbing.
