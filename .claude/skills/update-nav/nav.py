#!/usr/bin/env python
"""Edit docs/docs.json nav without re-serializing (keeps hand formatting and CRLF).

  nav.py find <text>                       list groups (path) and pages matching text
  nav.py groups [<text>]                   list group paths (Tab > Group > Subgroup)
  nav.py add <page> --group "<group path or unique group name>" [--after <page>|--sorted]
  nav.py rename <old-page> <new-page>      update nav entry + add redirect /old -> /new
  nav.py check                             JSON valid; every nav page exists; live pages missing from nav

Pages are extensionless paths from docs/, e.g. integrations/toolkits/tavily_toolkit.
"""
import json
import os
import re
import sys

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
DOCS = os.path.join(REPO, "docs")
CFG = os.path.join(DOCS, "docs.json")
UNLISTED_OK = ("archive/", "styleguides/", "release-notes/archived/")


def load():
    raw = open(CFG, encoding="utf-8", newline="").read()
    return raw, json.loads(raw)


def save(raw):
    json.loads(raw)  # never write invalid JSON
    open(CFG, "w", encoding="utf-8", newline="").write(raw)


def walk(node, trail, out):
    """Yield (group_trail, pages_list) for every group."""
    if isinstance(node, dict):
        label = node.get("tab") or node.get("group") or node.get("anchor")
        t = trail + [label] if label else trail
        if "pages" in node and node.get("group"):
            out.append((t, node["pages"]))
        for k in ("tabs", "groups", "pages", "anchors"):
            for child in node.get(k, []) or []:
                walk(child, t, out)
    return out


def groups(data):
    return walk(data["navigation"], [], [])


def all_pages(data):
    res = []
    for _, pages in groups(data):
        res += [p for p in pages if isinstance(p, str)]
    return res


def pick_group(data, spec):
    gs = groups(data)
    exact = [g for g in gs if " > ".join(g[0]) == spec]
    cand = exact or [g for g in gs if g[0][-1] == spec] or [g for g in gs if spec.lower() in " > ".join(g[0]).lower()]
    if len(cand) != 1:
        names = "\n  ".join(" > ".join(g[0]) for g in cand) or "(none)"
        sys.exit(f"Group '{spec}' matched {len(cand)} groups:\n  {names}")
    return cand[0]


def page_exists(p):
    return os.path.isfile(os.path.join(DOCS, p + ".mdx")) or os.path.isfile(os.path.join(DOCS, p + ".md"))


def cmd_add(page, spec, after=None, sort=False):
    raw, data = load()
    if page in all_pages(data):
        sys.exit(f"Already in nav: {page}")
    if not page_exists(page):
        print(f"warning: docs/{page}.mdx does not exist yet")
    trail, pages = pick_group(data, spec)
    strs = [p for p in pages if isinstance(p, str)]
    if not strs:
        sys.exit("Target group has no string pages to anchor on; edit manually.")
    if after:
        if after not in strs:
            sys.exit(f"--after page not in group: {after}")
        anchor, before = after, False
    elif sort:
        later = [p for p in strs if p.lower() > page.lower()]
        anchor, before = (later[0], True) if later else (strs[-1], False)
    else:
        anchor, before = strs[-1], False
    tok = json.dumps(anchor)
    hits = [m.start() for m in re.finditer(re.escape(tok), raw)]
    if len(hits) != 1:
        sys.exit(f"Anchor {anchor} appears {len(hits)} times in docs.json; edit manually.")
    i = hits[0]
    line_start = raw.rfind("\n", 0, i) + 1
    indent = raw[line_start:i]
    nl = "\r\n" if "\r\n" in raw else "\n"
    new = json.dumps(page)
    if indent.strip() == "":  # multi-line array
        if before:
            raw = raw[:i] + new + "," + nl + indent + raw[i:]
        else:
            end = i + len(tok)
            raw = raw[:end] + "," + nl + indent + new + raw[end:]
    else:  # inline array
        if before:
            raw = raw[:i] + new + ", " + raw[i:]
        else:
            end = i + len(tok)
            raw = raw[:end] + ", " + new + raw[end:]
    save(raw)
    print(f"Added {page} to {' > '.join(trail)}")


def cmd_rename(old, new):
    raw, data = load()
    tok = json.dumps(old)
    n = raw.count(tok)
    if n != 1:
        sys.exit(f"{old} appears {n} times in docs.json; edit manually.")
    raw = raw.replace(tok, json.dumps(new))
    m = re.search(r'("redirects"\s*:\s*\[)', raw)
    nl = "\r\n" if "\r\n" in raw else "\n"
    entry = '{ "source": %s, "destination": %s }' % (json.dumps("/" + old), json.dumps("/" + new))
    if m:
        raw = raw[:m.end()] + nl + "    " + entry + "," + raw[m.end():]
    else:
        sys.exit("No redirects array found; add the redirect manually.")
    save(raw)
    print(f"Renamed {old} -> {new}; redirect added. Move the file and fix inbound links (fix-links skill).")


def cmd_find(text):
    _, data = load()
    t = text.lower()
    for trail, pages in groups(data):
        path = " > ".join(trail)
        hits = [p for p in pages if isinstance(p, str) and t in p.lower()]
        if t in path.lower() or hits:
            print(path + (": " + ", ".join(hits) if hits else ""))


def cmd_groups(text=""):
    _, data = load()
    for trail, pages in groups(data):
        path = " > ".join(trail)
        if text.lower() in path.lower():
            print(f"{path}  ({len(pages)})")


def cmd_check():
    raw, data = load()
    nav = all_pages(data)
    bad = 0
    dup = {p for p in nav if nav.count(p) > 1}
    for p in sorted(dup):
        print(f"duplicate in nav: {p}"); bad += 1
    for p in nav:
        if not page_exists(p):
            print(f"nav page missing file: {p}"); bad += 1
    navset = set(nav)
    for root, dirs, files in os.walk(DOCS):
        dirs[:] = [d for d in dirs if d not in ("img", "node_modules")]
        for f in files:
            if f.endswith(".mdx"):
                rel = os.path.relpath(os.path.join(root, f[:-4]), DOCS).replace("\\", "/")
                if rel not in navset and not rel.startswith(UNLISTED_OK):
                    print(f"not in nav: {rel}"); bad += 1
    print(f"docs.json valid JSON; {len(nav)} nav pages; {bad} issue(s)")
    return 1 if bad else 0


def main(a):
    if not a:
        sys.exit(__doc__)
    c = a[0]
    if c == "find" and len(a) > 1:
        return cmd_find(a[1])
    if c == "groups":
        return cmd_groups(a[1] if len(a) > 1 else "")
    if c == "add" and len(a) > 1 and "--group" in a:
        g = a[a.index("--group") + 1]
        after = a[a.index("--after") + 1] if "--after" in a else None
        return cmd_add(a[1], g, after, "--sorted" in a)
    if c == "rename" and len(a) == 3:
        return cmd_rename(a[1], a[2])
    if c == "check":
        return cmd_check()
    sys.exit(__doc__)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]) or 0)
