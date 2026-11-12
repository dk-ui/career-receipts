#!/usr/bin/env python3
"""Report numbers on your CV that have no row in evidence-ledger.md.

Why this exists
---------------
evidence-ledger.md maps every claim on your CV to the file that backs it. AI
tailoring is good at writing confident numbers, and a number you can't back up in
an interview costs more than leaving it off. So this makes the ledger mechanical:
if a number appears on the CV and no ledger row carries it, it says so by name.

What counts as a claim
----------------------
The human rule is "could someone reasonably ask how you know that." The machine
proxy is "it has a digit in it," because numbers are the checkable surface of a
resume. Adjectives don't attract a follow-up question; "grew revenue 40%" does.

Never blocks
------------
Only the privacy gate may fail a commit, because a leak is the one mistake you
can't undo. A ledger that's behind is always fixable, so this reports and exits 0
unless --strict is passed. If there is no CV yet, the CV check is skipped.

Which CV
--------
career-ops/cv.md if career-ops is installed, otherwise cv.md at the vault root.
--cv PATH checks another file instead; its ledger is the evidence-ledger.md next
to it if there is one (that is how the sample vault in examples/ is checked).
"""

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LEDGER = ROOT / "evidence-ledger.md"
# The live CV only: career-ops' copy if it is installed, else the vault's own.
# Old versions in resumes/ can carry numbers you've since retired, so checking
# one proves nothing about the CV you'd actually send.
CV_CANDIDATES = [ROOT / "career-ops" / "cv.md", ROOT / "cv.md"]

# Sections whose numbers are not claims about achievement.
SKIP_HEADINGS = {"core competencies", "skills", "education", "certifications"}

# Contact details, employment dates, and degree years are verifiable elsewhere
# and are not the kind of thing an interviewer probes for evidence.
MONTHS = r"Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec"
NOISE_PATTERNS = [
    re.compile(rf"(?:{MONTHS})\w*\s+\d{{4}}"),      # Aug 2022
    re.compile(r"\b(?:19|20)\d{2}\b"),               # bare years
    re.compile(r"\b\d{3}-\d{3}-\d{4}\b"),            # phone
    re.compile(r"\b[A-Z][A-Za-z]*-?\d+(?:\.\d+)?\b"),  # names fused to digits: GPT-4, Q3, H1
    re.compile(r"\bB2B\b|\bB2C\b", re.I),        # not a quantity
    # Tenure and team size: true, low-risk, and rarely asked for proof. Flagging them
    # buries the numbers that are -- percentages, money, counts of outcomes.
    re.compile(r"\b\d+\+?\s*(?:years?|yrs?)\b", re.I),
    re.compile(r"\bteam\s+of\s+\d+\b|\b\d+[- ](?:person|people)\b", re.I),
]

# A number as it appears in prose: optional $, digits with separators, optional
# decimal, optional K/M/B/x/%/+ suffix.
NUMBER = re.compile(r"\$?\d[\d,]*(?:\.\d+)?\s?(?:%|\+|x\b|K\b|M\b|B\b)?", re.I)


def normalize(tok: str) -> str:
    """Collapse surface differences so '$1.3B', '1.3 B' and '1.3B' compare equal."""
    return re.sub(r"[\s,$+]", "", tok).lower().rstrip(".")


def strip_noise(line: str) -> str:
    for pat in NOISE_PATTERNS:
        line = pat.sub(" ", line)
    return line


def claims_from_cv(path: Path):
    """Yield (line_number, raw_line, [normalized numbers]) for claim-bearing lines."""
    heading = ""
    lines = path.read_text(encoding="utf-8").splitlines()
    start = 0
    if lines and lines[0].strip() == "---":            # skip YAML frontmatter
        for j in range(1, len(lines)):
            if lines[j].strip() == "---":
                start = j + 1
                break
    for i, raw in enumerate(lines[start:], start + 1):
        line = raw.strip()
        if line.startswith("#"):
            heading = line.lstrip("#").strip().lower()
            continue
        if heading in SKIP_HEADINGS:
            continue
        # Claims live in bullets and in the summary paragraph, not in the
        # italic company descriptor lines under each role heading.
        if not line or line.startswith("*") and line.endswith("*"):
            continue
        if line.startswith("**") and line.count("**") == 2 and ":" in line[:40]:
            continue  # contact block
        found = [normalize(m.group()) for m in NUMBER.finditer(strip_noise(line))]
        found = [f for f in found if f and any(c.isdigit() for c in f)]
        if found:
            yield i, line, sorted(set(found))


def ledger_numbers(ledger_raw: str):
    """(numbers in usable rows, numbers that appear only in 🔴 rows)."""
    usable, red = set(), set()
    for line in ledger_raw.splitlines():
        nums = {normalize(m.group()) for m in NUMBER.finditer(line)}
        if line.startswith("|") and "🔴" in line:
            red |= nums
        else:
            usable |= nums
    return usable, red - usable


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--strict", action="store_true",
                    help="exit 1 on unsourced claims (default: report and exit 0)")
    ap.add_argument("--cv", type=Path,
                    help="check this CV instead of the live one (ledger: the one beside it)")
    args = ap.parse_args()

    ledger = LEDGER
    if args.cv is not None:
        beside = args.cv.resolve().parent / "evidence-ledger.md"
        ledger = beside if beside.exists() else LEDGER

    if not ledger.exists():
        print("claims: no evidence-ledger.md, skipping")
        return 0

    ledger_raw = ledger.read_text(encoding="utf-8")
    ledger_nums, red_only = ledger_numbers(ledger_raw)
    # Table rows only, and not the legend row that defines what 🔴 means.
    gap_rows = [l for l in ledger_raw.splitlines()
                if l.startswith("|") and "🔴" in l and "**GAP**" not in l]

    if args.cv is not None:
        cv = args.cv if args.cv.exists() else None
        if cv is None:
            print(f"claims: {args.cv} not found")
            return 1
    else:
        cv = next((p for p in CV_CANDIDATES if p.exists()), None)

    missing, red_used = [], []
    for lineno, line, nums in (claims_from_cv(cv) if cv else []):
        absent = [n for n in nums if n not in ledger_nums and n not in red_only]
        if absent:
            missing.append((lineno, line, absent))
        # A 🔴 row means "no file yet". It never goes on a CV.
        red = [n for n in nums if n in red_only]
        if red:
            red_used.append((lineno, line, red))

    if cv is None:
        # No CV yet. The open-gap report below still runs, and it is the half
        # that does not need the CV.
        print("claims: no cv.md yet, skipping the number check")
    rel = cv.resolve().relative_to(ROOT) if cv and ROOT in cv.resolve().parents else cv
    for label, rows in (("assert numbers with no ledger row", missing),
                        ("use numbers whose only ledger row is 🔴", red_used)):
        if not rows:
            continue
        print(f"claims: {len(rows)} line(s) in {rel} {label}\n")
        for lineno, line, nums in rows:
            snippet = line if len(line) <= 96 else line[:93] + "..."
            print(f"  {rel}:{lineno}")
            print(f"    {'unsourced' if rows is missing else 'gap only'}: {', '.join(nums)}")
            print(f"    {snippet}\n")
    if missing or red_used:
        print("Fix: add a row to evidence-ledger.md pointing at the artifact,")
        print("     or drop the number from the CV. See that file's inclusion rule.")
    elif cv is not None:
        print(f"claims: every number in {rel} has a usable ledger row (none 🔴)")

    if gap_rows:
        print(f"\nclaims: {len(gap_rows)} ledger row(s) still marked 🔴 (claim with no artifact)")
        for row in gap_rows:
            claim = row.split("|")[1].strip() if row.count("|") >= 2 else row
            print(f"  - {claim}")

    return 1 if ((missing or red_used) and args.strict) else 0


if __name__ == "__main__":
    sys.exit(main())
