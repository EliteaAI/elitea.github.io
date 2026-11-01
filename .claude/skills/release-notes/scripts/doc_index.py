#!/usr/bin/env python3
"""Search the docs for pages, heading anchors and images to use in release notes.

The index (pages, headings with Mintlify anchors, accuracy markers, images) is cached in
/tmp/rn/docs-index.json and rebuilt only when an .mdx file changes.

Usage:
  doc_index.py links  "web search" "tavily"        # best pages/anchors per query
  doc_index.py images "web search" "schedules"     # existing images per query
  doc_index.py check  ../menus/settings/general#web-search ...   # verify links resolve
All link paths are printed relative to docs/release-notes/ (e.g. ../menus/settings/general#web-search).
"""
import json
import os
import re
import sys
from pathlib import Path

DOCS = Path(__file__).resolve().parents[4] / "docs"
CACHE = Path("/tmp/rn/docs-index.json")
SKIP = ("release-notes/", "admin-guide/", "_local_preview/", "archive/")
STOP = set("a an and the of to in for with on by from is are be how use using your new".split())


def slug(heading: str) -> str:
    h = re.sub(r"<[^>]*>", " ", heading)  # <Icon .../> and other inline components
    h = re.sub(r"\{[^}]*\}", " ", h)
    h = re.sub(r"[*_`]", "", h).strip().lower()
    h = h.replace("&", "%26")
    h = re.sub(r"[^a-z0-9%\s-]", "", h)
    return re.sub(r"\s", "-", h)


def build():
    pages = []
    for p in sorted(DOCS.rglob("*.mdx")):
        rel = p.relative_to(DOCS).as_posix()
        if rel.startswith(SKIP):
            continue
        text = p.read_text(errors="ignore")
        title = re.search(r'^title:\s*"?([^"\n]*)', text, re.M)
        acc = re.search(r"PAGE ACCURACY CONFIRMED for ([\d.]+)", text)
        heads, seen, in_code = [], {}, False
        for line in text.splitlines():
            if line.lstrip().startswith("```"):
                in_code = not in_code
            m = None if in_code else re.match(r"(#{2,4})\s+(.*)", line)
            if m:
                s = slug(m.group(2))
                n = seen.get(s, 0)
                seen[s] = n + 1
                heads.append([len(m.group(1)), re.sub(r"<[^>]*>", "", m.group(2)).strip(), s if n == 0 else f"{s}-{n}"])
        imgs = sorted(set(re.findall(r'(?:src="|\]\()((?:\.\./)+img/[^")\s]+)', text)))
        imgs = [re.sub(r"^(\.\./)+", "", i) for i in imgs]
        pages.append({"path": rel[:-4], "title": title.group(1).strip() if title else "",
                      "accuracy": acc.group(1) if acc else "", "headings": heads, "images": imgs})
    files = sorted(p.relative_to(DOCS).as_posix() for p in (DOCS / "img").rglob("*")
                   if p.suffix.lower() in (".png", ".jpg", ".jpeg", ".gif", ".webp", ".mp4")
                   and not {"release-notes", "archive"} & set(p.parts))
    return {"pages": pages, "image_files": files}


def index():
    stamp = max(os.path.getmtime(p) for p in DOCS.rglob("*.mdx"))
    if CACHE.exists():
        data = json.loads(CACHE.read_text())
        if data.get("stamp") == stamp:
            return data
    data = build()
    data["stamp"] = stamp
    CACHE.parent.mkdir(parents=True, exist_ok=True)
    CACHE.write_text(json.dumps(data))
    return data


def words(q):
    return [w for w in re.findall(r"[a-z0-9]+", q.lower()) if w not in STOP]


def score(text, ws):
    t = text.lower()
    return sum(1 for w in ws if w in t) / max(len(ws), 1)


def links(data, q, top=5):
    ws = words(q)
    hits = []
    for p in data["pages"]:
        ps = score(p["path"] + " " + p["title"], ws)
        if ps:
            hits.append((ps * 2.5 + 0.1, p, None))
        for lvl, h, a in p["headings"]:
            hs = score(h, ws)
            if hs >= 0.5:
                hits.append((hs * 3 + ps * 0.5 + (0.2 if lvl == 2 else 0) + (0.1 if p["accuracy"] else 0), p, (h, a)))
    hits.sort(key=lambda x: -x[0])
    out, seen = [], set()
    for s, p, h in hits:
        key = (p["path"], h[1] if h else "")
        if key in seen:
            continue
        seen.add(key)
        acc = f" [accuracy {p['accuracy']}]" if p["accuracy"] else ""
        if h:
            out.append(f"  [{h[0]}](../{p['path']}#{h[1]})  — {p['title']}{acc}")
        else:
            out.append(f"  [{p['title']}](../{p['path']}){acc}")
        if len(out) >= top:
            break
    return out


def images(data, q, top=5):
    ws = words(q)
    scored = []
    for f in data["image_files"]:
        name = re.sub(r"[_\-./]", " ", f)
        s = score(name, ws)
        if s >= 0.5:
            scored.append((s, f))
    for p in data["pages"]:
        if score(p["path"] + " " + p["title"], ws) >= 0.5:
            scored += [(0.4, i) for i in p["images"][:3]]
    scored.sort(key=lambda x: -x[0])
    out, seen = [], set()
    for s, f in scored:
        if f not in seen and (DOCS / f).exists():
            seen.add(f)
            out.append(f"  ../{f}")
        if len(out) >= top:
            break
    return out


def check(data, targets):
    pages = {p["path"]: {h[2] for h in p["headings"]} for p in data["pages"]}
    for t in targets:
        path, _, anchor = re.sub(r"^(\.\./)+", "", t).partition("#")
        if path not in pages:
            print(f"MISSING PAGE  {t}")
        elif anchor and anchor not in pages[path]:
            print(f"MISSING ANCHOR {t}")
        else:
            print(f"ok            {t}")


def main():
    if len(sys.argv) < 3:
        print(__doc__)
        return 1
    cmd, args = sys.argv[1], sys.argv[2:]
    data = index()
    if cmd == "check":
        return check(data, args)
    for q in args:
        res = links(data, q) if cmd == "links" else images(data, q)
        print(f"# {q}")
        print("\n".join(res) or "  (nothing found)")


if __name__ == "__main__":
    sys.exit(main())
