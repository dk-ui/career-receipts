# Security

career-receipts holds people's work history, so a privacy flaw matters more here than most.

## What counts

- The privacy check (`tools/privacy_scan.py`) letting an ID, card or account number through
- Any path where a vault could be pushed to a public repo or a remote it shouldn't reach
- Any instruction in `.claude/skills/` or `CLAUDE.md` that could make Claude share,
  publish or send something without the owner's yes

## How to report

Use GitHub's private reporting: the **Security** tab of this repo → **Report a
vulnerability**. Please don't open a public issue, and never include real personal data.
Describe the pattern with made-up values instead.
