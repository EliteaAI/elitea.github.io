---
name: update-doc
description: Use when an existing doc page must be updated or rewritten after a feature/code change, a ticket, or because it is outdated ("update X for #6785", "page X is outdated", "rewrite the nodes section").
---

# Update doc

Standards: `.claude/rules/` (auto-loaded). Goal: smallest correct diff.

1. **Scope**
   - Ticket given: `gh issue view <n> -R EliteaAI/elitea_issues --comments` (linked PRs: `gh pr view <n> -R EliteaAI/<repo>` / `gh pr diff`). Scope = acceptance criteria only.
   - Branch: current `release/*` of the sibling repos, not `main`; confirm if the ticket names another.
2. **Map the page**: `grep -n "^#" <page>` for the outline. Read only the sections in scope.
3. **Research**: call `doc-researcher` with the page's affected sections and a checklist of facts to verify (labels, fields, defaults, behavior). For a whole-page rewrite, one call per major area, run in parallel.
4. **Gap list**: from the fact sheet, list per section: outdated, missing (e.g. skipped config fields), wrong. Show it to the user only if the rewrite is large (>3 sections) or scope is unclear.
5. **Edit section by section**
   - One Edit per section, in page order; keep each reply short.
   - Do not touch text outside scope; do not restyle untouched sentences.
   - Add missing fields to the existing table instead of new tables; merge duplicate tables.
   - New subtopics go into the nearest existing section or a `<Note>`, not a new heading.
   - Explain inline; do not send the reader to another page for something one sentence covers.
   - Keep `accuracy:` front matter unchanged.
6. **Images**: changed UI → keep existing refs, list affected screenshots under Open questions.
7. **Moves/renames**: `update-nav` skill.
8. **Check**: `python .claude/hooks/validate_doc.py <page>`; fix issues in lines you touched.
9. **Report**: `Changed: <files> | Notes: <≤3 lines> | Open questions: <list>`. Suggested commit: `Update <page topic> documentation`.

If the session is interrupted, resume at the next unedited section from the gap list.
