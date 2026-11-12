---
name: add-chapter
description: Create a new chapter folder under chapters/ for a job, venture, degree, freelance stint, volunteer role or major project, from the template, and register it in the chapter list. Use when the owner mentions work that has no chapter yet, or file-inbox finds an artifact with no home.
---

# Add a chapter

1. **Slug.** Lowercase, hyphenated, short, usually the organization: `acme`,
   `state-university`, `freelance-branding`. If the same org appears twice in different
   roles, suffix the role: `acme-intern`, `acme-manager`.
2. **Copy the template.** Copy `.claude/skills/add-chapter/template/README.md` and `index.md`
   into `chapters/<slug>/`, and create `chapters/<slug>/media/`. Fill the README header from
   what you know: role, org, dates, one-line summary. Leave unknowns as `?` rather than
   guessing.
3. **Status starts ⚪ not started.** Put the owner's claims about this role in the gap list
   as `- [ ]` items, each naming the kind of file that would prove it, and move the flag to
   🔴. Describe flags to the owner as progress ("2 of 4 proven"), never as a grade.
4. **Register it.** Add a row to the table in `chapters/README.md` (newest first) and a line
   to `chapters/index.md`.
5. **Commit** with `add: <slug> chapter` (skip this if you're mid-way through another
   skill, which will commit).
