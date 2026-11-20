# Doc-factory kit: what is inside

State on 2026-11-18, branch `euch/doc-factory` of `elitea.github.io`. Code maps were built from `main` (EliteaUI `55fe88c`, elitea-sdk `e9d96aa`, elitea_core `8cb174b`). For setup on a new machine, see [README.md](README.md).

The kit has six parts:

| Part | Folder | What it does | Token cost |
|---|---|---|---|
| Entry point | `CLAUDE.md`, `.claude/kit/KIT.md` | Tells Claude how to work on the docs | Loaded into every chat |
| Rules | `.claude/rules/` | House style, compiled from `docs/styleguides/` | Loaded only when a `docs/` page is used |
| Routines (skills) | `.claude/skills/<name>/SKILL.md` | Step lists for typical tasks | A one-line description per chat; the full text only when used |
| Helpers (agents) | `.claude/agents/` | Separate Claude sessions for big jobs | About 40k tokens each time one starts |
| Scripts | `.claude/kit/df.py`, `.claude/kit/lib/` | Checks and searches without the model | None |
| Hooks | `.claude/kit/hooks/`, wired in `.claude/settings.json` | Run automatically around Claude's actions | None |

Caches and findings lists go to the system temp folder `doc-factory/` (on Windows `%TEMP%\doc-factory\`), never into the repo. Deleting that folder is safe, except `maps/gaps.md` (see [Knowledge maps](#knowledge-maps)).

## Entry Point

- **`CLAUDE.md`** (repo root): one line that imports `KIT.md`. The parent folder has its own `CLAUDE.md` with the same import, for sessions started there.
- **`.claude/kit/KIT.md`**: the short instructions Claude always follows:
  - where content, navigation and media live
  - the code repos are read-only and are read on the chosen branch through git (`origin/<branch>`)
  - ask for the code branch before every code task, and show branch and SHAs in every code-based report
  - precedence: code > existing pages > styleguides (style only)
  - gates: report first and act only on approved numbered findings, re-read before each edit, never invent (use `{{TODO: …}}`), never commit or push
  - the report table format and the findings numbers
  - which model each helper uses, and when to use the reviewer (more than three changed sentences)
  - rules load automatically only in `docs/`; for temp copies they must be read by hand

## Rules

Each rule file starts with `paths:`. Claude Code loads it automatically when a matching file is used.

| File | Loads for | Content |
|---|---|---|
| `mdx-language.md` | `docs/**/*.mdx` | Voice, grammar, punctuation, capitalization |
| `mdx-words.md` | `docs/**/*.mdx` | Usage dictionary: words to use and avoid, time-anchored words |
| `mdx-structure.md` | `docs/**/*.mdx` | Headings, links, lists, tables, numbers and dates |
| `mdx-highlighting.md` | `docs/**/*.mdx` | Bold, italic, inline code, code blocks |
| `mdx-components.md` | `docs/**/*.mdx` | Callouts, See Also, accordions, tabs, tooltips, cards |
| `mdx-media.md` | `docs/**/*.mdx` | Images, alt text, videos, deleting media |
| `mdx-inclusive.md` | `docs/**/*.mdx` | Navigation wording, sensitive data, accessibility, localization |
| `work-gates.md` | `docs/**` | How to work with the user: approval, editing, "done" checks, reports, findings file format and states |
| `release-notes-scope.md` | `docs/release-notes/**` | Release notes belong to the `release-notes` skill |

## Routines (Skills)

Claude starts a routine when a request fits its description. You can also type `/<name>`. **STOP** means Claude waits for your answer.

| Routine | Use it for | Helpers | Stops |
|---|---|---|---|
| `audit` | Compare a page, section or line with the code, or check release-notes text against pages. Reports only. Two modes: **full** (is everything correct?) and **changes** (what changed since the page's SHAs, from `git diff`; for a legacy `verified:` block too). | full: code-scout; changes: main chat, code-scout only for 15+ files | Branch, report |
| `update` | Update one named part of a page after a release change | code-scout; writer for more than 3 changed sentences; reviewer on request | Branch and stamp (one question), findings, wording, polish |
| `rework` | Review a whole page against the code and rework it section by section | code-scout; writer; reviewer on request | Branch and stamp (one question), findings, each section, polish, links |
| `new` | Write a new page: facts, outline, draft, media, polish, stamp line, backlinks, navigation | code-scout, writer; reviewer on request | Branch and stamp (one question), facts and outline, review, polish, backlinks, navigation |
| `research` | Find facts about a feature in the code and add them at a given place | code-scout; writer for more than 3 sentences | Branch, facts, text |
| `radar` | Has anything in the code changed since the page's stamp? On request only. | drift-triager (Haiku) | Report |
| `non-fact-polish` | Check form, not facts: spelling, grammar, wording, formatting, links, media paths, Mintlify validity | proofreader for more than 3 sentences | Report |
| `format` | Change the layout without changing the words: list, table, callout, tabs, See Also and more | none | Result |
| `media` | Add an image or video, place it correctly, or fix alt texts | none | Result |
| `relink` | Find links to a page or section, and fix them after a rename, move or deletion | none | Report |
| `rename-term` | Find a term across pages, or change a label or feature name everywhere | none | Report |
| `orphans` | Where is a media file used? Which media in a folder are unused? Reports file names only. | none | None |
| `stamp` | Read a page's stamp, or build a new stamp line and show it in chat for you to paste (never edits the page) | none | None |

`release-notes` (with its helper `rn-drafter`) is a separate skill and not part of the kit.

## Helpers (Agents)

| Helper | Model | Tools | Job |
|---|---|---|---|
| `code-scout` | Sonnet | Bash, Read, Grep, Glob | Reads the code repos through git on the chosen branch. Returns doc-relevant facts with `repo file:line`, or drafts a knowledge map. Read-only. |
| `writer` | Sonnet | Read, Grep, Glob, Edit, Write | Writes MDX from given facts, the rules and a reference page. New pages and sections go straight into the file; rewrites are proposals only. |
| `proofreader` | Sonnet | Read, Grep, Glob, Bash | Language check against the rules, including what the lint script cannot check. Reports only. |
| `reviewer` | Sonnet | Read, Grep, Glob | Fresh-eyes content and wording review of changed text. Reports only. Inside `new`, `rework` and `update` it runs only after you say yes. |
| `drift-triager` | Haiku | Read | Sorts radar candidates into likely affected, unclear and unaffected. Reports only. |

## Scripts

Run from `elitea.github.io`: `python .claude/kit/df.py <command>`. None of them use the model, and none edit pages: `docs.json` edits are only proposed, and Claude applies them with Edit after your approval. The stamp line is shown in chat, and you paste it yourself.

### Config

| Command | What it does |
|---|---|
| `cfg` | Shows the repo paths, the saved code branch and the lock state |
| `cfg branches` | Lists the release branches in each code repo |
| `cfg branch <name>` / `cfg branch clear` | Saves the code branch (checked in all three repos) or clears it |
| `cfg repo <name> <path>` | Sets a code repo path for this machine |
| `cfg lock on` | Turns on the setup lock: `docs/` becomes read-only for Claude. Only you can run `cfg lock off`, in your own terminal. |

The values are saved in `.claude/local.json` (git-ignored, per machine).

### Checks (read-only)

| Command | What it does |
|---|---|
| `lint <page> [--lines A-B,C] [--as <page>]` | Style patterns: en dash, ellipsis, spaced em dash, exclamation mark, contractions, "ELITEA's", "allows you", "need to", words to avoid (simply, click, navigate to, pop-up and others), time-anchored words, below/above, "personal project", "This page is about", "here" as link text. `--as` applies a real page's rules to a temp copy. |
| `links <page>` / `links --all` | Broken links, anchors and media paths. For a missing file it shows where a file with that name exists. |
| `inbound <page>` | Pages that link to a page, with lines, link texts and anchors |
| `media used <file>` | Pages and lines that use a media file |
| `media orphans <folder>` | Media in a folder that no page uses |
| `media big [MB]` | Videos and GIFs over the size limit (default 20 MB) |
| `validate` | Runs `mint validate` in `docs/` |
| `size <page> [--lines A-B]` | Counts prose sentences. Alt text, headings, table headers, tags and media lines are not counted. Up to 3 changed sentences: the main chat does the work; more: a helper. |
| `find <regex> [--in <folder>] [--words]` | Finds text in page prose only, skipping code, comments and frontmatter. Used for renames. |

### Navigation (`docs/docs.json`, read-only)

| Command | What it does |
|---|---|
| `toc find <text>` | Groups and pages that match a text |
| `toc add <page> --group "<group>" [--after <page>]` | The exact edit that adds a page to the navigation |
| `toc rename <old> <new>` | Navigation entries to change, plus the redirect to add |
| `toc check` | Navigation pages that do not exist, and pages missing from the navigation |

### Accuracy

| Command | What it does |
|---|---|
| `radar <page>` | Code changes since the page's stamp: UI labels from the page that changed or were removed, and changes in code folders the maps link to the page's doc folder |
| `stamp read <page>` | The stamp's version, workflow, date and baseline. A page without SHAs has an "unknown baseline". |
| `stamp build <page> <version> <n\|f\|u> [--branch B]` | Builds the new stamp line and says where it goes. It does not write. `n` = new, `f` = rewritten (rework), `u` = updated. |

Stamp format, one line in the frontmatter:

```
accuracy: {/*PAGE ACCURACY CONFIRMED for 2.0.9 | updated 2026-11-18 | EliteaUI main@f4a1c64 | elitea-sdk main@b3f1d74 | elitea_core main@097b574*/}
```

### Knowledge Maps

The maps in `.claude/kit/maps/` (`EliteaUI.md`, `elitea-sdk.md`, `elitea_core.md`, under 100 lines each, plus `TEMPLATE.md`) point to where facts live in each code repo. Each has a header (repo, branch, SHA, date) and these sections: lookup, features to code folders and doc pages, doc-relevant gotchas, config and flags.

| Command | What it does |
|---|---|
| `map status` | Each map's branch and SHA compared with the saved code branch |
| `map skeleton <repo>\|all` | Writes a script-made fact sheet to the temp folder, as input for a code-scout map draft |
| `map advice [topic]` | Says whether to offer a rebuild: branch switch, 300 or more commits behind, or a known gap for the topic |
| `map gap <repo> "<topic>" "<pointer>"` | Records a gap a code-scout reported, to cover at the next rebuild |
| `map gaps` | Lists the recorded gaps |

Gaps are saved in the temp folder (`doc-factory/maps/gaps.md`). Copy that file before you clean the temp folder.

### Findings

Numbered findings per page, so "fix 1, 2, 5" and "which are still open?" work. Numbers never change.

| Command | What it does |
|---|---|
| `findings add <key> <json-file>` | Adds items from a JSON list with `line`, `finding`, `evidence`, `change` and `severity`, and prints their numbers |
| `findings show <key> [state]` | The table, optionally for one state |
| `findings set <key> <state> <n,n,…>` | Changes the state: `open`, `approved`, `done`, `ok` (checked, no change needed) or `rejected` (you said no) |
| `findings lists` | All keys that have findings |

### Library Files (`.claude/kit/lib/`)

| File | Job |
|---|---|
| `config.py` | Repo paths, code branch, setup lock, temp folder, git calls |
| `mdx.py` | MDX parsing shared by all checks: prose without code, headings and anchors, links, media references, sentence count |
| `checks.py` | Lint patterns, link and anchor check, inbound links, media index |
| `toc.py` | Reads `docs.json`, proposes navigation edits |
| `stamp.py` | Reads and builds stamps |
| `radar.py` | Finds the code changes since a stamp |
| `maps.py` | Map skeletons, status, advice, gaps |
| `findings.py` | The numbered findings lists |

## Hooks

Set in `.claude/settings.json`. They run without the model and cost no tokens.

| Hook | When | What it does |
|---|---|---|
| `guard.py` | Before every Write, Edit or shell command | Allow-list. File tools may write only to `docs/` (blocked while the lock is on), the kit folders, `CLAUDE.md`, the temp folder and Claude's memory notes. Never written: styleguides, `docs/archive/`, the release-notes skill, `.claude/local.json`. Changes to settings, hooks, `config.py` and `.gitignore` need your confirmation. Shell commands may write only to the temp folder. Git: only reading commands; pull, fetch, checkout, switch, merge, rebase, commit and push are yours. It also blocks `cfg lock off` and `gh pr create` or `merge`. |
| `post_edit.py` | After every edit of a `docs/` page | Lints only the changed lines and tells Claude about up to 3 issues. It never blocks or edits. |
| `session_start.py` | When a chat starts | One line: the saved code branch, the lock state, and missing code repos. The VS Code extension does not show it; ask "what's the status?". |

Known limit: the guard reads shell commands as text. A path hidden in a variable or wildcard may not be caught. The Claude Code permission prompt still applies.

## Settings and Local Files

| File | In git | Content |
|---|---|---|
| `.claude/settings.json` | Yes (changed) | Kit permissions (`df.py`, `mint`, reading git commands) and the three hooks, next to the release-notes permissions |
| `.gitignore` | Yes (changed) | Adds `.claude/local.json` |
| `.claude/local.json` | No | Your repo paths, code branch and lock state |
| `.claude/settings.local.json` | No | Your read access to the three code repos |

## Measured Costs (Sonnet 5.5, List Prices)

| Test, 2026-11-18 | With the kit | Without the kit |
|---|---|---|
| Update "Project Details" in `general.mdx` | $0.69, 2.0M tokens, 23 turns, 2 helpers (code-scout, writer) | $0.32, 0.6M tokens, 8 turns |
| Compare Web Search page with the code | One code-scout: 76k tokens, 18 findings | 70k tokens, 10 findings |

Most of the cost is main-chat turns: each turn sends the whole chat again. Every helper start costs about 40k tokens.
