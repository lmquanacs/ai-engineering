# Starter skills

Copy one of these into your project, edit the commands and rules so they match your repo, and commit it. Your coding agent will then follow **your** conventions, not generic ones.

| Skill | For | Copy |
|---|---|---|
| [python-service](python-service/SKILL.md) | Python services with uv, ruff, pytest, Pydantic v2 / FastAPI | `cp -r python-service <your-repo>/.claude/skills/` |
| [typescript-service](typescript-service/SKILL.md) | TypeScript/Node services with pnpm, strict tsconfig, Vitest | `cp -r typescript-service <your-repo>/.claude/skills/` |
| [spring-boot-kotlin](spring-boot-kotlin/SKILL.md) | Spring Boot 4 + Kotlin with Gradle Kotlin DSL | `cp -r spring-boot-kotlin <your-repo>/.claude/skills/` |

**Tips**
- Keep the `description` short and specific. It is the only part the agent sees until the skill triggers.
- Put long reference material (API conventions, error catalogues) in separate files next to `SKILL.md` and link to them, so they load only when needed.
- Whenever the agent makes a mistake twice, add a rule. That habit is the core of harness engineering.
