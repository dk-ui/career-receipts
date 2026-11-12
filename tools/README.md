---
type: readme
updated: 2026-11-11
links: [CLAUDE.md]
---

# tools/

The scripts behind the vault's gates. Python 3 standard library only, no installs. Each one
finds the vault from its own location, so they work from any clone. Only `privacy_scan.py`
can stop a commit; everything else reports. See [CLAUDE.md](../CLAUDE.md) "Gates".

| Script | What it does | Blocks? |
|--------|--------------|---------|
| `privacy_scan.py` | Finds ID, card, account and date-of-birth numbers in text files | Yes: commit and push |
| `add_frontmatter.py` | Fills in each `.md` file's frontmatter; refreshes `links:` every run | No |
| `gen_manifest.py` | Writes `MANIFEST.md`; `--check` fails on a stale manifest or dead link | No (`--check` exits 1) |
| `claims_check.py` | Lists CV numbers with no ledger row, or only a 🔴 one; `--cv PATH` checks another CV | No (`--strict` exits 1) |
| `vault_integrity.py` | Files no `index.md` registers, missing README/index pairs, frontmatter breaks | No (`--strict` exits 1) |

Tests: `python3 -m unittest discover tools`.
