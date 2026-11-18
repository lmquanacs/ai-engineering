# Instructions for agents working in this repo

This repo is a daily-updated, categorised catalogue of AI engineering utilities.

- For the scheduled daily update, follow `.automation/DAILY_UPDATE.md` exactly. Sources are in `.automation/sources.md`.
- Keep the entry format described in `README.md` ("How to read an entry").
- Never invent versions, numbers, API IDs or install commands. Confirm them at a primary source.
- Before committing, run `python3 .automation/check_links.py` and fix any failures.
- Commit directly to `main` with `chore(daily): YYYY-MM-DD update`, using the Australia/Brisbane date. Never force-push.
