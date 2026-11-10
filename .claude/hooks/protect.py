#!/usr/bin/env python
"""PreToolUse guard (Write|Edit|MultiEdit|Bash|PowerShell).

Block (exit 2): protected paths; docs.json edits that leave invalid JSON.
Ask (permissionDecision=ask): edits under docs/release-notes/; deleting or
moving files under docs/ from a shell.
"""
import fnmatch
import json
import os
import re
import sys

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

BLOCK = [
    "docs/mintlify.schema.json",
    "docs/archive/*",
    "docs/styleguides/*",
    ".claude/skills/release-notes/*",
    ".claude/agents/rn-drafter.md",
    "site/*", "_local_preview/*", "_deploy/*", "out/*", ".next/*",
    "node_modules/*", "*/node_modules/*", "docs/admin-guide/*",
]
ASK = ["docs/release-notes/*"]
SHELL_MUTATE = re.compile(r"\b(rm|mv|git\s+rm|git\s+mv|Remove-Item|Move-Item|Rename-Item|del|ren)\b", re.I)


def rel(path):
    p = os.path.relpath(os.path.abspath(path), REPO).replace("\\", "/")
    return None if p.startswith("..") else p


def ask(reason):
    print(json.dumps({"hookSpecificOutput": {
        "hookEventName": "PreToolUse",
        "permissionDecision": "ask",
        "permissionDecisionReason": reason}}))
    return 0


def block(reason):
    sys.stderr.write(reason + "\n")
    return 2


def check_docs_json(path, tool, ti):
    if tool == "Write":
        new = ti.get("content", "")
    else:
        try:
            new = open(path, encoding="utf-8").read()
        except OSError:
            return 0
        edits = ti.get("edits") or [ti]
        for e in edits:
            old = e.get("old_string", "")
            if old not in new:
                return 0  # Edit itself will fail
            new = new.replace(old, e.get("new_string", ""), -1 if e.get("replace_all") else 1)
    try:
        json.loads(new)
    except ValueError as err:
        return block(f"docs.json would be invalid JSON ({err}). Fix the edit or use nav.py.")
    return 0


def main():
    try:
        data = json.load(sys.stdin)
    except ValueError:
        return 0
    tool = data.get("tool_name", "")
    ti = data.get("tool_input") or {}
    if tool in ("Bash", "PowerShell"):
        cmd = ti.get("command", "")
        if SHELL_MUTATE.search(cmd) and re.search(r"docs[/\\]", cmd):
            return ask("Deletes/moves files under docs/. Renamed pages need nav.py rename (redirect).")
        return 0
    path = ti.get("file_path") or ""
    r = rel(path) if path else None
    if not r:
        return 0
    for pat in BLOCK:
        if fnmatch.fnmatch(r, pat):
            return block(f"Protected path: {r} (see .claude/hooks/protect.py).")
    if r == "docs/docs.json":
        return check_docs_json(path, tool, ti)
    for pat in ASK:
        if fnmatch.fnmatch(r, pat):
            return ask(f"{r} is owned by the release-notes workflow. Approve this edit?")
    return 0


if __name__ == "__main__":
    sys.exit(main())
