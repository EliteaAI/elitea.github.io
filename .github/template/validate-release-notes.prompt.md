# Validate Release Notes Draft

Use this prompt to check a generated release notes MDX file for completeness,
tone, and compliance with the ELITEA style guide.

---

## Usage

```
@release-notes Validate #file:docs/releases/release-2.0.2.mdx
against #file:exports/RN2_0_2.json
```

---

## Prompt

```
Review the release notes draft at **{DRAFT_MDX_PATH}** against the source
data at **{JSON_PATH}**.

Check for:

1. **Coverage** — Every issue in the JSON that meets the categorisation rules
   in .github/skills/release-notes-skill.md must appear in the draft.
   List any that are missing.

2. **Known-issue reconciliation** — Compare any issue listed in the draft's
   Known Issues section against the export status. Flag any Known Issue that
   should now be moved to Fixed Issues.

3. **Miscategorisation** — Are any issues placed in the wrong section?
   (e.g. a Bug in "New Features", or a "Bugs"-status item in "Fixed Issues")

4. **Issue links** — Every Fixed Issue and Known Issue entry must start with the
   correct GitHub issue ID and URL from the export. Flag any missing or wrong link.

5. **Feature links** — For every "For more information" line in New and Changed
   Features, verify that the linked doc page exists in `docs/`. Flag invented or
   broken doc links.

6. **Tone** — Flag any sentences that:
   - Contain raw error messages or exception text
   - Use passive voice excessively
   - Are too technical for an end-user audience
   - Use first-person ("I", "we") instead of second-person ("you")

7. **MDX validity** — Flag any broken front-matter, unclosed JSX/HTML tags,
   or stray `<` characters that would break Mintlify rendering.

8. **Completeness** — Every New/Changed Feature entry should have:
   - A plain-language title (no `[BUG]` / `[Enhancement]` prefix)
   - A summary paragraph
   - A "What you can do now:" bullet list
   - A "Benefits:" line

Output a structured report with a section for each check above.
For each issue found, give the issue number, the problem, and a suggested fix.
```
