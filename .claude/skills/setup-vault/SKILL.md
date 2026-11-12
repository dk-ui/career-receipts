---
name: setup-vault
description: First-run setup for this career vault, in two parts. Fast start gets the owner from zero to an honest CV, built from what they already have, in about 15 minutes; deepen (later, at their pace) builds the full record, a private backup, and optional extras like the career-ops job-search engine. Use when profile/README.md says status not-set-up, or the owner says "set me up", "start", "get started", "what do I do", or "what's next".
---

# Setup

The owner may not be technical. Talk in plain language, one step at a time, and **say what
each step is for before running it.** Don't paste raw command output at them. Summarize it.
If a step fails, explain the fix in one or two sentences and offer to do it.

**The goal of the first session is a usable CV where every number is honestly labeled, not
a complete vault.** Get them to something useful fast, then deepen the vault over the
following weeks. Every step is safe to re-run. Skip anything already done.

# Part 1 — Fast start (~15 minutes)

## 1. Location and prerequisites

**Check the location first:** run `pwd`. If the path contains `/Documents/`, `/Desktop/`,
`/Downloads/`, `Mobile Documents`, `OneDrive` or `Dropbox`, stop. Sync services can corrupt
git history, and macOS stops scheduled jobs from reading those folders. Ask the owner to quit
VS Code, move the folder to their home folder (on a Mac: Finder → Go → Home), and reopen it
there. Don't continue until it lives directly in the home folder.

```bash
git --version     || echo "need git"
python3 --version || echo "need python3"
```

On macOS, `xcode-select --install` provides both: a dialog appears, they click Install and
wait about 5 minutes. On Windows or Linux, point them to git-scm.com and python.org. Don't
install system software silently.

## 2. Make the folder theirs

```bash
[ -d .git ] || git init -b main
git config core.hooksPath .githooks
git remote -v
git config user.name  >/dev/null || echo "need name"
git config user.email >/dev/null || echo "need email"
```

**Disconnect the template.** If the folder came from `git clone` of the public template,
`origin` still points at that public repo. Before the first commit, check it:

- `origin` exists and `gh repo view "$(git remote get-url origin)" --json visibility -q .visibility`
  prints `PRIVATE`: it's the owner's own repo (made with **Use this template → Private**).
  Keep it.
- Anything else (it prints `PUBLIC`, `gh` isn't installed, or the check fails): rename it so
  nothing can ever be pushed there, and tell the owner in one line why:

  ```bash
  git remote rename origin template
  ```

  "This folder still pointed at the public template it was copied from. I've disconnected
  it, so your vault can never be sent there. Your own private backup comes later."

The pre-push hook also refuses to push to a remote named `template`, or to any repo `gh` can
see isn't private. That's a backstop, not a reason to skip the rename.

If name or email is missing, ask and set them **for this repo only** (no `--global`). One
line of explanation: "git is your undo button. Each time we finish something, I save a
checkpoint you can go back to."

**Swap the front page.** If `README.md` contains `<!-- template-readme -->`, it's the GitHub
page for strangers, not the owner's. Replace it:

```bash
cp .claude/skills/setup-vault/owner-README.md README.md
```

First commit: `chore: start vault`.

## 3. Five questions

Ask together, in one friendly message, and write the answers into `profile/README.md`:

1. Your name as you want it on your CV, and the email you use for work things.
2. Your current role and organization, and where you're based.
3. What do you want this for first: a performance review, a promotion case, a job search,
   or just a record you trust?
4. If you're looking now or soon: what roles and level, and your salary floor? (Skip if not.)
5. Anything you'd never take on again?

## 4. Current resume → CV

"Drop your current resume into the **inbox** folder (PDF or Word is fine)." Then:
- `file-inbox` it into `resumes/`.
- `sync-cv` in **fast-start mode**. That builds `cv.md` from the resume, with every number on
  it logged in the ledger as 🔵 *self-attested, from resume*.

Then show them the result in a few lines: "Your CV is in `cv.md`. Every number on it now has
a row in `evidence-ledger.md`, marked 🔵 (from memory) for now. As you drop in screenshots,
reviews and emails, those turn 🟢. When someone asks 'how do you know that?', you'll have
the answer."

## 5. The sample vault

If `examples/` exists, offer: **"Want to see what a filled-in vault looks like?"** If yes,
walk them through `examples/sample-vault/`: the chapter table in `chapters/README.md` (one
chapter at each flag), one chapter's gap list, and `evidence-ledger.md`. Say plainly that the
person and companies are invented.

Then offer to delete it, along with the files that only matter to the template's public
GitHub page (`build.sh`, `SETUP-PROMPT.md`, and `.github/` with its banner and issue
forms): "That sample isn't yours, so I'd remove it to keep your vault clean. OK?" On yes:

```bash
git rm -r -q --ignore-unmatch examples build.sh SETUP-PROMPT.md .github
```

Remove their rows from the root `index.md`, and commit `chore: remove template sample`.

## 6. Done

Set `profile/README.md` frontmatter `status:` to `active` and commit `chore: fast start done`.

Close with: "Your vault is running. Drop files in **inbox** whenever you have them and say
**file my inbox**. Whenever you have 20 minutes, come back and say **what's next**, and
we'll fill in your history one step at a time."

# Part 2 — Deepen (one item per session, at their pace)

When they say "what's next", pick the first undone item, do it, and stop. Don't run the
whole list at once.

**a. History.** "Walk me through your work history, newest first. Just organization, title,
rough dates." Include freelance, school, volunteering and side projects that matter.
`add-chapter` for each. Then: "Which 2–3 things would you lead with in a review or an
interview?" Those become highlights and gap-list items.

**b. The big drop.** "Drop everything into inbox: old resumes, cover letters, your LinkedIn
PDF (profile → More → Save to PDF), headshots, screenshots of your work, kudos emails,
performance reviews. Don't sort it. Skip passports, licenses, bank statements, and anything
with an ID number on it." Then `file-inbox`, then `sync-cv`. 🔵 rows from their resume
upgrade to 🟢 as files arrive.

**c. Backup.** Everything is on one laptop right now. Offer a **private** GitHub repo. If a
private `origin` already exists (step 2 kept it), just `git push` and skip the rest.

```bash
python3 tools/privacy_scan.py --all          # must be clean first
gh --version || brew install gh              # if no Homebrew: cli.github.com installer
gh auth login                                 # they do this; it opens a browser
gh repo create career-vault --private --source . --remote origin --push
gh repo view --json visibility -q .visibility   # must print PRIVATE
```

If visibility isn't `PRIVATE`, stop and fix it before anything else. Then tell them: future
checkpoints back up with `git push` (you'll do it at the end of each session), and a
pre-push check blocks a push if anything looks like an ID number. Also recommend a disk
backup (Time Machine or similar). It's the only backup for files git skips, like videos.

**d. Story depth.** Pick the weakest-evidence highlight in the ledger and ask about it like
an interviewer or a promotion committee would: "How do you know it was 40%? What did the
before look like? Who else was involved?" Write the answer into the chapter.

**e. Review-ready.** Ask when their next review or promotion conversation is. Draft a one-page
brag document from the chapters, newest work first, using only ledger-backed numbers. Save it
as a `doc` in the current chapter. Nothing is sent for them.

**f. Optional: a job-search engine.** Only if they're looking or expect to soon. Offer
[career-ops](https://github.com/santifer/career-ops) (open source, MIT): it scans company job
boards, scores postings against their background, and tailors a CV for each one. It needs
Node 18.17+ (nodejs.org → LTS installer; send them there, don't install silently).

```bash
git clone https://github.com/santifer/career-ops.git career-ops
cd career-ops && npm install    # also downloads Chromium, used to render CV PDFs
node doctor.mjs --json --init-templates
```

`career-ops/` is gitignored here and is its own repo. Then run `sync-career-ops`. From now on
`career-ops/cv.md` is the live CV. Tell them: "Open a second VS Code window on the
**career-ops** folder and paste a link to a job you're interested in. It scores the posting
and writes a tailored CV." Say plainly that evaluations use their Claude plan.

**g. Optional: weekly scan.** Only if career-ops is installed. Free: `node scan.mjs` makes
plain web requests to company job boards and uses no AI. Matches land in
`career-ops/data/pipeline.md`. Follow `career-ops/docs/AUTOMATION.md`. Schedule **only** the
scan, never evaluations or `/loop` jobs, because those use their Claude plan every time they
fire. See CLAUDE.md "Money".

When everything they want is done, tell them: "You're fully set up. Drop files in inbox
whenever you have them, sync after you add work, and every number on your CV will always
have an answer to 'how do you know that?'"
