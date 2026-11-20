"""docs/docs.json navigation (read-only). Proposes exact text edits; the main session applies them with Edit.

Pages are extensionless paths from docs/, e.g. how-tos/modules/web-search.
"""
import json
import re

import mdx as M

CFG = M.DOCS / "docs.json"
UNLISTED_OK = ("archive/", "styleguides/", "release-notes/archived/")


def load():
    return CFG.read_text(encoding="utf-8")


def walk(node, trail, out):
    if isinstance(node, dict):
        label = node.get("tab") or node.get("group") or node.get("anchor")
        t = trail + [label] if label else trail
        if node.get("group") and "pages" in node:
            out.append((t, node["pages"]))
        for k in ("tabs", "groups", "pages", "anchors"):
            for v in node.get(k, []) or []:
                walk(v, t, out)


def groups():
    out = []
    walk(json.loads(load())["navigation"], [], out)
    return out


def find(text):
    text = text.lower()
    rows = []
    for trail, pages in groups():
        g = " > ".join(trail)
        if text in g.lower():
            rows.append(("group", g, len([p for p in pages if isinstance(p, str)])))
        for p in pages:
            if isinstance(p, str) and text in p.lower():
                rows.append(("page", g, p))
    return rows


def check():
    data = json.loads(load())
    out, listed = [], set()
    walk(data["navigation"], [], out)
    problems = []
    for trail, pages in out:
        for p in pages:
            if isinstance(p, str):
                listed.add(p)
                if not (M.DOCS / f"{p}.mdx").exists():
                    problems.append(f"in nav but no file: {p} ({' > '.join(trail)})")
    for f in M.pages():
        rel = M.docs_rel(f)[:-4]
        if rel not in listed and not rel.startswith(UNLISTED_OK) and rel != "index":
            problems.append(f"page not in nav: {rel}")
    return problems


def plan_add(page, group, after=None):
    """Return (old_text, new_text) for one Edit, or raise ValueError."""
    raw = load()
    hits = [(t, ps) for t, ps in groups() if t and (t[-1] == group or " > ".join(t) == group)]
    if len(hits) != 1:
        raise ValueError(f"group '{group}' matches {len(hits)} groups; use the full path from `toc find`")
    trail, pages = hits[0]
    strs = [p for p in pages if isinstance(p, str)]
    if page in strs:
        raise ValueError(f"{page} is already in '{' > '.join(trail)}'")
    if not after:
        raise ValueError(f"say where: --after <page>, one of: {', '.join(strs) or 'none (group has only subgroups)'}")
    anchor = after
    if anchor not in strs:
        raise ValueError(f"{anchor} is not a page of this group; one of: {', '.join(strs)}")
    m = list(re.finditer(rf'^([ \t]*)"{re.escape(anchor)}"(,?)[ \t]*$', raw, re.M))
    if len(m) != 1:
        raise ValueError(f'"{anchor}" appears {len(m)} times in docs.json; place it by hand')
    ind, comma = m[0].group(1), m[0].group(2)
    old = m[0].group(0)
    new = f'{ind}"{anchor}",\n{ind}"{page}"{comma}'
    return old, new, " > ".join(trail)


def plan_rename(old_page, new_page):
    raw = load()
    m = list(re.finditer(rf'"{re.escape(old_page)}"', raw))
    nav = [x for x in m]
    return {"nav_occurrences": len(nav), "old": f'"{old_page}"', "new": f'"{new_page}"',
            "redirect": {"source": f"/{old_page}", "destination": f"/{new_page}"}}
