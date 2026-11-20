---
name: new
description: Use whenever the user wants a new ELITEA docs page written, from research to navigation, in any wording (for example "write a new page about Image Creation" or "create a page for the Webhooks feature").
---
# new — new page (workflow n)

Stops for the user are marked **STOP**. Every addition is reported for review. The user commits (n-12).

## n-0 Brief
- Ask for anything missing: topic, page path (folder and file name), page type, reference page (ask if none is given), target release version.
- Ask in one message: "Use code branch `<saved>` for EliteaUI, elitea-sdk and elitea_core? Stamp when done: no, or yes with version `<x.y.z>`?" Wait.

## n-1 Issues
- Issues are not used yet. If the user pastes issue text or links, keep it as input (adapt, never copy verbatim).

## n-2 Code
- Run `df.py map advice <topic>`; offer a rebuild only if it says so.
- One **code-scout** for the three repos, task **facts**, for the feature (UI labels, flows, limits, permissions, settings, who sees what). Record map gaps.

## n-3 Template and similar pages
- Read only the outline of the reference page (headings, components, See Also form). Find 1-3 similar pages with `df.py find "<feature term>" --words`.

## n-4 Reusable media
- Search for existing images and videos of the feature: `df.py media used <name>` or Glob in `docs/img/` by feature words. List them.
- **STOP**: show the facts (with evidence), the planned outline, and the reusable media. Wait for approval or changes.

## n-5 Draft
- **writer** helper, mode **new page**, with the approved facts, outline and reference. It creates the file at the given path and reports placeholders.

## n-6 Content review
- Ask: "Run the reviewer on the new page?" On yes, run the **reviewer**. Show its findings. **STOP**: the user approves fixes; apply only approved ones (writer in rewrite mode, or you for 3 sentences or fewer).

## n-7 Media, mermaid, links
- `media` for each `{{MEDIA}}` placeholder (reuse found files first). Mermaid only if the user asks. Add internal links per the rules (sparingly, See Also at the end).

## n-8 Non-content check
- Run `non-fact-polish` on the whole page (report, **STOP**, fix approved items).

## n-9 Stamp
- Only if the user said yes in n-0: `stamp` with workflow `n` and that version. Show the line in the final summary; do not edit the page.

## n-10 Backlinks (separate change set)
- Find related pages (`df.py find`), propose where a link to the new page belongs (`page:line`, link text). **STOP**. Add approved links only. Report them as a separate commit-sized set.

## n-11 Navigation
- `df.py toc find <group words>`, then `df.py toc add <page> --group "<group>" --after <page>`; show the exact edit. **STOP**. Re-read `docs/docs.json`, apply the edit with Edit, run `df.py toc check` and `df.py validate`.

## End
- Summary: files created or changed, placeholders still open, findings still open, and the change sets (page; backlinks; navigation). The user commits.
