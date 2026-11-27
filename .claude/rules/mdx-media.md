---
paths:
  - "docs/**/*.mdx"
  - "elitea.github.io/docs/**/*.mdx"
---
# Images & videos (from styleguide: visual standards)

## When to use
- Use illustrations sparingly: they go out of date and are expensive to update and localize. They supplement the text, never replace it.
- Screenshots show UI when text cannot. GIFs and videos only when text cannot convey the information; videos only for key use cases, very rarely.
- Never a screenshot of text, code or terminal output: use real text. Avoid text inside illustrations.

## Placement
- Right after the text it illustrates. When it illustrates a step, put it inside that list item, indented to the item's first character.
- Introduce general illustrations (full interfaces, process diagrams) with one or two sentences; no intro for illustrations right after their text. No captions.

## Images
- Tag: `<img src="../../img/<section>/<area>/<page-slug>/<file>.png" alt="…" />`, relative path. `width` is optional; never add, change or remove it on your own.
- Formats: `.png` for screenshots, `.svg` for diagrams. Mermaid diagrams are allowed (no diagram rules enforced yet).
- New files go in `docs/img/<section>/<area>/<page-slug>/`. File names are not enforced (user decision): keep the existing name when reusing a file.

## Alt text
- On every screenshot, diagram and GIF. Describe the purpose in context, using the terms of the page, for someone who cannot see it.
- Up to 155 characters, sentence case, ends with a period. No bold, italics or all caps.
- `alt=""` only for purely decorative images (report them: such images should be avoided) or when the preceding text fully describes the image.
- The same alt text for the same recurring UI element (icons, buttons, status indicators).

## Videos
- Videos are not images. Tag: `<video src="../../img/…/<file>.mp4" controls />`. No `alt`, no `<img>` for videos.
- New motion media is MP4 under 20 MB (user decision: no new GIFs; existing GIFs stay until the user replaces them).
- Prefer embedded videos from the ELITEA YouTube channel where they exist.

## Before deleting media
- Check every page for references first (script), list the files, and delete only after the user confirms. Never delete or rename media another page uses.

## Human-only (do not check)
Screenshot creation (theme, browser, zoom, margins), highlights (arrows, boxes, numerals, colors), borders and transparency, diagram drawing, masking or blurring personal data, flicker in videos, the three-month cleanup schedule.
