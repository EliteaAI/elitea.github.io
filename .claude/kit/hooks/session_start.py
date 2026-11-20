"""SessionStart: one short line. Saved code branch, lock state, missing repos.

The user checks and pulls all branches herself; this hook never asks about them.
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "lib"))
import config as C  # noqa: E402

cfg = C.load()
parts = [f"code branch {cfg.get('code_branch') or 'not set (user sets it: df.py cfg branch <name>)'}"]
missing = [n for n in cfg["repos"] if not (C.repo_path(cfg, n) / ".git").exists()]
if missing:
    parts.append("repo not found: " + ", ".join(missing))
if cfg.get("setup_lock"):
    parts.append("lock ON: docs/ read-only")
line = "doc-factory: " + "; ".join(parts)
# systemMessage is shown to the user; additionalContext goes to Claude.
print(json.dumps({
    "systemMessage": line,
    "hookSpecificOutput": {"hookEventName": "SessionStart", "additionalContext": line},
}))
