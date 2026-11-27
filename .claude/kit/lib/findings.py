"""Numbered findings kept in the temp cache, so "fix 1, 2, 5" and "which are open?" work.

One list per page (key = docs-relative path or a free label). Numbers never change.
States: open, approved, done, ok (checked, no change needed), rejected (the user said no).
"""
import json
from datetime import datetime

import config as C

STATES = ("open", "approved", "done", "ok", "rejected")


def _file(key):
    safe = key.replace("/", "__").replace("\\", "__").replace(":", "_")
    return C.cache("findings", safe + ".json")


def load(key):
    f = _file(key)
    return json.loads(f.read_text(encoding="utf-8")) if f.exists() else {"key": key, "items": []}


def save(data):
    _file(data["key"]).write_text(json.dumps(data, indent=1, ensure_ascii=False), encoding="utf-8")


def add(key, items):
    """items: list of dicts with line, finding, evidence, change, severity. Returns new numbers."""
    data = load(key)
    n = max((i["n"] for i in data["items"]), default=0)
    nums = []
    for it in items:
        n += 1
        data["items"].append({"n": n, "state": "open", "added": datetime.now().isoformat(timespec="minutes"), **it})
        nums.append(n)
    save(data)
    return nums


def set_state(key, nums, state):
    data = load(key)
    hit = [i for i in data["items"] if i["n"] in nums]
    for i in hit:
        i["state"] = state
    save(data)
    return [i["n"] for i in hit], sorted(set(nums) - {i["n"] for i in hit})


def table(key, states=None):
    data = load(key)
    rows = [i for i in data["items"] if not states or i["state"] in states]
    if not rows:
        return f"{key}: no findings" + (f" in state {', '.join(states)}" if states else "")
    out = [f"{key}", "| # | state | line | finding | evidence | was → is | severity |", "|---|---|---|---|---|---|---|"]
    for i in rows:
        out.append(f"| {i['n']} | {i['state']} | {i.get('line', '')} | {i.get('finding', '')} | {i.get('evidence', '')} "
                   f"| {i.get('change', '')} | {i.get('severity', '')} |")
    return "\n".join(out)


def lists():
    d = C.cache("findings", "x").parent
    return sorted(json.loads(f.read_text(encoding="utf-8"))["key"] for f in d.glob("*.json"))
