# Contributing

Thanks for helping keep this guide useful. An automated research agent updates the repo every morning (about 9:00 AM Brisbane time), but it misses things, and it can be wrong. People who build with these tools every day are the best source of corrections and picks.

## Ways to help (easiest first)

1. **Report something outdated or wrong.** A version, price, model ID or install command that no longer matches its source. [Open an issue](https://github.com/lmquanacs/ai-engineering/issues/new/choose) with the link that shows the correct value.
2. **Suggest an item.** A skill, MCP server, library, pattern, case study or paper that would change an engineer's decision. Use the *Suggest an item or correction* issue form.
3. **Open a pull request** that adds or fixes an entry yourself (see below).
4. **Propose a category** (for example Azure or Google Cloud under ☁️ Platforms). Open an issue first so we can agree on its scope.

Small PRs are welcome: fixing one link or one version number is a real contribution.

## The bar for an entry

Include something only if a working engineer would **change a decision** because of it: adopt, upgrade, migrate, avoid or try. "Interesting" is not enough.

- **Primary sources only.** Link the vendor changelog, release notes, pricing page, official blog, GitHub release or paper. Aggregators are fine for finding things, not for citing them.
- **Never invent numbers.** Versions, prices, model and API IDs, benchmark scores and install commands must match the source. Mark vendor claims *(self-reported)*, and date any snapshot such as stars or installs.
- **Your own words.** Paraphrase, with at most one short quote (under 15 words) per source.
- **Safety.** Only recommend skills and MCP servers that trace back to a real repository, and flag anything that asks for broad credentials.
- **No self-promotion without disclosure.** Adding your own project is fine if it meets the bar and you say it's yours in the PR.

## Entry format

Every entry uses the same shape (see [How to read an entry](README.md#-how-to-read-an-entry)):

```markdown
### Name · short tag 🆕
One or two sentences on what it is.
**Why it matters:** the practical reason an engineer cares.
Source: [primary link](url) · <metric snapshot (date)> · Added: YYYY-MM-DD
```

Put 🆕 only in headings; the generator removes it after 7 days. Search the repo for the name and URL first, and update an existing entry rather than duplicating it.

## Making a pull request

```bash
git clone https://github.com/<you>/ai-engineering && cd ai-engineering
git checkout -b fix/short-description
# edit the category page under build/, models/, architecture/, platforms/ or learn/
python3 .automation/update_index.py   # regenerate tables, badges and indexes
python3 .automation/check_links.py    # must print OK
```

- Don't hand-edit the generated parts: the `CATEGORIES` and `BADGES` blocks in `README.md`, the group index pages, `daily/README.md` or `feed.xml`. The scripts write those.
- Don't edit past daily digests except to fix a factual error.
- The daily agent pushes to `main` every morning, so rebase on `main` before you open the PR if it's more than a day old.
- CI runs the link check on every PR.

Categories and their scope live in [`.automation/categories.json`](.automation/categories.json); the daily agent's rules are in [`.automation/DAILY_UPDATE.md`](.automation/DAILY_UPDATE.md). If you're changing the structure, read the "Changing the structure" section there.

## Conduct

Be kind and assume good faith. See the [Code of Conduct](CODE_OF_CONDUCT.md).

By contributing, you agree that your contributions are licensed under the [MIT License](LICENSE).
