---
name: update
description: Use whenever the user names a part of an ELITEA docs page (section, paragraph or sentence) and what changed in the release, and wants only that part checked against the code and updated, in any wording (for example "update the Share Chats section, sharing changed in 2.0.9").
---
# update — release-related partial update (workflow u)

Same as `rework`, but limited to the part the user names. Never touch other parts of the page. Stops are marked **STOP**.

## u-0 Brief
- Scope: the exact section, paragraph or sentence, and what changed (the user's words). Ask if unclear. Turn a section name into a line range.
- Ask in one message: "Use code branch `<saved>` for EliteaUI, elitea-sdk and elitea_core? Stamp when done: no, or yes with version `<x.y.z>` (only if you confirm the whole page for that version)?" Wait.

## u-1 Issues
- Not used yet. User-pasted issue text is input (adapt, never copy verbatim).

## u-2 / u-3 Code and scoped comparison report
- Run `audit` on the scoped lines only (one code-scout for the three repos), with the user's "what changed" as the topic.
- If the scout finds that the change also affects lines outside the scope, list them separately under "outside scope" (no edits there).
- **STOP**: wait for approval of findings (this approves *what* changes; mark checked items with no change as `ok`).

## u-4 Edit the scope
- Re-read the scope. Up to 3 changed sentences → do it yourself; more → **writer**, rewrite mode (proposal), or new-section mode for a new subsection. Show `was → is`. **STOP** only for the wording; apply only approved text.
- More than 3 sentences changed: ask "Run the reviewer on lines A-B?"; run it only on a yes.

## u-5 Media, links
- `media` for placeholders; links per the rules, only inside the scope.

## u-6 Non-content check
- `non-fact-polish` on the scope only (report, **STOP**, fix approved items). For up to 3 changed sentences, `df.py lint <page> --lines A-B` plus your own check against the rules is enough.

## u-7 Stamp
- Only if the user said yes in u-0: `stamp` with workflow `u` and that version. Show the line in the final summary, with the note that only the scope was checked against the code; do not edit the page.

## u-8 Incoming links
- Only if a heading in the scope was renamed or removed: `relink`.

## u-9 Backlinks
- Only for a new subsection: propose links from related pages; **STOP**; separate change set.

## End
- Summary: changes in the scope, findings open, "outside scope" items, and the change sets. The user commits.
