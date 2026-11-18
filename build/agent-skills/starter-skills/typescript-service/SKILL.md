---
name: typescript-service
description: Conventions for writing, testing and reviewing TypeScript/Node code in this repository (pnpm, strict tsconfig, Vitest, Zod, ESM). Use whenever creating or editing .ts/.tsx files, adding packages, or running tests.
---

# TypeScript service conventions

## Toolchain (always use these commands)
- Install: `pnpm install` · Add: `pnpm add <pkg>` (dev: `pnpm add -D <pkg>`)
- Type check: `pnpm tsc --noEmit`
- Lint/format: `pnpm biome check --write .` (or `pnpm eslint . --fix && pnpm prettier -w .`)
- Tests: `pnpm vitest run`

## Definition of done
1. A failing test exists first, and it passes after the change.
2. `tsc --noEmit`, the lint step and `vitest run` all pass.
3. No new `any`, `@ts-ignore` or non-null `!` without a comment explaining why.

## Code rules
- `strict: true` and `noUncheckedIndexedAccess: true`. ESM only.
- Validate every external input (HTTP bodies, env, LLM output) with **Zod** at the boundary; infer types with `z.infer`.
- Prefer discriminated unions over boolean flags; use exhaustive `switch` statements with a `never` check.
- Return `Result`-style objects for expected failures; throw only for bugs.
- No default exports; use named exports and barrel files only at package roots.
- Async: no floating promises (`await` or explicit `void`); use `AbortSignal` for timeouts.
- Config from env through a single validated `config.ts` module.

## Tests
- Vitest; co-locate as `*.test.ts`; use `msw` for HTTP mocks; fake timers for time.

## Before finishing
Run the full check sequence and report the result of each step.
