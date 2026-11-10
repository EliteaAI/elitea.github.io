---
name: place-images
description: Use when the user pastes screenshot/GIF/video paths and asks to add them to a doc page ("add these images to the X tabs", "paste the images in the appropriate places").
---

# Place images

Standard: `.claude/rules/images-and-media.md`.

1. Identify the target page and the feature folder name (existing folder under `docs/img/...` if the page already has images: grep the page for `img/`).
2. Look at each image (Read it) only as needed to match it to a step, tab or section. Decide a short descriptive name per image: `cred-navigate`, `toolkit-configs`, `add-agent`.
3. Copy with the script (never overwrite; it prints refs, sizes, KB):
   `python .claude/skills/place-images/place_images.py --page docs/<page>.mdx --feature <feature> --names a,b,c <src1> <src2> <src3>`
   Use `--dry` first if names are uncertain.
4. Insert each reference right after the step or paragraph it illustrates, indented to the step text:
   - wide screenshots (>900 px): `![Alt.](ref)`
   - narrow forms/dialogs: `<img src="ref" alt="Alt." width="400"/>` (500 for tall forms)
   - video: `<video controls><source src="ref" type="video/mp4"/></video>`
5. Write alt text per the rule (context, sentence case, period, ≤155 chars).
6. If a placeholder reference already points at the planned filename, reuse that name so no edit is needed beyond the file copy.
7. If an image matches no section, do not invent one; list it under Open questions.
8. Report: `Changed: <page>, <n> images in docs/img/... | Notes: ... | Open questions: ...`
