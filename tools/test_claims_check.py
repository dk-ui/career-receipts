"""Tests for claims_check.py: unsourced numbers and 🔴-only numbers are reported.

Run: python3 -m unittest discover tools
"""
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

TOOL = Path(__file__).with_name("claims_check.py")
LEDGER = """| Claim | Evidence | Status |
|---|---|---|
| Cut onboarding 40% | dashboard.png | 🟢 |
| Shrink down 15% | no file yet | 🔴 |
"""


def run(cv_body: str) -> subprocess.CompletedProcess:
    with tempfile.TemporaryDirectory() as tmp:
        (Path(tmp) / "evidence-ledger.md").write_text(LEDGER, encoding="utf-8")
        cv = Path(tmp) / "cv.md"
        cv.write_text("# Someone\n\n## Experience\n\n" + cv_body, encoding="utf-8")
        return subprocess.run([sys.executable, str(TOOL), "--cv", str(cv), "--strict"],
                              capture_output=True, text=True)


class ClaimsCheck(unittest.TestCase):
    def test_sourced_number_passes(self):
        self.assertEqual(run("- Cut onboarding 40% in Q3 2024.\n").returncode, 0)

    def test_unsourced_number_is_reported(self):
        r = run("- Grew signups 77%.\n")
        self.assertEqual(r.returncode, 1)
        self.assertIn("77%", r.stdout)

    def test_gap_only_number_is_reported(self):
        r = run("- Cut shrink 15%.\n")
        self.assertEqual(r.returncode, 1)
        self.assertIn("gap only: 15%", r.stdout)

    def test_skills_and_education_are_not_claims(self):
        self.assertEqual(run("## Skills\n\nSQL, 10 years of Excel\n\n## Education\n\nB.S., 2016\n").returncode, 0)


if __name__ == "__main__":
    unittest.main()
