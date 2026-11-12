#!/usr/bin/env python3
"""
Structural integrity check: does every folder's index.md agree with what is on disk?

Every folder has an index.md (manifest; entries are links or `backtick` names) and a
README.md (the narrative). gen_manifest.py --check already catches links pointing at nothing. This catches the
other direction, the drift that check cannot see: a file or folder that exists but
was never registered in its folder's index.md, so an agent navigating by index
never finds it. Plus the frontmatter contract and chapter-README rules in CLAUDE.md.

Read-only. Advisory by default (exit 0); --strict exits 1 on any finding.
Scope is `git ls-files -co --exclude-standard`, so ignored paths (career-ops/,
inbox/ contents) are never walked. Run it after filing anything.
"""
import os
import re
import subprocess
import sys
from collections import defaultdict
from pathlib import PurePosixPath

# repo root = parent of tools/. Derived, not hardcoded, so this runs on a CI
# runner and from any clone path.
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

INFRA = {"index.md", "README.md", "CLAUDE.md"}
GENERATED = {"MANIFEST.md"}
# Folders not held to the README/index/frontmatter contract:
#   inbox/     a drop zone; its two files are deliberately frontmatter-free
#   examples/  the fictional sample vault, never part of the owner's record
SKIP_TOP = ("inbox", "examples")
# media/ and profile/photos/ have no README or index of their own: their files
# are listed in the parent folder's index.md (CLAUDE.md "Documentation convention").
ASSET_DIRS = {"media", "photos"}
VALID_TYPES = {"vault-root", "chapter-readme", "readme", "manifest", "doc"}
CHAPTER_STATUSES = ("strong", "partial", "none", "not-started")
TEMPLATE_README_MARKER = "<!-- template-readme -->"

# Link target allowing one level of balanced parens, e.g. "Blueprint (1).png".
LINK = re.compile(r"\]\(<?((?:[^()<>]|\([^()]*\))+)>?\)")
TICK = re.compile(r"`([^`/]+(?:\.[A-Za-z0-9]{2,5}|/))`")
FRONTMATTER = re.compile(r"\A---\n(.*?)\n---\n", re.S)

# Severity order for the report: structure first, then registration, then metadata.
ORDER = ["index-missing", "readme-missing", "corrupt-index", "indexed-entry-missing",
         "subfolder-not-indexed", "file-not-indexed", "asset-not-indexed"]


def tracked_files(root):
    out = subprocess.run(["git", "-C", root, "ls-files", "-co", "--exclude-standard"],
                         capture_output=True, text=True, check=True).stdout
    keep = []
    for f in out.split("\n"):
        if not f or "__pycache__" in f:
            continue
        if any(part.startswith(".") for part in f.split("/")[:-1]) or f.startswith("."):
            continue
        if f.split("/")[0] in SKIP_TOP:
            continue
        keep.append(f)
    return keep


def build_tree(files):
    """{dir: set(file names)}, {dir: set(subdir names)}; '.' is the root."""
    names, subdirs = defaultdict(set), defaultdict(set)
    for f in files:
        p = PurePosixPath(f)
        names[str(p.parent)].add(p.name)
        parts = p.parts[:-1]
        for i, part in enumerate(parts):
            subdirs["/".join(parts[:i]) or "."].add(part)
            names.setdefault("/".join(parts[: i + 1]), set())
    return names, subdirs


def read(root, rel):
    with open(os.path.join(root, rel), encoding="utf-8", errors="replace") as fh:
        return fh.read()


def parse_frontmatter(text):
    m = FRONTMATTER.match(text)
    if not m:
        return None
    fields = {}
    for line in m.group(1).splitlines():
        if ":" in line and not line.startswith(" "):
            key, value = line.split(":", 1)
            fields[key.strip()] = value.strip()
    return fields


def registered_entries(index_text):
    """Names an index.md registers in its own folder: links and `backtick` names."""
    found = {t.rstrip("/") for t in TICK.findall(index_text)}
    for target in LINK.findall(index_text):
        target = target.split("#")[0].strip()
        if not target or "://" in target or target.startswith(("mailto:", "..")):
            continue
        target = target[2:] if target.startswith("./") else target
        # sub/index.md or sub/ both register the subfolder `sub`
        found.add(target.rstrip("/").split("/")[0])
    return found


def asset_names(root, rel_index):
    """Files listed in an index.md, by bare name, for its media/ or photos/ folder."""
    text = read(root, rel_index)
    found = {PurePosixPath(t).name for t in TICK.findall(text)}
    found |= {PurePosixPath(t.split("#")[0]).name for t in LINK.findall(text)}
    return found


def check_folder(root, d, names, subdirs):
    rel = (lambda n: n) if d == "." else (lambda n: f"{d}/{n}")
    out = []
    if PurePosixPath(d).name in ASSET_DIRS:
        parent = str(PurePosixPath(d).parent)
        parent_index = "index.md" if parent == "." else f"{parent}/index.md"
        listed = asset_names(root, parent_index) if os.path.exists(
            os.path.join(root, parent_index)) else set()
        return [("asset-not-indexed", rel(n), f"list it in {parent_index}")
                for n in sorted(names) if not n.startswith(".") and n not in listed]
    if "README.md" not in names:
        out.append(("readme-missing", d, ""))
    if "index.md" not in names:
        out.append(("index-missing", d, ""))
        return out
    text = read(root, rel("index.md"))
    if parse_frontmatter(text) is None:
        out.append(("corrupt-index", rel("index.md"), "no frontmatter"))
    registered = registered_entries(text)
    for n in sorted(names - INFRA - GENERATED):
        if not n.startswith(".") and n not in registered:
            out.append(("file-not-indexed" if n.endswith(".md") else "asset-not-indexed", rel(n), ""))
    for s in sorted(subdirs):
        if s not in registered:
            out.append(("subfolder-not-indexed", rel(s) + "/", ""))
    for t in sorted(registered - names - subdirs - INFRA - GENERATED):
        # backtick names elsewhere in the prose (e.g. `tools/x.py`) are not
        # registrations; only report links that resolve to nothing on disk
        if f"]({t}" in text and not os.path.exists(os.path.join(root, rel(t))):
            out.append(("indexed-entry-missing", rel(t), f"linked from {rel('index.md')}"))
    return out


def check_frontmatter(root, f):
    name = PurePosixPath(f).name
    if not f.endswith(".md") or name == "CLAUDE.md" or name in GENERATED:
        return []
    text = read(root, f)
    if f == "README.md" and TEMPLATE_README_MARKER in text:
        return []  # the GitHub visitor page; setup-vault replaces it
    fm = parse_frontmatter(text)
    if fm is None:
        return [("frontmatter-missing", f, "")]
    out = [("frontmatter-field-missing", f, k) for k in ("type", "updated", "links") if k not in fm]
    kind = fm.get("type")
    if kind and kind not in VALID_TYPES:
        out.append(("frontmatter-bad-type", f, kind))
    if name == "index.md" and kind not in (None, "manifest"):
        out.append(("frontmatter-wrong-type", f, f"{kind}, expected manifest"))
    if kind == "chapter-readme":
        if fm.get("status") not in CHAPTER_STATUSES:
            out.append(("chapter-status-missing", f, str(fm.get("status"))))
        if not re.search("[\U0001F7E2\U0001F7E1\U0001F534\u26AA]", text[:1500]):
            out.append(("chapter-flag-missing", f, "no status flag near top"))
        if not re.search(r"^#+ .*gap", text, re.I | re.M):
            out.append(("chapter-gaplist-missing", f, ""))
    return out


def run(root):
    files = tracked_files(root)
    names, subdirs = build_tree(files)
    findings = []
    for d in sorted(names):
        findings += check_folder(root, d, names[d], subdirs.get(d, set()))
    for f in files:
        findings += check_frontmatter(root, f)
    findings.sort(key=lambda x: (ORDER.index(x[0]) if x[0] in ORDER else len(ORDER), x[1]))
    return findings, len(names), len(files)


def main():
    findings, n_dirs, n_files = run(ROOT)
    for kind, path, detail in findings:
        print(f"{kind:28} {path}" + (f"  ({detail})" if detail else ""))
    counts = defaultdict(int)
    for kind, _, _ in findings:
        counts[kind] += 1
    summary = ", ".join(f"{k}={v}" for k, v in counts.items()) or "clean"
    print(f"vault integrity: {summary} -- {n_dirs} folders, {n_files} files")
    return 1 if findings and "--strict" in sys.argv else 0


if __name__ == "__main__":
    sys.exit(main())
