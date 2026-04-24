# Generate Release Notes

Use this prompt in GitHub Copilot Chat (with the `@release-notes` agent or
directly in chat) to generate release notes from a GitHub Projects JSON export.

---

## Usage

```
@release-notes Generate release notes from #file:exports/RN2_0_2.json
Version: 2.0.2
Release date: 2026-05-01
```

Or paste the prompt below directly into Copilot Chat, replacing the
placeholder values.

---

## Prompt

```
You are a senior technical writer for the ELITEA AI platform.

Generate a complete, publication-ready release notes document in MDX format
from the GitHub Projects JSON export at: **{FILE_PATH}**

Before finalising Fixed Issues and Known Issues, compare the export against the
existing Known Issues in **docs/release-notes/rn_current.mdx** and move any issue
that is now fixed out of Known Issues.

Release metadata:
- Version: {VERSION}          (e.g. 2.0.2)
- Release date: {DATE}        (e.g. 26-Apr-2026)
- Environment URL: https://next.elitea.ai

Follow the rules in .github/skills/release-notes-skill.md exactly.

Categorisation rules (from the skill):
- Known Issues   → status is "Bugs" or "Development"
- Fixed Issues   → issue_type is "Bug" AND status is "In Testing",
                   "Verified on DEV Env", "Ready for Public Release", or "Done"
- New/Changed    → issue_type is "Enhancement", "Story", or "Epic"
                   AND status is "In Testing", "Verified on DEV Env",
                   "Ready for Public Release", or "Done"

Additional required checks:
- Every Fixed Issue and Known Issue bullet must start with a linked GitHub issue
  ID using the export `url` field.
- For New and Changed Features, add a "For more information" line only when you
  verify that the linked doc page exists in `docs/`.

Output:
1. A single .mdx file named `release-{VERSION}.mdx`
2. Save it to the `docs/release-notes/` folder, or replace
   `docs/release-notes/rn_current.mdx` when updating the current release page
3. Print a brief summary of what was included (counts per section)
```

---

## Tips

- If Copilot misses items, ask: _"Show me all issue numbers you included in
  each section"_ and cross-check with the JSON.
- To regenerate just one section: _"Rewrite only the Fixed Issues section
  with more user-friendly language."_
- To adjust grouping: _"Move the Notification Center feature to the
  'Administration & Settings' section."_
