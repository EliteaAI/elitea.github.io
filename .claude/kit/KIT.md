# ELITEA docs: doc-factory kit

Mintlify site. Content `docs/**/*.mdx`, nav `docs/docs.json`, media `docs/img/<section>/<area>/<page-slug>/` (~680 MB: scan with scripts only).
Styleguides `docs/styleguides/*.mdx` are the human standard (read-only); the kit's rules in `.claude/rules/` are compiled from them. Do not re-read styleguides unless the kit asks.
Rules load automatically only for files in `docs/`. For a page outside `docs/` (for example a temp copy), read every `.claude/rules/mdx-*.md` and `work-gates.md` before writing or checking text.

## Sources of truth
- Code repos (paths in `.claude/local.json`, defaults `../EliteaUI`, `../elitea-sdk`, `../elitea_core`) are read-only. Read the saved branch via git refs (`git grep origin/<branch>`, `git show origin/<branch>:<path>`).
- Branches: the user checks, switches and pulls all branches (doc and code) herself; never fetch, pull, check out or switch.
- Before every task that reads code, ask: "Use code branch `<saved>` for EliteaUI, elitea-sdk and elitea_core?" Wait for the answer; save a new one with `df.py cfg branch <name>`. Show the branch and SHAs at the top of every code-based report.
- Knowledge maps `.claude/kit/maps/<repo>.md` point to where facts live; read only the matching lines. Before a code task run `df.py map advice <topic>`; offer a rebuild only if it says so (branch switch, 300+ commits behind, known gap). Record every "map gap" a scout reports: `df.py map gap <repo> "<topic>" "<pointer>"`.
- Precedence: code on the chosen branch > existing pages > styleguides (style only, never facts). Flag where a page contradicts the styleguides.
- Issues: not used yet.

## Gates (always)
- Report first, act only on approval of numbered findings. Suggestions are fine; changes need a yes.
- Re-read target lines right before every edit; the user edits in parallel.
- Never revert, move or reformat what the user placed or did not ask about.
- Never invent. Missing data → placeholder `{{TODO: …}}`, and list all placeholders at the end.
- Pasted text: adapt to the page's pattern, never verbatim; report it for review.
- Before "done", check coverage against the source list (every line, row, column, item).
- Never commit, push or open PRs; never suggest commit messages. Group changes into commit-sized sets on request.
- Release notes (`docs/release-notes/**`) belong to the `release-notes` skill; do not edit its files or `rn-drafter`.

## Reports
Compact table in chat, no files: `# | line | finding | evidence (repo path:line) | was → is | severity`.
Numbers persist in the session (`df.py findings`), so "fix 1, 2, 5" and "which are still open?" work.

## Models
Scripts (`python .claude/kit/df.py …`) for everything mechanical. Sonnet: code-scout, writer, proofreader, reviewer (ask before running it inside new/rework/update). Haiku: drift-triager.
Each helper costs ~40k tokens to start. Review requests: run `df.py size <page> --lines A-B`; ≤3 sentences → review it yourself with the reviewer's checklist; >3 → reviewer. Everywhere in the kit, "3 sentences" counts only the lines that change (or are added), not the whole scope. Alt text, headings, table headers, tags and media lines are not counted. The user can override ("use the reviewer" / "do it yourself").

## Commands
- Config: `python .claude/kit/df.py cfg` (paths, branch, lock).
- Mintlify: `cd docs && mint validate`, `mint broken-links`.
- Use `python` (not `python3`). Caches go to the system temp dir (`doc-factory/`), never the repo.
