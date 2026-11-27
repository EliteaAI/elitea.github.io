---
name: non-fact-polish
description: Use whenever the user wants the form of a docs page or some lines checked or fixed rather than its facts — spelling, grammar, punctuation, wording, formatting, broken links or anchors, media paths, video size or Mintlify validity — in any wording (for example "check the page for misspellings" or "fix the broken links"); if they only say "check this page", ask whether they mean facts or form.
---
# non-fact-polish

Scope comes from the user: whole page, a section, or lines. Do only the checks asked for ("only links" means only links). Never check facts against the code here: this kit checks form only.

## 1. Prepare (no LLM)
- Page = the file the user names, else the file open in the IDE; if unclear, ask.
- Turn a section name into a line range (heading to next heading of the same or higher level).
- Run what applies, from `elitea.github.io`:
  - Style: `python .claude/kit/df.py lint <page> --lines A-B`
  - Links, anchors, media paths: `python .claude/kit/df.py links <page>` (keep only rows in scope). A missing media file shows where a file with that name exists ("found: …").
  - Video size, when videos are in scope: `python .claude/kit/df.py media big`
- Size: `python .claude/kit/df.py size <page> --lines A-B`.

## 2. Language check
- 3 sentences or fewer: check them yourself against all `.claude/rules/mdx-*.md`.
- More: run the **proofreader** helper with the page, range and the lint output (so it does not repeat it). If the user said "do it yourself", skip the helper.

## 3. Report (gate)
- One table, numbered, saved with `df.py findings add <page> <json>`: `# | line | finding | evidence (rule or script) | was → is | severity`.
- Merge duplicates (script and proofreader). Drop false alarms you can see (for example "new" meaning newly created, "Personal" as a UI label) and say how many you dropped.
- For each broken link give the fix: the moved page (`df.py inbound`/redirects) or the found media path. If no target exists, say so; never invent a target.
- Stop. Wait for "fix 1, 3, 5", "fix all" or "fix none".

## 4. Fix approved items only
- Re-read each target line right before editing. If it changed since the report, re-check it and tell the user instead of editing.
- Edit only the approved spans. Mark them done: `df.py findings set <page> done 1,3,5`.
- If links or media changed: rerun `df.py links <page>`. If structure or components changed: `python .claude/kit/df.py validate`.
- Report each change as `line N: was → is`, then the open findings (`df.py findings show <page> open`).
