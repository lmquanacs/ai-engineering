---
name: spring-boot-kotlin
description: Conventions for Spring Boot 4 services written in Kotlin with Gradle Kotlin DSL (build.gradle.kts), JUnit 5, MockK and Testcontainers. Use whenever editing .kt or .kts files, adding dependencies, writing tests, or creating controllers, services or repositories.
---

# Spring Boot 4 + Kotlin conventions

## Toolchain (always use these commands)
- Build + test: `./gradlew build`
- Tests only: `./gradlew test` (one class: `./gradlew test --tests '*OrderServiceTest'`)
- Format/lint: `./gradlew ktlintFormat` (or `spotlessApply`)
- Run locally: `./gradlew bootRun` with `docker compose up -d` for backing services

## Build (Gradle Kotlin DSL)
- Declare dependencies through the version catalog `gradle/libs.versions.toml`; never hard-code versions in `build.gradle.kts`.
- Keep the `kotlin("plugin.spring")` and `kotlin("plugin.jpa")` plugins (they open classes and generate no-arg constructors).
- JVM toolchain 21+: `kotlin { jvmToolchain(21) }`. Compiler flag `-Xjsr305=strict`.

## Code rules
- Constructor injection only; no `@Autowired` fields and no `lateinit` for beans.
- Immutable `data class` DTOs; never expose JPA entities from controllers.
- Use nullability instead of `Optional`; `findByIdOrNull` for repositories.
- Configuration through `@ConfigurationProperties` data classes, not `@Value`.
- Controllers stay thin; transactions (`@Transactional`) go on service methods, not controllers.
- Errors: domain exceptions mapped in one `@RestControllerAdvice` that returns `ProblemDetail`.
- Coroutines only end to end (WebFlux/R2DBC); do not mix blocking JPA calls into `suspend` functions.
- Spring AI: put LLM calls behind an interface; tools are `@Tool` methods on beans; MCP servers use `@McpTool`.

## Tests
- JUnit 5 + **MockK** (`springmockk` for `@MockkBean`); AssertJ or Kotest assertions.
- Slice tests (`@WebMvcTest`, `@DataJpaTest`) for layers; Testcontainers with `@ServiceConnection` for databases.
- Name tests with backticks: `` `rejects order when stock is insufficient` ``.

## Before finishing
Run `./gradlew build` and report the result; fix every warning introduced by your change.
