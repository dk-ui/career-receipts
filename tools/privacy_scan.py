#!/usr/bin/env python3
"""Blocking privacy gate for the vault.

The ONLY vault tool allowed to fail a commit. Once a government ID or an account
number is in git history it stays there until someone rewrites history, so it has
to be caught before the commit exists, not after.

What it catches (in any tracked text file: .md .txt .csv .tsv .json .yml):
  - US Social Security numbers (123-45-6789)
  - payment card numbers (13-19 digits that pass the Luhn check)
  - labeled account / routing / passport / license / student-ID numbers
  - masked or last-four card/account forms (****1234, card ending in 1234)
  - date of birth written next to a "DOB" / "date of birth" label

What it can't catch: anything inside a PDF or an image. A transcript scan or a
photo of a passport is invisible to it. That is why CLAUDE.md says those never
get filed at all.

Modes:
  --staged   scan what is staged (pre-commit hook)
  --all      scan every tracked file

Exit 0 clean, 1 on any violation.

Escape hatch: put `privacy-scan: allow` on a line to exempt that line, with a note
saying why. Whole-file exemptions live in ALLOWLIST and are reserved for the
documents that have to quote the patterns they forbid.
"""

import argparse
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ALLOWLIST = {"CLAUDE.md", "tools/privacy_scan.py"}
PRAGMA = "privacy-scan: allow"
TEXT_EXTS = {".md", ".txt", ".csv", ".tsv", ".json", ".yml", ".yaml"}

# \b matters: without it, a label hiding inside an ordinary word ("protein",
# "basin", "handled") followed by a number was reported as an ID.
LABEL_ID = r"\b(?:acct|account|routing|aba|iban|passport|driver'?s?\s*licen[cs]e|dl|student\s*id|member\s*id|ssn|sin|tax\s*id|ein|itin)"
RULES = [
    (re.compile(r"\b\d{3}-\d{2}-\d{4}\b"), "looks like a Social Security number"),
    (re.compile(LABEL_ID + r"\s*(?:no\.?|num(?:ber)?|#)?\s*[:#]?\s*[A-Z]{0,3}\d[\d\s-]{4,}", re.I),
     "labeled ID or account number"),
    (re.compile(r"(?:x{3,}|\*{3,}|·{3,}|•{3,})\s*\d{3,}", re.I), "masked card or account number"),
    (re.compile(r"\b(?:card|account|acct|visa|mastercard|amex)\b[^.\n]{0,20}?\bending\s+(?:in\s+)?\d{4}\b", re.I),
     "card or account last four"),
    (re.compile(r"\b(?:dob|date\s+of\s+birth|born\s+on)\s*[:\-]?\s*\S*\d", re.I), "date of birth"),
]
CARD = re.compile(r"\b(?:\d[ -]?){13,19}\b")


def luhn_ok(digits: str) -> bool:
    total, alt = 0, False
    for ch in reversed(digits):
        d = int(ch)
        if alt:
            d = d * 2 - 9 if d > 4 else d * 2
        total, alt = total + d, not alt
    return total % 10 == 0


def scan_text(path: str, text: str) -> list[tuple[str, int, str]]:
    hits = []
    for n, line in enumerate(text.splitlines(), 1):
        if PRAGMA in line:
            continue
        for pat, why in RULES:
            if pat.search(line):
                hits.append((path, n, why))
        for m in CARD.finditer(line):
            digits = re.sub(r"\D", "", m.group())
            if 13 <= len(digits) <= 19 and luhn_ok(digits) and len(set(digits)) > 1:
                hits.append((path, n, "looks like a payment card number"))
    return hits


def git(*args: str) -> bytes:
    return subprocess.run(["git", "-C", str(ROOT), *args],
                          capture_output=True, check=True).stdout


def decode(raw: bytes) -> str:
    # A stray non-UTF-8 byte must not crash the gate: a crash here reads as
    # "commit blocked" with no reason given.
    return raw.decode("utf-8", errors="replace")


def candidates(staged: bool) -> list[tuple[str, str]]:
    # -z: without it git quotes paths with spaces or non-ASCII characters
    # ("r\303\251sum\303\251.md"), and the quoted name matches no file.
    if staged:
        listing = git("diff", "--cached", "--name-only", "--diff-filter=ACM", "-z")
        read = lambda p: decode(git("show", f":{p}"))
    else:
        listing = git("ls-files", "-z")
        read = lambda p: (ROOT / p).read_text(encoding="utf-8", errors="replace")
    out = []
    for p in filter(None, decode(listing).split("\0")):
        if p in ALLOWLIST or Path(p).suffix.lower() not in TEXT_EXTS:
            continue
        try:
            out.append((p, read(p)))
        except (subprocess.CalledProcessError, OSError):
            continue
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    mode = ap.add_mutually_exclusive_group(required=True)
    mode.add_argument("--staged", action="store_true")
    mode.add_argument("--all", action="store_true")
    args = ap.parse_args()

    hits = [h for path, text in candidates(args.staged) for h in scan_text(path, text)]
    if not hits:
        print("privacy scan: clean")
        return 0
    print(f"\nPRIVACY GATE: {len(hits)} finding(s). Nothing was committed.\n", file=sys.stderr)
    for path, n, why in hits:
        # Never echo the matched text: the finding itself is the sensitive part.
        print(f"  {path}:{n}  {why}", file=sys.stderr)
    print("\nRemove the number from the file (keep only what a CV needs), then commit again.",
          file=sys.stderr)
    return 1


if __name__ == "__main__":
    sys.exit(main())
