# Triage packet: status OPEN

loki-tva runs the build only after you close every item below.

## 1. Ladder read
See the memo test in `storyline.md`. Structurally it passes, but these 14 `[TK]` items are open:

| Slide | Fill with | From |
|---|---|---|
| S01 | application growth %, disbursement growth % | [D1] |
| S02 | disbursed per 100 applications | [D1] |
| S03 | confirm process drop-outs > credit declines (if not, swap S03–S06) | [D2] |
| S04 | % of process drop-outs from invalid docs; top failing document | [D4] |
| S05 | median days to decision | [D3][D10] |
| S06 | rule declines ÷ SLIK declines | [D2][D5] |
| S07 | IDR bn forgone interest; analyst-hours wasted | [D1][D8][D9] |
| S09 | % of rule declines at or below approved-book risk | [D6][D7] |
| S11 | loans added per month under option D | derived |
| S12 | pilot length in weeks; which segment | your call |
| Ask | owners' names, start date | your call |

## 2. Exhibit digest
| E | Slide | Form | Kicker |
|---|---|---|---|
| E01 | S01 | indexed line chart | Demand rose; loans did not |
| E02 | S02 | funnel bars per 100 applications | [TK] of 100 reach disbursement |
| E03 | S03 | 100% stacked bar | Process losses outnumber credit declines |
| E04 | S04 | sorted horizontal bar | One document drives most failures |
| E05 | S05 | histogram + median line | Cancel rate rises with waiting time |
| E06 | S06 | horizontal bar | Our rules, not SLIK, decline most |
| E07 | S07 | waterfall (EST) | The leak costs IDR [TK] bn a year |
| E08 | S09 | bars by A-score band + reference line | A low-risk subset exists among declines |
| E09 | S11 | options matrix | D adds loans without adding loss |

## 3. Look
OCBC red, theme intensity 0, all-exhibit deck (no generated images). Mind map in the appendix (`slides/mindmap.png`).

## 4. Disposition policy
Defaults: SEV-1 fix, SEV-2 fix, SEV-3 accept.

## 5. The ask, verbatim
"Approve a [TK]-week pilot of document pre-check, a decision-time SLA, and A-score review of rule-based declines, co-owned by Credit Risk and Consumer Lending, starting [TK]."
