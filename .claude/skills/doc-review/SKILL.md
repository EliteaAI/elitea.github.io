---
name: doc-review
description: Use when asked to review a doc page or apply the style guide to it ("review X", "check X against the style guide", "apply all style rules to X").
---

# Doc review

1. Run `python .claude/hooks/validate_doc.py <file>` (draft outside docs/: add `--as docs/<path>.mdx`) (deterministic findings).
2. Call the `doc-reviewer` agent with the file path and the validator output. It returns findings only.
3. Mode:
   - "review" / "check": show the findings table; change nothing.
   - "apply" / "fix": apply findings with one Edit per section, wording-only; never change facts, structure or component types unless a finding says so. Ask before restructuring (heading levels, merging sections).
4. Re-run step 1; it must report no new issues in edited lines.
5. Report: `Changed: <file or none> | Notes: <counts by category> | Open questions: <findings needing a decision>`
