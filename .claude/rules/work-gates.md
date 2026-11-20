---
paths:
  - "docs/**"
  - "elitea.github.io/docs/**"
---
# How to work with the user on docs

## Before acting
- Know the page type first (how-to, settings/menu, toolkit, overview, release notes). Apply its rules only.
- Ask the user for the reference page when a task needs one and none is given.
- Do only what was asked. "Fix only links" means links. You may suggest more; act on it only after a yes.
- Every change goes through a numbered finding the user approved. "Stop" means stop, at once.
- Exception: new pages and new sections are written straight into the file, then reported (file, lines, placeholders) for approval. If rejected, remove exactly the inserted lines, after re-reading them.

## While editing
- Re-read the exact target lines right before each edit; the user edits the same file in the IDE.
- Never revert, move or reformat what the user placed, removed or did not mention. If something she did looks wrong, report it.
- Edit only the approved lines. Keep untouched text byte-for-byte.
- Never invent facts, labels, limits or names. Unknown → `{{TODO: what is missing}}`.
- Pasted text: adapt it to the page's pattern and the rules; never insert it verbatim. Show it for review.
- "Rewrite X like Y": copy Y's structure and phrasing patterns, not its facts.

- After an edit of more than 3 sentences outside the new/rework/update workflows, offer once: "Run non-fact-polish on lines A-B?" Never run it without a yes.

## Before saying "done"
- Coverage check: compare against the source list (every line range, row, column, list item, footer, See Also). Say what was checked.
- List every placeholder left, with its line.
- Report each change as `line N: was → is`.

## Reports
- Table in chat, no files: `# | line | finding | evidence | was → is | severity`. Severity: high (wrong fact), medium (omission or broken), low (style).
- Keep finding numbers for the whole session. Answer "which are still open?" from the findings list.
- Findings file for `df.py findings add <page> <json-file>`: a JSON list of objects with `line`, `finding`, `evidence`, `change` (the "was → is"), `severity`. Write it to the kit's temp folder with the Write tool.
- States (`df.py findings set`): `open`, `approved`, `done`, `ok` (checked, no change needed), `rejected` (the user said no). Never use `rejected` for `ok`.
- Code-based reports start with the code branch and short SHAs of each repo.
