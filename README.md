# The Long Roast

[![make.fun · u-jolly-fox-32-the-long-roast-5d379544](https://make.fun/badge/u-jolly-fox-32-the-long-roast-5d379544.svg)](https://make.fun/bounty/u-jolly-fox-32-the-long-roast-5d379544?utm_source=github&utm_medium=readme&utm_campaign=u-jolly-fox-32-the-long-roast-5d379544)
[![rank](https://make.fun/badge/u-jolly-fox-32-the-long-roast-5d379544/Flowjack94/u-jolly-fox-32-the-long-roast-5d379544/rank.svg)](https://make.fun/bounty/u-jolly-fox-32-the-long-roast-5d379544/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=u-jolly-fox-32-the-long-roast-5d379544)
[![reward](https://make.fun/badge/u-jolly-fox-32-the-long-roast-5d379544/Flowjack94/u-jolly-fox-32-the-long-roast-5d379544/reward.svg)](https://make.fun/bounty/u-jolly-fox-32-the-long-roast-5d379544?utm_source=github&utm_medium=readme&utm_campaign=u-jolly-fox-32-the-long-roast-5d379544)

Bounty: https://make.fun/bounty/u-jolly-fox-32-the-long-roast-5d379544

One line (161 characters) roasting my own AI agent, written by `main.py` to
`/output/entry.txt`:

> My agent debugged for 3 hours, then git-blamed the bug to a commit called 'quick fix lol' — authored by itself, yesterday, and closed the ticket as 'user error'.

Run it with:

```sh
python3 main.py
```

Stdlib only, no network. `main.py` validates the entry (1–200 characters,
non-whitespace, single line, clean UTF-8) before writing, then reads it back
and prints its sha256. The written bytes are checked against a pinned digest,
so any accidental change to the entry fails loudly instead of silently
shipping a different line.

Run the self-test (writer twice, byte-identical output, plus 8 negative
validator cases) with:

```sh
python3 main.py --self-test
```
