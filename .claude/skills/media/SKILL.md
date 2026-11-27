---
name: media
description: Use whenever the user wants an image or video added to a docs page, an existing one placed correctly (for example inside its list item), or alt texts added or fixed, in any wording (for example "to line 40 add the video chat_import" or "fix the alt texts on this page").
---
# media

## 1. Find the file (no LLM)
- The user gives a file name, a path or a description. Find it: `python .claude/kit/df.py media used <name>` (where it is already used) or search `docs/img/` with Glob for the name.
- Several matches: list them and ask. No match: say so; never invent a path.
- Video: check the size (`df.py media big`, limit 20 MB) and format (MP4). A new GIF: tell the user the rule says MP4 and ask before using it.

## 2. Prepare the insertion
- Re-read the target line and its surroundings.
- If the target line is a list item (or the image illustrates a step), place the media **inside** that item, indented to the item's text, after an empty line.
- Path: relative from the page to `docs/img/…` (`../../img/…`). Tags exactly:
  - image: `<img src="…" alt="…" />` (copy a `width` only if the user gives one)
  - video: `<video src="…" controls />` (no alt)
- Alt text (images only): describe the purpose in this context, with the page's own terms for the UI (read the step and the nearby text). Up to 155 characters, sentence case, ends with a period, no formatting. Reuse the alt text other pages use for the same recurring UI element.

## 3. Apply and report
- Insertion of one requested item: insert it, then report `line N: added <tag>` with the alt text, and ask for approval (remove it on "no").
- Several items, or changes to existing alt texts: show a table `# | line | was → is` first and wait for approval.
- After writing: `python .claude/kit/df.py links <page>` for the new path. The after-edit hook checks the tag and alt text.
