"""Doc-factory form kit config: code repo paths and code branch (used only by the stamp), temp folder.

Shared defaults live here; per-machine values live in the git-ignored
.claude/local.json. No absolute paths are stored in shared files.
"""
import json
import os
import subprocess
import tempfile
from pathlib import Path

KIT_DIR = Path(__file__).resolve().parent.parent          # .claude/kit
DOC_ROOT = KIT_DIR.parent.parent                          # elitea.github.io
LOCAL_FILE = DOC_ROOT / ".claude" / "local.json"
CACHE_DIR = Path(tempfile.gettempdir()) / "doc-factory"

DEFAULTS = {
    "repos": {
        "EliteaUI": "../EliteaUI",
        "elitea-sdk": "../elitea-sdk",
        "elitea_core": "../elitea_core",
    },
    "code_branch": None,      # stored only when the user sets it (df.py cfg branch)
}


def load():
    cfg = json.loads(json.dumps(DEFAULTS))
    if LOCAL_FILE.exists():
        local = json.loads(LOCAL_FILE.read_text(encoding="utf-8"))
        cfg["repos"].update(local.get("repos", {}))
        for k in ("code_branch",):
            if k in local:
                cfg[k] = local[k]
    return cfg


def save_local(key, value):
    data = {}
    if LOCAL_FILE.exists():
        data = json.loads(LOCAL_FILE.read_text(encoding="utf-8"))
    if key.startswith("repos."):
        data.setdefault("repos", {})[key.split(".", 1)[1]] = value
    elif value is None:
        data.pop(key, None)
    else:
        data[key] = value
    LOCAL_FILE.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")


def repo_path(cfg, name):
    p = Path(cfg["repos"][name])
    return p if p.is_absolute() else (DOC_ROOT / p).resolve()


def git(repo, *args):
    r = subprocess.run(["git", "-C", str(repo), *args], capture_output=True,
                       text=True, encoding="utf-8", errors="replace")
    return r.stdout.strip() if r.returncode == 0 else None


def cache(*parts):
    p = CACHE_DIR.joinpath(*parts)
    p.parent.mkdir(parents=True, exist_ok=True)
    return p


def env_root():
    return Path(os.environ.get("CLAUDE_PROJECT_DIR") or DOC_ROOT)
