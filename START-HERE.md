---
type: doc
updated: 2026-11-11
links: []
---

# Start here

This folder is a private record of your working life that you run with Claude Code. Every
job, project and degree gets a folder with the story of what you did and the files that
prove it: screenshots, reviews, kudos emails, dashboards. Your CV is rebuilt from it, and
every number on that CV points at a file.

Hiring managers and promotion committees ask "how do you know that?" This vault means you
always have the answer. Use it for performance reviews, promotion cases, brag documents, and
a job search when one comes.

## What you need

- **A Claude Pro or Max subscription.** Claude Code runs on it. You don't need an API key.
- **VS Code** with the **Claude Code** extension (search "Claude Code" in Extensions, publisher
  Anthropic). Sign in with your Claude account.
- **git and python3.** You may already have them. Claude checks during setup and walks you
  through anything missing. On a Mac it's one installer, about 5 minutes.
- **Node.js** only if you later add the optional job-search engine.

## Setup: about 15 minutes

1. Put this folder in your **home folder** (on a Mac: Finder → **Go → Home**, the one with
   your name and a house icon). **Not Documents, Desktop, Downloads, iCloud, OneDrive or
   Dropbox.** Sync services can corrupt the vault's history.
2. In VS Code: **File → Open Folder…** and pick it.
3. Open Claude Code (the Claude icon in the sidebar) and type **`set me up`**.

Claude checks your tools, asks five quick questions, and asks for your current resume. Setup
ends with a CV where every number has a row in your evidence ledger.

**After that, build it up at your own pace.** Whenever you have 20 minutes, say **"what's
next"**. Claude does one step at a time: your work history, dropping in old files and
photos, a private backup, prep for your next review.

## Everyday use

- Drop files into `inbox/` and say **"file my inbox"**. Old resumes, LinkedIn PDF, headshots,
  screenshots, decks, kudos emails, reviews: anything. Don't sort them.
- Or just tell Claude about something you did. It writes it into the right chapter.
- Say **"update my CV"** after adding real work. It rebuilds `cv.md` and flags any number
  with no proof behind it.
- Say **"what's next"** whenever you have 20 minutes.

**Nothing is ever sent or submitted for you.** Claude drafts, and you hit send.

## Job searching (optional)

If you're looking, Claude can install [career-ops](https://github.com/santifer/career-ops),
an open-source job-search engine, inside this folder. It scans company job boards, scores
postings against your background, and writes a tailored CV for each one, all from this
vault. Say **"what's next"** until it's offered, or ask for it.

## Costs: read this once

- Everything here runs on your Claude subscription. Nothing is billed per use **unless you add
  an API key.** Don't add one. Some optional career-ops features (OpenRouter or Gemini
  runners) use paid keys, and Claude is told to ask before anything like that.
- Big batch jobs, like scoring 50 job postings in one go, use a lot of plan capacity.

## Privacy

- Everything stays on your computer. Claude reads files to help you, under Anthropic's
  privacy terms. Nothing gets published.
- Your history is saved with git, which acts as an undo button. Under "what's next", Claude
  sets up a **private** GitHub backup and checks it's private before anything is sent. Keep a
  disk backup too (Time Machine or similar): videos are too big for git, so it's their only
  backup. **Never make this folder public.**
- A built-in check blocks saving anything that looks like a Social Security, card, account,
  passport or license number. It can't read images or PDFs, so **don't drop ID documents or
  bank statements in at all.**

## The one habit that makes this work

**Every number on your CV should trace back to something in the vault.** "Grew signups 40%"
is strongest with a screenshot, review, or email behind it. The vault tracks which claims are
proven (🟢), estimated (🟡), from memory (🔵), or still looking for proof (🔴). Numbers from
your current resume start as 🔵. That's fine to use, and they upgrade as you drop in files.
A 🔴 number never goes on your CV.
