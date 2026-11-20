---
name: stamp
description: Use whenever the user wants a page's accuracy stamp built or read, or wants to know which code state a page was checked against, in any wording (for example "stamp this page for 2.0.9" or "what is this page's baseline"); also the last content step of new, rework and update.
---
# stamp

The stamp says which product version and which code state a page was checked against. Format (one frontmatter line):
`accuracy: {/*PAGE ACCURACY CONFIRMED for 2.0.9 | updated 2026-11-17 | EliteaUI main@55fe88c | elitea-sdk main@e9d96aa | elitea_core main@8cb174b*/}`

The kit never writes the stamp into the page. It shows the line in chat; the user pastes it.

## Read
- `python .claude/kit/df.py stamp read <page>` → version, workflow, date and baseline ("unknown baseline" if the page has no stamp or no SHAs). A legacy `verified:` block is reported, not changed; its SHAs can be read from the frontmatter.

## Questions: all at the first stop
- In new, rework and update, the stamp questions are asked in the brief (n-0, f-0, u-0), together with the code branch: "Stamp when done: no, or yes with version `<x.y.z>`?" Do not ask again at the end.
- Called on its own, ask everything in one message: version, workflow (`n` new page, `f` full rework, `u` partial update) and code branch (offer the saved one).

## Build and show
1. `python .claude/kit/df.py stamp build <page> <version> <n|f|u> [--branch <name>]`. It prints the line, where it goes, and the old line it replaces.
2. Show it in the final summary, ready to paste:
   - the line itself, in a code block;
   - where it goes: "replace line N" (quote the old line) or "add before the closing `---`";
   - a note if only part of the page was checked against the code.
3. Do not edit the page, read it back or run validate for the stamp.

## Rules
- Build a stamp only after the content was checked against the code on that branch. If it was not (for example a language-only fix), say so and give no line.
- One stamp line per page. Never suggest removing a `verified:` block; say it can be replaced by the line if the user wants.
