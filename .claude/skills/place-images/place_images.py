#!/usr/bin/env python
"""Copy screenshots into docs/img with house naming and print ready-to-paste references.

  place_images.py --page docs/<path>.mdx --feature <feature> [--names a,b,...] [--dry] <src>...

- Destination: docs/img/<page section dirs>/<feature>/ (e.g. img/integrations/toolkits/tavily/).
- Name: <feature>-<name>.<ext>, kebab-case. <name> comes from --names (same order as sources)
  or from the source basename. Existing files are never overwritten.
- Prints, per image: the markdown reference relative to the page, pixel size, and KB.
"""
import argparse
import os
import re
import shutil
import struct
import sys

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
DOCS = os.path.join(REPO, "docs")
OK_EXT = {".png", ".gif", ".svg", ".mp4", ".jpg", ".jpeg", ".webp"}


def kebab(s):
    s = re.sub(r"([a-z0-9])([A-Z])", r"\1-\2", s)
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")


def size(path):
    try:
        with open(path, "rb") as f:
            head = f.read(26)
        if head[:8] == b"\x89PNG\r\n\x1a\n":
            return struct.unpack(">II", head[16:24])
        if head[:6] in (b"GIF87a", b"GIF89a"):
            return struct.unpack("<HH", head[6:10])
    except OSError:
        pass
    return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--page", required=True)
    ap.add_argument("--feature", required=True)
    ap.add_argument("--names", default="")
    ap.add_argument("--dry", action="store_true")
    ap.add_argument("src", nargs="+")
    a = ap.parse_args()

    page = os.path.abspath(a.page)
    rel_dir = os.path.relpath(os.path.dirname(page), DOCS)
    if rel_dir.startswith(".."):
        sys.exit("--page must be under docs/")
    feature = kebab(a.feature)
    dest = os.path.join(DOCS, "img", rel_dir, feature)
    names = [n.strip() for n in a.names.split(",") if n.strip()]
    if names and len(names) != len(a.src):
        sys.exit("--names count must match sources")
    if not a.dry:
        os.makedirs(dest, exist_ok=True)
    for i, src in enumerate(a.src):
        if not os.path.isfile(src):
            print(f"MISSING {src}")
            continue
        ext = os.path.splitext(src)[1].lower()
        if ext not in OK_EXT:
            print(f"SKIP {src}: unsupported type")
            continue
        base = kebab(names[i] if names else os.path.splitext(os.path.basename(src))[0])
        if not base.startswith(feature + "-"):
            base = f"{feature}-{base}"
        target = os.path.join(dest, base + ext)
        if os.path.exists(target):
            print(f"EXISTS {os.path.relpath(target, REPO)} (not overwritten)")
        elif not a.dry:
            shutil.copy2(src, target)
        ref = os.path.relpath(target, os.path.dirname(page)).replace("\\", "/")
        dim = size(src)
        kb = os.path.getsize(src) // 1024
        warn = " LARGE" if kb > 1024 and ext != ".mp4" else ""
        print(f"{ref} | {dim[0]}x{dim[1]} | {kb} KB{warn}" if dim else f"{ref} | {kb} KB{warn}")


if __name__ == "__main__":
    main()
