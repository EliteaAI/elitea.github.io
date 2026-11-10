---
paths:
  - "docs/**/*.mdx"
  - "elitea.github.io/docs/**/*.mdx"
---
# Content sourcing

- Document only behavior, labels, fields and defaults that exist in the code. No assumptions, no invented features.
- Check the release branch (`release/x.y.z`) of `../EliteaUI`, `../elitea-sdk` and `../repos/elitea_core`, not only `main`.
- Take UI labels, button text and field names verbatim from `../EliteaUI`.
- Take tool names, parameters and credential fields from `../elitea-sdk`.
- When a ticket drives the change, cover only its acceptance criteria.
- If code and ticket disagree, or a fact is missing, ask; mark the gap as an open question, never guess.
- Delegate wide code research to the `doc-researcher` agent; keep raw code out of the page.
