---
name: file-inbox
description: File everything in inbox/ (or a file or photo the owner shares in chat) to its real home in the vault, update that folder's README and index, tick any gaps it closes, delete the original, and commit. Use whenever inbox/ is not empty, or the owner says "file my inbox", "I dropped some files", or shares a document or image.
---

# File the inbox

The promise to the owner: **they never have to know which folder something goes in, and the
vault never drifts because a file arrived without its paperwork.**

List `inbox/` (including subfolders). For **each** file:

## 1. Identify it

Open it. Read the text, or look at the image. For `.docx`/`.pages`/`.rtf` use
`textutil -convert txt -stdout <file>`. Work out:
- **What it is.** Resume, cover letter, headshot, work screenshot, offer letter, review,
  certificate, LinkedIn export, reference letter, portfolio piece.
- **Which chapter it belongs to.** Use dates, company names and logos. If no chapter fits,
  create one with `add-chapter`.
- **What it proves.** Which claim or gap-list item does it back?

Ask the owner **at most one question per batch**, and only when a wrong guess would be
expensive, like a misdated job or a confidential file. Otherwise make your best call and say
what you assumed.

## 2. Screen it

Before filing, check the rules in CLAUDE.md "Privacy":
- **ID documents and statements** (passport, license, SSN card, bank or pay statement,
  transcript with a student ID): don't file. Extract only what a CV needs into the chapter
  or `profile/` README, then tell the owner you left the original out and why.
- **Employer-internal or NDA material:** file it, but mark it confidential in the chapter
  README.
- **Other people's personal details** in references or reviews: keep them, but flag in the
  README that those files can't be quoted externally without the person's OK.

## 3. File it

| It is | Goes to |
|-------|---------|
| Resume (any version) | `resumes/YYYY-MM-<short-label>.<ext>`, dated by the file's content, not today |
| Cover letter | `cover-letters/YYYY-MM-DD-<company>.<ext>` |
| Headshot / personal photo | `profile/photos/<descriptive-name>.<ext>` |
| LinkedIn PDF, bio, certifications, references | `profile/` |
| Work screenshot, sample, deck, case study, award, review | `chapters/<slug>/` (images and videos in `media/`) |

Videos are gitignored (too large for history). File them anyway, describe them in the README,
and tell the owner their only backup is a disk backup (Time Machine or similar). If one is also hosted online, record
the link.

Use descriptive lowercase-hyphenated names. Never overwrite. If the name is taken, add `-2`.
Move with plain `mv`. Inbox files are untracked, so `git mv` won't work.

**Text matters more than the file.** For every artifact, write one or two lines in the
destination README about what it shows: "Before/after of the checkout flow; conversion went
from X to Y per the dashboard in `media/2024-q3-dashboard.png`." A screenshot nobody wrote
down is one nobody will find again.

## 4. Update the paperwork, in the same change

- Destination `index.md`: add a line for the new file.
- Destination `README.md`: what it shows. **Tick any gap it closes, and re-judge the status
  flag.** For example, 🔴 → 🟡 when the first real artifact lands.
- `evidence-ledger.md`: if it backs a number or a superlative the owner uses, add or update
  the row and set its status.
- A new **resume version**: note in `resumes/README.md` whether it changes what the live CV
  should say. If it does, offer `sync-cv` (or `sync-career-ops` if career-ops is installed).

## 5. Clean up and save

- Delete the original from `inbox/`. **The inbox should be empty when you finish.** If you
  have to leave something (waiting on the owner's answer), say so.
- Run `python3 tools/vault_integrity.py` and fix anything it reports about what you just
  filed (usually a file missing from an `index.md`).
- `git add` the files you filed and the docs you changed, then commit:
  `file: <what> → <where>`. If the privacy gate blocks, fix the content and retry. Never
  `--no-verify`. If a private `origin` exists, `git push`.

## 6. Report

Tell the owner, in a few lines: what got filed where, which gaps closed, what you left out
and why, and any question you still need answered.
