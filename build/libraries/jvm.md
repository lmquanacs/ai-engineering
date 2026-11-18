# Libraries · ☕ JVM (Java / Kotlin / Spring Boot)

← [Back to Libraries](README.md) · _Last updated: 2026-11-19_

| Library | Latest confirmed | What it is | Pick it when |
|---|---|---|---|
| [**Spring AI**](https://github.com/spring-projects/spring-ai) | 2.0.2 (2026-10-22); 2.1.0-RC2 (2026-11-05) | Spring-native LLM framework: ChatClient, advisors, tool calling, RAG, memory, observability, MCP client/server. **2.0 requires Spring Boot 4.** | Any Spring Boot service adding AI |
| [**Embabel**](https://github.com/embabel/embabel-agent) | 1.5.4 (2026-10-28) | Goal-oriented agent framework by Rod Johnson (creator of Spring). Uses **GOAP planning** (A* search) over typed Java/Kotlin domain objects and runs on top of Spring AI. | Multistep agents where you want deterministic, type-safe, replannable flows |
| [**Koog**](https://github.com/JetBrains/koog) | 1.3.0 (2026-09-23) | JetBrains' Kotlin agent framework with a type-safe DSL. Kotlin Multiplatform (JVM, Android, iOS, JS, Wasm), A2A support, persistence, plus a Java builder API. | Kotlin-first teams, or agents that must run on mobile and server alike |
| [**LangChain4j**](https://github.com/langchain4j/langchain4j) | 1.24.0 (2026-11-18) | Framework-agnostic Java LLM library with integrations for Spring Boot, Quarkus and Micronaut, plus a `langchain4j-agentic` module | Non-Spring stacks (Quarkus/Micronaut) or the widest provider coverage |
| [**MCP Java SDK**](https://java.sdk.modelcontextprotocol.io/latest/) (`io.modelcontextprotocol.sdk:mcp`) | 2.2.0 (2026-11-13) | Official MCP SDK for Java; one module implements both the stateless 2026-07-28 spec ("modern") and 2025-11-25 and earlier ("legacy") | Plain-Java MCP servers/clients; Spring AI builds its MCP support on it |
| [**LangGraph4j**](https://github.com/bsorrentino/langgraph4j) | — | Stateful multi-agent graphs inspired by LangGraph; works with LangChain4j and Spring AI, has a Studio UI | Explicit graph control flow on the JVM |
| [**Google ADK (Java)**](https://github.com/google/adk-java) | — | Google's code-first Agent Development Kit with A2A; Gemini-native, other models via LangChain4j | Gemini/Google Cloud shops |
| **Quarkus LangChain4j** | — | Red Hat/IBM-maintained Quarkus extension; GraalVM native, Dev UI | Quarkus services |

## 🆕 Notable changes

### Spring AI 2.0: a rebuilt foundation on Boot 4 🆕
GA on 2026-06-12. It needs Spring Boot 4.0/4.1 and Spring Framework 7. MCP annotations (`@McpTool`, `@McpResource`, `@McpPrompt`) and the WebMVC/WebFlux MCP transports moved into core, and tool calling became composable. Teams staying on Boot 3.x keep receiving patches on the 1.1.x line.
**Why it matters:** The upgrade path is Boot 4 first, then Spring AI 2.0.
Sources: [Spring AI 2.0.0 GA](https://spring.io/blog/2026/06/12/spring-ai-2-0-0-GA-available-now/) · [Visual Studio Magazine](https://visualstudiomagazine.com/articles/2026/06/29/spring-ai-2-0-goes-ga-giving-java-developers-a-more-mature-ai-app-stack.aspx) · Added: 2026-11-18

### Spring AI Agents: planned for November 2026 🆕
The 2.1.0-M1 notes say new agentic support will ship in **November 2026** as a separate Spring Projects Experimental project, with a plan to merge it into **Spring AI 3.0** in mid-2027.
**Why it matters:** Watch this for a Spring-native way to orchestrate agent CLIs such as Claude Code and Codex. The daily job will flag the release.
Source: [Spring AI 2.1.0-M1](https://spring.io/blog/2026/09/25/spring-ai-2-1-0-M1-available-now/) · Added: 2026-11-18

### Spring Boot 4.1 → 4.2 🆕
Boot 4.1 (2026-06-10) added gRPC auto-configuration, HTTP-client SSRF mitigation, OpenTelemetry environment-variable support and a **Kotlin 2.3** baseline. **Boot 4.2 is expected in November 2026** with the AMQP 1.0 module, and Kotlin 2.4 is expected as its baseline. As of 2026-11-19 the latest on Maven Central is **4.2.0-RC2** (2026-11-05), with 4.1.2 (2026-10-22) the latest GA; Spring AI 2.1.0-RC2 shipped the same day.
Sources: [Maven Central: spring-boot](https://repo1.maven.org/maven2/org/springframework/boot/spring-boot/maven-metadata.xml) · [InfoQ: Spring Boot 4.1](https://infoq.com/news/2026/06/spring-boot-4-1) · [Spring I/O slides (Kotlin baselines)](https://2026.springio.net/slides/idiomatic-kotlin-applications-with-spring-boot-4-springio16.pdf) · Added: 2026-11-18

## 🧭 How they fit together

```
Spring Boot 4 ──► Spring AI 2.0 (LLM plumbing, tools, MCP, RAG)
                    ├──► Embabel (typed planning / orchestration layer)
                    └──► your @McpTool beans exposed to any MCP client
Kotlin-first / multiplatform ──► Koog
Quarkus / Micronaut ──► LangChain4j (+ LangGraph4j for graphs)
```

Version numbers confirmed on 2026-11-19 at [Maven Central](https://repo1.maven.org/maven2/) (artifact publish dates).
