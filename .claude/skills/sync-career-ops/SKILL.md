---
name: sync-career-ops
description: Only if career-ops is installed. Two-way sync between the vault and career-ops. First pull back what happened in career-ops (fact corrections, sent cover letters, the application tracker), then rebuild career-ops/cv.md and article-digest.md from the vault, pre-fill its profile, and check every number against the ledger. Use after new work is filed, before or after a job-search session, or when the owner says "update my CV" or "sync".
---

# Sync the vault and career-ops

**Why this exists.** career-ops only trusts files *inside* its own folder (`cv.md`,
`article-digest.md`, `config/profile.yml`, `modes/_profile.md`). By its own rules it never
reads this vault. So the vault pushes a distilled copy in.

**But the owner lives in career-ops while job hunting.** That's where they fix a bullet
mid-application, send cover letters, and track where they applied. If sync only pushed, every push would erase
those fixes. So the order is always: **pull back, then push.**

If `career-ops/` doesn't exist, use `sync-cv` instead. Installing career-ops is optional
(`setup-vault` Part 2, item f).

## 0. Make sure career-ops logs corrections

Check that `career-ops/modes/_custom.md` exists (if not, `cd career-ops && node doctor.mjs
--json --init-templates`) and contains the marker `<!-- vault-sync -->`. If the marker is
missing, append this block under `## House Rules`:

```markdown
<!-- vault-sync -->
- **cv.md and article-digest.md are generated** from the owner's career vault (the parent
  folder). Edit them freely when asked, but whenever the owner corrects or adds a *fact*
  about their experience (a number, a date, a title, scope, an achievement), also append one
  line to `data/vault-corrections.md`:
  `- YYYY-MM-DD | <file> | <what changed> | <what they said, briefly>`
  Create that file if missing. Wording and tailoring for a specific posting are not facts,
  so don't log those.
<!-- /vault-sync -->
```

`_custom.md` is a user-layer file. career-ops' updater never touches it, so this survives
updates.

## 1. Pull back

**Corrections.** Read `career-ops/data/vault-corrections.md`. Apply each unapplied line to
the vault, wherever that fact belongs: a chapter README, `profile/README.md`, or
`evidence-ledger.md`. A new number they state becomes a ledger row (🔵 self-attested unless
they have a file for it). Then move those lines under an `## Applied YYYY-MM-DD` heading in
the same file, so they're never applied twice.

**Hand edits that skipped the log.** Diff `career-ops/cv.md` against
`job-search/cv-last-sync.md`, the copy of what the last sync wrote. Any fact change that isn't
in the corrections log: ask the owner whether it's real, and bring it into the vault if so. Never
let step 3 silently erase it.

**Sent cover letters.** For each tracker row in `career-ops/data/applications.md` with status
`Applied` or later, find the matching cover letter in `career-ops/output/` (filename contains
the company slug and `cover`). Copy (don't move) any that aren't in `cover-letters/` yet, as
`cover-letters/YYYY-MM-DD-<company>.pdf`, dated by the tracker row. Add each to that folder's
`index.md`.

**Tracker snapshot.** Copy `career-ops/data/applications.md` to
`job-search/applications.md`, overwriting the old snapshot. career-ops keeps its tracker out
of git, so this snapshot is its only backup. Update the counts line in
`job-search/README.md` (applied / interviewing / offers).

## 2. Read the source

- `profile/README.md`: identity, targets, deal-breakers.
- Every `chapters/*/README.md`: the story, highlights, artifacts, gaps.
- `evidence-ledger.md`: which numbers are 🟢 / 🟡 / 🔵 / 🔴.
- The newest file in `resumes/`: their own phrasing and section order. Match it unless
  they've asked for a change.
- `career-ops/examples/cv-example.md` and `career-ops/examples/article-digest-example.md`:
  the format career-ops parses.

## 3. Build `cv.md`

Follow `sync-cv` steps 2 and 3 exactly (the ledger rules, no 🔴 numbers, rephrase don't
embellish, NDA material out, fast-start mode), writing to `career-ops/cv.md` in the
example's format. If the vault already has a root `cv.md` from before career-ops was
installed, start from it, then tell the owner that `career-ops/cv.md` is the live CV from now
on and the root copy can be deleted.

## 4. Build `article-digest.md`

This is the deep proof-point file career-ops reads when it tailors a CV to a posting. Write
one section per strong highlight, using the example's format. Include the context, what they
did, the result, and the evidence line ("Source: chapter acme, dashboard screenshot
2024-q3"). In fast-start mode with no chapters yet, skip this step. career-ops treats the
file as optional.

## 5. Profile pre-fill (first sync only, or when targets change)

If `career-ops/config/profile.yml` or `career-ops/modes/_profile.md` are missing or still
template content (`node doctor.mjs --json` lists them under `missing` / `unpersonalized`),
draft them from `profile/README.md`: name, contact, location, target roles, comp range,
archetypes, deal-breakers. Follow the structure of `config/profile.example.yml` and
`modes/_profile.template.md`. **Leave `spend_tier` at `standard`** unless the owner chose
otherwise. Also set `title_filter.positive` in `portals.yml` to their target titles, if that
file exists.

## 6. Source documents

Copy (don't move) the newest resume into `career-ops/documents/cv/` and the LinkedIn PDF, if
filed, into `career-ops/documents/linkedin/`. career-ops can't read `.docx`, so for a Word
resume put a text copy there instead (`textutil -convert txt -output <dest>.txt <file>`). career-ops' own `intake` mode can then
cross-check them. Those folders are gitignored inside career-ops.

## 7. Show, then write

These files are the owner's, and career-ops treats them as the truth. **Never overwrite them
silently.**

- First sync: show a short summary of what you're writing, then write.
- Later syncs: show the **diff**: which bullets changed, which numbers appeared or
  disappeared. Get a yes before writing.

After writing, copy `career-ops/cv.md` to `job-search/cv-last-sync.md`. That's the baseline
step 1 diffs against next time, and a backup of the live CV.

## 8. Check

From the vault root:

```bash
python3 tools/claims_check.py
```

Every number on the CV should have a ledger row. For each one listed: add the row (with its
artifact), or drop the number from the CV. Also report the ledger's open 🔴 gaps, since those
are the highest-value files to go find.

Then, inside career-ops: `node doctor.mjs --json` and, if present,
`npm run cv:verify-facts`. Fix what they flag.

## 9. Save

Commit the vault side (`sync: <what came back>, cv rebuilt`), and `git push` if `origin`
exists. Don't commit inside
career-ops. Its user files are gitignored by design, which is why step 1 snapshots them here.

Tell the owner in a few lines: what came back from career-ops, what changed on the CV, any
numbers you dropped and why, and the top gap worth closing.
