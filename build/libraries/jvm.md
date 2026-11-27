# Libraries · ☕ JVM (Java / Kotlin / Spring Boot)

← [Back to Libraries](README.md) · _Last updated: 2026-11-28_

| Library | Latest confirmed | What it is | Pick it when |
|---|---|---|---|
| [**Spring AI**](https://github.com/spring-projects/spring-ai) | **2.1.0 (2026-11-19; announced 11-20)**; 2.0.3 for 2.0.x | Spring-native LLM framework: ChatClient, advisors, tool calling, RAG, memory, observability, MCP client/server. **2.0 requires Spring Boot 4; 2.1 is built on Boot 4.2.** | Any Spring Boot service adding AI |
| [**Embabel**](https://github.com/embabel/embabel-agent) | 1.5.4 (2026-10-28) | Goal-oriented agent framework by Rod Johnson (creator of Spring). Uses **GOAP planning** (A* search) over typed Java/Kotlin domain objects and runs on top of Spring AI. | Multistep agents where you want deterministic, type-safe, replannable flows |
| [**Koog**](https://github.com/JetBrains/koog) | 1.3.0 (2026-09-23) | JetBrains' Kotlin agent framework with a type-safe DSL. Kotlin Multiplatform (JVM, Android, iOS, JS, Wasm), A2A support, persistence, plus a Java builder API. | Kotlin-first teams, or agents that must run on mobile and server alike |
| [**LangChain4j**](https://github.com/langchain4j/langchain4j) | 1.24.1 / 1.24.1-beta34 (2026-11-26); the Tika parser now caps extracted text, see below | Framework-agnostic Java LLM library with integrations for Spring Boot, Quarkus and Micronaut, plus a `langchain4j-agentic` module | Non-Spring stacks (Quarkus/Micronaut) or the widest provider coverage |
| [**MCP Java SDK**](https://java.sdk.modelcontextprotocol.io/latest/) (`io.modelcontextprotocol.sdk:mcp`) | 2.2.0 (2026-11-13) | Official MCP SDK for Java; one module implements both the stateless 2026-07-28 spec ("modern") and 2025-11-25 and earlier ("legacy") | Plain-Java MCP servers/clients; Spring AI builds its MCP support on it |
| [**LangGraph4j**](https://github.com/bsorrentino/langgraph4j) | — | Stateful multi-agent graphs inspired by LangGraph; works with LangChain4j and Spring AI, has a Studio UI | Explicit graph control flow on the JVM |
| [**Google ADK (Java)**](https://github.com/google/adk-java) | — | Google's code-first Agent Development Kit with A2A; Gemini-native, other models via LangChain4j | Gemini/Google Cloud shops |
| **Quarkus LangChain4j** | — | Red Hat/IBM-maintained Quarkus extension; GraalVM native, Dev UI | Quarkus services |

## 🆕 Notable changes

### LangChain4j 1.24.1: Apache Tika parser stops at 10,000,000 characters · 2026-11-26 🆕
The GitHub release has no notes, but the published sources show the change. In `langchain4j-document-parser-apache-tika` 1.24.1-beta34, `ApacheTikaDocumentParser`'s default content handler extracts at most 10,000,000 characters. Previously it had no limit. A longer document now makes `parse()` throw a `RuntimeException` caused by Tika's `WriteLimitReachedException`, where it used to return a `Document`. The parser gains a `builder()` with `maxCharacters` (`-1` restores unlimited extraction). `DEFAULT_CONTENT_HANDLER_SUPPLIER` and the two four-argument constructors are deprecated in favour of the builder. The Javadoc also warns that the cap limits text but not Tika's memory use. For untrusted files, it recommends running Tika's `ForkParser` in a separate process with its own heap limit.
**Why it matters:** RAG ingestion of very large documents can start failing after the upgrade, so set `maxCharacters` explicitly. The change matches the 10M default cap that Spring AI 2.1 added. Separately, the Elasticsearch and OpenSearch modules still pull `parsson` versions below 1.1.8, so keep any dependency override you already have.
Source: [LangChain4j 1.24.1 release](https://github.com/langchain4j/langchain4j/releases/tag/1.24.1) · [`ApacheTikaDocumentParser` Javadoc](https://docs.langchain4j.dev/apidocs/dev/langchain4j/data/document/parser/apache/tika/ApacheTikaDocumentParser.html) · sources jar 1.24.1-beta34 on [Maven Central](https://repo1.maven.org/maven2/dev/langchain4j/langchain4j-document-parser-apache-tika/) · Added: 2026-11-28

### Spring AI 2.1.0 and 2.0.3: Session API, tool approval, 13 CVE fixes · 2026-11-20 🆕
Spring AI 2.1 is built on Spring Boot 4.2, so upgrade the two together. It adds a Session API (event-log memory with turn-aware compaction) that replaces ChatMemory (now deprecated, removal planned for 3.0), tools marked `requiresConfirmation = true` that pause for human approval, per-turn tool-call limits (defaults 40 per tool and 150 in total, under `spring.ai.tools.limits.*`), a typed `DecisionModel` API, OpenAI Responses API support, `VectorStore.upsert()`, and client and server support for MCP 2026-07-28. It fixes 13 CVEs, one Critical (cross-user disclosure in the Redis semantic cache); 2.0.3 carries the same fixes for 2.0.x.
**Why it matters:** The 2.1 milestones and RCs lack the CVE fixes, so move to 2.1.0 (or 2.0.3) now. Check three behaviour changes: `SemanticCacheAdvisor` needs a `SemanticCacheScopeResolver` bean, Tika extraction is capped at 10,000,000 characters by default, and long agent loops can now hit `ToolCallLimitExceededException`.
Sources: [Spring AI 2.1.0 GA and 2.0.3](https://spring.io/blog/2026/11/20/spring-ai-2-1-0-GA-available-now) · [Upgrading to 2.1](https://docs.spring.io/spring-ai/reference/2.1-SNAPSHOT/upgrading/spring-ai-2-1.html) · Added: 2026-11-21

### Spring Boot 4.2.0: AMQP 1.0, `RestTemplate` deprecated · 2026-11-19 🆕
Highlights: AMQP 1.0 support (generic and RabbitMQ-specific), opt-in OpenTelemetry semantic conventions, SSL bundles for LDAP, registry-backed Buildpacks caches with Ubuntu 26.04 as the default base image, and faster executable-jar startup. `RestTemplate`/`TestRestTemplate` support is deprecated in favour of `RestClient`/`RestTestClient`, as is Apache Pulsar support. Patches 4.1.3 and 4.0.10 shipped on 2026-11-20.
**Why it matters:** Spring AI 2.1 needs it, and the `RestTemplate` deprecation is worth planning for now.
Sources: [Spring Boot 4.2.0 available now](https://spring.io/blog/2026/11/19/spring-boot-4-2-0-available-now) · [Spring Boot 4.2 release notes](https://github.com/spring-projects/spring-boot/wiki/Spring-Boot-4.2-Release-Notes) · Added: 2026-11-21

### Spring AI 2.0: a rebuilt foundation on Boot 4
GA on 2026-06-12. It needs Spring Boot 4.0/4.1 and Spring Framework 7. MCP annotations (`@McpTool`, `@McpResource`, `@McpPrompt`) and the WebMVC/WebFlux MCP transports moved into core, and tool calling became composable. Teams staying on Boot 3.x keep receiving patches on the 1.1.x line.
**Why it matters:** The upgrade path is Boot 4 first, then Spring AI 2.0.
Sources: [Spring AI 2.0.0 GA](https://spring.io/blog/2026/06/12/spring-ai-2-0-0-GA-available-now/) · [Visual Studio Magazine](https://visualstudiomagazine.com/articles/2026/06/29/spring-ai-2-0-goes-ga-giving-java-developers-a-more-mature-ai-app-stack.aspx) · Added: 2026-11-18

### Spring AI Agents: planned for early December 2026
The 2.1.0 GA post (2026-11-20) moves the date to **early December**: Spring AI Agent will ship under Spring Projects Experimental, built on Spring AI 2.1. The 2.1.0-M1 notes had said **November 2026** as a separate Spring Projects Experimental project, with a plan to merge it into **Spring AI 3.0** in mid-2027.
**Why it matters:** Watch this for a Spring-native way to orchestrate agent CLIs such as Claude Code and Codex. The daily job will flag the release.
Sources: [Spring AI 2.1.0 GA](https://spring.io/blog/2026/11/20/spring-ai-2-1-0-GA-available-now) · [Spring AI 2.1.0-M1](https://spring.io/blog/2026/09/25/spring-ai-2-1-0-M1-available-now/) · Added: 2026-11-18

### Spring Boot 4.1 → 4.2
Boot 4.1 (2026-06-10) added gRPC auto-configuration, HTTP-client SSRF mitigation, OpenTelemetry environment-variable support and a **Kotlin 2.3** baseline. **Boot 4.2 is expected in November 2026** with the AMQP 1.0 module, and Kotlin 2.4 is expected as its baseline. **4.2.0 GA** shipped on 2026-11-19 (see above).
Sources: [Maven Central: spring-boot](https://repo1.maven.org/maven2/org/springframework/boot/spring-boot/maven-metadata.xml) · [InfoQ: Spring Boot 4.1](https://infoq.com/news/2026/06/spring-boot-4-1) · [Spring I/O slides (Kotlin baselines)](https://2026.springio.net/slides/idiomatic-kotlin-applications-with-spring-boot-4-springio16.pdf) · Added: 2026-11-18

## 🧭 How they fit together

```
Spring Boot 4 ──► Spring AI 2.0 (LLM plumbing, tools, MCP, RAG)
                    ├──► Embabel (typed planning / orchestration layer)
                    └──► your @McpTool beans exposed to any MCP client
Kotlin-first / multiplatform ──► Koog
Quarkus / Micronaut ──► LangChain4j (+ LangGraph4j for graphs)
```

Version numbers confirmed on 2026-11-28 at [Maven Central](https://repo1.maven.org/maven2/) (artifact publish dates).
