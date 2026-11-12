"""Tests for vault_integrity.py, run against a throwaway git repo."""
import os
import subprocess
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import vault_integrity as vi  # noqa: E402

FM = "---\ntype: {t}\nupdated: 2026-01-01\nlinks: []\n---\n"


class IntegrityTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = self.tmp.name
        subprocess.run(["git", "init", "-q", self.root], check=True)

    def tearDown(self):
        self.tmp.cleanup()

    def write(self, rel, body):
        path = os.path.join(self.root, rel)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(body)

    def kinds(self):
        return {(k, p) for k, p, _ in vi.run(self.root)[0]}

    def healthy_root(self, index_rows=""):
        self.write("README.md", FM.format(t="vault-root") + "# root\n")
        self.write("index.md", FM.format(t="manifest") + "| [`README.md`](README.md) | x |\n" + index_rows)

    def test_clean_vault_has_no_findings(self):
        self.healthy_root()
        self.assertEqual(self.kinds(), set())

    def test_unregistered_file_and_subfolder_are_reported(self):
        self.healthy_root()
        self.write("note.md", FM.format(t="doc"))
        self.write("sub/README.md", FM.format(t="readme"))
        self.write("sub/index.md", FM.format(t="manifest") + "[`README.md`](README.md)\n")
        self.assertEqual(self.kinds(), {("file-not-indexed", "note.md"),
                                        ("subfolder-not-indexed", "sub/")})

    def test_missing_index_and_readme(self):
        self.healthy_root("| [sub/](sub/) | x |\n")
        self.write("sub/a.py", "")
        self.assertEqual(self.kinds(), {("index-missing", "sub"), ("readme-missing", "sub")})

    def test_backtick_names_and_paren_links_count_as_registered(self):
        self.healthy_root("| `a.png` | x |\n| [`b (1).png`](b (1).png) | x |\n| `sub/` | x |\n")
        self.write("a.png", "")
        self.write("b (1).png", "")
        self.write("sub/README.md", FM.format(t="readme"))
        self.write("sub/index.md", FM.format(t="manifest") + "[`README.md`](README.md)\n")
        self.assertEqual(self.kinds(), set())

    def test_dead_link_is_reported(self):
        self.healthy_root("| [`gone.md`](gone.md) | x |\n")
        self.assertEqual(self.kinds(), {("indexed-entry-missing", "gone.md")})

    def test_frontmatter_and_chapter_rules(self):
        self.healthy_root("| [`a.md`](a.md) | x |\n| [ch/](ch/) | x |\n")
        self.write("a.md", "# no frontmatter\n")
        self.write("ch/README.md", FM.format(t="chapter-readme") + "# ch\n")
        self.write("ch/index.md", FM.format(t="manifest") + "[`README.md`](README.md)\n")
        found = self.kinds()
        self.assertIn(("frontmatter-missing", "a.md"), found)
        self.assertIn(("chapter-status-missing", "ch/README.md"), found)
        self.assertIn(("chapter-flag-missing", "ch/README.md"), found)
        self.assertIn(("chapter-gaplist-missing", "ch/README.md"), found)

    def test_media_files_are_registered_in_the_parent_index(self):
        self.healthy_root("| [ch/](ch/) | x |\n")
        self.write("ch/README.md", FM.format(t="readme"))
        self.write("ch/index.md", FM.format(t="manifest") + "[`README.md`](README.md)\n"
                   "| [`a.png`](media/a.png) | x |\n")
        self.write("ch/media/a.png", "")
        self.write("ch/media/b.png", "")
        self.assertEqual(self.kinds(), {("asset-not-indexed", "ch/media/b.png")})

    def test_inbox_and_examples_are_out_of_scope(self):
        self.healthy_root("| `inbox/` | x |\n| `examples/` | x |\n")
        self.write("inbox/README.md", "# no frontmatter, by design\n")
        self.write("examples/sample/notes.md", "# not the owner's record\n")
        self.assertEqual(self.kinds(), set())

    def test_template_readme_is_exempt_from_frontmatter(self):
        self.write("README.md", "<!-- template-readme -->\n# visitor page\n")
        self.write("index.md", FM.format(t="manifest") + "| [`README.md`](README.md) | x |\n")
        self.assertEqual(self.kinds(), set())

    def test_not_started_chapter_is_valid(self):
        self.healthy_root("| [ch/](ch/) | x |\n")
        self.write("ch/README.md", "---\ntype: chapter-readme\nupdated: 2026-01-01\nlinks: []\n"
                   "status: not-started\n---\n**Status: \u26aa not started**\n## Gaps\n")
        self.write("ch/index.md", FM.format(t="manifest") + "[`README.md`](README.md)\n")
        self.assertEqual(self.kinds(), set())

if __name__ == "__main__":
    unittest.main()
