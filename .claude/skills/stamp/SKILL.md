---
name: stamp
description: Use whenever the user wants a page's accuracy stamp built or read, or wants to know which code state a page was checked against, in any wording (for example "stamp this page for 2.0.9" or "what is this page's baseline").
---
# stamp

The stamp says which product version and which code state a page was checked against. Format (one frontmatter line):
`accuracy: {/*PAGE ACCURACY CONFIRMED for 2.0.9 | updated 2026-11-17 | EliteaUI main@55fe88c | elitea-sdk main@e9d96aa | elitea_core main@8cb174b*/}`

The kit never writes the stamp into the page. It shows the line in chat; the user pastes it.

This kit does not check facts. Build a stamp only when the user says the page was checked against the code on that branch (by them or another tool). Otherwise say so and give no line.

## Read
- `python .claude/kit/df.py stamp read <page>` → version, workflow, date and baseline ("unknown baseline" if the page has no stamp or no SHAs). A legacy `verified:` block is reported, not changed.

## Build and show
1. Ask everything in one message: version (for example 2.0.9), workflow (`n` new page, `f` full rework, `u` partial update) and code branch (offer the saved one).
2. `python .claude/kit/df.py stamp build <page> <version> <n|f|u> [--branch <name>]`. It reads the current SHA of `origin/<branch>` in each code repo, and prints the line, where it goes, and the old line it replaces.
3. Show it, ready to paste:
   - the line itself, in a code block;
   - where it goes: "replace line N" (quote the old line) or "add before the closing `---`".
4. Do not edit the page.

## Setup
- The code repos must be cloned next to `elitea.github.io` (`../EliteaUI`, `../elitea-sdk`, `../elitea_core`), or set with `df.py cfg repo <name> <path>`.
- Save the code branch once: `python .claude/kit/df.py cfg branch <name>`. `df.py cfg` shows the paths and the branch.

## Rules
- One stamp line per page. Never suggest removing a `verified:` block; say it can be replaced by the line if the user wants.
