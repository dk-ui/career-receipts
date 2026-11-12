#!/usr/bin/env python3
"""
Adds the vault's common frontmatter contract (type, updated, links, status) to
every markdown file. Idempotent. Never overwrites existing keys except `links:`,
which is derived from the body and refreshed every run. See CLAUDE.md
"Frontmatter contract". The pre-commit hook runs this; you rarely need to.
"""
import os
import re
import subprocess
from datetime import date

# repo root = parent of tools/. Derived, not hardcoded, so this runs on a CI
# runner and from any clone path.
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# examples/ holds a fictional sample vault. It must never show up in the owner's
# MANIFEST.md or counts, and its frontmatter is maintained by hand.
EXCLUDE_DIRS = {".git", "career-ops", "node_modules", "inbox", "examples"}

# A chapter is any folder directly under chapters/ -- one per job, venture,
# degree, or major project. Detected by location, so adding one needs no config.
CHAPTERS_ROOT = "chapters"

STATUS_MAP = {"🟢": "strong", "🟡": "partial", "🔴": "none", "⚪": "not-started"}

# The repo-root README.md of a fresh template is the GitHub visitor page, not
# the owner's front page. GitHub would render frontmatter as a table at the top
# of it, so it is left alone until setup-vault replaces it.
TEMPLATE_README_MARKER = "<!-- template-readme -->"

LINK_RE = re.compile(r"\[[^\]]*\]\(([^)]+)\)")

def git_updated(path):
    try:
        out = subprocess.run(
            ["git", "log", "-1", "--format=%ad", "--date=short", "--", path],
            cwd=ROOT, capture_output=True, text=True, timeout=10,
        ).stdout.strip()
        return out or date.today().isoformat()
    except Exception:
        return date.today().isoformat()

def classify_type(relpath):
    parts = relpath.split("/")
    name = parts[-1]
    dirpath = "/".join(parts[:-1])

    if name == "CLAUDE.md":
        return None  # excluded entirely

    # gen_manifest.py owns MANIFEST.md's format and rewrites the whole file. Adding
    # frontmatter here just gets stripped on the next generate -- the two tools were
    # silently fighting over this file on every commit until CI made it visible.
    if relpath == "MANIFEST.md":
        return None

    if name == "index.md":
        return "manifest"

    if name == "README.md":
        if dirpath == "":
            return "vault-root"
        if len(parts) == 3 and parts[0] == CHAPTERS_ROOT:
            return "chapter-readme"
        return "readme"

    return "doc"

def mine_status(body):
    m = re.search(r"(🟢|🟡|🔴|⚪)", body[:1500])
    return STATUS_MAP.get(m.group(1)) if m else None

def tracked_files():
    """Files git knows about. Links resolve against this, not the disk -- a link to
    a gitignored file exists on the author's machine but in no clone, and would
    pass here while failing CI."""
    return set(subprocess.run(
        ["git", "-C", ROOT, "ls-files"],
        capture_output=True, text=True, check=True).stdout.splitlines())

def extract_links(body, file_dir, tracked):
    links = set()
    for target in LINK_RE.findall(body):
        target = target.split("#")[0].strip()
        if not target or target.startswith(("http://", "https://", "mailto:")):
            continue
        abs_path = os.path.normpath(os.path.join(ROOT, file_dir, target))
        rel = os.path.relpath(abs_path, ROOT)
        if rel in tracked:
            links.add(rel)
    return sorted(links)

def replace_key(fm_body, key, value):
    """Replace a single-line frontmatter value in place. Returns (body, changed)."""
    out, changed = [], False
    for line in fm_body.split("\n"):
        if re.match(rf"^{key}:", line):
            if line != f"{key}: {value}":
                changed = True
            out.append(f"{key}: {value}")
        else:
            out.append(line)
    return "\n".join(out), changed

def split_frontmatter(text):
    if text.startswith("---\n"):
        end = text.find("\n---", 4)
        if end != -1:
            fm_body = text[4:end]
            rest = text[end + 4:]
            rest = rest[1:] if rest.startswith("\n") else rest
            return fm_body, rest, True
    return "", text, False

def existing_keys(fm_body):
    keys = set()
    for line in fm_body.split("\n"):
        m = re.match(r"^([A-Za-z_]+):", line)
        if m:
            keys.add(m.group(1))
    return keys

def fmt_list(items):
    return "[" + ", ".join(items) + "]"

def main():
    changed, skipped = [], []
    tracked = tracked_files()
    for dirpath, dirnames, filenames in os.walk(ROOT):
        dirnames[:] = [d for d in dirnames if d not in EXCLUDE_DIRS and not d.startswith(".")]
        for fn in filenames:
            if not fn.endswith(".md"):
                continue
            full = os.path.join(dirpath, fn)
            relpath = os.path.relpath(full, ROOT)
            ftype = classify_type(relpath)
            if ftype is None:
                skipped.append(relpath)
                continue

            with open(full, "r", encoding="utf-8") as f:
                text = f.read()
            if relpath == "README.md" and TEMPLATE_README_MARKER in text:
                skipped.append(relpath)
                continue

            fm_body, rest, had_fm = split_frontmatter(text)
            have = existing_keys(fm_body)
            file_dir = os.path.dirname(relpath)

            new_lines = []
            if "type" not in have:
                new_lines.append(f"type: {ftype}")
            if "updated" not in have:
                new_lines.append(f"updated: {git_updated(full)}")
            desired_links = fmt_list(extract_links(rest, file_dir, tracked))
            if "links" not in have:
                new_lines.append(f"links: {desired_links}")
            if ftype == "chapter-readme" and "status" not in have:
                status = mine_status(rest)
                if status:
                    new_lines.append(f"status: {status}")

            # links: is derived from the body, so it has to be refreshed, not just
            # inserted. Insert-only meant a link left a stale entry behind forever
            # once the body changed -- that is how a dead link reached CI.
            fm_refreshed = False
            if "links" in have:
                fm_body, fm_refreshed = replace_key(fm_body, "links", desired_links)

            if not new_lines and not fm_refreshed:
                continue

            if had_fm:
                new_fm_body = fm_body.rstrip("\n") + "\n" + "\n".join(new_lines)
                new_text = "---\n" + new_fm_body.strip("\n") + "\n---\n" + rest
            else:
                new_text = "---\n" + "\n".join(new_lines) + "\n---\n\n" + text

            with open(full, "w", encoding="utf-8") as f:
                f.write(new_text)
            changed.append(relpath)

    print(f"frontmatter added/merged: {len(changed)} files")
    print(f"skipped (generated, CLAUDE.md, template README): {len(skipped)} files")

if __name__ == "__main__":
    main()
