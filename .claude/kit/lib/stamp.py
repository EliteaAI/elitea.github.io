"""Page accuracy stamp: read and build. Writing is done by the main session with Edit (after approval).

Format (one frontmatter line, hidden MDX comment):
accuracy: {/*PAGE ACCURACY CONFIRMED for 2.0.8 | rewritten 2026-11-13 | EliteaUI release/2.0.8@abc1234 | elitea-sdk release/2.0.8@def5678 | elitea_core release/2.0.8@0123abc*/}
"""
import re
from datetime import date

import config as C

LINE = re.compile(r"^accuracy:\s*\{/\*(.*?)\*/\}\s*$", re.M)
WORKFLOWS = {"n": "created", "new": "created", "f": "rewritten", "rework": "rewritten",
             "u": "updated", "update": "updated"}
REPOS = ("EliteaUI", "elitea-sdk", "elitea_core")


def frontmatter(text):
    m = re.match(r"\A---\n(.*?)\n---", text, re.S)
    return (m.start(1), m.end(1), m.group(1)) if m else None


def read(text):
    """Return dict: present, version, workflow, date, repos {name: (branch, sha)}, legacy (verified: block)."""
    fm = frontmatter(text)
    out = {"present": False, "version": None, "workflow": None, "date": None, "repos": {},
           "legacy_verified": bool(fm and re.search(r"^verified:", fm[2], re.M))}
    if not fm:
        return out
    m = LINE.search(fm[2])
    if not m:
        return out
    out["present"] = True
    parts = [p.strip() for p in m.group(1).split("|")]
    v = re.search(r"CONFIRMED for (\S+)", parts[0])
    out["version"] = v.group(1) if v else None
    for p in parts[1:]:
        w = re.match(r"(created|rewritten|updated)\s+(\d{4}-\d{2}-\d{2})$", p)
        r = re.match(r"(\S+)\s+(\S+)@([0-9a-f]{7,40})$", p)
        if w:
            out["workflow"], out["date"] = w.groups()
        elif r and r.group(1) in REPOS:
            out["repos"][r.group(1)] = (r.group(2), r.group(3))
    return out


def baseline(info):
    if not info["present"]:
        return "no stamp: unknown baseline"
    if len(info["repos"]) < len(REPOS):
        return "stamp without code SHAs: unknown baseline"
    return "baseline: " + ", ".join(f"{k} {b}@{s}" for k, (b, s) in info["repos"].items())


def build(version, workflow, branch=None, when=None):
    cfg = C.load()
    branch = branch or cfg.get("code_branch")
    if not branch:
        raise ValueError("no code branch saved")
    wf = WORKFLOWS.get(workflow)
    if not wf:
        raise ValueError(f"workflow must be one of {sorted(set(WORKFLOWS))}")
    parts = [f"PAGE ACCURACY CONFIRMED for {version}", f"{wf} {when or date.today().isoformat()}"]
    for name in REPOS:
        sha = C.git(C.repo_path(cfg, name), "rev-parse", "--short=7", f"origin/{branch}")
        if not sha:
            raise ValueError(f"origin/{branch} not found in {name}")
        parts.append(f"{name} {branch}@{sha}")
    return "accuracy: {/*" + " | ".join(parts) + "*/}"


def plan(text, new_line):
    """Return (old_line or None, where) for the main session to apply with Edit."""
    fm = frontmatter(text)
    if not fm:
        return None, "no frontmatter: add the line inside a new --- block (ask the user)"
    m = LINE.search(fm[2])
    if m:
        return m.group(0), "replace the existing accuracy line"
    return None, "add after the last frontmatter line (before the closing ---)"
