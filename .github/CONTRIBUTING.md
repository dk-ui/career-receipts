# Contributing

Thanks for helping make career-receipts better. It's a small, free project, so the bar is
simple: keep it private by default, easy for non-technical people, and honest about evidence.

## Before you post anything

**Never paste content from your own vault**: no real names, employers, numbers, files or
screenshots. Describe the problem with made-up details instead, or reproduce it in
`examples/sample-vault`, which is fictional.

## Good first contributions

- A step in the setup that confused you, with the exact words Claude used
- Windows notes (the Mac path is the tested one)
- Privacy-check patterns it misses, or ordinary text it wrongly blocks

## Changing the code

The tools in `tools/` are Python standard library only, with no installs. Keep it that way.

```sh
python3 -m unittest discover tools        # all tests must pass
python3 tools/privacy_scan.py --all       # must print "clean"
python3 tools/gen_manifest.py --check     # must pass
python3 tools/vault_integrity.py          # should report "clean"
```

Rules the project holds to:

- **Only the privacy check may block a save.** Everything else reports and never blocks.
- **No paid API calls, keys or schedules** in anything the vault runs.
- **Plain language** in anything an owner reads. Say what a step is for before it runs.
- **The sample vault stays fictional.** Every person, organization and number in it is
  invented. Check a new organization name with a web search before you add it.

## Pull requests

Keep them small and say what problem they solve. If a change touches a skill in
`.claude/skills/`, describe how you tested it in a real setup conversation.
