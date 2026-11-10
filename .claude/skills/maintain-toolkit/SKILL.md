---
name: maintain-toolkit
description: Use when doc conventions change or the user corrects a recurring mistake and the Claude toolkit (CLAUDE.md, .claude/rules, skills, agents, hooks) must be updated.
---

# Maintain toolkit

Single source of truth. Put each change in exactly one place:

| Change is about | Edit |
|---|---|
| WHAT the standard is (style, structure, naming, links, images, sourcing) | `.claude/rules/<topic>.md` |
| HOW to do a task (steps, commands, order) | `.claude/skills/<task>/SKILL.md` |
| Page shape for toolkit guides | `.claude/skills/create-toolkit-guide/skeleton.md` |
| WHO does it (role, tools, model, return format) | `.claude/agents/<name>.md` |
| Deterministic enforcement (paths, regexes, banned words) | `.claude/hooks/*.py` |
| Repo map, commands, pointers | `CLAUDE.md` |

1. Find where the topic lives: `grep -rn "<keyword>" CLAUDE.md .claude/rules .claude/skills .claude/agents .claude/hooks`.
2. Update that one place; replace duplicates elsewhere with a reference.
3. Limits: CLAUDE.md ≤60 lines; rule ≤40 lines, imperative bullets, `paths:` scoped; SKILL.md ≤100 lines, one-sentence `description`; agent prompt ≤40 lines.
4. A banned word/pattern that is checkable → add to `STYLE` in `validate_doc.py`; a protected path → `BLOCK`/`ASK` in `protect.py`.
5. After hook edits, test: `echo '{"tool_name":"Write","tool_input":{"file_path":"docs/x.mdx"}}' | python .claude/hooks/protect.py; echo $?` and `python .claude/hooks/validate_doc.py docs/<page>.mdx`.
6. Do not edit `docs/styleguides/**` (the human standard), `.claude/skills/release-notes/**` or `.claude/agents/rn-drafter.md` (owned by Levon Dadayan).
7. Report: `Changed: <files> | Notes: <what rule changed> | Open questions: <none or list>`
