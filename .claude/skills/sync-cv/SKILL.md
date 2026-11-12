---
name: sync-cv
description: Rebuild the live CV (cv.md at the vault root) from the vault, so every number on it traces to an evidence-ledger row. Use when the owner says "update my CV", "sync my CV", "sync" (and career-ops is not installed), after new work is filed, or before a review, promotion case or application. If career-ops is installed, use sync-career-ops instead; it follows these same rules.
---

# Sync the CV

The live CV is `cv.md` at the vault root. If `career-ops/` exists, the live CV is
`career-ops/cv.md` and `sync-career-ops` owns it, using the rules in steps 2 to 4 below.

## 1. Don't erase the owner's edits

If `cv.md` exists, diff it against `job-search/cv-last-sync.md` (the copy of what the last
sync wrote). For any **fact** that changed by hand (a number, a date, a title, scope), ask
the owner whether it's real, and if so write it into the vault first: the chapter README,
`profile/README.md`, or a ledger row (🔵 self-attested unless they have a file for it).
Wording changes aren't facts. Keep them if the owner wants. Never let step 3 silently erase
an edit.

## 2. Read the source

- `profile/README.md`: name, contact, current role, goals.
- Every `chapters/*/README.md`: the story, highlights, artifacts, gaps.
- `evidence-ledger.md`: which numbers are 🟢 / 🟡 / 🔵 / 🔴.
- The newest file in `resumes/`: the owner's own phrasing and section order. Match it unless
  they've asked for a change.

Never read `examples/`. It's a fictional sample, not the owner's record.

## 3. Build `cv.md`

Clean markdown: name and contact block, Summary, Experience (newest first), Projects,
Education, Skills. Rules:

- **Every number comes from a ledger row.** Use 🟢 and 🟡 freely. Use 🔵 self-attested only
  if the owner keeps it. **Never use a 🔴 number**, and never invent one. When a highlight has
  no usable number, write it without one.
- **Write the number the way the ledger writes it** (`$1.2M`, `18%`), so the claims check can
  match it.
- **Rephrase, don't embellish.** Tighten their words. Don't upgrade "helped with" to "led".
- Leave confidential (NDA) material out entirely.

**Fast-start mode** (first sync, while chapters are still stubs): build `cv.md` straight from
the owner's current resume. Take every number on it into the ledger as 🔵 *self-attested,
from resume YYYY-MM*. That's honest, and the claims check stays quiet. Those rows upgrade to
🟢 as files arrive.

## 4. Show, then write

The CV is the owner's. **Never overwrite it silently.**

- First build: show a short summary of what you're writing, then write.
- Later builds: show the **diff**: which bullets changed, which numbers appeared or
  disappeared. Get a yes before writing.

After writing, copy `cv.md` to `job-search/cv-last-sync.md`. That's the baseline step 1
diffs against next time.

## 5. Check

```bash
python3 tools/claims_check.py
```

Every number on the CV needs a usable ledger row. For each one listed, add the row (with its
artifact) or drop the number from the CV. Also report the ledger's open 🔴 gaps, since those
are the highest-value files to go find.

## 6. Save

Commit (`sync: cv rebuilt, <what changed>`), and `git push` if a private `origin` exists.
Tell the owner in a few lines: what changed on the CV, any numbers you dropped and why, and
the single most valuable 🔴 gap to go find.
