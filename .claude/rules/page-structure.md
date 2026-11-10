---
paths:
  - "docs/**/*.mdx"
  - "elitea.github.io/docs/**/*.mdx"
---
# Page structure

- Front matter: `title` and `description` in double quotes; optional `sidebarTitle`. No other keys on new pages.
- Never add or change `accuracy: {/*PAGE ACCURACY CONFIRMED for X*/}`; keep it where it exists.
- After front matter: a blank line, `---`, a blank line, then `## Introduction`.
- No H1 in the body; the `title` is the H1.
- Headings in Title Case; "&" instead of "and" unless part of a name.
- Use H2 and H3. Use H4 only inside Accordion or Tab content, or to match the existing page.
- Never skip a heading level. A section with one subsection has no subsection.
- A section with two or more subsections starts with an introduction paragraph.
- Task headings use infinitives or nouns, not -ing: "Create a Credential". Setup steps: `### Step 1: Create Credentials`.
- Prefix non-basic sections: `Optional: ...`, `Legacy: ...`.
- Do not create a separate section for a small topic; fold it into the nearest section or a `<Note>`.
- Document every configuration field; one table per form, columns `Field | Required | Description` (add `Default` when several fields have defaults). Use "None" for empty cells.
- Components: `<Note>`, `<Tip>`, `<Info>`, `<Warning>` (optional `title=`), `<Tabs>/<Tab>`, `<Steps>`, `<CardGroup>/<Card>`, `<AccordionGroup>/<Accordion>`. Use cards or tabs when asked.
- Leave a blank line between headings, paragraphs, lists, components and images.
- File names: kebab-case `.mdx`; toolkit pages snake_case `integrations/toolkits/<name>_toolkit.mdx`.
- Toolkit page skeleton: `.claude/skills/create-toolkit-guide/skeleton.md`.
