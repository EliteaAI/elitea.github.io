---
paths:
  - "docs/**/*.mdx"
  - "elitea.github.io/docs/**/*.mdx"
---
# Structure & formatting (from styleguide: wording and formatting)

## Titles & headings
- No steps or numbers as page titles.
- No skipped levels; prefer H3 as the deepest. Report every H4. Before adding an H4, ask the user whether that depth is needed.
- Never one lone subsection. Two or more subsections → an intro before the first.
- Title case: all major words, plus the first and last word. "&" instead of "and" (unless an official name). No links in headings.
- Task headings as infinitives ("Create a Chat"); otherwise noun phrases. No -ing headings. Prefix non-basic sections: `Optional: …`, `Legacy: …`.

## Links
- Use links sparingly and inline, with descriptive text; never "here" or "this page".
- Standard phrasing: "For more information, see [X](…)." or "To *do this*, see [X](…)."
- Relative paths without extension, with anchors: `../../menus/chat#share-chats` (user decision; Mintlify resolves them). One link per target per page, in the most useful place; avoid several links in one paragraph.
- Avoid anchor links to sections of the same page (exception: CardGroup intro, see mdx-components).
- Avoid links to external documentation; if one cannot be omitted, report it so the user can plan regular checks.
- No links to restricted pages; if unavoidable, state the access rights or permissions needed.
- Related and further reading go in the See Also callout at the page end (see mdx-components).

## Lists
- Numbered for sequences (steps, rules); bulleted for one-step sequences and unordered items. One action per step; menus as **One** > **Two**.
- Bulleted lists may sit inside numbered lists. Avoid sublevels in numbered lists; none in bulleted lists.
- Align nested items (code, images, tables) with the first character of the list item text.
- In most cases, introduce a list with a sentence. Start items with a capital letter. A period only for full sentences.

## Tables
- Use sparingly. Introduce a table with a short sentence, unless it comes right after the information it illustrates. No captions.
- Sentence-case headers; "None" for empty cells; **Description** column last if possible.
- Avoid footnotes; at most three, and only when the content cannot go in the table.

## Numbers, dates, spacing
- Zero to nine in words, 10 and more in numerals; numerals in titles. Never start a sentence with a number (spell it out). A period as the decimal point.
- `&nbsp;` only between a number and its unit; standard spaces everywhere else. One space between sentences.
- Avoid dates and times. Formats: `YYYY-MM-DD`, `Month DD, YYYY`, `Month, YYYY`, `hh:mm AM`/`hh:mm PM`.
- One empty line between blocks (headings, paragraphs, lists, callouts).
