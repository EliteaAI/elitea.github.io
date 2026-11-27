---
paths:
  - "docs/**/*.mdx"
  - "elitea.github.io/docs/**/*.mdx"
---
# Mintlify components (from styleguide: Mintlify components, plus user decisions)

## Callouts (alert boxes)
- Use sparingly. Never a callout right after a callout. No blockquotes.
- `<Note>`: additional information that the reader does not need to succeed.
- `<Warning>`: deprecated features, legacy disclaimers, future-feature disclaimers.
- `<Danger>`: removed features.
- `<Tip>`: never (ambiguous). `<Check>`: not used.
- `<Info>`: no "when to use" rule yet. Never for See Also (book callout), definitions or concept explanations (put them in the text), prerequisites or structure (heading or list), or plain extra information (`<Note>`).
- ELITEA tip: `<Callout icon="lightbulb" color="#a855f7" title="…">`.
- Cross-references ("For more information, see …") are normal sentences, never inside a callout.

## See Also (page end)
- Exactly `<Callout icon="book" color="#C9B896" title="See Also">`, then a `-` bullet list of links (relative, no `.mdx` extension). No "See also:" line inside, no explanations after the links.

## Accordions
- No general rule in the styleguide yet. Troubleshooting entries (user decision): `<Accordion title="…">` with **Cause:** and **Solution:**.

## Tabs
- Titles: brief (under 25 characters), parallel, sentence case. Other tab rules are not defined yet.

## Tooltips
- Only for abbreviations that are not common. Never at the first use (spell the abbreviation out there).

## Cards
- `<CardGroup>` with same-page `#anchor` cards is fine as a page intro (user decision; overrides "avoid same-page anchors" for this case).
