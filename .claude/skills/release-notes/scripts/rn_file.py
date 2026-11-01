#!/usr/bin/env python3
"""Deterministic edits to the current release-notes file and docs.json navigation.

Usage:
  rn_file.py current                                   # print version and path of the latest release
  rn_file.py init 2.0.9 [--date "December 06, 2026"]   # archive latest, create new file, update docs.json
  rn_file.py set {intro|new|changed|fixed|known} DRAFT [--append]
        new/changed: DRAFT holds "### ..." feature blocks (replaced, or appended with --append)
        fixed/known: DRAFT holds "* [#id](...) text" lines; merged with --append, deduped by id,
                     always sorted by id descending
        intro:       DRAFT holds the intro paragraph
  rn_file.py order {new|changed} "Heading A" "Heading B" ...   # reorder feature blocks (others keep order, go last)
  rn_file.py status                                    # sections, counts, TODOs, missing images
"""
import argparse
import datetime as dt
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
DOCS = ROOT / "docs"
RN = DOCS / "release-notes"
NAV = DOCS / "docs.json"
SECTIONS = {"new": "New Features", "changed": "Changed Features", "fixed": "Fixed Issues", "known": "Known Issues"}
ISSUE_URL = "https://github.com/EliteaAI/elitea_issues/issues/"

TEMPLATE = """---
title: "Release Notes - {v}"
---

{{/* TODO: intro — run /release-notes intro after the sections are filled */}}

* **Release version**: {v}
* **Released on**: {date}
* **Access**: [ELITEA Platform](https://next.elitea.ai)

## New Features

## Changed Features

## Fixed Issues

## Known Issues
"""


def nav_text():
    return NAV.read_text()


def group_pages(text, group):
    m = re.search(r'"group":\s*"%s"[^\[]*?"pages":\s*\[(.*?)\]' % re.escape(group), text, re.S)
    if not m:
        sys.exit(f"docs.json: group '{group}' not found")
    return m, re.findall(r'"([^"]+)"', m.group(1))


def current():
    _, pages = group_pages(nav_text(), "Latest Release")
    page = pages[0]
    v = re.sub(r"^.*rn-", "", page).replace("-", ".")
    return v, DOCS / (page + ".mdx")


def deepen_links(text):
    # a file moved one folder down: ../x -> ../../x (only for links that were one level up)
    return re.sub(r'(?<=["(])\.\./(?!\.\./)', "../../", text)


def init(v, date):
    old_v, old_path = current()
    slug = "rn-" + v.replace(".", "-")
    new_path = RN / f"{slug}.mdx"
    if new_path.exists():
        sys.exit(f"{new_path} already exists")
    if old_v == v:
        sys.exit(f"{v} is already the latest release")
    archived = RN / "archived" / old_path.name
    archived.write_text(deepen_links(old_path.read_text()))
    old_path.unlink()
    new_path.write_text(TEMPLATE.format(v=v, date=date))

    text = nav_text()
    latest_m, _ = group_pages(text, "Latest Release")
    text = text[:latest_m.start(1)] + f'"release-notes/{slug}"' + text[latest_m.end(1):]
    recent_m, recent = group_pages(text, "Recent Releases")
    old_page = f"release-notes/archived/{old_path.stem}"
    moved = recent[1:]  # keep two recent releases; the rest go to Older Releases
    new_recent = [old_page] + recent[:1]
    text = text[:recent_m.start(1)] + ", ".join(f'"{p}"' for p in new_recent) + text[recent_m.end(1):]
    if moved:
        older_m, older = group_pages(text, "Older Releases")
        indent = re.search(r'\n(\s*)"', older_m.group(1))
        ind = indent.group(1) if indent else "              "
        body = older_m.group(1)
        first = re.search(r'\s*"', body)
        insert = "".join(f'\n{ind}"{p}",' for p in moved)
        body = insert + body[first.start():] if first else insert.rstrip(",")
        text = text[:older_m.start(1)] + body + text[older_m.end(1):]
    json.loads(text)  # fail loudly on broken JSON
    NAV.write_text(text)
    print(f"archived {old_v} -> {archived.relative_to(ROOT)} (links deepened)")
    print(f"created  {new_path.relative_to(ROOT)}")
    print(f"docs.json: latest={slug}; recent={new_recent}; moved to older={moved}")


def split(text, title):
    m = re.search(rf"^## {re.escape(title)}[ \t]*\n", text, re.M)
    if not m:
        sys.exit(f"section '## {title}' not found")
    nxt = re.search(r"^## ", text[m.end():], re.M)
    end = m.end() + nxt.start() if nxt else len(text)
    return text[:m.end()], text[m.end():end], text[end:]


def blocks(body):
    parts = re.split(r"(?=^### )", body.strip(), flags=re.M)
    return [p.strip() for p in parts if p.strip().startswith("### ")]


def issue_lines(body):
    out = {}
    for line in body.splitlines():
        m = re.match(r"\*\s*\[#(\d+)\]", line.strip())
        if m:
            out[int(m.group(1))] = line.strip()
        elif re.match(r"\*?\s*#?(\d+)\s+\S", line.strip()):  # tolerate "#123 text" / "123 text"
            n, t = re.match(r"\*?\s*#?(\d+)\s+(.*)", line.strip()).groups()
            out[int(n)] = f"* [#{n}]({ISSUE_URL}{n}) {t}"
    return out


def set_section(sec, draft, append):
    path = current()[1]
    text = path.read_text()
    new = Path(draft).read_text().strip()
    if sec == "intro":
        m = re.search(r"^---\n.*?\n---\n(.*?)(?=^\* \*\*Release version)", text, re.S | re.M)
        if not m:
            sys.exit("intro position not found")
        text = text[:m.start(1)] + "\n" + new + "\n\n" + text[m.end(1):]
        path.write_text(text)
        print("intro updated")
        return
    head, body, tail = split(text, SECTIONS[sec])
    if sec in ("fixed", "known"):
        lines = issue_lines(body) if append else {}
        lines.update(issue_lines(new))
        body = "\n".join(lines[k] for k in sorted(lines, reverse=True))
        count = len(lines)
    else:
        bl = (blocks(body) if append else []) + blocks(new)
        body = "\n\n".join(bl)
        count = len(bl)
    path.write_text(head + "\n" + body + "\n\n" + tail.lstrip("\n"))
    print(f"{SECTIONS[sec]}: {count} item(s) ({'appended' if append else 'replaced'})")


def order(sec, headings):
    path = current()[1]
    head, body, tail = split(path.read_text(), SECTIONS[sec])
    bl = blocks(body)
    name = lambda b: b.splitlines()[0][4:].strip()
    rank = {h: i for i, h in enumerate(headings)}
    unknown = [h for h in headings if h not in {name(b) for b in bl}]
    bl.sort(key=lambda b: rank.get(name(b), len(rank)))
    path.write_text(head + "\n" + "\n\n".join(bl) + "\n\n" + tail.lstrip("\n"))
    print("order: " + " > ".join(name(b) for b in bl))
    if unknown:
        print("not found: " + ", ".join(unknown))


def status():
    v, path = current()
    text = path.read_text()
    print(f"{v}  {path.relative_to(ROOT)}")
    date = re.search(r"\*\*Released on\*\*:\s*(.*)", text)
    print(f"released on: {date.group(1) if date else '?'}")
    for key, title in SECTIONS.items():
        _, body, _ = split(text, title)
        items = [b.splitlines()[0][4:] for b in blocks(body)] if key in ("new", "changed") else list(issue_lines(body))
        print(f"{title}: {len(items)}" + (f" — {'; '.join(map(str, items))}" if key in ("new", "changed") else ""))
    todos = re.findall(r"\{/\*\s*TODO:([^*]*)\*/\}", text)
    if todos:
        print(f"TODOs ({len(todos)}): " + "; ".join(t.strip() for t in todos))
    missing = [i for i in re.findall(r'(?:src="|\]\()\.\./(img/[^")]+)', text) if not (DOCS / i).exists()]
    if missing:
        print("images to create: " + ", ".join(missing))


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("current")
    p = sub.add_parser("init")
    p.add_argument("version")
    p.add_argument("--date", default=None)
    p = sub.add_parser("set")
    p.add_argument("section", choices=["intro", *SECTIONS])
    p.add_argument("draft")
    p.add_argument("--append", action="store_true")
    p = sub.add_parser("order")
    p.add_argument("section", choices=["new", "changed"])
    p.add_argument("headings", nargs="+")
    sub.add_parser("status")
    a = ap.parse_args()
    if a.cmd == "current":
        v, path = current()
        print(v, path)
    elif a.cmd == "init":
        init(a.version, a.date or "{/* TODO: release date, e.g. %s */}" % dt.date.today().strftime("%B %d, %Y"))
    elif a.cmd == "set":
        set_section(a.section, a.draft, a.append)
    elif a.cmd == "order":
        order(a.section, a.headings)
    else:
        status()


if __name__ == "__main__":
    sys.exit(main())
