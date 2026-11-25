---
name: format
description: Use whenever the user wants existing docs lines to look or be structured differently without changing the words — as a list, table, callout, accordion, cards, tabs or See Also, with a given image width, or laid out like another section — in any wording (for example "format lines 31-32 as a bulleted list" or "make this a note"); if they may want the words changed too, ask.
---
# format

Formatting only. Every word stays as it is. This routine never writes or rewrites text.

## 1. Read
- Re-read the target lines and a few lines around them. For "like section Y", read section Y too.
- Check `.claude/rules/mdx-components.md` for the component: allowed types (no `<Tip>`, `<Check>`; `<Info>` limits), no callout right after a callout, See Also form, troubleshooting accordions with **Cause:**/**Solution:**.
- If the request conflicts with a rule (for example a callout right after another one), say so and ask before going on.

## 2. Build the new markup
- Use the exact component syntax already used on the page or in the rules; keep indentation consistent with the page.
- Keep every word, link, image tag and `width`. Only markup, line breaks, list markers and component tags change. Add or change a `width` only when the user gives the value.
- Images that illustrate a step stay inside that list item, also inside accordions and tabs.
- When a component needs text that is not there (for example an accordion title, a card title, a tab title): use `{{TODO: title}}` and list it. Never write it yourself.
- "Like section Y": copy Y's layout and components only (not its wording, not its facts).
- If the text itself would need changes to fit (for example it repeats a "See also:" line, or a sentence must be split), report it as a finding; do not change it.
- Never move content to another place on the page unless asked.

## 3. Show and apply
- One component or 3 sentences or fewer: apply it, then report `lines A-B: was → is` and ask for approval; undo exactly those lines on "no".
- Bigger changes or "like section Y": show `lines A-B: was → is` first and wait for approval.
- After applying: `python .claude/kit/df.py validate` when a component was added or changed; `df.py links <page>` if links moved.
