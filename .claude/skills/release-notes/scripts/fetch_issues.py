#!/usr/bin/env python3
"""Fetch ELITEA issues (with sub-issues, comments and merged PRs) and write compact digests.

Raw GitHub data is cached; only short, user-facing digests are meant to be read by the model.

Usage:
  fetch_issues.py --release 2.0.8 [--brief] [--refresh] [--no-prs] SPEC [SPEC ...]
  SPEC is an issue number, or several joined with "+" to form one feature group (e.g. 6903+6904).

Output: one digest per group in /tmp/rn/<release>/digests/<group>.md, plus a one-line summary per
group (path, size, flags) on stdout.
"""
import argparse
import json
import re
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

REPO = "EliteaAI/elitea_issues"
ORG = "EliteaAI"
MAX_PRS = 3
ISSUE_BUDGET = 11000  # chars per issue digest
UI_REPOS = ("EliteaUI", "admin_ui")  # user-facing behaviour is described best here
SKIP_PR = re.compile(r"^(refactor|chore|test|ci|build|docs)\b|\bbump\b", re.I)

KEEP = re.compile(
    r"summary|purpose|user story|goal|scope|proposed|proposal|solution|requirement|functional|"
    r"acceptance|expected|ux|\bui\b|behaviou?r|out of scope|decision|what to change|enhancement|"
    r"description|actual|steps|problem|how it works|changes|update", re.I)
DROP = re.compile(
    r"current (state|implementation)|from the code|root cause|analysis|technical|implementation|"
    r"\btests?\b|testing|repos|files|architecture|api contract|back-?end|migration|nfr|"
    r"non-functional|risks|references|definition of done|related|open questions|background", re.I)
META_ROW = re.compile(r"\|\s*\**(type|area|repos?( impacted)?|primary repo|supporting repos|priority|owner|design|labels|depends on|blocks|supersedes( / refines)?|related|parent|epic|size|prs|audience|inspiration|analysed code.*|projects|backend dependency)\**\s*\|", re.I)
FLAG_WORDS = re.compile(
    r"verified|decision|scope update|supersed|instead|differs|revised|vs\. spec|changed|"
    r"out of scope|follow-?up|not implemented|only for|moved to|postpone", re.I)


def gh(args):
    r = subprocess.run(["gh", *args], capture_output=True, text=True)
    if r.returncode:
        return None
    try:
        return json.loads(r.stdout)
    except json.JSONDecodeError:
        return r.stdout


def cached(path: Path, refresh: bool, fn):
    if path.exists() and not refresh:
        return json.loads(path.read_text())
    data = fn()
    path.write_text(json.dumps(data))
    return data


def fetch_issue(n, raw: Path, refresh: bool, with_prs: bool, depth: int):
    def load():
        issue = gh(["issue", "view", str(n), "-R", REPO, "--json",
                    "number,title,body,state,milestone,labels,comments"]) or {}
        subs = gh(["api", f"repos/{REPO}/issues/{n}/sub_issues", "--jq", "[.[].number]"]) or []
        issue["sub_issues"] = subs if isinstance(subs, list) else []
        prs = []
        if with_prs:
            refs = set()
            tl = gh(["api", f"repos/{REPO}/issues/{n}/timeline", "--paginate", "--jq",
                     '[.[] | select(.event=="cross-referenced") | .source.issue '
                     '| select(.pull_request) | "\\(.repository.full_name)#\\(.number)"]'])
            if isinstance(tl, list):
                refs.update(x for x in tl if x.startswith(ORG + "/"))
            text = (issue.get("body") or "") + " ".join(c.get("body", "") for c in issue.get("comments", []))
            for repo, num in re.findall(rf"{ORG}/([\w.-]+)(?:#|/pull/)(\d+)", text):
                if repo != "elitea_issues":
                    refs.add(f"{ORG}/{repo}#{num}")
            mine = re.compile(rf"(#|EL-|issues/){n}\b")
            for ref in sorted(refs, key=lambda r: (r.split("/")[1].split("#")[0] not in UI_REPOS, r))[:10]:
                repo, num = ref.split("#")
                pr = gh(["api", f"repos/{repo}/pulls/{num}", "--jq",
                         "{title: .title, body: .body, merged: (.merged_at != null)}"])
                if not (isinstance(pr, dict) and pr.get("merged")):
                    continue
                if SKIP_PR.search(pr.get("title", "")) or not mine.search((pr.get("title") or "") + (pr.get("body") or "")):
                    continue
                pr["ref"] = ref
                prs.append(pr)
                if len(prs) >= MAX_PRS:
                    break
        issue["prs"] = prs
        return issue

    issue = cached(raw / f"{n}.json", refresh, load)
    issue["children"] = []
    if depth > 0:
        for s in issue.get("sub_issues", []):
            issue["children"].append(fetch_issue(s, raw, refresh, False, depth - 1))
    return issue


def strip_code(md: str) -> str:
    md = md or ""
    md = re.sub(r"<!--.*?-->", "", md, flags=re.S)
    md = re.sub(r"```.*?```", "[code omitted]", md, flags=re.S)
    md = re.sub(r"<img[^>]*>|!\[[^\]]*\]\([^)]*\)", "[image]", md)
    md = re.sub(r"https://github\.com/user-attachments/\S+", "[attachment]", md)
    # backticked identifiers and paths are implementation detail; keep short UI tokens like `DELETE`
    md = re.sub(r"`[^`\n]*(?:[/_()]|\.[a-z]{2,4}\b|[a-z][A-Z])[^`\n]*`", "", md)
    md = re.sub(r"\(https?://[^)]*\)", "", md)
    out = []
    for line in md.splitlines():
        s = line.strip()
        if s.startswith("|") and (len(re.sub(r"[|\s\-:]", "", s)) < 12 or META_ROW.match(s)):
            continue  # table row left almost empty after stripping
        out.append(line.rstrip())
    return re.sub(r"\n{3,}", "\n\n", "\n".join(out)).strip()


def sections(md: str):
    parts, head, buf = [], "", []
    for line in md.splitlines():
        m = re.match(r"#{1,2}\s+(.*)", line)
        if m:
            parts.append((head, "\n".join(buf).strip()))
            head, buf = m.group(1).strip(), []
        else:
            buf.append(line)
    parts.append((head, "\n".join(buf).strip()))
    return [p for p in parts if p[1] or p[0]]


def cap(s: str, n: int) -> str:
    return s if len(s) <= n else s[:n].rsplit(" ", 1)[0] + " […]"


def body_digest(body: str, limit: int) -> str:
    md = strip_code(body)
    parts = sections(md)
    if len(parts) <= 1:
        return cap(md, limit)
    kept, dropped = [], []
    for head, text in parts:
        if head and DROP.search(head) and not KEEP.search(head):
            dropped.append(head)
        elif not head or KEEP.search(head) or len(kept) < 2:
            kept.append(f"**{head}**\n{cap(text, 2600)}" if head else cap(text, 1000))
        else:
            dropped.append(head)
    out = cap("\n\n".join(kept), limit)
    if dropped:
        out += "\n\n_[skipped sections: " + "; ".join(cap(d, 40) for d in dropped[:10]) + "]_"
    return out


def comments_digest(comments, limit: int, last: int = 6) -> str:
    picked = comments[-last:]
    earlier = [c for c in comments[:-last] if FLAG_WORDS.search(c.get("body", ""))][-3:]
    out, total = [], 0
    for c in earlier + picked:
        text = cap(strip_code(c.get("body", "")), 700)
        if not text:
            continue
        line = f"- {c.get('author', {}).get('login', '?')} {c.get('createdAt', '')[:10]}: {text}"
        total += len(line)
        if total > limit:
            break
        out.append(line)
    return "\n".join(out)


def ms(i):
    return (i.get("milestone") or {}).get("title") or "-"


def flags_for(i, milestone, brief):
    f = []
    if ms(i) != milestone:
        f.append(f"milestone {ms(i)} ≠ {milestone}")
    if i.get("state") == "OPEN" and brief:
        f.append("issue still OPEN")
    later = [f"#{c['number']}→{ms(c)}" for c in i["children"] if ms(c) not in (milestone, "-")]
    if later:
        f.append("sub-issues in other milestones: " + ", ".join(later))
    if i["children"] and all(c.get("state") == "OPEN" for c in i["children"]):
        f.append("all sub-issues OPEN")
    revising = [c for c in i.get("comments", []) if re.search(
        r"vs\. spec|scope update|supersed|differs|decision|instead of|final plan|revised", c.get("body", ""), re.I)]
    if revising:
        f.append(f"{len(revising)} comment(s) revise the spec — comments override the body")
    if any(re.search(r"\bverified\b", c.get("body", ""), re.I) for c in i.get("comments", [])):
        f.append("verified on an environment")
    if any("not implemented" in c.get("body", "").lower() or "only for" in c.get("body", "").lower()
           for c in i.get("comments", [])):
        f.append("a comment limits what was implemented")
    return f


def digest(i, milestone, brief):
    lines = [f"## #{i['number']} {i.get('title', '')}",
             f"state: {i.get('state')} · milestone: {ms(i)} · labels: "
             + ", ".join(l["name"] for l in i.get("labels", []))]
    fl = flags_for(i, milestone, brief)
    if fl:
        lines.append("FLAGS: " + " | ".join(fl))
    if brief:
        lines += ["", cap(strip_code(i.get("body", "")), 900)]
        last = i.get("comments", [])[-2:]
        if last:
            lines += ["", "Comments:", comments_digest(last, 600, 2)]
        return "\n".join(lines), fl
    lines += ["", body_digest(i.get("body", ""), 4500)]
    if i.get("comments"):
        lines += ["", "### Comments (newest last)", comments_digest(i["comments"], 4500)]
    for pr in i.get("prs", []):
        lines += ["", f"### Merged PR {pr['ref']}: {pr.get('title', '')}", cap(strip_code(pr.get("body") or ""), 900)]
    head = "\n".join(lines)
    lines = []
    if i["children"]:
        # shipped first, then this release, then the rest; detail only for the first few
        kids = sorted(i["children"], key=lambda c: (c.get("state") != "CLOSED", ms(c) != milestone, c["number"]))
        detail = 8 if len(kids) <= 12 else 6
        lines += ["", f"### Sub-issues ({len(kids)}; closed and {milestone} first)"]
        for k, c in enumerate(kids):
            lines.append(f"- #{c['number']} [{c.get('state')} · {ms(c)}] {c.get('title', '')}")
            if k < detail:
                lines.append("  " + cap(strip_code(c.get("body", "")), 450).replace("\n", "\n  "))
                if c.get("comments"):
                    lines.append("  last comment: " + cap(strip_code(c["comments"][-1].get("body", "")), 250).replace("\n", " "))
            for g in c["children"][:5]:
                lines.append(f"  - #{g['number']} [{g.get('state')} · {ms(g)}] {g.get('title', '')}")
    subs = "\n".join(lines)
    room = max(ISSUE_BUDGET - len(subs), 4000)  # the sub-issue list is never cut
    if len(head) > room:
        head = head[:room].rsplit("\n", 1)[0] + "\n[…truncated — full data in the raw cache]"
    return head + ("\n" + subs if subs else ""), fl


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("specs", nargs="+")
    ap.add_argument("--release", required=True, help="e.g. 2.0.8")
    ap.add_argument("--brief", action="store_true", help="short digests for Fixed/Known issues")
    ap.add_argument("--refresh", action="store_true", help="ignore the raw cache")
    ap.add_argument("--no-prs", action="store_true")
    a = ap.parse_args()

    base = Path("/tmp/rn") / a.release
    raw, dig = base / "raw", base / "digests"
    raw.mkdir(parents=True, exist_ok=True)
    dig.mkdir(parents=True, exist_ok=True)
    milestone = f"R-{a.release}"
    groups = [s.split("+") for s in a.specs]
    ids = sorted({int(x) for g in groups for x in g})
    depth = 0 if a.brief else 2
    with ThreadPoolExecutor(8) as ex:
        issues = dict(zip(ids, ex.map(
            lambda n: fetch_issue(n, raw, a.refresh, not a.brief and not a.no_prs, depth), ids)))

    if a.brief:
        out = dig / ("brief_" + "_".join(map(str, ids[:3])) + (f"_and_{len(ids) - 3}" if len(ids) > 3 else "") + ".md")
        texts = []
        for n in sorted(ids, reverse=True):
            t, fl = digest(issues[n], milestone, True)
            texts.append(t)
            print(f"#{n}: {', '.join(fl) or 'ok'}")
        out.write_text("\n\n".join(texts))
        print(f"BRIEF {out} ({out.stat().st_size} B)")
        return
    for g in groups:
        texts, fls = [], []
        for n in g:
            t, fl = digest(issues[int(n)], milestone, False)
            texts.append(t)
            fls += [f"#{n}: {x}" for x in fl]
        out = dig / ("+".join(g) + ".md")
        out.write_text("\n\n---\n\n".join(texts))
        print(f"{'+'.join(g)}\t{out}\t{out.stat().st_size} B\t{' | '.join(fls) or 'no flags'}")


if __name__ == "__main__":
    sys.exit(main())
