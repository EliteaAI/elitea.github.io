---
name: release-notes
description: Create or update ELITEA release notes (docs/release-notes/rn-X-Y-Z.mdx) from GitHub issue numbers in EliteaAI/elitea_issues. Use for "/release-notes", "add these issues to new/changed/fixed/known", "start release notes for X.Y.Z", or "write the release intro".
argument-hint: "init <ver> [date] | new|changed [--append] <ids> | fixed|known [--append] <ids> | intro | order <section> <headings…> | status"
---

# ELITEA Release Notes

Turns issue numbers into finished release-notes sections. Scripts do the fetching, doc lookup and file edits;
the model only writes text. Keep token use low: **read digests, never raw issues; never re-read the whole release file.**

All paths below are relative to the repo root (`elitea.github.io`). Scripts:
`S=.claude/skills/release-notes/scripts`

- `$S/fetch_issues.py` — issues + sub-issues + comments + merged PRs → compact digests and FLAGS (cached in `/tmp/rn/<ver>/`)
- `$S/doc_index.py` — doc pages, anchors and images (`links`, `images`, `check`)
- `$S/rn_file.py` — `current`, `init`, `set`, `order`, `status` on the latest release file and `docs.json`

Style and scope rules: [style-guide.md](style-guide.md). Read it once per session before writing.

## Arguments

`$ARGUMENTS` = `<command> [options] <specs>`

| Command | Meaning |
|---|---|
| `init <ver> [date]` | Start a release: archive the current latest file (links fixed for the deeper folder), create `rn-<ver>.mdx` from the template, update `docs.json` (Latest, Recent keeps 2, rest moves to Older). |
| `new <specs>` / `changed <specs>` | Write the New / Changed Features section. |
| `fixed <specs>` / `known <specs>` | Write the Fixed / Known Issues list (sorted by ID descending). |
| `intro` | Rewrite the intro paragraph from the current sections. |
| `order <new\|changed> "Heading" …` | Reorder feature blocks. |
| `status` | Show sections, TODO links and images to create. |

**Specs**: issue numbers or URLs separated by spaces or commas. `A+B+C` groups issues into **one** feature.
URLs like `https://github.com/EliteaAI/elitea_issues/issues/7011` → `7011`.

**Replace vs append**: by default the command **replaces** the section. Add `--append` (or the user says "add", "also add", "add these too") to keep existing items. For `fixed`/`known` appending merges by issue ID.

If the user writes in free form ("add these under Changed Features: …", "group these into one feature: …"), map it to the commands above. Separate lists of single issues and groups may arrive in one message: build one spec list (`7011 6958 6903+6904`).

## Workflow

### 0. Current release
```bash
python3 $S/rn_file.py current        # version + path
```
Use that version as `<ver>` for every script (milestone = `R-<ver>`). If the user names a version that isn't the latest, run `init` first (ask only if the version is older than the latest).

### 1. `new` / `changed`
1. Fetch digests (one call, all specs):
   ```bash
   python3 $S/fetch_issues.py --release <ver> <specs>
   ```
   It prints one line per group: `group  digest-path  size  FLAGS`.
2. Draft in parallel — one `rn-drafter` subagent per group, **all in one message**, only after step 1 has printed every digest path (never start drafters in the same turn as the fetch). Prompt each with only:
   `digest: <path>; section: new|changed; release: <ver>; image_n: <n>; out: /tmp/rn/<ver>/blocks/<section>-<group>.md`
   Image numbers: `new` → 1, 2, 3…; `changed` → c1, c2…; continue after existing numbers when appending (see `status`).
   For a single small group you may draft it yourself instead.
3. Order the blocks: SIZE big → medium → small; keep the user's order within the same size.
4. Concatenate the blocks in that order into `/tmp/rn/<ver>/draft-<section>.md` (one `cat` command) and write it:
   ```bash
   python3 $S/rn_file.py set <section> /tmp/rn/<ver>/draft-<section>.md [--append]
   ```
5. Skim the draft file once (not the release file) for style-guide violations: technical terms, missing **Benefits**, more than 6 bullets. Fix them in the draft and run `set` again.

### 2. `fixed` / `known`
1. ```bash
   python3 $S/fetch_issues.py --release <ver> --brief <ids>
   ```
   Read the single `BRIEF` file it prints.
2. Write one line per issue (style guide) to `/tmp/rn/<ver>/draft-<section>.md` in the format
   `* [#ID](https://github.com/EliteaAI/elitea_issues/issues/ID) Sentence.`
   No subagents — this is cheap.
3. `python3 $S/rn_file.py set <section> /tmp/rn/<ver>/draft-<section>.md [--append]` (sorting is automatic).

### 3. `intro`
1. `python3 $S/rn_file.py status` gives all feature headings.
2. Write the paragraph (style guide → Intro) to `/tmp/rn/<ver>/draft-intro.md`, then
   `python3 $S/rn_file.py set intro /tmp/rn/<ver>/draft-intro.md`.

### 4. `init`
```bash
python3 $S/rn_file.py init <ver> [--date "December 06, 2026"]
```
Report what was archived and how `docs.json` changed. Remind the user to check `git diff docs/docs.json`.

## Report (always, at the end)

Keep it short. Use this structure:

```
**Added to <Section>** (<n>): <Heading> (#ids), …
**Check these scope decisions**
- #id: <decision, e.g. "left out #7164 (R-2.0.9)", "sub-issue #7242 covers Chats only — wrote the full story">
**Still to do**
- TODO doc links: <features>
- Screenshots to create: <placeholder files>
- Not in R-<ver>: <ids with another milestone>   (fixed/known: "still OPEN" is expected, do not list)
```

Flag, never stop and ask, unless the command itself is ambiguous.

## Guardrails

- Never edit sections other than the one requested (the scripts guarantee this — always use `rn_file.py set`).
- Never commit or push unless the user asks.
- The release file may have been edited by the user; `rn_file.py` works on the current file content, so their edits in other sections are kept.
- If `gh` fails (auth, rate limit), report it and stop.
- `--refresh` on `fetch_issues.py` when the user says issues were updated since the last run.
