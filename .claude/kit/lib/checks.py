"""Script checks (no LLM): style lint, links/anchors, inbound links, media usage."""
import os
import re
from pathlib import Path

import config as C
import mdx as M

# --- lint: (id, regex, message, scope) scope: "prose" (blanked text) or "raw"
LINT = [
    ("en-dash", r"–", "en dash: use - in words, — between them"),
    ("ellipsis", r"\.\.\.(?!\])|…", "ellipsis"),
    ("em-dash-space", r"\s—|—\s", "em dash with spaces"),
    ("exclamation", r"[A-Za-z0-9)\"*]!(?=\s|$)", "exclamation mark"),
    ("contraction", r"\b(?:\w+n't|it's|you're|we're|they're|that's|there's|let's|you'll|we'll|it'll|you've|we've|I'm)\b",
     "contraction"),
    ("possessive", r"\bELITEA's\b", "possessive on product name"),
    ("allow-you", r"\b(?:allows?|enables?|lets?) (?:you|users?|the user|the LLM|the agent|admins?|administrators?)\b",
     "use 'can'"),
    ("need-to", r"\bneeds? to\b", "use must/should/can"),
    ("words", r"\b(?:simply|easily|utilize[sd]?|navigate to|please note|at this time|respectively|dialog box|"
              r"pop-up|modal window|dialog window|click(?:s|ed|ing)?|press(?:es)?|tap|touch)\b", "word to avoid"),
    ("time-word", r"\b(?:currently|presently|at present|as of this writing|soon|eventually|in the future|newer|older|"
                  r"does not yet)\b",
     "time-anchored word"),
    ("below-above", r"\b(?:below|above)\b", "use following/previous or a link"),
    ("personal-project", r"\bpersonal projects?\b", "projects are 'private' (unless UI label)"),
    ("this-page", r"\b(?:This page is about|This guide explains)\b", "phrase to avoid"),
    ("link-here", r"\[(?:here|this page|this link|click here)\]", "non-descriptive link text"),
]
LINT = [(i, re.compile(p, re.I if i not in ("possessive",) else 0), m) for i, p, m in LINT]

SEE_ALSO = re.compile(r'<Callout[^>]*title="See Also"[^>]*>(.*?)</Callout>', re.S)


def lint(text, lines=None, page_rel=""):
    """Return findings [(line, id, message, excerpt)]. lines: set of line numbers to keep, or None."""
    b = M.blank(text)
    raw_lines, b_lines = text.split("\n"), b.split("\n")
    rn = page_rel.startswith("release-notes/")
    out = []

    def add(ln, rid, msg):
        if lines is None or ln in lines:
            out.append((ln, rid, msg, raw_lines[ln - 1].strip()[:90]))

    for i, line in enumerate(b_lines, 1):
        stripped = re.sub(r"<[^>]+>", " ", line)  # ignore tag attributes
        stripped = re.sub(r"\]\([^)]*\)", "]", stripped)  # ignore link targets
        for rid, rx, msg in LINT:
            if rn and rid == "time-word":
                continue
            if rx.search(stripped):
                add(i, rid, msg)
    for ln, level, h in M.headings(b):
        if level >= 4:
            add(ln, "h4", f"H{level} heading: report; ask if this depth is needed")
        if re.search(r"\]\(", h):
            add(ln, "heading-link", "link in heading")
        if re.search(r"\band\b", h) and level >= 2:
            add(ln, "heading-and", "use & in headings (unless official name)")
    for r in M.refs(text):
        a = r.get("attrs", {})
        tgt = r["target"].lower()
        ext = os.path.splitext(M.split_target(tgt)[0])[1]
        if r.get("tag") == "img" and ext in M.VIDEO_EXT:
            add(r["line"], "video-as-img", "video in <img>: use <video src=… controls />")
        if r.get("tag") == "img" and "alt" not in a:
            add(r["line"], "alt-missing", "image without alt")
        if r.get("tag") in ("video",) and "alt" in a:
            add(r["line"], "video-alt", "<video> takes no alt")
        if r.get("tag") == "img" and a.get("alt"):
            alt = a["alt"]
            if len(alt) > 155:
                add(r["line"], "alt-long", f"alt text {len(alt)} chars (max 155)")
            if not alt.rstrip().endswith((".", "?")):
                add(r["line"], "alt-period", "alt text must end with a period")
            if re.search(r"\*|_[^_]+_", alt):
                add(r["line"], "alt-format", "no bold/italics in alt text")
        if r.get("tag") == "img" and ext == ".gif" and lines is not None:
            add(r["line"], "gif-new", "new GIF: use MP4")
        if r["kind"] == "image" and r.get("tag") is None:
            add(r["line"], "md-image", "markdown image: use <img src=… alt=… />")
    for m in re.finditer(r"<(Tip|Check)\b", b):
        add(M.line_of(b, m.start()), "callout-type", f"<{m.group(1)}> is not used")
    for m in re.finditer(r'<Info\b[^>]*title="See [Aa]lso"|^#{2,3} See [Aa]lso', b, re.M):
        add(M.line_of(b, m.start()), "see-also-form", 'See Also must be <Callout icon="book" color="#C9B896" title="See Also">')
    for m in SEE_ALSO.finditer(b):
        body, start = m.group(1), M.line_of(b, m.start(1))
        for k, l in enumerate(body.split("\n")):
            ls = l.strip()
            if re.match(r"(?i)see also:?$", ls):
                add(start + k, "see-also-label", "no 'See also:' line inside the callout")
            elif ls.startswith("* "):
                add(start + k, "see-also-bullet", "use '-' bullets in See Also")
            elif re.match(r"- \[[^\]]+\]\([^)]+\)\s*\S", ls):
                add(start + k, "see-also-explain", "no explanation after See Also links")
    for m in re.finditer(r"^>\s", b, re.M):
        add(M.line_of(b, m.start()), "blockquote", "no blockquotes")
    for m in re.finditer(r"</(Note|Warning|Info|Danger|Callout)>\s*\n\s*\n?\s*<(Note|Warning|Info|Danger|Callout)\b", b):
        add(M.line_of(b, m.end()), "callout-after-callout", "callout right after a callout")
    out.sort()
    return out


# --- links and anchors
_anchor_cache = {}


def page_anchors(p):
    key = str(p)
    if key not in _anchor_cache:
        _anchor_cache[key] = M.anchors(M.read(p)) if Path(p).exists() else set()
    return _anchor_cache[key]


def check_links(text, page):
    """Findings [(line, kind, target, problem, hint)] for internal links, anchors and media."""
    out = []
    own = M.anchors(text)
    for r in M.refs(text):
        t = r["target"]
        if not t or M.EXTERNAL.match(t) or t.startswith("{"):
            continue
        path, anchor = M.split_target(t)
        if not path:
            if anchor and M.norm_anchor(anchor) not in own:
                out.append((r["line"], r["kind"], t, "anchor not found on this page", ""))
            continue
        cands = M.resolve(page, path)
        if path.lower().endswith(".md"):
            cands = [Path(str(c)[:-3] + ".mdx") for c in cands if str(c).lower().endswith(".md")] + cands
        hit = next((c for c in cands if c.is_file()), None)
        if hit and path.lower().endswith((".md", ".mdx")) and hit.suffix == ".mdx":
            out.append((r["line"], r["kind"], t, "works, but drop the extension", M.docs_rel(hit)))
        if not hit:
            red = redirect_for(page, path)
            if red:
                out.append((r["line"], r["kind"], t, "works via redirect", f"update to {red}"))
                continue
            hint = ""
            if os.path.splitext(path)[1].lower() in M.MEDIA_EXT:
                found = media_index().get(Path(path).name.lower(), [])
                hint = ("found: " + ", ".join(found[:3])) if found else "no file with this name in docs/img"
            out.append((r["line"], r["kind"], t, "target not found", hint))
            continue
        if anchor and hit.suffix == ".mdx" and M.norm_anchor(anchor) not in page_anchors(hit):
            out.append((r["line"], r["kind"], t, "anchor not found in target", M.docs_rel(hit)))
    return out


_redirects = None


def redirect_for(page, path):
    """Destination if the link's site path matches a docs.json redirect source."""
    global _redirects
    if _redirects is None:
        import json
        try:
            d = json.loads((M.DOCS / "docs.json").read_text(encoding="utf-8"))
            _redirects = {re.sub(r"/+", "/", r["source"]).rstrip("/").lower(): r["destination"]
                          for r in d.get("redirects", [])}
        except (OSError, ValueError, KeyError):
            _redirects = {}
    p = (M.DOCS / path.lstrip("/")) if path.startswith("/") else (page.parent / path)
    site = "/" + M.docs_rel(p.resolve()).removesuffix(".mdx").removesuffix(".md")
    return _redirects.get(site.lower())


_media = None


def media_index():
    """{lowercase file name: [docs-relative paths]} for every media file under docs/img."""
    global _media
    if _media is None:
        _media = {}
        for root, _, files in os.walk(M.DOCS / "img"):
            for f in files:
                if os.path.splitext(f)[1].lower() in M.MEDIA_EXT:
                    _media.setdefault(f.lower(), []).append(M.docs_rel(Path(root) / f))
    return _media


# --- inbound links: which pages link to target page (and anchors used)
def inbound(target):
    tgt = (M.DOCS / target).resolve() if not Path(target).is_absolute() else Path(target).resolve()
    if tgt.suffix != ".mdx":
        tgt = tgt.with_suffix(".mdx")
    rows = []
    for p in M.pages(include_archive=True):
        text = M.read(p)
        for r in M.refs(text):
            path, anchor = M.split_target(r["target"])
            if not path or M.EXTERNAL.match(path):
                continue
            if any(c == tgt for c in M.resolve(p, path)):
                rows.append((M.docs_rel(p), r["line"], r["target"], r["text"][:60]))
    return M.docs_rel(tgt), rows


# --- media usage and orphans
def media_refs():
    """{docs-relative media path: [(page, line)]} for every media reference in all pages."""
    used = {}
    for p in M.pages(include_archive=True):
        for r in M.refs(M.read(p)):
            path, _ = M.split_target(r["target"])
            if not path or M.EXTERNAL.match(path) or os.path.splitext(path)[1].lower() not in M.MEDIA_EXT:
                continue
            cands = M.resolve(p, path)
            hit = next((c for c in cands if c.is_file()), None)
            key = M.docs_rel(hit) if hit else "BROKEN:" + path
            used.setdefault(key, []).append((M.docs_rel(p), r["line"]))
    return used


def media_files(folder=None):
    base = M.DOCS / (folder or "img")
    for root, _, files in os.walk(base):
        for f in files:
            if os.path.splitext(f)[1].lower() in M.MEDIA_EXT:
                full = Path(root) / f
                yield M.docs_rel(full), full.stat().st_size
