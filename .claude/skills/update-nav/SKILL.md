---
name: update-nav
description: Use when a page must be added to, moved in, or renamed in the docs.json navigation, or to check that nav and pages are in sync.
---

# Update nav

Standard: `.claude/rules/links-and-nav.md`. Never hand-edit `docs/docs.json` arrays; use the script (it keeps formatting and CRLF, refuses invalid JSON).

Script: `python .claude/skills/update-nav/nav.py`

1. Find the group: `nav.py groups <text>` or `nav.py find <similar page>`. Choose the group where sibling pages live; ask if two groups fit.
2. Add: `nav.py add <page-path-without-ext> --group "<Tab > Group > Subgroup>" --sorted`
   - Toolkit groups are alphabetical: always `--sorted`.
   - Other groups follow reading order: use `--after <page>` (ask if order is unclear).
3. Rename or move a page:
   1. `nav.py rename <old> <new>` (updates nav + adds redirect).
   2. Move the file with `git mv` (the protect hook asks for approval).
   3. Fix inbound links: `grep -rl "<old basename>" docs --include=*.mdx`, then edit each to the new relative path.
4. New group or tab: ask first, then edit `docs.json` by hand with minimal Edit calls matching the surrounding style.
5. Verify: `nav.py check` (expect 0 issues for the page you touched).
6. Do not touch `release-notes/**` entries.
