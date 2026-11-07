# Release Notes Automation

A Claude Code skill that writes the ELITEA release notes (`docs/release-notes/rn-X-Y-Z.mdx`) from issue
numbers in [EliteaAI/elitea_issues](https://github.com/EliteaAI/elitea_issues).

## Requirements

- [Claude Code](https://claude.com/claude-code), opened in this repo (`elitea.github.io`).
- GitHub CLI `gh`, signed in with access to `EliteaAI` (`gh auth status`).
- Python 3.9+ (standard library only).

## Usage

Run these in Claude Code, in this order for a new release:

```text
/release-notes init 2.0.9 December 06, 2026
/release-notes new 7011 6958 6903+6904
/release-notes changed 6896 7087+7194+7033
/release-notes fixed 7173 6725 7236
/release-notes known 7128 7233
/release-notes intro
```

- `A+B` groups issues into one feature. Issue URLs work too.
- Each command **replaces** its section. Add `--append` (or say "also add …") to keep what is there.
- `/release-notes status` lists the sections, TODO doc links and screenshots still to create.
- `/release-notes order changed "Pipelines Editor 2.0" "Skills as Standalone Entities"` reorders features.
- Plain requests also work: "add 7264 and 1977 under New Features".

After each command Claude reports what it added, the scope decisions to check, missing doc links and
screenshot placeholders. Review the diff before committing.

## How it works

| Part | Role |
|---|---|
| `SKILL.md` | Workflow and commands the model follows |
| `style-guide.md` | Writing style, feature block template, scope rules. **Edit this to change how notes are written.** |
| `scripts/fetch_issues.py` | Fetches issues, sub-issues, comments and merged PRs in parallel; writes short user-facing digests with FLAGS (other milestone, comments that change scope, …). Cache: `/tmp/rn/<version>/` |
| `scripts/doc_index.py` | Finds doc pages, heading anchors and existing images; checks links |
| `scripts/rn_file.py` | Creates the release file, archives the previous one, updates `docs.json`, replaces sections, sorts issue lists |
| `../../agents/rn-drafter.md` | Sonnet subagent that drafts one feature block; several run in parallel |

The scripts do all GitHub and file work, so the model reads only ~1–10 KB per feature instead of full issues.

## Contributing

- Writing rules → `style-guide.md`. Workflow → `SKILL.md`. Keep both short; they are loaded on every run.
- Script changes: run them by hand first, e.g.
  `python3 .claude/skills/release-notes/scripts/fetch_issues.py --release 2.0.8 7189` and read the digest in `/tmp/rn/2.0.8/digests/`.
- `rn_file.py init` can be tested safely on a copy: `cp -R docs .claude /tmp/x && cd /tmp/x && python3 .claude/skills/release-notes/scripts/rn_file.py init 9.9.9`.
