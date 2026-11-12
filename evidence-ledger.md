---
type: doc
links: []
updated: 2026-11-11
---

# Evidence Ledger

**One row per claim on the live CV (`cv.md`, or `career-ops/cv.md` if installed), pointing at
the file that backs it.** Read this before a review or an interview, and before any number
goes into a resume, cover letter, promotion case or portfolio.

## What earns a row

A fact gets a row when it becomes a **claim**, meaning you assert it to someone outside this
vault. All three of these have to hold:

1. **It will leave the vault**, in a CV, review, cover letter, portfolio, or interview answer.
2. **Someone could reasonably ask "how do you know that?"** That covers numbers, percentages,
   dollar figures, team sizes, and superlatives like *first*, *only*, *largest*.
3. **Being wrong would cost something**, like your credibility with a hiring manager or a
   promotion committee.

**Not rows:** tool lists, titles, dates, and plain descriptions of responsibilities.

`tools/claims_check.py` enforces a cruder version: **if it has a digit, it needs a row.**

## Status key

| | Meaning |
|---|---|
| 🟢 **SOURCED** | A file in this vault shows the number: a screenshot, report, review, or award letter |
| 🟡 **DERIVED** | Calculated or estimated from something documented. Fine to use if you can explain the math |
| 🔴 **GAP** | No file yet, but one could exist. Go find it. **Never used on a CV** |
| 🔵 **SELF-ATTESTED** | Your recollection, and the document is gone (it stayed with the employer), or a number carried over from your resume that hasn't been backed yet. Fine to use: be ready to say "that's from memory". Upgrade it to 🟢 if a file turns up |

## Summary

| Claim | Evidence | Status |
|---|---|---|

<!-- One section per chapter, newest first. Example row format:
| Cut onboarding time 40% | chapters/acme/README.md (linked), dashboard in media/ | 🟢 |
-->
