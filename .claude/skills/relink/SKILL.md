---
name: relink
description: Use whenever the user wants to know which pages link to a docs page or section, or wants those links and link texts fixed after a page or heading was renamed, moved or deleted, in any wording (for example "look for links that target config-mnmt.mdx" or "I renamed this page, fix the links").
---
# relink

Links only. Do not change any other text on the linking pages.

## 1. Understand the change
- Ask if not given: old path (and old anchor or heading), new path (and new heading or anchor), or "deleted".
- For a renamed heading, the new anchor is the new heading in lowercase with spaces as hyphens; check it with `df.py links` after the change.

## 2. Find (no LLM)
- From `elitea.github.io`: `python .claude/kit/df.py inbound <old-page>` lists every page, line, link text and target.
- For an anchor change, keep only rows whose target ends with the old anchor.
- Check `docs/docs.json` `redirects` for the old path and report whether a redirect exists.

## 3. Report (gate)
- Table: `# | page:line | link text | was → is (target) | link text was → is`.
- Link text: update it when it names the old title; keep it when it is generic or already right. Match the linking page's wording.
- Deleted page: propose the closest replacement page if one exists (say why), else "remove the link and keep the text". Never point to a page you did not open.
- Note separately: links from release notes (ask before touching them) and from `docs/archive/` (never edited).
- Stop. Wait for approval.

## 4. Apply
- One page at a time. Re-read each line right before editing; skip and report a line that changed.
- Edit only the link target (relative, no `.mdx` extension) and, if approved, the link text.
- Rerun `python .claude/kit/df.py inbound <old-page>` (expect only the rows the user chose to keep) and `df.py links <page>` for each edited page.
- Report `page:line: was → is` per change. These are a separate commit-sized set from the rename itself; say so.
