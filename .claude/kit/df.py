"""Doc-factory scripts (no LLM). Usage: python .claude/kit/df.py <command> [args]

Config
  cfg                              repo paths, code branch, lock
  cfg branches                     release branches per code repo
  cfg branch <name>|clear          set (validated in all repos) or clear the code branch
  cfg repo <name> <path>           set a repo path for this machine
  cfg lock on                      setup lock on (only the user turns it off)
Checks (read-only)
  lint <page> [--lines A-B,C] [--as <page>]    style rules a script can check
  links <page>|--all [--as <page>]             broken links, anchors, media (with "found in" hints)
  inbound <page>                               pages that link to <page>, with lines and anchors
  media used <file>                            pages that use a media file
  media orphans <folder>                       media in folder used by no page
  media big [MB]                               videos and GIFs over the limit (default 20)
  validate                                     mint validate (in docs/)
  size <page> [--lines A-B]                    sentences of prose (decides: <=3 main session, >3 reviewer)
  find <regex> [--in <folder>] [--words]       occurrences in pages (prose only), for renames
Navigation (docs.json, read-only; the main session applies edits)
  toc find <text>                              groups and pages matching text
  toc add <page> --group "<group or path>" [--after <page>]   exact edit to add a page
  toc rename <old-page> <new-page>             nav occurrences + redirect to add
  toc check                                    nav pages exist; pages missing from nav
Accuracy check
  radar <page>                                 candidates since the page's stamp (labels, mapped folders)
Stamp
  stamp read <page>                            stamp fields and baseline
  stamp build <page> <version> <n|f|u> [--branch B]   the new stamp line + where it goes (no write)
Knowledge maps (.claude/kit/maps/)
  map status                                   each map's branch/SHA vs the saved code branch
  map skeleton <repo>|all                      script fact sheet in temp (input for code-scout)
  map advice [topic]                           whether to offer a rebuild (branch switch, >=300 commits, known gap)
  map gap <repo> "<topic>" "<code pointer>"     record a gap a scout found (covered at the next rebuild)
  map gaps                                     list recorded gaps
Findings (temp cache)
  findings add <key> <json-file>               add items, prints their numbers
  findings show <key> [open|approved|done|ok|rejected]   ok = checked, no change needed
  findings set <key> <state> <n,n,...>         e.g. findings set docs/x.mdx approved 1,2,5
  findings lists                               keys with findings
"""
import json
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "lib"))
import config as C  # noqa: E402

for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8", errors="replace")
    except AttributeError:
        pass


def cmd_cfg(args):
    cfg = C.load()
    if not args:
        for name in cfg["repos"]:
            p = C.repo_path(cfg, name)
            state = "ok" if (p / ".git").exists() else "MISSING"
            print(f"{name}: {cfg['repos'][name]} [{state}]")
        print(f"code_branch: {cfg['code_branch'] or '(not set)'}")
        print(f"setup_lock: {'on' if cfg['setup_lock'] else 'off'}")
        return 0
    sub, rest = args[0], args[1:]
    if sub == "branches":
        for name in cfg["repos"]:
            p = C.repo_path(cfg, name)
            if not (p / ".git").exists():
                print(f"{name}: REPO NOT FOUND at {cfg['repos'][name]} (set with: cfg repo {name} <path>)")
                continue
            out = C.git(p, "for-each-ref", "--sort=-committerdate",
                        "--format=%(refname:short) %(committerdate:short)",
                        "refs/remotes/origin/release/", "refs/remotes/origin/main")
            if out is None:
                print(f"{name}: git error reading branches")
                continue
            rows = out.splitlines()[:4]
            print(f"{name}: " + ("; ".join(rows) if rows else "no origin/main or origin/release/* refs"))
        return 0
    if sub == "branch" and rest:
        if rest[0] == "clear":
            C.save_local("code_branch", None)
            print("code_branch cleared")
            return 0
        name = rest[0].removeprefix("origin/")
        missing = [r for r in cfg["repos"] if C.git(C.repo_path(cfg, r), "rev-parse", "--verify", "--quiet",
                                                       f"refs/remotes/origin/{name}") is None]
        if missing:
            print(f"Not saved: origin/{name} not found in {', '.join(missing)}. Check the name with: cfg branches")
            return 1
        C.save_local("code_branch", name)
        print(f"code_branch: {name} (found in all repos)")
        return 0
    if sub == "repo" and len(rest) == 2 and rest[0] in C.DEFAULTS["repos"]:
        C.save_local(f"repos.{rest[0]}", rest[1])
        print(f"{rest[0]}: {rest[1]}")
        return 0
    if sub == "lock" and rest == ["on"]:
        C.save_local("setup_lock", True)
        print("setup_lock: on")
        return 0
    print(__doc__)
    return 1


def opt(args, name):
    if name in args:
        i = args.index(name)
        val = args[i + 1] if i + 1 < len(args) else None
        del args[i:i + 2]
        return val
    return None


def parse_lines(spec):
    if not spec:
        return None
    out = set()
    for part in spec.split(","):
        a, _, b = part.partition("-")
        out.update(range(int(a), int(b or a) + 1))
    return out


def cmd_lint(args):
    import checks, mdx as M
    as_ = opt(args, "--as")
    lines = parse_lines(opt(args, "--lines"))
    if not args:
        print("usage: lint <page> [--lines A-B] [--as <page>]")
        return 1
    f, loc = M.as_page(args[0], as_)
    rows = checks.lint(M.read(f), lines, M.docs_rel(loc))
    for ln, rid, msg, ex in rows:
        print(f"{ln}: [{rid}] {msg} | {ex}")
    print(f"{len(rows)} finding(s)" + (f" in lines {opt_desc(lines)}" if lines else ""))
    return 0


def opt_desc(lines):
    return f"{min(lines)}-{max(lines)}" if lines else ""


def cmd_links(args):
    import checks, mdx as M
    as_ = opt(args, "--as")
    targets = list(M.pages()) if args == ["--all"] else [M.as_page(args[0], as_)] if args else []
    if not targets:
        print("usage: links <page>|--all [--as <page>]")
        return 1
    total = 0
    for t in targets:
        f, loc = t if isinstance(t, tuple) else (t, t)
        for ln, kind, tgt, prob, hint in checks.check_links(M.read(f), loc):
            total += 1
            print(f"{M.docs_rel(loc)}:{ln}: {kind} {tgt} -> {prob}" + (f" ({hint})" if hint else ""))
    print(f"{total} problem(s) in {len(targets)} page(s)")
    return 0


def cmd_inbound(args):
    import checks
    if not args:
        print("usage: inbound <page>")
        return 1
    tgt, rows = checks.inbound(args[0])
    for page, ln, target, text in rows:
        print(f"{page}:{ln}: [{text}]({target})")
    print(f"{len(rows)} link(s) to {tgt} from {len({r[0] for r in rows})} page(s)")
    return 0


def cmd_media(args):
    import checks, mdx as M
    if not args:
        print("usage: media used <file> | orphans <folder> | big [MB]")
        return 1
    sub, rest = args[0], args[1:]
    if sub == "used" and rest:
        used = checks.media_refs()
        name = Path(rest[0]).name.lower()
        hits = {k: v for k, v in used.items() if Path(k).name.lower() == name}
        for k, v in hits.items():
            for page, ln in v:
                tag = "  (broken path: file not found there)" if k.startswith("BROKEN:") else ""
                print(f"{k.removeprefix('BROKEN:')} <- {page}:{ln}{tag}")
        ok = sum(len(v) for k, v in hits.items() if not k.startswith("BROKEN:"))
        bad = sum(len(v) for k, v in hits.items() if k.startswith("BROKEN:"))
        print(f"{ok} use(s)" + (f", {bad} broken reference(s)" if bad else ""))
        return 0
    if sub == "orphans" and rest:
        used = checks.media_refs()
        folder = rest[0].replace("\\", "/").removeprefix("docs/")
        rows = [(p, s) for p, s in checks.media_files(folder) if p not in used]
        for p, s in rows:
            print(f"{p} ({s / 1048576:.1f} MB)")
        print(f"{len(rows)} unused file(s) in {folder}")
        return 0
    if sub == "big":
        limit = float(rest[0]) if rest else 20.0
        rows = [(p, s) for p, s in checks.media_files() if Path(p).suffix.lower() in M.VIDEO_EXT | {".gif"}
                and s > limit * 1048576]
        for p, s in rows:
            print(f"{p} ({s / 1048576:.1f} MB)")
        print(f"{len(rows)} file(s) over {limit:g} MB")
        return 0
    print("usage: media used <file> | orphans <folder> | big [MB]")
    return 1


def cmd_size(args):
    import mdx as M
    lines = parse_lines(opt(args, "--lines"))
    if not args:
        print("usage: size <page> [--lines A-B]")
        return 1
    f, _ = M.as_page(args[0])
    n = M.count_sentences(M.read(f), lines)
    print(f"{n} sentence(s) -> {'main session' if n <= 3 else 'reviewer'}")
    return 0


def cmd_validate(args):
    r = subprocess.run("mint validate", shell=True, cwd=C.DOC_ROOT / "docs", capture_output=True, text=True,
                       encoding="utf-8", errors="replace")
    import re
    clean = re.sub(r"\x1b\[[0-9;]*[A-Za-z]", "", (r.stdout + r.stderr).replace("\r", "\n"))
    lines = [l.strip() for l in clean.splitlines() if l.strip() and not re.match(r"^[⠀-⣿]", l.strip())]
    print("\n".join(lines[-15:]) or f"(no output, exit {r.returncode})")
    return r.returncode


def cmd_findings(args):
    import findings as F
    if not args:
        print(__doc__)
        return 1
    sub, rest = args[0], args[1:]
    if sub == "add" and len(rest) == 2:
        items = json.loads(Path(rest[1]).read_text(encoding="utf-8"))
        print("added: " + ", ".join(map(str, F.add(rest[0], items))))
        return 0
    if sub == "show" and rest:
        print(F.table(rest[0], rest[1:] or None))
        return 0
    if sub == "set" and len(rest) == 3 and rest[1] in F.STATES:
        nums = [int(x) for x in rest[2].split(",") if x.strip()]
        done, missing = F.set_state(rest[0], nums, rest[1])
        print(f"{rest[1]}: {done}" + (f"; not found: {missing}" if missing else ""))
        return 0
    if sub == "lists":
        print("\n".join(F.lists()) or "no findings")
        return 0
    print(__doc__)
    return 1


def cmd_stamp(args):
    import mdx as M, stamp as S
    branch = opt(args, "--branch")
    if len(args) == 2 and args[0] == "read":
        info = S.read(M.read(M.as_page(args[1])[0]))
        if info["present"]:
            print(f"version {info['version']} | {info['workflow'] or '-'} {info['date'] or '-'}")
        if info["legacy_verified"]:
            print("note: page has a legacy 'verified:' block (migrate later)")
        print(S.baseline(info))
        return 0
    if len(args) == 4 and args[0] == "build":
        f = M.as_page(args[1])[0]
        try:
            line = S.build(args[2], args[3], branch)
        except ValueError as e:
            print(f"cannot build stamp: {e}")
            return 1
        old, where = S.plan(M.read(f), line)
        print(line)
        print(f"where: {where}" + (f"\nold:   {old}" if old else ""))
        return 0
    print("usage: stamp read <page> | stamp build <page> <version> <n|f|u> [--branch B]")
    return 1


def cmd_toc(args):
    import toc as T
    after = opt(args, "--after")
    group = opt(args, "--group")
    if len(args) == 2 and args[0] == "find":
        for kind, g, x in T.find(args[1]):
            print(f"{kind}: {g}" + (f" ({x} pages)" if kind == "group" else f" -> {x}"))
        return 0
    if len(args) == 2 and args[0] == "add" and group:
        try:
            old, new, where = T.plan_add(args[1].removesuffix(".mdx").removeprefix("docs/"), group, after)
        except ValueError as e:
            print(f"cannot add: {e}")
            return 1
        print(f"group: {where}\nreplace:\n{old}\nwith:\n{new}")
        return 0
    if len(args) == 3 and args[0] == "rename":
        p = T.plan_rename(args[1], args[2])
        print(f"{p['nav_occurrences']} occurrence(s) of {p['old']} -> {p['new']}\nadd redirect: {p['redirect']}")
        return 0
    if args == ["check"]:
        rows = T.check()
        print("\n".join(rows) if rows else "nav OK")
        return 0
    print("usage: toc find <text> | add <page> --group G [--after P] | rename <old> <new> | check")
    return 1


def cmd_radar(args):
    import mdx as M, radar as R
    as_ = opt(args, "--as")
    if not args:
        print("usage: radar <page> [--as <page>]")
        return 1
    f, loc = M.as_page(args[0], as_)
    info, base, rows = R.candidates(f, loc)
    print(base)
    if info is None:
        print("cannot compare: unknown baseline (stamp the page after the next full check)")
        return 0
    n = 0
    for r in rows:
        if r["kind"] == "summary":
            print(f"{r['repo']}: {r['text']}")
            continue
        n += 1
        lines = ",".join(map(str, r["lines"])) or "-"
        print(f"{n}. [{r['repo']}] {r['kind']}: {r['text']} | page lines {lines} | {r.get('evidence', '')}")
    print(f"{n} candidate(s)")
    return 0


def cmd_find(args):
    import re, mdx as M
    folder = opt(args, "--in")
    words = "--words" in args
    args = [a for a in args if a != "--words"]
    if not args:
        print("usage: find <regex> [--in <folder>] [--words]")
        return 1
    pat = re.compile(rf"\b(?:{args[0]})\b" if words else args[0])
    total, pages_hit = 0, 0
    for p in M.pages():
        rel = M.docs_rel(p)
        if folder and not rel.startswith(folder.replace("\\", "/").removeprefix("docs/")):
            continue
        text = M.read(p)
        b, raw = M.blank(text).split("\n"), text.split("\n")
        hits = [(i, raw[i - 1].strip()) for i, l in enumerate(b, 1) if pat.search(l)]
        if hits:
            pages_hit += 1
            for i, l in hits:
                total += 1
                print(f"{rel}:{i}: {l[:120]}")
    print(f"{total} occurrence(s) in {pages_hit} page(s) (prose only; code, comments, frontmatter skipped)")
    return 0


def cmd_map(args):
    import maps
    if args == ["status"]:
        for name, state, refreshed in maps.status():
            print(f"{name}: {state}" + (f" (refreshed {refreshed})" if refreshed else ""))
        return 0
    if args and args[0] == "advice":
        rows = maps.advice(maps.status(), args[1] if len(args) > 1 else None)
        print("\n".join(rows) if rows else "no rebuild needed")
        return 0
    if len(args) == 4 and args[0] == "gap":
        print("gap recorded" if maps.add_gap(*args[1:]) else "gap already recorded")
        return 0
    if args == ["gaps"]:
        g = maps.gaps()
        print("\n".join(g) if g else "no recorded gaps")
        return 0
    if len(args) == 2 and args[0] == "skeleton":
        names = list(maps.GITHUB) if args[1] == "all" else [args[1]]
        rc = 0
        for n in names:
            if n not in maps.GITHUB:
                print(f"unknown repo {n}; use one of {', '.join(maps.GITHUB)}")
                return 1
            path, msg = maps.skeleton(n)
            print(f"{msg}" + (f" -> {path}" if path else ""))
            rc |= path is None
        return rc
    print("usage: map status | map skeleton <repo>|all")
    return 1


COMMANDS = {"cfg": cmd_cfg, "map": cmd_map, "stamp": cmd_stamp, "find": cmd_find, "toc": cmd_toc, "radar": cmd_radar, "lint": cmd_lint, "links": cmd_links, "inbound": cmd_inbound,
            "media": cmd_media, "validate": cmd_validate, "size": cmd_size, "findings": cmd_findings}

if __name__ == "__main__":
    if len(sys.argv) < 2 or sys.argv[1] not in COMMANDS:
        print(__doc__)
        sys.exit(1)
    sys.exit(COMMANDS[sys.argv[1]](sys.argv[2:]))
