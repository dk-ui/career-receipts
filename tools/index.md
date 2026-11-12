---
type: manifest
updated: 2026-11-11
links: [tools/README.md]
---

# tools/ — index

Gate scripts and their tests.

## Files
| Name | What it is |
|------|------------|
| [`README.md`](README.md) | What each script does, and which ones block |
| `privacy_scan.py` | Blocking privacy gate |
| `add_frontmatter.py` | Frontmatter generator |
| `gen_manifest.py` | `MANIFEST.md` generator and checker |
| `claims_check.py` | CV numbers vs the evidence ledger |
| `vault_integrity.py` | Index vs disk, frontmatter contract |
| `test_privacy_scan.py` | Tests: what the gate blocks and lets through |
| `test_claims_check.py` | Tests: unsourced and 🔴-only CV numbers are reported |
| `test_gen_manifest.py` | Tests: manifest describes git, not the disk |
| `test_precommit_manifest.py` | Tests: a hooked commit passes the manifest check on a fresh clone |
| `test_vault_integrity.py` | Tests: integrity checker |

---
[README.md](README.md) for narrative/status
