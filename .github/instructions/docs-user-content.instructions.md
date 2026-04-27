# Specialized Instructions – Docs Content

1. Map request to existing nav group (check `docs/docs.json` on the `mintlify` branch for current groups). Ask if ambiguous.
2. Use category skeletons from global instructions (Section 5).
3. Callouts: ALWAYS use Mintlify syntax (`<Note>`, `<Warning>`, `<Tip>`, `<Info>`). Do NOT use MkDocs `!!! note` syntax.
4. For new page, propose:
   - File path (kebab-case, `.mdx` extension)
   - Front matter block (`title`, `description`)
   - Nav insertion snippet for `docs/docs.json`
5. Quick Start: ≤7 steps; each begins with imperative verb.
6. How TO: Action-focused title; no conceptual deep dive beyond brief context.
7. Feature Guides: Include Concepts and Best Practices sections.
8. Platform Menu pages: Emphasize navigation path and typical tasks; link to relevant Quick Starts / How TOs.
9. Internal links: use absolute paths from docs root (e.g., `/getting-started/chat-quick-start`). Do NOT use `/docs/...` prefix.
10. If Glossary term used but not defined: append "(Add to Glossary)" note once.
11. Screenshot placeholders:
    ![<purpose>](proposed-relative-path)
12. Release notes editing in these files is allowed but major workflow adjustments should go through changelog instructions.
13. Always include front matter (`title`, `description`) on new pages.
14. Provide internal self-check summary at end (optional) if substantive restructure.

Return full file content (not a diff) unless user explicitly requests a diff.
