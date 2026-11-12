#!/bin/bash
# Build career-vault.zip: the template without .git and without examples/, with the
# top-level folder named career-vault. The zip is for people who have already decided
# to use it, so the sample vault stays on GitHub. Whoever unzips it runs `git init`
# (the setup-vault skill does it on first run).
set -e
cd "$(dirname "$0")"
here="$(pwd)"
stage="$(mktemp -d)"
trap 'rm -rf "$stage"' EXIT

# Tracked files only: nothing untracked, ignored, or half-done gets shipped.
git ls-files -z | while IFS= read -r -d '' f; do
    case "$f" in
        examples/*|build.sh) continue ;;
    esac
    mkdir -p "$stage/career-vault/$(dirname "$f")"
    cp -p "$f" "$stage/career-vault/$f"
done

rm -f "$here/career-vault.zip"
(cd "$stage" && zip -qr "$here/career-vault.zip" career-vault -x '*/__pycache__/*' '*.DS_Store')
echo "built $here/career-vault.zip"
