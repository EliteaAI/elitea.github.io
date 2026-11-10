---
name: create-doc-page
description: Use when asked to write a new documentation page that is not a toolkit integration guide (feature, how-to, menu, settings, getting-started or concept page).
---

# Create doc page

Standards: `.claude/rules/` (auto-loaded). Toolkit pages: use `create-toolkit-guide` instead.

1. **Scope**
   - Get the topic, ticket (optional) and target section. With a ticket: `gh issue view <n> -R EliteaAI/elitea_issues --comments`; scope = acceptance criteria.
   - Pick the folder by section (`menus/`, `how-tos/<area>/`, `getting-started/`, `home/key-concepts/`) and a kebab-case filename. Confirm path and title with the user if not obvious.
2. **Model page**: find one sibling page in the same folder (`ls docs/<folder>`), grep its headings (`grep -n "^#" <file>`) and mirror its section pattern. Do not read it whole.
3. **Research**: for any UI or behavior fact, call `doc-researcher` with a precise checklist (labels, fields, defaults, flows, limits). Small single-fact lookups: Grep the sibling repo directly.
4. **Draft**: start from `template.mdx` in this folder. Write once, then Edit section by section.
   - Fold small topics into existing sections or a `<Note>`; no one-paragraph sections.
   - Explain concepts inline; link only for real next steps.
   - Image refs use planned names; list them under Open questions.
5. **Nav**: `update-nav` skill (`nav.py add <page> --group "<group>" --after <page>`).
6. **Check**: `python .claude/hooks/validate_doc.py docs/<page>.mdx`; fix everything except planned images.
7. **Report**: `Changed: <files> | Notes: <≤3 lines> | Open questions: <list>`. Suggested commit: `Add <topic> documentation`.
