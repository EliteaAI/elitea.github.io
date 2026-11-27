# ELITEA docs: form kit

Mintlify site. Content `docs/**/*.mdx`, nav `docs/docs.json`, media `docs/img/<section>/<area>/<page-slug>/` (~680 MB: scan with scripts only).
Styleguides `docs/styleguides/*.mdx` are the human standard (read-only); the kit's rules in `.claude/rules/` are compiled from them. Do not re-read styleguides unless the user asks.
Rules load automatically only for files in `docs/`. For a page outside `docs/`, read every `.claude/rules/mdx-*.md` before writing or checking text.

This kit checks and fixes **form, not facts**: spelling, grammar, wording, formatting, links, anchors, images, videos, alt texts, Mintlify validity. It never checks facts against the code.

## Gates (always)
- Report first, act only on approval of numbered findings. Suggestions are fine; changes need a yes.
- Re-read target lines right before every edit; the user edits in parallel.
- Edit only the approved lines. Never revert, move or reformat what the user placed or did not ask about.
- Never invent facts, labels, limits or names. Missing data → placeholder `{{TODO: …}}`, and list all placeholders at the end.
- Before "done", check coverage against the scope (every line, row, item). Report each change as `line N: was → is`.
- Never commit, push or open PRs; never suggest commit messages.
- Release notes (`docs/release-notes/**`) belong to the `release-notes` skill; do not edit its files or `rn-drafter`.

## Reports
Compact table in chat, no files: `# | line | finding | evidence (rule or script) | was → is | severity`. Severity: high (wrong meaning or broken), medium (rule violation), low (style).
Numbers persist (`df.py findings`), so "fix 1, 2, 5" and "which are still open?" work.
Findings file for `df.py findings add <page> <json-file>`: a JSON list with `line`, `finding`, `evidence`, `change`, `severity`, written to the temp folder. States: `open`, `approved`, `done`, `ok` (checked, no change needed), `rejected` (the user said no).

## Models
Scripts (`python .claude/kit/df.py …`) for everything mechanical. Sonnet: proofreader. Each helper costs ~40k tokens to start: for up to 3 changed sentences (`df.py size`), check them yourself against the rules.

## Commands
- `python .claude/kit/df.py` lists all commands: lint, links, inbound, media, validate, size, find, findings, stamp, cfg.
- Mintlify: `cd docs && mint validate`, `mint broken-links`.
- Use `python` (not `python3`). Caches go to the system temp dir (`doc-factory/`), never the repo.
