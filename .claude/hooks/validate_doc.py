#!/usr/bin/env python
"""Deterministic checks for ELITEA Mintlify pages.

Hook mode (no args, PostToolUse JSON on stdin): checks the edited .mdx file and
reports warnings to Claude via additionalContext. Never blocks.
CLI mode: validate_doc.py <file|dir> [...] [--links-only] [--as docs/<path>.mdx]  -> exit 1 if issues.
  --as: validate a draft stored elsewhere as if it lived at that docs path.

Scope: for an Edit, style/link checks cover only the inserted text; for a
Write or CLI run they cover the whole file. Front matter and naming are
checked on full-scope runs only.
"""
import json
import os
import re
import sys
from urllib.parse import unquote, urljoin

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DOCS = os.path.join(REPO, "docs")
SKIP_DIRS = ("archive", "styleguides")
MAX_LINES = 12

FENCE = re.compile(r"^\s*(```|~~~)")
MD_LINK = re.compile(r"(!?)\[([^\]]*)\]\(<?((?:[^()\s>]|\([^()\s]*\))+)>?(?:\s+\"[^\"]*\")?\)")
SRC_ATTR = re.compile(r"<(img|source|video)\b[^>]*?\bsrc=[\"']([^\"']+)[\"'][^>]*>", re.I)
HREF_ATTR = re.compile(r"<(?:Card|a)\b[^>]*?\bhref=[\"']([^\"']+)[\"']", re.I)
IMG_TAG = re.compile(r"<img\b[^>]*>", re.I)
STYLE = [
    (re.compile(r"\b\w+(?:n't|'ll|'re|'ve|'m)\b|\b(?:it|that|there|what|here)'s\b", re.I), "contraction"),
    (re.compile(r"\b(?:click|clicking|clicked)\b", re.I), "use 'select' not 'click'"),
    (re.compile(r"\bnavigate to\b", re.I), "use 'go to'"),
    (re.compile(r"\bplease note\b", re.I), "drop 'please note'"),
    (re.compile(r"\b(?:utilize|simply|easily)\b", re.I), "banned word"),
    (re.compile(r"–"), "en dash; use - or —"),
    (re.compile(r"\bpop-?up\b|\bmodal\b", re.I), "use 'dialog'"),
]
FM_KEYS = {"title", "description", "sidebarTitle", "accuracy", "icon", "verified", "tag", "hideFooterPagination"}

_index = None
_redirects = None


def redirects():
    global _redirects
    if _redirects is None:
        try:
            d = json.load(open(os.path.join(DOCS, "docs.json"), encoding="utf-8"))
            _redirects = {r["source"].rstrip("/") for r in d.get("redirects", [])}
        except (OSError, ValueError, KeyError):
            _redirects = set()
    return _redirects


def page_index():
    global _index
    if _index is None:
        _index = {}
        for root, dirs, files in os.walk(DOCS):
            dirs[:] = [d for d in dirs if d not in ("img", "node_modules")]
            for f in files:
                if f.endswith(".mdx"):
                    rel = os.path.relpath(os.path.join(root, f[:-4]), DOCS).replace("\\", "/")
                    _index.setdefault(os.path.basename(rel), []).append(rel)
    return _index


def resolve(page, target, is_asset):
    """Return None if target resolves, else a short problem string."""
    if re.match(r"^(https?:|mailto:|tel:|#|\{|data:)", target):
        return None
    path = unquote(target.split("#")[0].split("?")[0])
    if not path:
        return None
    # Browser/Mintlify semantics: resolve against the page URL; "../" stops at root.
    page_url = "/" + os.path.relpath(page, DOCS).replace("\\", "/")
    url = urljoin(page_url, path)
    full = os.path.normpath(os.path.join(DOCS, url.lstrip("/")))
    if is_asset:
        return None if os.path.isfile(full) else "missing file"
    if re.search(r"\.mdx?$", path):
        return "remove .md/.mdx extension"
    for cand in (full + ".mdx", full + ".md", os.path.join(full, "index.mdx"), full):
        if os.path.isfile(cand):
            return None
    if "/" + os.path.relpath(full, DOCS).replace("\\", "/") in redirects():
        return None
    hits = page_index().get(os.path.basename(path.rstrip("/")), [])
    if hits:
        sugg = os.path.relpath(os.path.join(DOCS, hits[0]), os.path.dirname(page)).replace("\\", "/")
        return "broken; try " + sugg
    return "broken"


def check_text(page, lines, offset, out):
    in_fence = False
    for i, line in enumerate(lines, offset):
        if FENCE.match(line):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        prose = re.sub(r"`[^`]*`", "", line)
        for bang, alt, tgt in MD_LINK.findall(prose):
            asset = bool(bang) or re.search(r"\.(png|jpe?g|gif|svg|mp4|webp)$", tgt, re.I)
            if bang and not alt.strip():
                out.append(f"L{i}: image missing alt text")
            prob = resolve(page, tgt, bool(asset))
            if prob:
                out.append(f"L{i}: {tgt} -> {prob}")
        for _tag, src in SRC_ATTR.findall(prose):
            prob = resolve(page, src, True)
            if prob:
                out.append(f"L{i}: {src} -> {prob}")
        for href in HREF_ATTR.findall(prose):
            prob = resolve(page, href, False)
            if prob:
                out.append(f"L{i}: {href} -> {prob}")
        for tag in IMG_TAG.findall(prose):
            if "alt=" not in tag:
                out.append(f"L{i}: <img> missing alt")
        if re.search(r"(?:\]\(|src=[\"'])(?:[A-Za-z]:\\|/Users/|file:)", prose):
            out.append(f"L{i}: absolute local path")
        for rx, msg in STYLE:
            m = rx.search(prose)
            if m:
                out.append(f"L{i}: '{m.group(0)}' {msg}")
        h = re.match(r"^(#{1,6})\s+(.*)", prose)
        if h:
            if len(h.group(1)) == 1:
                out.append(f"L{i}: H1 in body; title is the H1")
            if re.search(r"\]\(", h.group(2)):
                out.append(f"L{i}: link in heading")


def check_full(page, text, out):
    rel = os.path.relpath(page, DOCS).replace("\\", "/")
    name = os.path.basename(rel)[:-4]
    if rel.startswith("integrations/toolkits/"):
        if not re.fullmatch(r"[a-z0-9]+(?:_[a-zA-Z0-9]+)*_toolkit", name) and name != "index":
            out.append(f"name: toolkit page should be <name>_toolkit.mdx")
    elif not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", name):
        out.append("name: use kebab-case")
    m = re.match(r"---\r?\n(.*?)\r?\n---\r?\n", text, re.S)
    if not m:
        out.append("front matter missing")
        return
    keys = {}
    for line in m.group(1).splitlines():
        k = re.match(r"^(\w+):\s*(.*)$", line)
        if k:
            keys[k.group(1)] = k.group(2)
    for req in ("title", "description"):
        v = keys.get(req)
        if v is None:
            out.append(f"front matter: missing {req}")
        elif not re.fullmatch(r"\".*\"", v.strip()):
            out.append(f"front matter: {req} must be double-quoted")
    extra = set(keys) - FM_KEYS
    if extra:
        out.append("front matter: unexpected keys " + ", ".join(sorted(extra)))


def validate(page, scope_text=None, links_only=False, as_path=None):
    out = []
    try:
        text = open(page, encoding="utf-8").read()
        if as_path:
            page = os.path.abspath(as_path)
    except OSError as e:
        return [f"cannot read: {e}"]
    if scope_text is None:
        if not links_only:
            check_full(page, text, out)
        lines, offset = text.splitlines(), 1
    else:
        idx = text.find(scope_text)
        offset = text[:idx].count("\n") + 1 if idx >= 0 else 1
        lines = scope_text.splitlines()
    check_text(page, lines, offset, out)
    if links_only:
        out = [o for o in out if "->" in o or "alt" in o]
    return out


def in_scope(path):
    rel = os.path.relpath(os.path.abspath(path), DOCS).replace("\\", "/")
    return path.endswith(".mdx") and not rel.startswith("..") and rel.split("/")[0] not in SKIP_DIRS


def hook():
    try:
        data = json.load(sys.stdin)
    except ValueError:
        return 0
    ti = data.get("tool_input") or {}
    path = ti.get("file_path") or ""
    if not in_scope(path):
        return 0
    scope = None
    if data.get("tool_name") == "Edit":
        scope = ti.get("new_string") or ""
    elif data.get("tool_name") == "MultiEdit":
        scope = "\n".join(e.get("new_string", "") for e in ti.get("edits", []))
    issues = validate(path, scope)
    if not issues:
        return 0
    shown = issues[:MAX_LINES]
    more = f" (+{len(issues) - MAX_LINES} more)" if len(issues) > MAX_LINES else ""
    msg = f"doc-check {os.path.basename(path)}{more}: " + "; ".join(shown)
    print(json.dumps({"hookSpecificOutput": {"hookEventName": "PostToolUse", "additionalContext": msg}}))
    return 0


def cli(args):
    links_only = "--links-only" in args
    as_path = None
    if "--as" in args:
        i = args.index("--as")
        as_path = args[i + 1]
        args = args[:i] + args[i + 2:]
    files = []
    for a in (x for x in args if not x.startswith("--")):
        if os.path.isdir(a):
            for root, dirs, fs in os.walk(a):
                dirs[:] = [d for d in dirs if d not in SKIP_DIRS + ("img",)]
                files += [os.path.join(root, f) for f in fs if f.endswith(".mdx")]
        else:
            files.append(a)
    bad = 0
    for f in sorted(files):
        issues = validate(os.path.abspath(f), None, links_only, as_path)
        if issues:
            bad += 1
            print(f"{os.path.relpath(f).replace(os.sep, '/')}:")
            for i in issues:
                print("  " + i)
    print(f"{len(files)} file(s), {bad} with issues")
    return 1 if bad else 0


if __name__ == "__main__":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    sys.exit(cli(sys.argv[1:]) if len(sys.argv) > 1 else hook())
