---
name: research
description: Use whenever the user wants information about a feature found in the code repos and added to a docs page at a given place, in any wording (for example "review the repos and find info about webhooks, add it to line 40").
---
# research

## 1. Ask and prepare
- What to find (the feature), where to add it (page and line or "after section X"), and how much (a sentence, a list, a section). Ask if unclear.
- Ask: "Use code branch `<saved>` for EliteaUI, elitea-sdk and elitea_core?" Wait.
- Run `python .claude/kit/df.py map advice <feature>`; offer a rebuild only if it says so.
- Ask for a reference section to copy the pattern from if the place has no clear neighbor pattern.

## 2. Facts (one code-scout)
- Run the **code-scout** helper once, task **facts**, for the three repos, with the feature, the maps and the page terms near the target line.
- Record any "map gap" it reports (`df.py map gap …`).
- Show the facts to the user (each with `repo path:line`) before writing. Ask which ones to include. Facts the code does not show are never written.

## 3. Write
- 3 sentences or fewer: write it yourself.
- More: run the **writer** helper, mode **new section** (or rewrite, if it changes existing lines), with the approved facts and the reference.
- New text goes straight into the file at the target place (re-read it first); report `added lines A-B`, the facts used and every `{{TODO}}`/`{{MEDIA}}` placeholder, and ask for approval. Remove exactly those lines on "no".

## 4. After writing
- If more than 3 sentences were added: ask "Run the reviewer on lines A-B?" and run it only on a yes.
- Offer `non-fact-polish` for the new lines and `media` for any `{{MEDIA}}` placeholders.
- Do not stamp the page (only a full check of the page does that).
