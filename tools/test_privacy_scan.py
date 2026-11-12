"""Tests for privacy_scan.py: what it must block, and what it must let through.

A gate that cries wolf gets bypassed with --no-verify, which takes the real rules
down with it, so the false-positive cases matter as much as the hits.
Run: python3 -m unittest discover tools
"""
import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import privacy_scan as ps  # noqa: E402


def flagged(line: str) -> bool:
    return bool(ps.scan_text("x.md", line))


class Blocks(unittest.TestCase):
    def test_ssn(self):
        self.assertTrue(flagged("SSN 123-45-6789"))  # privacy-scan: allow (test fixture)

    def test_card_passing_luhn(self):
        self.assertTrue(flagged("card 4111 1111 1111 1111"))  # privacy-scan: allow (test fixture)

    def test_labeled_numbers(self):
        for line in ("acct # 12345678", "Passport no. X1234567", "student ID: 20190042"):  # privacy-scan: allow (test fixture)
            self.assertTrue(flagged(line), line)

    def test_masked_and_last_four(self):
        self.assertTrue(flagged("Visa ending in 4242"))  # privacy-scan: allow (test fixture)
        self.assertTrue(flagged("account ****1234"))  # privacy-scan: allow (test fixture)

    def test_date_of_birth(self):
        self.assertTrue(flagged("DOB: 04/12/1990"))  # privacy-scan: allow (test fixture)


class LetsThrough(unittest.TestCase):
    def test_ordinary_career_numbers(self):
        for line in ("Cut onboarding time 40%", "Managed a $1.2M budget",
                     "handled 12,000 orders a week", "a 16-digit order ref 1234567890123456",
                     "fiscal year ending 2024", "protein 120000 units", "Call 614-555-0142"):
            self.assertFalse(flagged(line), line)

    def test_pragma_exempts_a_line(self):
        self.assertFalse(flagged("SSN 123-45-6789  privacy-scan: allow (docs)"))  # privacy-scan: allow


if __name__ == "__main__":
    unittest.main()
