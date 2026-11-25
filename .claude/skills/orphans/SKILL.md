---
name: orphans
description: Use whenever the user wants to know where a media file is used, or which media in a folder no page uses (or only other pages use), in any wording (for example "find pages that use settings_general.png" or "are there images in the analytics folder used nowhere?"); reports file names only.
---
# orphans

Scripts only; no helper. The media folder is large: never list or read it by hand.

## Where is a file used
- `python .claude/kit/df.py media used <file name>` → every page and line. Report the list. Done.

## Unused files in a folder
- `python .claude/kit/df.py media orphans <folder>` (for example `img/how-tos/chat-conversations/chats/config-mnmt`).
- "Used only by other pages": for each file in the folder run `df.py media used <file>`, and keep files whose pages are not the page the folder belongs to. Report them separately from orphans.
- Also report files of the same name that exist in another folder (one may be a copy that is used).

## Report
- Table: `# | file (path from docs/) | size MB | used by`. File names only; no commands.
- Mark a file as unused only if no page uses it, including release notes and `docs/archive/`.
- Never delete files: the user deletes them herself.

## After the user deletes files
- Only when she asks: run `python .claude/kit/df.py links --all` and report any broken references.
