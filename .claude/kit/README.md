# Form kit: setup and use

The form kit helps Claude Code check and fix the **form** of ELITEA user documentation: spelling, grammar, wording, formatting, links, anchors, images, videos, alt texts and Mintlify validity. It follows the house style, compiled from `docs/styleguides/`. It does not check facts against the code.

## What You Need

- Python 3.10 or later, available as `python`. On Windows, install it from python.org or with `winget install Python.Python.3.13`. The Microsoft Store placeholder does not work.
- Node.js and the Mintlify CLI (`npm i -g mint`), for `mint validate`.
- Claude Code (CLI or VS Code extension).
- For the stamp only: the code repos `EliteaUI`, `elitea-sdk` and `elitea_core` cloned next to `elitea.github.io`.

## Start

1. In VS Code, open the `elitea.github.io` folder itself.
2. Start a new Claude Code chat. `CLAUDE.md` and `.claude/settings.json` turn the kit on.

## What You Can Ask

| Ask, in any wording | Routine | What it does |
|---|---|---|
| "Check this page for misspellings", "fix the broken links" | `non-fact-polish` | Spelling, grammar, wording, formatting, links, anchors, media paths, video size, Mintlify validity. Reports first, fixes only what you approve. |
| "Format lines 31-32 as a bulleted list", "make this a note" | `format` | Changes the layout without changing the words |
| "Add the video chat_import to line 40", "fix the alt texts" | `media` | Adds images and videos, places them correctly, fixes alt texts |
| "Where is settings_general.png used?", "unused images in the analytics folder?" | `orphans` | Reports file names only. Never deletes. |
| "Which pages link to config-mnmt.mdx?", "I renamed this page, fix the links" | `relink` | Finds links to a page or section and fixes them after a rename, move or deletion |
| "Stamp this page for 2.0.9", "what is this page's baseline?" | `stamp` | Reads the accuracy stamp, or builds a new stamp line and shows it in chat for you to paste. Never edits the page. |

For longer text (more than 3 sentences), Claude runs the **proofreader** helper (Sonnet). Otherwise it checks the text itself.

For when each skill, rule, script and hook runs, and how to start each one, see [TRIGGERS.md](TRIGGERS.md).

## How It Behaves

- **Approval first.** Claude reports numbered findings and changes only what you approve. It never commits, pushes or opens PRs.
- **After-edit check.** After Claude edits a docs page, a script checks the changed lines and reports at most three issues to Claude. It never edits anything.
- **Temp folder.** Findings lists go to the system temp folder (`doc-factory/`), never to the repo. Deleting that folder is safe.

## Scripts

Run from `elitea.github.io`: `python .claude/kit/df.py <command>`. None of them use the model or edit pages.

| Command | What it does |
|---|---|
| `lint <page> [--lines A-B]` | Style patterns: en dash, ellipsis, spaced em dash, exclamation mark, contractions, "ELITEA's", "allows you", "need to", words to avoid, time-anchored words, below/above, "personal project", non-descriptive link text |
| `links <page>` / `links --all` | Broken links, anchors and media paths, with hints for moved files |
| `inbound <page>` | Pages that link to a page |
| `media used <file>` / `media orphans <folder>` / `media big [MB]` | Where a media file is used; unused media; videos and GIFs over the size limit |
| `validate` | Runs `mint validate` in `docs/` |
| `size <page> [--lines A-B]` | Counts prose sentences |
| `find <regex> [--in <folder>] [--words]` | Finds text in page prose |
| `findings add/show/set/lists` | The numbered findings lists |
| `stamp read <page>` / `stamp build <page> <version> <n\|f\|u>` | Reads a stamp, or builds a stamp line (no write) |
| `cfg`, `cfg branch <name>`, `cfg repo <name> <path>` | Code repo paths and the code branch, for the stamp. Saved in `.claude/local.json` (git-ignored). |

## Known Limits

- The script checks only patterns. Oxford commas, word order, ambiguous pronouns and real UI labels need the proofreader or a person.
- The stamp line contains code SHAs. Build it only after the page was checked against the code, by you or another tool.
