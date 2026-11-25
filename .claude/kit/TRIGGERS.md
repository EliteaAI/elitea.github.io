# Form kit: what runs when

This page explains when each part of the form kit runs, and how you start it. For setup, see [README.md](README.md).

The kit has five kinds of parts. They start in different ways:

| Part | Starts | You do |
|---|---|---|
| `CLAUDE.md` + `KIT.md` | At the start of every chat | Nothing |
| Rules | When Claude reads or edits a matching page | Nothing |
| Skills | When your request matches a skill's description, or when you type `/<name>` | Ask in your own words |
| Proofreader helper | When a skill decides the text is long enough | Nothing, or "use the proofreader" / "do it yourself" |
| Scripts | When a skill runs them, or when you run them in a terminal | Optional: run them yourself |
| Hook | After every edit Claude makes to a page | Nothing |

## Instructions: CLAUDE.md and KIT.md

| File | When | What it does |
|---|---|---|
| `CLAUDE.md` | At the start of every chat in `elitea.github.io` | Loads `KIT.md` |
| `.claude/kit/KIT.md` | Loaded through `CLAUDE.md` | The rules Claude always follows: report first and act only on approval, re-read before editing, never invent, never commit; the report table and the findings format |

These load only when the chat **starts** in `elitea.github.io`. If you open the parent folder instead, the kit does not load.

## Rules

Claude Code loads a rule file automatically when Claude reads or edits a file that matches the rule's `paths:`. You cannot start them by hand, and you do not need to.

| Rule file | Loads for | Content |
|---|---|---|
| `mdx-language.md` | any page `docs/**/*.mdx` | Voice, grammar, punctuation, capitalization |
| `mdx-words.md` | any page `docs/**/*.mdx` | Usage dictionary, time-anchored words |
| `mdx-structure.md` | any page `docs/**/*.mdx` | Headings, links, lists, tables, numbers |
| `mdx-highlighting.md` | any page `docs/**/*.mdx` | Bold, italic, code |
| `mdx-components.md` | any page `docs/**/*.mdx` | Callouts, See Also, accordions, tabs, cards |
| `mdx-media.md` | any page `docs/**/*.mdx` | Images, alt text, videos |
| `mdx-inclusive.md` | any page `docs/**/*.mdx` | Navigation wording, accessibility, localization |
| `release-notes-scope.md` | `docs/release-notes/**` | Release notes belong to the `release-notes` skill |

**Pages outside `docs/`** (for example a copy in a temp folder): the rules do not load. Say "read `.claude/rules/` first" in your request.

## Skills

A skill starts in one of two ways:
- **In your own words.** Claude compares your request with each skill's description. The examples below are not fixed phrases; any wording with the same meaning works.
- **By name.** Type `/` and the skill name, for example `/non-fact-polish`, optionally followed by the page and lines.

### non-fact-polish: check or fix the form of text

| | |
|---|---|
| **Starts when you ask** to check or fix spelling, grammar, punctuation, wording, formatting, broken links or anchors, media paths, video size or Mintlify validity |
| **Examples** | "check the page for misspellings"; "fix the broken links on lines 40-60"; "is this section valid for Mintlify?" |
| **Asks first** | If you only say "check this page": facts or form? (This kit checks form only.) |
| **Runs** | `df.py lint`, `df.py links`, `df.py size`, and `df.py media big` when there are videos. Then its own check (up to 3 sentences) or the **proofreader** (more). |
| **Stops** | After the numbered report: you say "fix 1, 3, 5", "fix all" or "fix none" |
| **Then** | Fixes only the approved items, reruns `links` or `validate` if needed, reports `was → is` |

### format: change the layout, not the words

| | |
|---|---|
| **Starts when you ask** for existing lines as a list, table, callout, accordion, cards, tabs or See Also, with an image width, or laid out like another section |
| **Examples** | "format lines 31-32 as a bulleted list"; "make this a note"; "lay out this section like Share Chats" |
| **Asks first** | If you might want the words changed too |
| **Runs** | `df.py validate` when a component changed; `df.py links` when links moved |
| **Stops** | One component or up to 3 sentences: applies it, then asks you to approve (undoes exactly those lines on "no"). Bigger: shows it first. |

### media: images, videos and alt texts

| | |
|---|---|
| **Starts when you ask** to add an image or video, place one correctly (for example inside its list item), or add or fix alt texts |
| **Examples** | "to line 40 add the video chat_import"; "fix the alt texts on this page"; "move this screenshot into step 3" |
| **Runs** | `df.py media used` (where the file is used), `df.py media big` (video size), `df.py links` after inserting |
| **Stops** | One requested item: inserts it, then asks you to approve (removes it on "no"). Several items or changes to existing alt texts: shows a table first. Always asks before using a new GIF (the rule says MP4). |
| **Then** | The post-edit hook checks the tag and alt text |

### orphans: where media is used, and unused media

| | |
|---|---|
| **Starts when you ask** where a media file is used, or which files in a folder no page uses |
| **Examples** | "find pages that use settings_general.png"; "are there images in the analytics folder used nowhere?" |
| **Runs** | `df.py media used`, `df.py media orphans`; `df.py links --all` only after you delete files and ask |
| **Stops** | Reports file names only. Never deletes or moves files. |

### relink: links to a page or section

| | |
|---|---|
| **Starts when you ask** which pages link to a page or section, or to fix those links after a rename, move or deletion |
| **Examples** | "look for links that target config-mnmt.mdx"; "I renamed this page, fix the links"; "the heading Share Chats is now Share a Chat" |
| **Runs** | `df.py inbound` (finds the links), `df.py links` (checks after fixing) |
| **Stops** | After the report: you choose which links to fix |

### stamp: the accuracy stamp

| | |
|---|---|
| **Starts when you ask** to build or read a page's accuracy stamp, or which code state a page was checked against |
| **Examples** | "stamp this page for 2.0.9"; "what is this page's baseline?" |
| **Asks first** | In one message: version, workflow (`n` new, `f` full rework, `u` partial update) and code branch. It builds the line only if you say the page was checked against the code. |
| **Runs** | `df.py stamp read`, `df.py stamp build` (reads the current SHAs from the code repos) |
| **Then** | Shows the line in chat with where it goes. **You paste it**; the kit never edits the page for the stamp. |
| **Setup once** | The code repos next to `elitea.github.io`, and `python .claude/kit/df.py cfg branch main` in your terminal |

### Skills that are not in this kit

These requests do **not** start a form-kit skill: checking facts against the code, writing a new page, updating a section after a release, renaming a term on every page. Claude answers them as a plain chat, without the kit's routines.

## Proofreader helper

| | |
|---|---|
| **Starts** | Only from `non-fact-polish`, when the scope has more than 3 prose sentences (`df.py size`). Alt text, headings, table headers, tags and media lines are not counted. |
| **You can change it** | "use the proofreader" (also for short text) or "do it yourself" (no helper) |
| **Model and cost** | Sonnet. About 40k tokens to start, so short text is checked without it. |
| **Does** | Language check against the rules, including what the lint script cannot check. Reports only; never edits. |

## Scripts

All scripts run without the model and never edit pages. Skills run them for you; you can also run them yourself, from `elitea.github.io`:

```
python .claude/kit/df.py <command>
python .claude/kit/df.py              (lists all commands)
```

| Command | Run by | Use it yourself to |
|---|---|---|
| `lint <page> [--lines A-B]` | non-fact-polish; the hook (changed lines only) | See style issues a script can find |
| `links <page>` / `links --all` | non-fact-polish, format, media, relink, orphans | Find broken links, anchors and media paths in one page or all pages |
| `inbound <page>` | relink, non-fact-polish | See which pages link to a page |
| `media used <file>` | media, orphans | See where an image or video is used |
| `media orphans <folder>` | orphans | List unused files in a media folder |
| `media big [MB]` | media, non-fact-polish | List videos and GIFs over the size limit (default 20 MB) |
| `validate` | non-fact-polish, format | Run `mint validate` in `docs/` |
| `size <page> [--lines A-B]` | non-fact-polish | Count prose sentences (decides: up to 3 → Claude itself, more → proofreader) |
| `find <regex> [--in <folder>] [--words]` | none in this kit | Find text in page prose, skipping code and frontmatter |
| `findings add/show/set/lists` | non-fact-polish | See the numbered findings, for example `findings show docs/menus/chat.mdx open` |
| `stamp read <page>` | stamp | See a page's stamp and baseline |
| `stamp build <page> <version> <n\|f\|u>` | stamp | Build a stamp line yourself (no write) |
| `cfg` / `cfg branch <name>` / `cfg repo <name> <path>` | stamp | Show or set the code repo paths and code branch, saved in `.claude/local.json` |

## Hook

| Hook | When | What it does | You do |
|---|---|---|---|
| `post_edit.py` (PostToolUse) | After every Write or Edit Claude makes to a `.mdx` page in `docs/`, except `styleguides/` and `archive/` | Runs `lint` and the link check on **only the changed lines**. If it finds something, it tells Claude at most 3 issues (and how many more). Silent when clean. Never blocks or edits. | Nothing. It is set in `.claude/settings.json`. |

The hook does not run for pages outside `docs/`, for edits you make yourself in the editor, or for files other than `.mdx`.

## Quick reference: from request to parts

| You say | Skill | Scripts | Helper | Hook |
|---|---|---|---|---|
| "check lines 10-30 for misspellings" | non-fact-polish | lint, links, size | proofreader if more than 3 sentences | after fixes |
| "fix the broken links" | non-fact-polish | links, inbound | none | after fixes |
| "make lines 31-32 a bulleted list" | format | validate, links | none | after the edit |
| "add the video chat_import to line 40" | media | media used, media big, links | none | after the edit |
| "where is settings_general.png used?" | orphans | media used | none | none (no edit) |
| "I renamed this page, fix the links" | relink | inbound, links | none | after fixes |
| "stamp this page for 2.0.9" | stamp | stamp read, stamp build | none | none (you paste the line) |
