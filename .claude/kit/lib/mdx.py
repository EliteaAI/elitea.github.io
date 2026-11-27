"""Shared MDX parsing: blanking of non-prose, headings/anchors, links, media refs."""
import re
from pathlib import Path

import config as C

DOCS = C.DOC_ROOT / "docs"
MEDIA_EXT = {".png", ".jpg", ".jpeg", ".gif", ".svg", ".webp", ".mp4", ".webm", ".mov", ".ico"}
VIDEO_EXT = {".mp4", ".webm", ".mov"}
EXTERNAL = re.compile(r"^(https?:|mailto:|tel:|//)", re.I)


def _keep_newlines(m):
    return re.sub(r"[^\n]", " ", m.group(0))


def blank(text):
    """Replace frontmatter, fenced code, inline code and MDX comments with spaces (newlines kept)."""
    t = re.sub(r"\A---\n.*?\n---[ \t]*(?=\n|\Z)", _keep_newlines, text, flags=re.S)
    t = re.sub(r"^[ \t]*(```|~~~).*?^[ \t]*\1[^\n]*", _keep_newlines, t, flags=re.S | re.M)
    t = re.sub(r"\{/\*.*?\*/\}", _keep_newlines, t, flags=re.S)
    t = re.sub(r"<!--.*?-->", _keep_newlines, t, flags=re.S)
    t = re.sub(r"`[^`\n]+`", _keep_newlines, t)
    return t


def line_of(text, pos):
    return text.count("\n", 0, pos) + 1


def slug(heading):
    """GitHub-style slug. Compare anchors with norm_anchor() to tolerate --."""
    h = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", heading)
    h = re.sub(r"<[^>]+>|[*_`]", "", h).strip().lower()
    h = re.sub(r"[^\w\- ]", "", h)
    return h.replace(" ", "-")


def norm_anchor(a):
    return re.sub(r"-+", "-", a.strip().lower()).strip("-")


HEADING = re.compile(r"^(#{1,6})[ \t]+(.+?)[ \t]*#*[ \t]*$", re.M)
ID_ATTR = re.compile(r"\bid=[\"']([^\"']+)[\"']")


def headings(btext):
    return [(line_of(btext, m.start()), len(m.group(1)), m.group(2)) for m in HEADING.finditer(btext)]


def anchors(text):
    b = blank(text)
    seen, out = {}, set()
    for _, _, h in headings(b):
        s = slug(h)
        n = seen.get(s, 0)
        seen[s] = n + 1
        out.add(norm_anchor(s if n == 0 else f"{s}-{n}"))
    out.update(norm_anchor(i) for i in ID_ATTR.findall(b))
    # Mintlify also makes anchors from Accordion/Tab/Step/Expandable titles.
    for t in re.findall(r"<(?:Accordion|Tab|Step|Expandable|ResponseField|ParamField)\b[^>]*?\btitle=\"([^\"]+)\"", b):
        out.add(norm_anchor(slug(t)))
    return out


MD_LINK = re.compile(r"(!?)\[((?:[^\[\]]|\[[^\]]*\])*)\]\(\s*(?:<([^>\n]+)>|([^)\s]+))(?:\s+\"[^\"]*\")?\s*\)")
TAG = re.compile(r"<(img|video|source|a|Card|iframe|Frame)\b([^>]*)>", re.S)
ATTR = re.compile(r"\b(src|href|alt|title)\s*=\s*(\"[^\"]*\"|'[^']*'|\{\"[^\"]*\"\})", re.S)


def attrs(s):
    return {k: v.strip("{}").strip("\"'") for k, v in ATTR.findall(s)}


def refs(text):
    """Yield dicts: line, kind (link|image|video|card), target, text."""
    b = blank(text)
    for m in MD_LINK.finditer(b):
        kind = "image" if m.group(1) else "link"
        yield {"line": line_of(b, m.start()), "kind": kind, "target": m.group(3) or m.group(4), "text": m.group(2)}
    for m in TAG.finditer(b):
        tag, a = m.group(1), attrs(m.group(2))
        for key in ("src", "href"):
            if key in a:
                kind = {"img": "image", "video": "video", "source": "video"}.get(tag, "link")
                yield {"line": line_of(b, m.start()), "kind": kind, "target": a[key], "text": a.get("alt", ""),
                       "tag": tag, "attrs": a, "raw": m.group(0)}


def split_target(t):
    t = t.split("?", 1)[0]
    path, _, anchor = t.partition("#")
    return path, anchor


def resolve(page, path):
    """Return candidate Paths for a link path from page (a Path under docs/)."""
    base = DOCS if path.startswith("/") else page.parent
    p = (base / path.lstrip("/")).resolve()
    if p.suffix.lower() in MEDIA_EXT or p.suffix.lower() == ".mdx":
        return [p]
    return [p.with_name(p.name + ".mdx"), p / "index.mdx", p]


TAG_ONLY = re.compile(r"^\s*</?[A-Za-z][^>]*>\s*$")
TABLE_SEP = re.compile(r"^\s*\|?\s*:?-{2,}")


def count_sentences(text, lines=None):
    """Sentences of prose in the given lines (all if None).

    Not counted: empty lines, tag-only lines, media/img lines (alt text), headings,
    table header rows and separators, frontmatter, code, MDX comments.
    List items and table body cells count as prose.
    """
    b = blank(text).split("\n")
    raw = text.split("\n")
    n, prev_table = 0, False
    for i, line in enumerate(b, 1):
        if lines is not None and i not in lines:
            prev_table = False
            continue
        s = line.strip()
        is_table = s.startswith("|")
        if not s or TAG_ONLY.match(s) or s.startswith("#") or TABLE_SEP.match(s):
            prev_table = is_table and prev_table
            continue
        if is_table:
            nxt = b[i].strip() if i < len(b) else ""
            if not prev_table and TABLE_SEP.match(nxt):  # header row
                prev_table = True
                continue
            prev_table = True
        else:
            prev_table = False
        s = re.sub(r"<(img|video|source|iframe)\b[^>]*/?>", " ", s)       # media incl. alt text
        s = re.sub(r"!\[[^\]]*\]\([^)]*\)", " ", s)                        # markdown images
        s = re.sub(r"<[^>]+>", " ", s)                                      # other tags
        s = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", s)                     # link text only
        s = re.sub(r"^\s*([-*+]|\d+\.)\s+", "", s).strip(" |")
        if not re.search(r"[A-Za-z]{2,}", s):
            continue
        if is_table:  # a row counts its sentence-ending cells; label-only cells are not sentences
            cells = [c.strip() for c in s.split("|") if re.search(r"[A-Za-z]{2,}", c)]
            n += max(1, sum(len(re.findall(r"[.!?](?=\s|$)", c)) for c in cells))
            continue
        parts = [p for p in re.split(r"(?<=[.!?])\s+", s) if re.search(r"[A-Za-z]{2,}", p)]
        n += max(1, len(parts))
    return n


def pages(include_archive=False):
    for p in sorted(DOCS.rglob("*.mdx")):
        rp = p.relative_to(DOCS).as_posix()
        if rp.startswith("styleguides/"):
            continue
        if not include_archive and rp.startswith("archive/"):
            continue
        yield p


def read(p):
    return Path(p).read_text(encoding="utf-8", errors="replace")


def as_page(path_arg, as_arg=None):
    """(file to read, page location for resolving). --as lets a temp fixture act as a real page."""
    f = Path(path_arg)
    if not f.is_absolute():
        f = (Path.cwd() / f).resolve()
        if not f.exists():
            f = (C.DOC_ROOT / path_arg).resolve()
    loc = Path(as_arg) if as_arg else f
    if not loc.is_absolute():
        loc = (C.DOC_ROOT / as_arg).resolve()
    return f, loc


def docs_rel(p):
    try:
        return Path(p).resolve().relative_to(DOCS).as_posix()
    except ValueError:
        return str(p)
