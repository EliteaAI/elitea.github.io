"""Accuracy check (radar), no LLM: what changed in the code since the page's stamp.

Signals (user decision): UI labels on the page that were changed or removed in the diff, and changes
in code folders the knowledge maps link to the page's doc folder.
"""
import re

import config as C
import mdx as M
import stamp as S

LABEL = re.compile(r"\*\*([^*\n]{2,60})\*\*")


def page_labels(text):
    b = M.blank(text)
    labels = {l.strip().rstrip(":") for l in LABEL.findall(b)}
    # Skip run-in headings and labels too short or too generic to tell anything (one lowercase word).
    return sorted(l for l in labels
                  if not re.match(r"^(Note|Warning|Caution|Cause|Solution|Tip|Important)$", l)
                  and not re.fullmatch(r"[a-z]+", l) and len(l) > 2)


def map_folders(repo, doc_folder):
    """Code paths named on map lines whose docs column includes this doc folder."""
    f = C.KIT_DIR / "maps" / f"{repo}.md"
    if not f.exists():
        return []
    out = []
    for line in f.read_text(encoding="utf-8").splitlines():
        if "docs:" in line and f"{doc_folder}/*" in line.split("docs:", 1)[1]:
            out += re.findall(r"`([^`\s]+/)[^`]*`|`([^`\s]+\.[a-z]{2,4})`", line)
            out += re.findall(r"(?<![`\w])((?:features|widgets|entities|pages|shared|api/v2|utils|tools|runtime)/[\w\-/\[\]{}.,]+)", line)
    flat = []
    for x in out:
        for y in (x if isinstance(x, tuple) else (x,)):
            y = y.strip("`,.;") if y else ""
            if y and y not in flat:
                flat.append(y)
    return flat


def diff_lines(repo_path, base, head):
    out = C.git(repo_path, "diff", "--unified=0", "--no-color", f"{base}..{head}") or ""
    removed, added, files = [], [], []
    cur = None
    for l in out.splitlines():
        if l.startswith("+++ b/"):
            cur = l[6:]
            files.append(cur)
        elif l.startswith("-") and not l.startswith("---"):
            removed.append((cur, l[1:]))
        elif l.startswith("+") and not l.startswith("+++"):
            added.append((cur, l[1:]))
    return removed, added, files


def candidates(page, as_page=None):
    text = M.read(page)
    info = S.read(text)
    rel = M.docs_rel(as_page or page)
    doc_folder = rel.rsplit("/", 1)[0]
    if not info["present"] or len(info["repos"]) < len(S.REPOS):
        return None, S.baseline(info), []
    cfg = C.load()
    labels = page_labels(text)
    rows = []
    for repo, (branch, sha) in info["repos"].items():
        rp = C.repo_path(cfg, repo)
        head = f"origin/{cfg.get('code_branch') or branch}"
        if C.git(rp, "rev-parse", "--verify", "--quiet", f"{sha}^{{commit}}") is None:
            rows.append({"repo": repo, "kind": "error", "text": f"stamp SHA {sha} not found (fetch?)", "lines": []})
            continue
        n = C.git(rp, "rev-list", "--count", f"{sha}..{head}") or "?"
        removed, added, files = diff_lines(rp, sha, head)
        for lab in labels:
            pat = re.compile(rf"['\">`]\s*{re.escape(lab)}\s*['\"<`]")
            gone = [(f, l) for f, l in removed if pat.search(l)]
            still = C.git(rp, "grep", "-l", "-F", lab, head, "--", "src", "elitea_sdk", "api", "utils", "models") if gone else "x"
            if gone and not still:
                lines = [i for i, t in enumerate(text.split("\n"), 1) if f"**{lab}" in t]
                rows.append({"repo": repo, "kind": "label removed", "text": lab,
                             "evidence": f"{gone[0][0]}", "lines": lines})
        broad = {"api/v2", "utils", "tools", "runtime", "features", "widgets", "entities", "pages", "shared",
                 "models", "rpc", "src"}
        for folder in map_folders(repo, doc_folder):
            key = folder.rstrip("/")
            if key in broad:  # a whole top-level folder says nothing about this page
                continue
            hit = [f for f in files if key in f]
            if hit:
                # one directory pathspec (literal: paths like src/[fsd]/ contain glob characters);
                # a list of files fails when one of them was deleted in the range
                d = hit[0][:hit[0].index(key) + len(key)]
                log = C.git(rp, "--literal-pathspecs", "log", "--no-merges", "--format=%h %s",
                            f"{sha}..{head}", "--", d) or ""
                commits = [l for l in log.splitlines() if "Increment version" not in l]
                rows.append({"repo": repo, "kind": "mapped folder changed", "text": key,
                             "evidence": f"{len(hit)} file(s), {len(commits)} commit(s): " + "; ".join(commits[:3]),
                             "lines": []})
        rows.append({"repo": repo, "kind": "summary", "text": f"{n} commits {sha}..{head}", "lines": []})
    return info, S.baseline(info), rows
