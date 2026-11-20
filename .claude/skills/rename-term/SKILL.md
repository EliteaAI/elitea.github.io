---
name: rename-term
description: Use whenever the user wants to find a term or text across docs pages, or to change a term, label or feature name on every page where it appears, in any wording (for example "the UI now says Share instead of Make public" or "give me the list of pages with this text").
---
# rename-term

## 1. Confirm the rename
- Old term, new term, and whether it is a UI label (bold, exact case) or a general term. Ask if unclear.
- If the rename comes from the code, ask which code branch to use, then confirm the new label in code (`git -C <repo> grep -n "<new>" origin/<branch> -- <paths from the knowledge map>`). Show the evidence.

## 2. Find (no LLM)
- From `elitea.github.io`: `python .claude/kit/df.py find "<old>" --words` (prose only; code, comments and frontmatter are skipped). Add `--in <folder>` if the user limits the scope.
- Also check headings (anchors change: their inbound links need `relink`), image alt texts, `docs/docs.json` titles, and media file names that contain the term (report only; never rename files here).

## 3. Report (gate)
- Table: `# | page:line | text | was → is | note` (note: heading → anchor changes; release notes; archive; different meaning).
- Mark occurrences where the old word has another meaning and must stay.
- Release-note pages: list them, but propose no change (they describe past releases) unless the user asks.
- `docs/archive/` and the styleguides: never changed.
- Stop. Wait for "apply 1-12, 15" or "apply all".

## 4. Apply
- One page at a time; re-read each line right before editing; keep the case and bold of the label style.
- After all pages: rerun `df.py find "<old>" --words` (expect only the kept rows) and `df.py links --all` (renamed headings).
- If headings changed, offer `relink` for their anchors. Report `page:line: was → is` grouped by page (each page group is one commit-sized set).
