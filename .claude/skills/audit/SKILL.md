---
name: audit
description: Use whenever the user wants a docs page, section, paragraph or line compared with the code (EliteaUI, elitea-sdk, elitea_core) to find contradictions, inconsistencies and omitted information, or a release-notes text checked against pages, in any wording (for example "check this page against the code repos, report inconsistencies and omitted info, change nothing"); reports only.
---
# audit

Reports only. Never edits the page. Also used as step n-2/f-3/u-3 of new, rework and update.

## 0. Mode
Two modes. Pick from the user's words; if unclear and the page has SHAs, ask: "Full check, or only what changed since <baseline>?"
- **full** (default): is everything on the page (or scope) correct? Steps 1-4, one code-scout.
- **changes**: what changed in the code since the page's SHAs ("since the stamp", "since the SHAs", "what changed since 2.0.8"). Steps 1, C1-C3 and 4. Needs a baseline: `df.py stamp read <page>`, or, for a legacy `verified:` block, its `ui`/`sdk`/`core` SHAs read from the frontmatter. No baseline: say so and offer **full**.

## 1. Scope and branch
- Page = the file the user names, else the file open in the IDE; scope = page, section (heading to next heading of the same or higher level), or lines. Read only the scoped lines.
- Ask: "Use code branch `<saved>` for EliteaUI, elitea-sdk and elitea_core?" Wait. Save a new one with `df.py cfg branch <name>`. When called from new, rework, update or research, the branch is already set there: do not ask again.
- Run `python .claude/kit/df.py map advice <topic>`. If it advises a rebuild, offer it (cost about 75k tokens per map) or go on with the old maps; the user decides.

## 2. Page terms (no LLM, main session)
- From the scoped lines, list: UI labels (bold), toolkit and tool names, routes, numbers and limits, settings and permissions mentioned, flows described (steps in order), and claims about who can do what.
- Write them to `audit/<page-slug>-terms.md` in the kit's temp folder (`doc-factory/` in the system temp dir, shown by `df.py cfg`), with the Write tool.

## 3. One code-scout for all three repos
- Run the **code-scout** helper once, task **facts**, with: the three repo paths, the ref `origin/<branch>`, the three map files, the terms file, and the topic.
- Ask it to answer each term as confirmed / different / not found (with `repo file:line`), and to list user-visible facts in the scoped feature that the terms do not mention.
- Record every "map gap" it reports: `df.py map gap <repo> "<topic>" "<pointer>"`.
- The user can ask for three scouts (one per repo, in parallel; about 3× the tokens) instead.

## C1. Changes mode: what changed (no helper, main session)
- For each repo: `git -C <repo> diff --stat <sha>..origin/<branch>` and `git -C <repo> log --oneline <sha>..origin/<branch>`. Show the commit count per repo.
- Keep only files and commits that touch the page's topic (page terms, the map lines for the topic, folder names). Ignore the rest.

## C2. Changes mode: read the relevant diffs
- Read `git -C <repo> diff <sha>..origin/<branch> -- <file>` for the kept files only, and compare them with the page lines they affect.
- Backend permissions and limits count too (`require_*`, roles, `MAX_*`), not only UI labels.
- If more than about 15 relevant files remain, run one **code-scout** with the list of files and commits instead of reading them yourself.

## C3. Changes mode: what it does not cover
- In the report, say plainly: claims on the page that did not change since the baseline were not checked; a full check finds facts that were already wrong before it.
- Note the baseline branch (for example `release/2.0.8`) and that the diff runs to `origin/<branch>`; do not claim which release a change shipped in.

## 4. Report (gate)
- First line: code branch and short SHAs of the three repos. In **changes** mode, also the baseline SHAs and the commit count since each.
- In **changes** mode, cite the commit (short SHA and ticket, for example EL-7489 `4fe117b8b`) for each finding where you have it.
- One table, numbered, saved with `df.py findings add <page> <json-file>` (format in `work-gates.md` > Reports): `# | line | finding | evidence (repo path:line) | was → is | severity`.
  - high: the page says something the code contradicts, or describes a step that does not work.
  - medium: user-visible information that is missing (limits, conditions, who sees what).
  - low: details, optional clarifications.
- Separate from the table, in two short lists: "could not verify" (term not found anywhere) and "style issues noticed" (do not mix them into facts; offer non-fact-polish).
- Never propose text for facts the code does not show; mark them "unverified".
- Stop. Change nothing. The user decides what happens next (fix some items here, or run update/rework).

## 5. Release-notes coverage (when asked)
- "Are all features in this text described in pages A and B?": list each feature from the text, then for each the page and line that covers it, or "not covered". No code check unless asked.
