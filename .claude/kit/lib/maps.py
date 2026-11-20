"""Knowledge-map skeletons (no LLM). Reads code repos via git refs only.

`skeleton(repo)` writes a fact sheet to the temp cache for the code-scout agent;
`status()` compares each map header with the current branch head.
"""
import re
from collections import Counter
from datetime import date

import config as C

MAP_DIR = C.KIT_DIR / "maps"
GITHUB = {"EliteaUI": "EliteaAI/EliteaUI", "elitea-sdk": "EliteaAI/elitea-sdk", "elitea_core": "EliteaAI/elitea_core"}

# Per repo: interesting folder roots (depth to list) and grep probes for doc-relevant facts.
PROFILE = {
    "EliteaUI": {
        "roots": [("src/[fsd]", 2), ("src/pages", 1), ("src/components", 1)],
        "files": ["src/routes.js", "src/common/constants.js", ".env.example", "AGENTS.md", "CLAUDE.md"],
        "probes": {
            "routes": r"path:\s*['\"`]/[^'\"`]*",
            "permissions": r"PERMISSIONS\.[a-zA-Z_.]+",
            "feature flags": r"(VITE_[A-Z_]+|ALLOW_[A-Z_]+|is[A-Z]\w*Enabled)",
            "i18n": r"(useTranslation|i18next|t\(['\"])",
        },
        "globs": ["src/**/*.js", "src/**/*.jsx"],
    },
    "elitea-sdk": {
        "roots": [("elitea_sdk", 1), ("elitea_sdk/tools", 1), ("elitea_sdk/configurations", 1),
                  ("elitea_sdk/runtime", 1)],
        "files": ["README.md", "pyproject.toml", ".elitea/agents/ELITEA_ARCHITECTURE.md"],
        "probes": {
            "toolkit names": r"(name|toolkit_name)\s*=\s*['\"][a-z0-9_]+['\"]",
            "pydantic fields": r"Field\([^)]*(description|title)\s*=",
            "limits/defaults": r"(max_|MAX_|DEFAULT_|default=)\w*",
        },
        "globs": ["elitea_sdk/**/*.py"],
    },
    "elitea_core": {
        "roots": [("api", 1), ("api/v2", 1), ("routes", 1), ("models", 1), ("rpc", 1), ("sio", 1)],
        "files": ["README.md", "config.yml", "metadata.json"],
        "probes": {
            "limits/defaults": r"(MAX_|DEFAULT_|_LIMIT|max_\w+\s*=|default\s*=)",
            "settings keys": r"(platform_settings|project_settings|governance)\w*",
            "permissions": r"@auth\.decorators\.check_api\(\s*\{?['\"]?[a-z_.]+",
        },
        "globs": ["api/**/*.py", "models/**/*.py", "rpc/**/*.py", "utils/**/*.py"],
    },
}


def ref(cfg):
    b = cfg.get("code_branch")
    return f"origin/{b}" if b else None


def head(repo_path, r):
    sha = C.git(repo_path, "rev-parse", "--short=9", r)
    when = C.git(repo_path, "log", "-1", "--format=%cs", r)
    return sha, when


def tree(repo_path, r, root, depth):
    out = C.git(repo_path, "ls-tree", "-r", "--name-only", r, "--", root) or ""
    dirs = Counter()
    for f in out.splitlines():
        rest = f[len(root):].lstrip("/").split("/")
        if len(rest) > 1:
            dirs["/".join(rest[:min(depth, len(rest) - 1)])] += 1
    return dirs


def probe(repo_path, r, pattern, globs, limit=25):
    out = C.git(repo_path, "grep", "-hoE", "-I", pattern, r, "--", *globs) or ""
    c = Counter(l.split(":", 1)[-1].strip()[:80] for l in out.splitlines())
    return c.most_common(limit)


def skeleton(name):
    cfg = C.load()
    r = ref(cfg)
    rp = C.repo_path(cfg, name)
    if not r:
        return None, "no code branch saved (df.py cfg branch <name>)"
    sha, when = head(rp, r)
    if not sha:
        return None, f"{r} not found in {name}"
    prof = PROFILE[name]
    lines = [f"# skeleton {name} {r}@{sha} ({when})", ""]
    for root, depth in prof["roots"]:
        d = tree(rp, r, root, depth)
        lines.append(f"## tree {root} ({sum(d.values())} files)")
        lines += [f"- {k} ({v})" for k, v in sorted(d.items())]
        lines.append("")
    for f in prof["files"]:
        exists = C.git(rp, "cat-file", "-e", f"{r}:{f}") is not None
        lines.append(f"- file {f}: {'present' if exists else 'missing'}")
    lines.append("")
    for label, pat in prof["probes"].items():
        hits = probe(rp, r, pat, prof["globs"])
        lines.append(f"## probe {label} ({len(hits)} distinct, top shown)")
        lines += [f"- {h} ({n})" for h, n in hits]
        lines.append("")
    g = [x for x in gaps() if x.startswith(f"- {name} |")]
    lines.append(f"## recorded gaps to cover ({len(g)})")
    lines += g
    lines.append("")
    log = C.git(rp, "log", "--since=45 days", "--no-merges", "--format=%cs %s", r) or ""
    tickets = Counter(re.findall(r"\bEL-\d+\b", log))
    lines.append("## doc folders (for the docs column)")
    lines += [f"- {d}" for d in doc_folders()]
    lines.append("")
    lines.append(f"## recent commits (45 days): {len(log.splitlines())}, tickets {len(tickets)}")
    lines += [f"- {l[:110]}" for l in log.splitlines()[:40] if "Increment version" not in l]
    path = C.cache("maps", f"{name}.skeleton.md")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return path, f"{name} {r}@{sha}: {len(lines)} lines"


HEADER = re.compile(r"^(branch|sha|refreshed):\s*(\S+)", re.M)


def doc_folders():
    docs = C.DOC_ROOT / "docs"
    out = []
    for d in sorted(p for p in docs.rglob("*") if p.is_dir()):
        rel = d.relative_to(docs).as_posix()
        if rel.split("/")[0] in ("img", "archive", "styleguides") or "/archived" in rel or rel == "release-notes/archived":
            continue
        n = len(list(d.glob("*.mdx")))
        if n:
            out.append(f"{rel}/* ({n})")
    return out


def status():
    cfg = C.load()
    r = ref(cfg)
    rows = []
    for name in GITHUB:
        f = MAP_DIR / f"{name}.md"
        if not f.exists():
            rows.append((name, "missing", ""))
            continue
        h = dict(HEADER.findall(f.read_text(encoding="utf-8")[:600]))
        cur, _ = head(C.repo_path(cfg, name), r) if r else (None, None)
        if not r:
            state = "no code branch saved"
        elif h.get("branch") != cfg.get("code_branch"):
            state = f"STALE: map is for {h.get('branch')}, saved branch is {cfg.get('code_branch')}"
        elif cur and not cur.startswith(h.get("sha", "")[:7]):
            n = C.git(C.repo_path(cfg, name), "rev-list", "--count", f"{h.get('sha')}..{r}")
            state = f"behind by {n or '?'} commits ({h.get('sha')} -> {cur})"
        else:
            state = "current"
        rows.append((name, state, h.get("refreshed", "")))
    return rows


REBUILD_COMMITS = 300  # offer a rebuild when a map is this many commits behind


def gaps_file():
    return C.cache("maps", "gaps.md")


def add_gap(repo, topic, pointer):
    f = gaps_file()
    line = f"- {repo} | {topic} | {pointer} | {date.today().isoformat()}\n"
    old = f.read_text(encoding="utf-8") if f.exists() else ""
    if f"- {repo} | {topic} |" not in old:
        f.write_text(old + line, encoding="utf-8")
        return True
    return False


def gaps():
    f = gaps_file()
    return [l for l in f.read_text(encoding="utf-8").splitlines() if l.startswith("- ")] if f.exists() else []


def advice(rows, topic=None):
    """When to offer a rebuild: branch switched, >= REBUILD_COMMITS behind, or the topic is a known gap."""
    out = []
    for name, state, _ in rows:
        if state.startswith("STALE") or state == "missing":
            out.append(f"{name}: offer rebuild ({state})")
        elif state.startswith("behind by"):
            n = re.match(r"behind by (\d+)", state)
            if n and int(n.group(1)) >= REBUILD_COMMITS:
                out.append(f"{name}: offer rebuild ({state})")
    if topic:
        hits = [g for g in gaps() if topic.lower() in g.lower()]
        out += [f"known gap for '{topic}': {g[2:]}" for g in hits]
    return out


def today():
    return date.today().isoformat()
