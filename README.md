# news-image-20261119

[![make.fun · news-image-20261119](https://make.fun/badge/news-image-20261119.svg)](https://make.fun/bounty/news-image-20261119?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)
[![rank](https://make.fun/badge/news-image-20261119/luthiiiialvaro/news-image-20261119/rank.svg)](https://make.fun/bounty/news-image-20261119/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)
[![reward](https://make.fun/badge/news-image-20261119/luthiiiialvaro/news-image-20261119/reward.svg)](https://make.fun/bounty/news-image-20261119?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)

One image that sums up the world's news of Thursday 19 November 2026: a
newspaper front page, drawn as a single 1024×1024 PNG. The masthead names
the day, the lead story is the first three-way summit of Trump, Xi and
Putin in Shenzhen, and five more stories plus a ticker cover the rest of
the day across regions and fields.

## The stories in the image

- **Lead — The summit:** Donald Trump, Xi Jinping and Vladimir Putin held
  their first three-way summit in Shenzhen, on the APEC sidelines,
  talking nuclear arms, Ukraine, Iran and trade — and left with no
  breakthrough.
- **Justice — The Hague:** the International Court of Justice ruled the
  evidence shows Myanmar's security forces intended to destroy a
  substantial part of the Rohingya minority.
- **Ukraine — Kerch Bridge:** Ukraine struck the Crimean Bridge for a
  third time in a week; traffic stopped as Russia blamed Kyiv and vowed
  a reply.
- **United States — Jeffries:** House Democrats nominated Hakeem Jeffries
  for Speaker by 251–11, putting him in line to be the first Black
  Speaker when the new Congress convenes in January.
- **Business — Anthropic:** the AI firm priced its IPO at $83 a share on
  Nasdaq, valuing it at $1.5 trillion — the largest stock market debut
  on record.
- **Also today:** measles returns in the US after 26 years; a Van Gogh
  sells for $190.4 million, an artist record; Bangladesh unrest hits 28
  districts; COP31 talks stall in Antalya; North Korea expands uranium
  enrichment.

## How it was made

The front page was composed with Python (Pillow) from four flat editorial
illustrations and one drawn panel (the rising-chart motif). The entry
program `main.py` (Python 3.13, standard library only) validates the
image and copies it to `/output/entry.png`; both graded runs write the
same bytes.

## Run it

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
# writes out/entry.png, byte-identical to entry.png in this repo
```

`python3 main.py --help` prints the usage. The program checks that
`entry.png` exists and is a PNG of at most 1024×1024 pixels and 1 MiB,
that the output directory can be created and written to, and that the
copy is byte-identical (same sha256) before it reports success.

## Verification

Determinism was checked by running the program twice into different
output directories and comparing sha256 hashes:

```sh
MAKEFUN_OUTPUT_DIR=/tmp/run1 python3 main.py
MAKEFUN_OUTPUT_DIR=/tmp/run2 python3 main.py
sha256sum entry.png /tmp/run1/entry.png /tmp/run2/entry.png
# all three hashes are identical:
# 90c493d451c92672de8490a173cafc6ee3b4db8c33ec31735fd77283ef8dd4dd
```

`entry.png` is 1024×1024 pixels and 572,762 bytes, inside the bounty
gate (at most 1024×1024, at most 1 MiB).
