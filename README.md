<!-- template-readme -->
<!-- This is the GitHub page for the template. When you say "set me up", Claude replaces it
     with your vault's own front page. -->

# Career vault

**A proof-backed record of your working life, where every claim has a receipt.**

Hiring managers and promotion committees ask "how do you know that?" This vault means you
always have the answer. It's a private folder that Claude Code keeps organized for you: one
folder per job or project, the files that prove what you did, and an evidence ledger that
ties **every number on your CV to a file**. Use it for performance reviews, promotion cases,
brag documents, and a job search when one comes. Free, open source, and it runs on your
Claude plan.

**[See a filled-in example →](examples/sample-vault/README.md)** (a fictional operations
lead with four chapters, an evidence ledger, and a CV where every number is sourced)

## Start in three steps

**1. Get a copy.** Pick one:

- **Use this template** (green button, top right) → **choose Private** → Create. GitHub
  defaults new repos to *public*. Your vault will hold your work history, so it must be
  private. Then clone your new repo into your home folder.
- **Or clone it** into your home folder:
  ```sh
  cd ~ && git clone https://github.com/dk-ui/career-receipts.git career-vault
  ```
  Setup disconnects it from this public repo, so your vault can never be pushed here.
- **Or download the ZIP** (Code → Download ZIP), unzip it, and move the folder into your
  home folder.

Keep it in your home folder, **not** Documents, Desktop, Downloads, iCloud, OneDrive or
Dropbox: sync services can corrupt git history.

**2. Open the folder in VS Code** with the Claude Code extension.

**3. Type `set me up`.** About 15 minutes later you have a CV built from your current
resume, with every number logged in your evidence ledger and honestly labeled.

No clone at all? [SETUP-PROMPT.md](SETUP-PROMPT.md) builds the same vault from a single
prompt in an empty folder.

## Requirements

- A **Claude Pro or Max** subscription
- **VS Code** with the **Claude Code** extension (or the Claude Code CLI)
- **git** and **python3** (on a Mac, `xcode-select --install` gives you both)
- **Node.js 18.17+** only for the optional career-ops step

## How it works

- **Drop, don't sort.** Put anything in `inbox/` (old resumes, screenshots, kudos emails,
  reviews) and say "file my inbox". Claude files it, describes it, and ticks the gap it
  proves.
- **A claim with no artifact is a gap, not a fact.** Each chapter carries a status flag
  (⚪ not started · 🔴 claims only · 🟡 partial · 🟢 strong) and a gap list.
- **Every number has a status.** 🟢 sourced, 🟡 derived, 🔵 from memory, 🔴 gap. A 🔴 number
  never goes on your CV, and `tools/claims_check.py` checks that for you.
- **Gates, not good intentions.** A pre-commit check blocks Social Security, card, account
  and passport numbers from entering history. Generators keep every index current.

## Privacy

- **Your vault must be private.** Choose Private when you use the template, and keep any
  backup repo private. The vault checks that a remote is private before it pushes.
- **Never commit ID documents**: passports, licenses, SSN cards, bank or pay statements. The
  scanner reads text, not images or PDFs, so don't drop them in at all.
- Everything stays on your computer except what you choose to back up.

## Costs

Everything runs on your Claude subscription. **Never add an API key.** The vault never needs
one, and the agent is told to ask before anything that could spend money.

## Optional: job search

When you're looking, setup can install
[santifer/career-ops](https://github.com/santifer/career-ops) (MIT) inside your vault. It
scans company job boards, scores postings against your background, and tailors a CV for each
one, all from your vault's evidence. Fixes you make there sync back. Thanks to its author
for building it and releasing it openly.

## What's in here

```
.
├── START-HERE.md          plain-language guide for the vault's owner
├── CLAUDE.md              rules the agent follows
├── evidence-ledger.md     every CV claim → the file that proves it
├── inbox/                 drop zone, filed and emptied each session
├── profile/               who you are, what you're aiming for, headshots
├── chapters/              one folder per job, degree or project
├── resumes/  cover-letters/  job-search/
├── tools/                 privacy gate, generators, claims check, tests (stdlib Python)
├── .githooks/             pre-commit and pre-push gates
├── .claude/skills/        setup-vault, file-inbox, add-chapter, sync-cv, sync-career-ops
├── examples/sample-vault/ a fictional filled-in vault (removed at setup)
└── SETUP-PROMPT.md        build it from one prompt instead
```

## License

[MIT](LICENSE).
