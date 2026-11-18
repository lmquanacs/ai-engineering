# Daily update playbook

This file is the **source of truth** for the scheduled research agent that updates this repository every day at about 09:00 Australia/Brisbane (UTC+10, no DST). Humans can follow it too.

**What's in scope, and how often**, comes from [`categories.json`](categories.json): each category's `path`, `scope` and `cadence`. Never hard-code the category list anywhere else.

## 0. Setup
1. Work on `main` in `lmquanacs/ai-engineering`.
2. `TODAY=$(TZ=Australia/Brisbane date +%F)`, `WEEKDAY=$(TZ=Australia/Brisbane date +%A)`. Use `TODAY` for every date you write.
3. Read `README.md`, `.automation/categories.json`, `.automation/sources.md`, the latest digest in `daily/`, and every category page you are about to edit.
4. Window: items published since the previous digest's date (normally 24–48h). If runs were missed, cover the whole gap.

## 1. Research
- For every category with `"cadence": "daily"`, and on **Mondays** also every `"weekly"` category, research its `scope` using web search and fetch. A weekly category may be updated on another day only for something exceptional.
- Prefer **primary sources** (vendor changelogs, release notes, pricing pages, official blogs, AWS What's New, GitHub releases, papers). Use aggregators only to *discover* items, then confirm them at the source. `sources.md` lists starting points.
- **Selection bar:** include an item only if a working engineer would change a decision because of it (adopt, upgrade, migrate, avoid, try). Aim for 0–5 items per category. "Nothing notable" is a valid outcome; never pad.
- **Special weeks:** during AWS re:Invent (2026: 30 Nov – 4 Dec; Brisbane editions 1–5 Dec plus the following Monday), add a `## 🎰 AWS re:Invent` section right after the TL;DR with the developer-relevant launches, and fold them into the affected categories. In other years, find the dates on AWS's event page.

## 2. Write entries on category pages
Use this shape, newest first within its section:

```markdown
### Name · short tag 🆕
One or two sentences on what it is, in your own words.
**Why it matters:** the practical reason an engineer cares.
<optional fenced install/config snippet, copied from official docs>
Source: [primary link](url) · <metric snapshot (date)> · Added: YYYY-MM-DD
```

Rules:
- **Deduplicate:** `grep -ri` for the name and URL first, and update an existing entry in place rather than duplicating it.
- **Accuracy:** never invent versions, prices, numbers, model or API IDs, or install commands. Label vendor claims *(self-reported)*. Write dates as `YYYY-MM-DD`.
- **Copyright:** paraphrase, with at most one short quote (<15 words) per source.
- **Safety:** only recommend skills and MCP servers you can trace to a real repository; flag anything that asks for broad credentials.
- Put 🆕 **only in headings**, never in table rows; the generator expires it after 7 days.
- Update the page's `_Last updated: YYYY-MM-DD_` line.
- Cross-link rather than repeat: architecture belongs in the hub (`architecture/README.md`), and details stay on their category page.

## 3. Housekeeping
- **LLM news** (`models/news`): keep about 30 days in the "New models" table; move older rows to `models/news/archive/YYYY-MM.md`.
- **Action-item and price-change tables** (LLM news, cost & serving, coding agents, AWS): remove rows whose date has passed and add new ones.
- A page with more than about 25 entries: move the least relevant into a `## Reference` section at the bottom, or into `archive.md` in that folder.
- **Mondays:** re-check the "Start here" picks and refresh star, install and price snapshots for them; rotate "Learn this week" in `learn/case-studies`.
- **First run of a month:** add a short "Last month in review" section to that day's digest.

## 4. Daily digest
Copy [`templates/digest.md`](templates/digest.md) to `daily/YYYY/MM/TODAY.md` and fill it in:
- A `<!-- summary: … -->` line: a one-line summary that the index shows.
- **TL;DR**: 3–6 bullets, most important first, including action items.
- One `##` section per **group** (🛠️ Build, 🧠 Models, 🏗️ Architecture & production, ☁️ Platforms, 📚 Learn), and a `###` per category **that has news**, each ending with a link to the category page. Omit empty categories, and end with a line such as "No notable updates: AI-native languages, Research".

## 5. Regenerate, validate, commit
```bash
python3 .automation/update_index.py      # README category tables + badges, group pages, digest index, 🆕 expiry
python3 .automation/check_links.py       # must print OK
```
Then edit only the `<!-- TODAY -->` block in `README.md`: a link to today's digest and 3–5 highlight bullets linking to category pages.

```bash
git add -A
git commit -m "chore(daily): TODAY update" -m "<one line per category touched>"
git push origin main
```
If the push is rejected because `main` moved: `git pull --rebase origin main`, resolve by keeping and deduplicating entries, then push once more. **Never force-push.**

## 6. Report
A short summary: the digest path, items added per category, action items, and anything you could not verify.

---

## Changing the structure (humans or agents, when asked)
- **Add a category:** add an entry under the right group in `categories.json` (`id`, `title`, `path`, `summary`, `best_for`, `cadence`, `scope`), create `<path>/README.md` from [`templates/category.md`](templates/category.md), add sources to `sources.md`, then run the two scripts above. Nothing else needs editing; the scheduled task reads this playbook and the registry.
- **Add a group** (for example Azure or Google Cloud under ☁️ Platforms): add it to `groups` in `categories.json`. Its group index page is generated.
- **Move or rename a category:** `git mv` the folder, update `path` in `categories.json`, fix links (`check_links.py` lists them), then regenerate.
