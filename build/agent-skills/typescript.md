# Agent skills · 🟦 TypeScript

← [Back to Agent skills](README.md) · _Last updated: 2026-11-23_

> Skills for TypeScript, Node.js and React/Next.js work. Also see the [TypeScript starter skill](starter-skills/typescript-service/SKILL.md).

## ⭐ Start here

### fastify-best-practices · `mcollina/skills` 🆕
Matteo Collina's Fastify skill covers routes, plugins, JSON Schema validation and serialization, hooks and the request lifecycle, error handling, Pino logging, testing with `inject`, and TypeScript via type stripping. The same repo has `node`, `typescript-magician`, `nodejs-core`, `oauth` and `linting-neostandard-eslint9` skills.
**Why it matters:** With ~107K installs it is by far the most-used Fastify skill, and it passes the skills.sh security audits (Gen Agent Trust Hub, Socket, Snyk); install it alongside your own skill that pins the test runner and lint setup.
```bash
npx skills add https://github.com/mcollina/skills --skill fastify-best-practices
```
Source: [github.com/mcollina/skills](https://github.com/mcollina/skills) · ~106.7K installs on [skills.sh](https://skills.sh/mcollina/skills/fastify-best-practices) (2026-11-23) · Added: 2026-11-23

### Vercel React best practices · `vercel-labs`
Vercel's own guidance on React and Next.js performance and patterns, packaged as a skill. One of the ten most-installed skills overall (~599K installs per Skillselion, Aug 2026).
**Why it matters:** It comes from the team that maintains Next.js, which makes it the most authoritative React skill available.
Source: [Skillselion: State of AI Agent Skills 2026](https://skillselion.com/state-of-ai-agent-skills-2026) · Added: 2026-11-18

### typescript-expert · nodejs-best-practices · `sickn33/antigravity-awesome-skills`
The most-installed TypeScript and Node skills in a 1,436-skill collection: `nodejs-best-practices` (~8.1K installs), `typescript-expert` (~7.1K) and `api-security-best-practices` (~6.4K).
**Why it matters:** These are general-purpose TS/Node guardrails. Pair them with a project skill that pins your tsconfig and test runner.
```bash
npx -y skills add sickn33/antigravity-awesome-skills --skill typescript-expert --agent claude-code
```
Source: [skills.sh/sickn33/antigravity-awesome-skills](https://skills.sh/sickn33/antigravity-awesome-skills) · Added: 2026-11-18

### typescript-advanced-types
Generics, conditional, mapped and template-literal types, and utility types, for building type-safe libraries and APIs.
**Why it matters:** Agents often reach for `any` when the type gets hard. This skill pushes them to model the type properly.
Source: [skills.sh/ovachiever/droid-tings](https://skills.sh/ovachiever/droid-tings) · Added: 2026-11-18

### dogfood · `vercel-labs/agent-browser`
Browser-driven self-testing for web apps. See [Agent skills](README.md#dogfood--vercel-labsagent-browser).

### find-skills · `vercel-labs`
The single most-installed skill in the ecosystem (~3M installs, Aug 2026). It finds and installs other skills for the task at hand.
Source: [Skillselion report](https://skillselion.com/state-of-ai-agent-skills-2026) · Added: 2026-11-18

## 🧩 Write your own

Encode the parts that differ between repos: package manager (`pnpm`/`bun`), `tsconfig` strictness, test runner (Vitest/Jest), lint (Biome/ESLint), runtime (Node/Bun/edge) and framework (Next.js, Hono, NestJS).

→ Template: [starter-skills/typescript-service/SKILL.md](starter-skills/typescript-service/SKILL.md)

## 🔭 Watching

- **Vercel AI SDK 7 harness adapters**. They let you run Claude Code, Codex and others as agents from TypeScript. See [Libraries · TypeScript](../libraries/typescript.md).
