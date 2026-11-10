---
paths:
  - "docs/**/*.mdx"
  - "docs/docs.json"
  - "elitea.github.io/docs/**/*.mdx"
  - "elitea.github.io/docs/docs.json"
---
# Links & nav

- Internal links: relative, no extension: `[Secrets](../../menus/settings/secrets)`. Never `.md`/`.mdx`.
- Link text is descriptive; never "here" or "this page". No links in headings.
- Link sparingly: once per target per page, at most one or two per paragraph.
- Related links: "For more information, see [Title](path)." or a final `## See Also` section.
- Avoid external links unless required.
- Every live page is in `docs/docs.json` nav as an extensionless path from `docs/`.
- Edit `docs.json` only with `nav.py` (keeps hand formatting); never re-serialize the whole file.
- Toolkit groups are alphabetical; insert new pages in order.
- Moving or renaming a page adds a redirect; never delete existing redirects.
- Do not touch `docs/release-notes/**` nav entries; the release-notes skill owns them.
