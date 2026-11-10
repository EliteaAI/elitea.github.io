---
name: fix-links
description: Use when asked to find or fix broken links, broken images, or .md/.mdx link extensions in one page, a folder, or the whole docs site.
---

# Fix links

Standard: `.claude/rules/links-and-nav.md`, `.claude/rules/images-and-media.md`.

1. Scan (deterministic, ~0.2 s for the whole site):
   `python .claude/hooks/validate_doc.py <file|dir> --links-only`
   Output per issue: `L<line>: <target> -> missing file | broken; try <suggestion> | remove .md/.mdx extension`.
2. Fix in place, one Edit per line, changing only the link target:
   - `remove .md/.mdx extension`: drop the extension, keep any `#anchor`.
   - `broken; try X`: use X if it is clearly the same page; otherwise search `nav.py find <word>` and choose; ask if ambiguous.
   - `missing file` (image/video): search `docs/img` by basename (`find docs/img -iname "<name>*"`). Fix the path if found; else list under Open questions, do not delete the reference.
3. Re-run step 1 on the same scope until clean (or only open questions remain).
4. Optional site-wide confirmation when the user asks or for >20 fixes: `cd docs && mint broken-links`.
5. Skip `docs/archive/**`. For `docs/release-notes/**`, the hook asks approval; group those fixes into one approval.
6. Report: `Changed: <files> (<n> links) | Notes: ... | Open questions: <unresolved targets>`
