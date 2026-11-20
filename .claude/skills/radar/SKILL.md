---
name: radar
description: Use whenever the user wants to know whether a docs page is still accurate — what changed in the code since the page's accuracy stamp — for one or more pages they name, in any wording (for example "check this page for accuracy" or "has anything changed for these pages since 2.0.8?"); runs only on request.
---
# radar

Runs only when the user asks, and only for the pages they name. Reports only.

## 1. Branch
- Ask: "Compare with code branch `<saved>`?" Wait. The stamp says where the page was checked; the branch says what to compare with.

## 2. Candidates (no LLM)
- For each page: `python .claude/kit/df.py radar <page>`.
- "unknown baseline" (no stamp, or a stamp without code SHAs): report it for that page and stop there. Offer `audit` (a full check) instead; after it, the page can be stamped.
- Otherwise the script lists, per repo, the commits since the stamp and the candidates:
  - **label removed**: a bold UI label on the page that the code no longer contains (with page lines and file);
  - **mapped folder changed**: code folders that the knowledge maps link to this page's doc folder, with commit subjects.

## 3. Triage (Haiku)
- No candidates: say "no changes found for this page since <stamp>" and stop.
- Otherwise run the **drift-triager** helper with the page, its stamp and the numbered candidates. It answers likely affected / unclear / unaffected for each.

## 4. Report
- Per page: the baseline, the commit counts, then a table `# | verdict | candidate | page lines | evidence`.
- End with a recommendation per page: nothing to do, `update` (name the sections), or `rework` (many affected sections). The user decides.
- Never edit the page here.
