# Instructions for agents working in this repo

This repo is a daily-updated, categorised catalogue of AI engineering utilities, organised into groups: `build/`, `models/`, `architecture/`, `platforms/`, `learn/`.

- `.automation/categories.json` is the single source of truth for categories (path, scope, cadence). Don't hard-code category lists elsewhere.
- For the scheduled daily update, follow `.automation/DAILY_UPDATE.md` exactly. Sources are in `.automation/sources.md`.
- Keep the entry format described in `README.md` ("How to read an entry"). Put 🆕 only in headings.
- Never invent versions, prices, numbers, model or API IDs, or install commands. Confirm them at a primary source.
- Don't hand-edit generated parts: the README `CATEGORIES` and `BADGES` blocks, group index pages, the `daily/README.md` index, or `feed.xml`. Run `python3 .automation/update_index.py` instead.
- Before committing, run `python3 .automation/check_links.py` and fix any failures.
- Commit directly to `main` with `chore(daily): YYYY-MM-DD update`, using the Australia/Brisbane date. Never force-push.
