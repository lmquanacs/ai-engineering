# Agent skills · ☕ Java / Kotlin + Spring Boot

← [Back to Agent skills](README.md) · _Last updated: 2026-11-23_

> Skills that make agents write idiomatic Spring Boot 4 code in Java or Kotlin, including Gradle Kotlin DSL builds. Also see the [Spring Boot + Kotlin starter skill](starter-skills/spring-boot-kotlin/SKILL.md).

## ⭐ Start here

### kotlin/kotlin-agent-skills · official JetBrains Kotlin skills 🆕
JetBrains' own skill collection (incubator status), named `kotlin-<category>-<name>`. For Spring work the key one is `kotlin-backend-jpa-entity-mapping`: entity design, identity and `equals`/`hashCode`, relationships and fetch plans, and Kotlin-specific JPA traps such as using `data class` for entities. The `tooling` skills cover Java-to-Kotlin conversion, AGP 9 and immutable-collections migrations, and moving Gradle builds to the Kotlin toolchain.
**Why it matters:** It comes from the language's maintainers, and the JPA skill targets the bugs agents most often write in Kotlin + Spring Data code (N+1 queries, `LazyInitializationException`, broken equality).
```bash
npx skills add Kotlin/kotlin-agent-skills
# Claude Code plugin form (also adds the Kotlin docs MCP server, https://mcp.kotlinlang.org/mcp):
claude plugin marketplace add Kotlin/kotlin-agent-skills
claude plugin install kotlin-agent-skills@Kotlin
```
Note: the plugin turns on a remote MCP server (no credentials needed) automatically; use the skills CLI or copy single skill folders if you only want the skills.
Source: [github.com/kotlin/kotlin-agent-skills](https://github.com/kotlin/kotlin-agent-skills) · 10 skills, ~14.3K installs, `kotlin-backend-jpa-entity-mapping` ~1.9K on [skills.sh](https://skills.sh/kotlin/kotlin-agent-skills) (2026-11-23) · Added: 2026-11-23

### kotlin-springboot · `github/awesome-copilot`
Best practices for idiomatic Spring Boot with Kotlin: constructor injection, immutability, package structure, and using Kotlin features rather than Java-style code. About 9.8K installs (2026-11-23).
**Why it matters:** It is maintained in GitHub's official awesome-copilot repo and works in Claude Code, Copilot and others through the open skill format.
```bash
npx -y skills add github/awesome-copilot --skill kotlin-springboot --agent claude-code
```
Source: [github.com/github/awesome-copilot/skills/kotlin-springboot](https://github.com/github/awesome-copilot/tree/main/skills/kotlin-springboot) · Added: 2026-11-18

### create-spring-boot-kotlin-project · `github/awesome-copilot`
Scaffolds a Spring Boot + Kotlin project skeleton (Java 21, Docker and Docker Compose for backing services, Gradle).
**Why it matters:** It gives agents a consistent, reproducible starting point for new services.
```bash
npx -y skills add github/awesome-copilot --skill create-spring-boot-kotlin-project --agent claude-code
```
Source: [claudemarketplaces.com listing](https://claudemarketplaces.com/skills/github/awesome-copilot/create-spring-boot-kotlin-project) · Added: 2026-11-18

### spring-boot-skills · `rrezartprebreza/spring-boot-skills`
Eighteen production-oriented Spring Boot skills, for example `rest-api-conventions` and `spring-data-jpa`. Each one has a `SKILL.md` stating when it should trigger. You can drop individual skills into `.claude/skills/`.
**Why it matters:** The skills are granular, so you install only the conventions you want, such as your REST and JPA rules.
```bash
mkdir -p .claude/skills
cp -r spring-boot-skills/skills/rest-api-conventions .claude/skills/
```
Source: [github.com/rrezartprebreza/spring-boot-skills](https://github.com/rrezartprebreza/spring-boot-skills) · Added: 2026-11-18

### sub-kopring-engineer (community)
A Kotlin/Java Spring Boot workflow skill that generates hexagonal-architecture code with JPA, jOOQ and test conventions, in Brainstorm → Plan → Implement → Verify phases.
**Why it matters:** It enforces an architecture as well as code style, which helps on larger services.
Source: [claudskills.com/skills/sub-kopring-engineer](https://claudskills.com/skills/sub-kopring-engineer/) · Added: 2026-11-18

### kotlin-spring-boot · `ashchupliak/dream-team`
An alternative Kotlin + Spring Boot skill from a team-of-agents plugin.
```bash
npx -y skills add ashchupliak/dream-team --skill kotlin-spring-boot --agent claude-code
```
Source: [claudemarketplaces.com listing](https://claudemarketplaces.com/skills/ashchupliak/dream-team/kotlin-spring-boot) · Added: 2026-11-18

## 🌱 Skills *inside* your Spring app (Spring AI)

Spring AI can also run skills inside your own agents, not only in your coding tool:

- **Generic agent skills:** LLM-agnostic skills that run in your environment (Spring AI agentic patterns, part 1, Jan 2026). [spring.io blog](https://spring.io/blog/2026/01/13/spring-ai-generic-agent-skills)
- **Anthropic native Skills API support:** cloud-side document generation and custom skills from Spring AI (Jan 2026). [spring.io blog](https://spring.io/blog?page=161)

## 💡 Idea worth stealing

At Spring I/O 2026, Sébastien Deleuze (Spring/Kotlin lead) argued for **turning your team's idiomatic Kotlin and Spring Boot practices into agent skills**: the build system, Gradle Kotlin DSL and the Kotlin 2.x baseline (Boot 4.1 → Kotlin 2.3, Boot 4.2 → Kotlin 2.4). The [starter skill](starter-skills/spring-boot-kotlin/SKILL.md) does exactly that.

Source: [Idiomatic Kotlin applications with Spring Boot 4 (slides)](https://2026.springio.net/slides/idiomatic-kotlin-applications-with-spring-boot-4-springio16.pdf) · Added: 2026-11-18
