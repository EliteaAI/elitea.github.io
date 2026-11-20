---
name: rework
description: Use whenever the user wants an existing ELITEA docs page fully reviewed against the code and reworked section by section, in any wording (for example "rework this page" or "do a full review and rewrite of the Chat page").
---
# rework — full review and rework (workflow f)

Stops for the user are marked **STOP**. Never move, revert or reformat what the user placed. The user commits (f-11).

## f-0 Brief
- Page = the file the user names, else the open file. Ask for the reference page if the page should change its pattern, and the target release version.
- `df.py stamp read <page>`: say what the current baseline is.
- Ask in one message: "Use code branch `<saved>` for EliteaUI, elitea-sdk and elitea_core? Stamp when done: no, or yes with version `<x.y.z>`?" Wait.

## f-1 Issues
- Not used yet. User-pasted issue text is input (adapt, never copy verbatim).

## f-2 / f-3 Code and comparison report
- Run `audit` on the whole page (one code-scout for the three repos). Its numbered findings table is the f-3 report.
- **STOP**: wait for approval of findings ("fix 1, 3, 5", "all"). Nothing is edited before.

## f-4 Section by section
- Work through the approved findings one section at a time, top to bottom.
- For each section: re-read it; up to 3 sentences of change → do it yourself; more → **writer**, rewrite mode (proposal only). Show `was → is`. **STOP** per section; apply only what is approved.
- After each applied section with more than 3 sentences changed, ask "Run the reviewer on lines A-B?"; run it only on a yes.
- Keep a list of headings you renamed or removed (needed in f-8).

## f-5 Media, mermaid, links
- `media` for `{{MEDIA}}` placeholders and wrong media; links per the rules; mermaid only if asked.

## f-6 Non-content check
- `non-fact-polish` on the whole page (report, **STOP**, fix approved items).

## f-7 Stamp
- Only if the user said yes in f-0: `stamp` with workflow `f` and that version. Show the line in the final summary; do not edit the page.

## f-8 Incoming links
- For every renamed or removed heading, and for a renamed page: `relink` (find links in other pages, **STOP**, fix approved ones).

## f-9 Backlinks for new sections
- For new sections: propose links from related pages (`df.py find`). **STOP**. Add approved links only, as a separate change set.

## f-10 Navigation
- Only if the page was renamed or moved: `df.py toc rename <old> <new>` (and the redirect). **STOP**. Apply with Edit, then `df.py toc check` and `df.py validate`.

## End
- Summary: findings done and still open, placeholders, and the change sets (page; incoming links; backlinks; navigation). The user commits.
