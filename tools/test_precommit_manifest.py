#!/usr/bin/env python3
"""End-to-end: a commit made through .githooks/pre-commit must leave MANIFEST.md passing
`gen_manifest.py --check` on a clean checkout (a fresh clone, or CI if you add it).

The hook runs add_frontmatter (rewrites each file's `links:` from its body), then
gen_manifest, then re-stages. gen_manifest reads the git index, so the re-stage has to
happen BEFORE it, or the manifest is built from stale links and a fresh clone calls it stale. This test pins
that ordering. Run: python3 -m unittest discover tools
"""
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
GIT = ["git", "-c", "user.name=t", "-c", "user.email=t@example.com"]


class HookKeepsManifestInSync(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = Path(tempfile.mkdtemp())
        shutil.copytree(ROOT / "tools", self.tmp / "tools", ignore=shutil.ignore_patterns("__pycache__", "test_*"))
        shutil.copytree(ROOT / ".githooks", self.tmp / ".githooks")
        self.git("init", "-q")
        self.git("config", "core.hooksPath", ".githooks")
        (self.tmp / "README.md").write_text("---\ntype: vault-root\n---\n\n# Root\n")
        self.git("add", ".")
        self.git("commit", "-q", "-m", "init")

    def tearDown(self) -> None:
        shutil.rmtree(self.tmp, ignore_errors=True)

    def git(self, *args: str, cwd: Path | None = None) -> subprocess.CompletedProcess:
        return subprocess.run([*GIT, *args], cwd=cwd or self.tmp, check=True, capture_output=True, text=True)

    def test_commit_through_the_hook_passes_ci_check_on_a_clean_clone(self) -> None:
        # index.md links to a.md in its BODY but has stale frontmatter. The hook fixes `links:`,
        # which makes a.md stop being an orphan. The committed manifest must reflect that.
        (self.tmp / "a.md").write_text("---\ntype: doc\n---\n\n# A\n")
        (self.tmp / "index.md").write_text("---\ntype: manifest\nlinks: []\n---\n\n[a](a.md)\n")
        self.git("add", "a.md", "index.md")
        self.git("commit", "-q", "-m", "add a and index")
        clone = self.tmp.parent / (self.tmp.name + "-clone")
        try:
            subprocess.run(["git", "clone", "-q", str(self.tmp), str(clone)], check=True, capture_output=True)
            check = subprocess.run(["python3", "tools/gen_manifest.py", "--check"], cwd=clone,
                                   capture_output=True, text=True)
            self.assertEqual(check.returncode, 0, check.stdout + check.stderr)
        finally:
            shutil.rmtree(clone, ignore_errors=True)


if __name__ == "__main__":
    unittest.main()
