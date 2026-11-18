# AI-native programming languages

_Last updated: 2026-11-18_

> Languages designed with LLMs and agents as primary users, and the essays arguing about whether we need them. All of these are experimental. Watch them; don't ship production code in them.

## 🧪 Languages

### Zero · Vercel Labs · systems language for agents
An experimental systems language whose toolchain talks to agents: every diagnostic is structured JSON with stable repair IDs and fix plans. Agents query and patch a **semantic program graph** instead of editing raw text, and the compiler checks every change. Native binaries are under 10 KiB. The design prefers one obvious way to write each thing ("regularity over syntax"). Apache-2.0, pre-1.0, breaking changes expected.
```bash
curl -fsSL https://zerolang.ai/install.sh | bash
npx skills add vercel-labs/zerolang      # agent bootstrap skill
zero skills get language                  # compiler ships version-matched skills
```
**Why it matters:** It is the most serious attempt so far to redesign the compiler ↔ agent contract. Even if Zero fades, expect JSON-first diagnostics and bundled skills to spread to mainstream toolchains.
Sources: [github.com/vercel-labs/zero](https://github.com/vercel-labs/zero) · [InfoQ](https://infoq.com/news/2026/08/vercel-ships-zero-ai) · First release May 2026 · Added: 2026-11-18

### NanoLang · Jordan Hubbard
A tiny language meant to be targeted by coding LLMs: unambiguous syntax, **mandatory tests**, and transpilation to C. It ships a `MEMORY.md` written for LLMs to read, so a model can learn the language in-context.
**Why it matters:** It shows the "teach the model the language in the prompt" approach to languages with no training data.
Sources: [jordanhubbard/nanolang](https://github.com/jordanhubbard/nanolang) · [Simon Willison's notes](https://simonwillison.net/2026/jan/19/nanolang) · Jan 2026 · Added: 2026-11-18

### Weft · LLM calls and humans as language primitives
An open-source language where calling an LLM, waiting for human input, orchestrating agents and **durable execution** are built-in primitives rather than library calls.
**Why it matters:** It points to the "workflow language" direction, the same space Temporal-style durable execution occupies.
Source: [Luca Berton: Weft overview](https://lucaberton.com/blog/weft-programming-language-ai-agents-durable-execution/) · Added: 2026-11-18

### SPELL · AI-native dataflow language (preprint)
A dataflow language with explicit dependencies and types, written in structured JSON, designed around how LLMs generate rather than how humans read.
Source: [Zenodo preprint, Dec 2025](https://zenodo.org/records/17826541) · Added: 2026-11-18

## 📝 Essays worth reading

| Essay | Argument |
|---|---|
| [Armin Ronacher: *A language for agents*](https://lucumr.pocoo.org/2026/2/9/a-language-for-agents/) (Feb 2026) | Agentic engineering will produce new languages. Priorities: less reliance on LSP, tokenisation-robust syntax, explicit flow context. |
| [Mark Seemann: *Which language is best suited for LLM generation?*](https://blog.ploeh.dk/2026/03/30/programming-languages-for-ai/) (Mar 2026) | Strong type systems (for example exhaustive sum types) catch LLM mistakes, but in practice Python or JS will probably win. |
| [Akita: *Best programming language for LLMs*](https://akitaonrails.com/en/2026/02/09/ai-agents-best-programming-language-for-llms/) (Feb 2026) | A thought experiment asking models to design their ideal language: a Lisp-like AST with rich metadata. |

## 🔭 What to watch

- JSON or SARIF diagnostics added to existing compilers (rustc, tsc, kotlinc) for agent consumption.
- Languages that ship their own agent skills, as Zero does with `zero skills`.
