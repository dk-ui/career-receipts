#!/usr/bin/env python3
"""Regression test: MANIFEST.md must describe what git will commit, not what is on disk.

The pre-commit hook regenerates MANIFEST.md, but CI runs `gen_manifest.py --check` on a
clean checkout. If the generator counted untracked files or read unstaged edits, every
commit made with other uncommitted work around produced a manifest that a check on a
fresh clone called stale. Run: python3 -m unittest discover tools
"""
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

GENERATOR = Path(__file__).with_name("gen_manifest.py")
README = "---\ntype: chapter-readme\nstatus: strong\n---\n\n# Chapter\n"
GIT = ["git", "-c", "user.name=t", "-c", "user.email=t@example.com"]


class ManifestMatchesGit(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = Path(tempfile.mkdtemp())
        (self.tmp / "tools").mkdir()
        shutil.copy(GENERATOR, self.tmp / "tools" / "gen_manifest.py")
        (self.tmp / "README.md").write_text(README)
        self.git("init", "-q")
        self.git("add", ".")
        self.run_tool()
        self.git("add", "MANIFEST.md")
        self.run_tool()  # MANIFEST.md counts itself once tracked, so settle it as the real repo is
        self.git("add", "MANIFEST.md")
        self.git("commit", "-q", "-m", "init")

    def tearDown(self) -> None:
        shutil.rmtree(self.tmp, ignore_errors=True)

    def git(self, *args: str) -> None:
        subprocess.run([*GIT, *args], cwd=self.tmp, check=True, capture_output=True)

    def run_tool(self, *args: str) -> subprocess.CompletedProcess:
        return subprocess.run(["python3", "tools/gen_manifest.py", *args], cwd=self.tmp,
                              capture_output=True, text=True)

    def test_untracked_file_does_not_make_the_manifest_stale(self) -> None:
        (self.tmp / "draft.md").write_text("# scratch\n")
        self.assertEqual(self.run_tool("--check").returncode, 0)

    def test_unstaged_edit_does_not_make_the_manifest_stale(self) -> None:
        (self.tmp / "README.md").write_text(README + "- [ ] a new gap\n")
        self.assertEqual(self.run_tool("--check").returncode, 0)

    def test_staging_a_new_file_does_make_it_stale(self) -> None:
        (self.tmp / "extra.md").write_text("# new\n")
        self.git("add", "extra.md")
        self.assertEqual(self.run_tool("--check").returncode, 1)

    def test_staged_edit_does_make_it_stale(self) -> None:
        (self.tmp / "README.md").write_text(README + "- [ ] staged gap\n")
        self.git("add", "README.md")
        self.assertEqual(self.run_tool("--check").returncode, 1)


if __name__ == "__main__":
    unittest.main()
