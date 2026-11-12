# CLAUDE.md — career vault

Rules for any agent working in this folder. Read this first. The person who owns this vault
is the **owner**. Their name, current role and goals live in `profile/README.md`. Read that
before doing anything for them.

## First run

If `profile/README.md` still says `status: not-set-up`, the owner hasn't been onboarded.
Run the `setup-vault` skill before anything else. They may just say "set me up", "start", or
"what do I do". When they say **"what's next"**, run its Part 2, one item per session.

## What this is

A private, local record of the owner's working life: every job, project and degree, the
artifacts that prove what they did, and the photos and files that go with them. It's what
they reach for at review time, for a promotion case, for a brag document, and for a job
search when one comes. **This folder is the source of truth.** Everything else reads from it:

```
career-vault/            ← you are here. Raw, complete, private.
   ├──→ cv.md            the live CV, rebuilt from the vault by `sync-cv`
   └──→ career-ops/      optional job-search engine (its own git repo, cloned inside,
                         gitignored). If installed, its cv.md becomes the live CV.
```

Anything downstream gets a distilled copy and never writes back silently. If career-ops is
installed, the owner spends a lot of time in it, so `sync-career-ops` runs both ways. It
first **pulls back** fact corrections (career-ops logs them to `data/vault-corrections.md`),
sent cover letters and the tracker, then **pushes** a rebuilt CV. Never push without
pulling first, or their fixes get erased.

## Layout

| Path | What lives there |
|------|------------------|
| `inbox/` | Drop zone. Anything the owner drops gets filed in the same session (`file-inbox` skill) |
| `profile/` | Who they are and what they want: bio, headshots (`profile/photos/`), links, goals, references, certifications |
| `chapters/<slug>/` | One folder per job, venture, degree, freelance stint or major project (`add-chapter` skill) |
| `chapters/<slug>/media/` | Screenshots, photos and work samples for that chapter |
| `evidence-ledger.md` | Every claim on the CV, pointing at the file that proves it |
| `cv.md` | The live CV, built by `sync-cv`. Created on the first sync. If career-ops is installed, the live CV is `career-ops/cv.md` instead |
| `resumes/` | Every past resume version, dated. History, not the working copy |
| `cover-letters/` | Every letter sent, named `YYYY-MM-DD-company.ext` |
| `job-search/` | `cv-last-sync.md` (the CV as last built), plus career-ops' tracker snapshot if installed |
| `MANIFEST.md` | Generated map of the whole vault. **Read this first when orienting**, never hand-edit it |
| `tools/` | The scripts behind the gates below, and their tests |
| `examples/` | A **fictional** filled-in sample vault, for showing the owner the finished state. Not their data: never read it as theirs, never file into it. `setup-vault` offers to delete it |

## Documentation convention

- **Every folder gets `README.md` and `index.md`.** `README.md` is the story: what this is,
  what's strong, what's missing. `index.md` is a terse manifest, one line per file or
  subfolder with a link. Read `index.md` first when navigating. A new folder gets both in the
  same change. The only exception is `media/` and `profile/photos/`: their files are listed in
  the parent's `index.md`.
- **Chapter READMEs** carry a status flag at the top (⚪ not started, 🔴 claims but no
  files yet, 🟡 partial, 🟢 strong) and a **gap list** of `- [ ]` items. A new chapter is
  ⚪. It moves to 🔴 once it has claims in its gap list, and up from there as files land.
  Present status as progress, never as a grade. **A claim with no artifact is a gap, not
  a fact.** When a filed artifact closes a gap, tick it and re-judge the flag in the same
  change. Otherwise the gap list stops being true.
- **Name files descriptively**, not what the camera or download called them:
  `2024-q3-checkout-redesign-before-after.png`, not `IMG_4471.png`.
- **Numbers need a source.** No figure goes into a CV, review, cover letter, or interview
  answer unless a file in this vault backs it and `evidence-ledger.md` points at that file.
  If the owner remembers a number but has no document, it goes in the ledger as 🔵
  self-attested. It isn't hidden, and it isn't treated as proven.

## Frontmatter contract

Every `.md` file except `CLAUDE.md`, `MANIFEST.md` and the two `inbox/` files starts with:

```yaml
---
type: vault-root | chapter-readme | readme | manifest | doc
updated: YYYY-MM-DD
links: [relative/path.md]    # derived from the body; tools refresh it, don't hand-edit
status: strong | partial | none | not-started   # chapter-readme only
---
```

You don't need to write this by hand. The pre-commit hook fills it in. To refresh mid-session:
`python3 tools/add_frontmatter.py && python3 tools/gen_manifest.py`. `examples/` is outside
the tools' scope. A root `README.md` containing `<!-- template-readme -->` is the template's
GitHub page, also skipped; `setup-vault` replaces it with the owner's front page.

## Saving work (git)

Git here is the owner's undo button. **Commit at the end of every task** that changed
files, with a plain message (`file: offer letter and screenshots for Acme chapter`). The
owner shouldn't have to think about git.

The only remote this vault may ever have is the owner's own **private** GitHub repo. Before
adding, changing or pushing to a remote, confirm with
`gh repo view --json visibility -q .visibility` that it prints `PRIVATE`. A vault cloned from
the public template starts with `origin` pointing at that template: `setup-vault` renames it
to `template`, and the pre-push hook refuses to push there. Never push anywhere else. If a
private `origin` exists, `git push` at the end of each session.

## Gates

The pre-commit hook (`.githooks/pre-commit`) runs three things. Only the first can fail.
A pre-push hook re-runs the privacy scan on the whole tree, and refuses any remote that isn't
private, before anything leaves the machine.

1. **`tools/privacy_scan.py --staged`** blocks the commit. It catches Social Security numbers,
   card numbers, masked or last-four card and account numbers, labeled account, passport,
   license and student-ID numbers, and dates of birth. A leak is the only mistake here you
   can't undo by editing a file later. **Fix the content. Never use `--no-verify`.** To exempt
   a line that has to quote a pattern, add `privacy-scan: allow` to it with a reason.
2. **Generators** (`add_frontmatter.py`, `gen_manifest.py`) keep frontmatter and
   `MANIFEST.md` current. They never block.
3. **`tools/claims_check.py`** lists numbers on the live CV that have no ledger row, or
   whose only row is 🔴. It runs when `cv.md` or the ledger is staged, and never blocks.
   Run it after every sync and before the owner sends anything with numbers in it.

`tools/vault_integrity.py` is advisory and not in the hook: it reports files on disk that no
`index.md` registers, missing README/index pairs, and frontmatter breaks. Run it after filing.
`python3 -m unittest discover tools` runs the tools' own tests.

The hooks only fire if `git config core.hooksPath .githooks` was run. It's a local setting,
so it has to be re-run after any fresh clone. `setup-vault` does it.

## Privacy

- **This vault never goes public.** No public repo, no shared drive link. Backup is a private
  GitHub repo plus a disk backup (Time Machine or similar). Video files are gitignored (too
  large), so the disk backup is their only copy.
- **Never file the raw form of an ID document.** That covers passports, driver's licenses,
  SSN cards, bank or pay statements with account numbers, and transcripts with student IDs.
  The scanner can't read PDFs or images, so this rule is yours to enforce. Extract what a CV
  needs ("B.S. Biology, State University, 2019") into the chapter README, tell the owner, and
  leave the original out. Offer letters and pay stubs: record the role, dates and comp, not
  the document.
- **Other people.** References and colleague quotes are fine to keep here. Never copy a
  named person's words or contact details into anything that leaves the vault (a CV, a cover
  letter, a portfolio, a review packet) without the owner confirming that person agreed.
- **Employer confidentiality.** Employers' internal documents and unreleased product screens
  may be under NDA. File them with a `> ⚠️ confidential — do not publish` line at the top of
  the chapter README section, and never move them into a CV or career-ops.

## Money

Ask before spending the owner's money, every time.

- Claude Code runs on the owner's Claude subscription. Long batch jobs (for example
  career-ops `batch`, evaluating dozens of postings) use up plan limits fast. Say roughly how
  big a job is before starting it.
- **Never add an API key, and never run anything that calls a paid API, without the owner's
  explicit yes for that specific run.** In career-ops that includes the `or:*` npm scripts
  (OpenRouter), the `gemini` scripts, and anything that asks for a key in `.env`. A general
  "set it up" isn't a yes.
- Never schedule anything that spends. career-ops' job scanner (`node scan.mjs`) is plain
  HTTP to public job boards and uses no AI, so a weekly scan is fine. A scheduled evaluation
  isn't.

## Boundaries

- **`career-ops/`**, if installed, is its own git repo. Read and write it only through the
  `sync-career-ops` skill, or when the owner is working on a job search. Follow its own
  `AGENTS.md` and `DATA_CONTRACT.md` when you're inside it. Never commit it from here. The
  one system-adjacent edit sync makes is a marked block in `modes/_custom.md`, a user-layer
  file that career-ops' updater never touches.
- **`inbox/` is a drop zone, not storage.** It should be empty between sessions. Its contents
  are gitignored, so a file sitting there has no backup. Never `git add -f` from it.
- **`examples/` is fiction.** Never mix it with the owner's record, and never copy its
  numbers or wording into their files.
- Nothing is ever sent, submitted, or posted on the owner's behalf. Draft it, and let them
  hit send.

## Skills

| Skill | When |
|-------|------|
| `setup-vault` | First run (fast start), "what's next" (deepen, one step per session), or missing prerequisites |
| `file-inbox` | Anything is in `inbox/`, or the owner shares a file or photo in chat |
| `add-chapter` | A job, project, degree or venture has no folder yet |
| `sync-cv` | "Update my CV", "sync my CV", or after new work is filed. Rebuilds `cv.md` from the vault |
| `sync-career-ops` | Only if career-ops is installed: "sync", after a job-search session. Pulls back from career-ops, then pushes a CV built by the `sync-cv` rules |
