"""PreToolUse guard (allow-list). Exit 2 + one stderr line blocks the call.

File tools (Write/Edit/...) may write only to WRITE_ALLOW places (plus the temp
cache). Shell commands may change files only inside the temp cache; for any
other place use the file tools, which this guard checks exactly.

Known limits (plain-text check of shell commands): a path hidden in a variable
or wildcard, or a script that writes without naming its target, is not caught.
Claude Code's own permission prompt still applies to those.
"""
import json
import re
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "lib"))
import config as C  # noqa: E402

# Doc-repo places Claude may write with file tools (repo-relative, lowercase).
WRITE_ALLOW = [
    "docs/",                 # pages, docs.json, img (blocked while the setup lock is on)
    ".claude/kit/",
    ".claude/rules/",
    ".claude/skills/",
    ".claude/agents/",
    "claude.md",
    ".gitignore",
    ".claude/settings.json",
]
# Never written by Claude, even inside allowed places.
DENY = [
    "docs/styleguides/",
    "docs/archive/",
    "docs/mintlify.schema.json",
    ".claude/skills/release-notes/",
    ".claude/agents/rn-drafter.md",
    ".claude/local.json",    # user-only; changed via df.py cfg
]
# Allowed, but the user must confirm (they control the kit's own protection).
ASK = [".claude/settings.json", ".claude/kit/hooks/", ".claude/kit/lib/config.py", ".gitignore"]

GIT_USER_ONLY = {"pull", "fetch", "checkout", "switch", "merge", "rebase", "commit", "push"}
GIT_READ = {"grep", "show", "log", "diff", "status", "rev-parse", "ls-tree", "ls-files", "cat-file",
            "blame", "branch", "for-each-ref", "merge-base", "rev-list", "describe", "shortlog",
            "check-ignore", "config", "remote", "tag", "stash", "name-rev", "show-ref", "help", "version"}
GIT_OPTS_WITH_VALUE = {"-c", "-C", "--git-dir", "--work-tree", "--namespace", "--exec-path"}
OTHER_BLOCKED = [
    (r"df\.py\s+cfg\s+lock\s+off", "unlocking (cfg lock off)"),
    (r"\bgh\s+pr\s+(create|merge)\b", "gh pr create/merge"),
]
WRITE_VERBS = re.compile(
    r"(\bsed\s+-i|\brm\b|\bmv\b|\bcp\b|\btee\b|>|\btouch\b|\bmkdir\b|\brmdir\b|\bunzip\b|\btar\s+-?x"
    r"|Set-Content|Add-Content|Out-File|Remove-Item|Move-Item|Copy-Item|Rename-Item|New-Item|Expand-Archive)", re.I)
PY_WRITE = re.compile(r"\bpython[0-9.]*\b.*\.(write|write_text|write_bytes|unlink|rename|replace|rmtree|mkdir)\b"
                      r"|open\([^)]*['\"][wax]", re.I)
INSTALLERS = re.compile(
    r"\b(npm|pnpm|yarn|npx|bun|poetry|pipenv|make)\b|\bpip[0-9.]*\s+install\b|\bpython[0-9.]*\s+-m\s+pip\b"
    r"|\buv\s+(pip|sync|add|remove|lock)\b", re.I)
HARMLESS_REDIRECTS = re.compile(r"\d?>\s*(/dev/null|\$null|nul)\b|\d?>&\d|\|\s*Out-Null", re.I)
# df.py writes only to the temp cache and .claude/local.json (via cfg); it is the kit's own tool.
KIT_SCRIPT = re.compile(r"^\s*(cd\s+\S+\s*&&\s*)?python[0-9.]*\s+\S*\.claude[/\\]kit[/\\]df\.py\b", re.I)


def norm(p):
    return str(p).replace("\\", "/").rstrip("/").lower()


TEMP_ROOTS = {norm(C.CACHE_DIR)}
TEMP_ROOTS.add(norm(Path(tempfile.gettempdir()).resolve() / "doc-factory"))
# Claude's own memory notes for this workspace (~/.claude/projects/<workspace>/memory/). File tools only.
MEMORY_ROOT = norm(Path.home() / ".claude" / "projects")


def is_memory(absp):
    return absp.startswith(MEMORY_ROOT + "/") and "/memory/" in absp[len(MEMORY_ROOT):] and absp.endswith(".md")


def rel(path):
    p = norm(Path(path).resolve()) if path else ""
    r = norm(C.DOC_ROOT)
    return p[len(r) + 1:] if p.startswith(r + "/") else None, p


def under(p, prefixes):
    return next((x for x in prefixes if p == x.rstrip("/") or (x.endswith("/") and p.startswith(x))), None)


def ask(reason):
    print(json.dumps({"hookSpecificOutput": {
        "hookEventName": "PreToolUse", "permissionDecision": "ask",
        "permissionDecisionReason": f"doc-factory guard: {reason}"}}))
    sys.exit(0)


def check_file(path, lock):
    r, absp = rel(path)
    if any(absp == t or absp.startswith(t + "/") for t in TEMP_ROOTS) or is_memory(absp):
        return None
    if r is None:
        return f"writing outside the doc repo is not allowed ({absp or 'no path'})"
    hit = under(r, DENY)
    if hit:
        return f"protected path: {hit}"
    if not under(r, WRITE_ALLOW):
        return f"{r} is not on the kit's write list"
    if lock and r.startswith("docs/"):
        return "setup lock is on (docs/ is read-only; user says 'unlock')"
    if under(r, ASK):
        ask(f"{r} controls the kit's protection; confirm this edit")
    return None


def git_calls(cmd):
    """Yield (subcommand, args). Only the word after `git` and its global options counts."""
    for seg in re.split(r"&&|\|\||[;|\n]|\$\(|`", cmd):
        toks = [t.strip("\"'") for t in re.findall(r'"[^"]*"|\'[^\']*\'|\S+', seg)]
        for i, t in enumerate(toks):
            if Path(t.replace("\\", "/")).name.lower() not in ("git", "git.exe"):
                continue
            j = i + 1
            while j < len(toks) and toks[j].startswith("-"):
                opt = toks[j].split("=", 1)[0]
                j += 2 if (opt in GIT_OPTS_WITH_VALUE and "=" not in toks[j]) else 1
            if j < len(toks):
                yield toks[j].lower(), [a.lower() for a in toks[j + 1:]]
            break


def git_read_only(sub, args):
    if sub not in GIT_READ:
        return False
    if sub == "stash":
        return bool(args) and args[0] in ("list", "show")
    if sub == "branch":
        return not any(a in ("-d", "-m", "-f", "-c", "--delete", "--move", "--force", "--copy")
                       or a.startswith("--set-upstream") for a in args)
    if sub == "tag":
        return not args or any(a in ("-l", "--list", "-n") for a in args)
    if sub == "remote":
        return not args or args[0] in ("-v", "show", "get-url")
    if sub == "config":
        return any(a in ("--get", "--list", "-l", "--get-all") for a in args)
    return True


def check_shell(cmd):
    for pat, label in OTHER_BLOCKED:
        if re.search(pat, cmd, re.I):
            return f"{label} is done by the user only, in their own terminal"
    for sub, args in git_calls(cmd):
        if sub in GIT_USER_ONLY:
            return f"git {sub} is done by the user only, in their own terminal"
        if not git_read_only(sub, args):
            return f"git {sub} changes a repo; only reading git commands are allowed"
    if KIT_SCRIPT.search(cmd):
        return None
    unquoted = HARMLESS_REDIRECTS.sub(" ", re.sub(r'"[^"]*"|\'[^\']*\'', " ", cmd))
    if INSTALLERS.search(unquoted):
        return "package and build tools are not allowed (they change files)"
    if WRITE_VERBS.search(unquoted) or PY_WRITE.search(cmd):
        low = norm(cmd)
        temp_named = any(t in low for t in TEMP_ROOTS) or re.search(r"(\$temp|\$env:temp|%temp%|(?<![\w.])/tmp)[/]doc-factory", low)
        if not temp_named:
            return "shell commands may write only inside the temp folder (doc-factory); use Write/Edit for other places"
    return None


def main():
    try:
        data = json.load(sys.stdin)
    except ValueError:
        print("doc-factory guard: unreadable hook input", file=sys.stderr)
        sys.exit(1)  # non-blocking error; Claude Code shows it, call proceeds
    tool = data.get("tool_name", "")
    ti = data.get("tool_input", {}) or {}
    reason = None
    if tool in ("Write", "Edit", "MultiEdit", "NotebookEdit"):
        reason = check_file(ti.get("file_path") or ti.get("notebook_path") or "", bool(C.load().get("setup_lock")))
    elif tool in ("Bash", "PowerShell"):
        reason = check_shell(ti.get("command", ""))
    if reason:
        print(f"Blocked by doc-factory guard: {reason}", file=sys.stderr)
        sys.exit(2)
    sys.exit(0)


if __name__ == "__main__":
    main()
