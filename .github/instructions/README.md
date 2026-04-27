# ELITEA Documentation Authoring & Copilot Instruction Guide

This README explains how to use, extend, and maintain the documentation authoring guidelines enforced through Copilot instruction files.

Documentation is served via **Mintlify** from the `mintlify` branch at [docs.elitea.ai](https://docs.elitea.ai).

## 1. What Lives Where

| File                                                   | Purpose                                                            |
| ------------------------------------------------------ | ------------------------------------------------------------------ |
| .github/copilot-instructions.md                        | Global rules (structure, tone, Mintlify usage).                    |
| .github/instructions/docs-user-content.instructions.md | Rules for general page creation & revision.                        |
| .github/instructions/changelog.instructions.md         | Release note workflow and template.                                |
| .github/instructions/glossary.instructions.md          | Format & curation rules for glossary.                              |
| .github/instructions/screenshots.instructions.md       | Screenshot naming and inclusion standards.                         |
| .github/instructions/prompt-helper.instructions.md     | Template guidance for asking Copilot for new docs.                 |
| docs/docs.json (on `mintlify` branch)                  | Mintlify navigation config; must be updated when adding new pages. |

## 2. Local Preview (Mintlify)

Install the Mintlify CLI:

```bash
npm install -g mintlify
```

Serve docs locally (run from the `docs/` directory on the `mintlify` branch):

```bash
cd docs
mintlify dev
```

Site will serve at http://localhost:3000 with live reload.

## 3. Adding a New Page

1. Check out the `mintlify` branch.
2. Choose appropriate nav group (confirm existing groups in `docs/docs.json` first).
3. Create file under matching directory with `.mdx` extension (kebab-case name).
4. Add front matter at top of file:
   ```yaml
   ---
   title: "Page Title"
   description: "One-sentence description."
   ---
   ```
5. Insert an entry into `docs/docs.json` under the correct group.
6. Run `mintlify dev` to validate navigation and links.
7. Open PR targeting the `mintlify` branch with:
   - New `.mdx` file
   - `docs/docs.json` diff
   - New image assets (if any)

## 4. Release Notes Workflow

When a new version is released:

1. Copy current content from `docs/release-notes/rn_current.mdx` to `archived/rn{nextNumber}.mdx`.
2. Add the archived file to the "Archive" group in `docs/docs.json`.
3. Overwrite `rn_current.mdx` with template:

```mdx
---
title: "Release X.Y.Z"
description: "Release notes for ELITEA X.Y.Z"
---

# Release X.Y.Z (YYYY-MM-DD)

## Added

## Changed

## Fixed

## Deprecated

## Security

## Known Issues
```

4. Update `docs/docs.json` label for `rn_current` to "RN X.Y.Z".
5. Validate links and section ordering.

## 5. Screenshot Standards

- Directory: `docs/img/<group>/<topic>-<state>-step<n>.png`
- Semantic names (no timestamps).
- Alt text: functional ("Chat canvas showing multi-agent outputs"), not aesthetic.
- Redact sensitive data; use dummy placeholders.
- Avoid including OS chrome unless necessary for clarity.

## 6. Callouts (Mintlify)

Use Mintlify's built-in callout components:

```mdx
<Note>Helpful information.</Note>
<Warning>Something that might break things.</Warning>
<Tip>A faster or easier way.</Tip>
<Info>Background context.</Info>
```

Do NOT use MkDocs admonition syntax (`!!! note`) — it does not render in Mintlify.

## 7. Tabs (When Needed)

````mdx
<Tabs>
  <Tab title="UI">1. Open **Agents**.</Tab>
  <Tab title="API">```bash curl -X POST /agents ```</Tab>
</Tabs>
````

Use sparingly — only for genuine modality differences (UI vs API).

## 8. Glossary Maintenance

File: `docs/home/glossary.mdx`
Add new terms alphabetically; keep definitions concise. Link to menu/feature docs where relevant.

## 9. Quality Checklist (Manual Review)

Before merging:

- Right nav group + `docs/docs.json` updated
- Front matter present (`title`, `description`)
- Heading hierarchy begins with `#` (one H1)
- Steps use imperative verbs
- Mintlify callout syntax used (not MkDocs `!!!`)
- No broken internal links
- Glossary terms cross-linked once
- Screenshots have alt text and semantic names

## 10. Requesting Copilot Assistance

Use prompt helper pattern (see `.github/instructions/prompt-helper.instructions.md`). Provide:

- Category
- Target path
- Prerequisites
- Desired outcome
- Steps count / constraints
- Needed screenshots
- Glossary additions

## 11. Updating Instructions

If site structure changes (new nav group, new content type):

1. Update `docs/docs.json` on the `mintlify` branch.
2. Amend `.github/copilot-instructions.md` (nav section + category definitions).
3. Adjust specialized instruction modules if new patterns needed.

## 12. Common Pitfalls & Resolutions

| Pitfall                                          | Resolution                                                                     |
| ------------------------------------------------ | ------------------------------------------------------------------------------ |
| Page added but not visible                       | Missing entry in `docs/docs.json`.                                             |
| Admonition renders as plain text                 | Using MkDocs syntax instead of Mintlify `<Note>` / `<Warning>`.                |
| Broken internal links                            | Use absolute paths from docs root (e.g., `/getting-started/chat-quick-start`). |
| Glossary term repeated with conflicting phrasing | Normalize to canonical term; merge variants.                                   |
| Release archive numbering skipped                | Recount existing files in `archived/`; next = max(n)+1.                        |
