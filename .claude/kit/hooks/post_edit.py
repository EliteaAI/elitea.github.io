"""PostToolUse: lint only the lines just changed in a docs .mdx page.

Silent when clean. Otherwise at most 3 short lines to Claude (never blocks, never edits).
Changed lines come from the tool result (structuredPatch), else from the original
file + old_string, else (approximate) from every occurrence of new_string.
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "lib"))
import checks  # noqa: E402
import config as C  # noqa: E402
import mdx as M  # noqa: E402

MAX = 3
# Lower number = shown first when the 3-line cap applies.
PRIORITY = {"link": 0, "video-as-img": 1, "alt-missing": 1, "md-image": 1, "video-alt": 1, "gif-new": 1,
            "h4": 2, "heading-link": 2, "see-also-form": 2, "see-also-label": 2, "see-also-bullet": 2,
            "see-also-explain": 2, "callout-type": 2, "callout-after-callout": 2, "blockquote": 2}


def from_patch(patch):
    """Exact new-file line numbers touched by structuredPatch hunks."""
    lines = set()
    for h in patch or []:
        cur = h.get("newStart", 1)
        for l in h.get("lines", []):
            if l.startswith("+"):
                lines.add(cur)
                cur += 1
            elif l.startswith("-"):
                lines.add(cur)  # a deletion: check the line that now sits there
            else:
                cur += 1
    return lines


def changed_lines(text, ti, tr, tool):
    """Return (lines or None for whole file, method)."""
    tr = tr if isinstance(tr, dict) else {}
    if tr.get("structuredPatch"):
        return from_patch(tr["structuredPatch"]), "patch"
    if tool == "Write":
        return None, "whole file"
    orig, old, new = tr.get("originalFile"), ti.get("old_string", ""), ti.get("new_string", "")
    if tool == "Edit" and orig and old and not ti.get("replace_all") and orig.count(old) == 1:
        start = M.line_of(orig, orig.find(old))
        return set(range(start, start + new.count("\n") + 1)), "original file"
    news = [e.get("new_string", "") for e in ti.get("edits", [])] if tool == "MultiEdit" else [new]
    lines = set()
    for n in filter(None, news):
        pos = text.find(n)
        while pos != -1:  # every occurrence: may over-report, never misses
            s = M.line_of(text, pos)
            lines.update(range(s, s + n.count("\n") + 1))
            pos = text.find(n, pos + 1)
    return lines, "approximate"


def main():
    try:
        data = json.load(sys.stdin)
    except ValueError:
        return
    tool = data.get("tool_name", "")
    ti = data.get("tool_input", {}) or {}
    tr = data.get("tool_response", {})
    path = Path(ti.get("file_path", ""))
    if tool not in ("Write", "Edit", "MultiEdit") or path.suffix.lower() != ".mdx":
        return
    as_page = data.get("_test_as_page")  # dry-run only: treat a temp file as this docs page
    rel = as_page or M.docs_rel(path)
    if rel == str(path) or rel.startswith(("styleguides/", "archive/")) or not path.exists():
        return
    text = M.read(path)
    if as_page:
        path = M.DOCS / as_page
    try:  # keys only, to confirm the tool_response shape once the hook is live
        C.cache("post_edit_last.json").write_text(json.dumps(
            {"tool": tool, "response_keys": sorted(tr) if isinstance(tr, dict) else str(type(tr))}), encoding="utf-8")
    except OSError:
        pass
    lines, method = changed_lines(text, ti, tr, tool)
    if lines is not None and not lines:
        return
    rows = checks.lint(text, lines, rel)
    rows += [(ln, "link", f"{tgt} -> {prob}", "") for ln, _, tgt, prob, _ in checks.check_links(text, path)
             if (lines is None or ln in lines) and not (as_page and prob.startswith("anchor not found on this page"))]
    if not rows:
        return
    rows.sort(key=lambda r: (PRIORITY.get(r[1], 3), r[0]))
    msg = [f"{ln}: {rid} {m}" for ln, rid, m, _ in rows[:MAX]]
    more = f" (+{len(rows) - MAX} more: df.py lint/links {rel})" if len(rows) > MAX else ""
    note = " [lines approximate]" if method == "approximate" else ""
    print(json.dumps({"hookSpecificOutput": {"hookEventName": "PostToolUse",
                      "additionalContext": f"lint {rel}{note}: " + "; ".join(msg) + more}}))


if __name__ == "__main__":
    main()
