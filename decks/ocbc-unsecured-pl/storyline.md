# storyline.md: OCBC unsecured personal loan

**Status:** v0.2 DRAFT. Titles are synced to the as-built deck. Numbers are ILLUSTRATIVE DUMMY values, so this is not frozen for real use (see `triage.md`).
**Built with:** loki-storyline Steps 0–6, with the clarity rewrite pass (Argument register, slides medium) run on the whole ladder.

## Frame

- **Belief shift:** Today the panel believes *low disbursement is the price of prudent
  risk appetite*. By the end they must believe *most of the gap sits inside our own
  funnel, and we can recover part of it without raising expected loss.*
- **Controlling idea (falsifiable, 24 words):** OCBC loses more unsecured-loan applications
  to its own documents, speed, and rules than to applicant risk. A-score lets us recover
  some at flat loss.
- **The ask:** Approve a `[TK: 8–12]`-week pilot of document pre-check, a decision-time
  SLA, and A-score review of rule-based declines. Credit Risk and Consumer Lending would
  own it jointly, starting `[TK: date]`.

**Terms used on every slide (one term per concept):**
- *process drop-out*: the application is lost before a credit decision (invalid documents, cancellation).
- *credit decline*: the application is rejected at credit review. These split into *SLIK declines* and *rule declines* (internal policy rules).
- *A-score*: application scorecard, the probability-of-default rank at entry.

## Beat sheet (Western skin over SCQA; theme intensity 0, so beats stay invisible)

| Beat | SCQA | Slides | Job here |
|---|---|---|---|
| Cold Open | Situation | S01–S02 | Demand is growing, but loans are not. Open on the funnel number. |
| The Stranger Rides In | Complication | S03–S06 | Name the leaks precisely: documents, speed, rules. |
| Raising the Stakes | Question | S07–S09 | Price the leak. Steelman "just loosen the rules", then show the A-score data that breaks it. |
| High Noon | Answer | S10–S11 | Criteria first, then four real options, "do nothing" priced, and the recommendation. |
| The New Order | Resolution | S12–S14 | Pilot plan mapped to the four proposed solutions, guardrails, the ask. |

## Title ladder

`S## | Act | TITLE | message detail | evidence | visual | status | transition-out`

```
S00b| —   | EXEC SUMMARY: "We lose more good applicants to our own process than to credit risk" (what is happening / why / what we propose / decision today)
S00 | —   | COVER: "Recovering lost unsecured-loan approvals at OCBC"  (subtitle: Graduate Program final presentation · name · date)
S01 | I   | Applications grew 34% in 12 months; disbursed loans grew only 6%
            | demand is not the constraint | [D1] | exhibit E01 (two-line index chart) | FACT
     ...therefore
S02 | I   | Only 30 of every 100 applications become a disbursed loan
            | the gap is inside our funnel | [D1] | exhibit E02 (funnel bar) | FACT
     ...but
S03 | II  | Two in three lost applications drop out before credit review, not at it
            | process drop-outs > credit declines (hypothesis; see triage note 1) | [D1][D2] | exhibit E03 (100% stacked bar) | FACT once [D2] mapped
     ...therefore
S04 | II  | Invalid documents cause 60% of process drop-outs, led by payslips
            | fixable at submission with a pre-check | [D4] | exhibit E04 (horizontal bar) | FACT
     ...but
S05 | II  | Even complete applicants cancel: our decision takes 7 days, median
            | speed loses applicants to faster banks | [D3][D10] | exhibit E05 (histogram, cancels by day) | FACT (peer speed EST)
     ...but
S06 | II  | At credit review, internal rules decline 2.8x more applicants than SLIK does
            | tightness is our policy, not bureau data | [D2][D5] | exhibit E06 (horizontal bar) | FACT
     ...therefore
S07 | III | These losses cost about IDR 35 bn interest and 8,000 analyst-hours yearly
            | lost approvals × ticket × yield; wasted hours on cancelled files | [D1][D8][D9] | exhibit E07 (waterfall) | EST, method on slide
     ...but
S08 | III | Loosening rules for everyone would add loans, but also add losses
            | steelman the easy answer; it fails risk appetite | [D7] | none (text + small table) | BELIEF/EST, disclosed
     ...but
S09 | III | 30% of rule-declined applicants score as low-risk as our approved book
            | A-score finds the safe subset | [D6][D7] | exhibit E08 (bar by A-score band) | FACT
     ...therefore
S10 | IV  | We judge four options on loans added, loss, cost and launch time
            | criteria stated before the reveal | — | none (criteria table) | —
     ...therefore
S11 | IV  | Process fixes plus A-score review add an estimated 350 loans monthly at flat loss
            | options matrix; "do nothing" priced; recommendation in accent | [D1][D6][D7][D8] | exhibit E09 (options matrix) | EST
     ...but
S12 | V   | A 12-week pilot on one segment proves it before any permanent rule change
            | 4 workstreams = the 4 proposed solutions | — | none (workplan) | —
     ...but
S13 | V   | Three guardrails stop the pilot if early losses rise
            | DPD trigger, volume cap, OJK/SLIK compliance review | — | none | —
     ...therefore
S14 | V   | Decision today: approve the pilot, co-owned by Credit Risk and Consumer Lending
            | the ask, verbatim | — | none | —
```

**S11 footnote (mandatory):** *What would change our mind: if the back-test shows
rule-declined applicants in low A-score bands default above the approved book's rate,
or if SLIK, not internal rules, drives most credit declines.*

## The four options for S11 (must stay real; no strawmen)

| | A. Do nothing | B. Process fixes only | C. Loosen rules for all | **D. Process fixes + A-score review (rec.)** |
|---|---|---|---|---|
| Loans added / month | 0 | +[TK] | +[TK] (largest) | +[TK] |
| Expected loss | unchanged | unchanged | **rises** [TK] bps | flat (est.; pilot tests it) |
| Cost | forgone IDR [TK] bn/yr | low | low | moderate (analytics + pilot ops) |
| Time to launch | — | 4–6 wks | 2 wks | 8–12 wks |
| Why someone would pick it | no risk change | quick, safe | fastest volume | volume without loss |

## S12 workplan: the four proposed solutions, as workstreams

| WS | Author's solution | What we do in the pilot | Output |
|---|---|---|---|
| 1 | Investigate where and why applications are rejected | Funnel dashboard by stage, channel, and reason code ([D1][D2]) | Weekly leak report |
| 2 | See current applications that can be improved | Recover pending and incomplete files; add a document pre-check at submission ([D4]) | Recovered applications, drop-out rate |
| 3 | Relook at credit history and reject reasons | Review rule by rule: which rules decline applicants with clean SLIK ([D2][D5]) | Rule-change candidates, sent to Credit Risk |
| 4 | Identify less-risky applicants with the A-score | Champion–challenger: low-risk A-score bands go to manual review under a volume cap ([D6][D7]) | Approvals, early DPD vs control |

## Memo test (Step 5): titles only, read as a skeptic

> Applications grew [TK]% last year; disbursed loans grew only [TK]%. *Therefore* only
> [TK] of every 100 applications become a disbursed loan. *But* most lost applications
> drop out before credit review, not at it. *Therefore* invalid documents cause [TK]% of
> process drop-outs. *But* even complete applicants cancel: our decision takes [TK] days.
> *But* at credit review, internal rules decline [TK]x more applicants than SLIK does.
> *Therefore* these losses cost about IDR [TK] bn a year. *But* loosening rules for
> everyone would also add losses. *But* [TK]% of rule-declined applicants score as
> low-risk as our approved book. *Therefore* we judge four options… *therefore* process
> fixes plus A-score review add [TK] loans monthly at flat loss. *But* a pilot proves it
> first. *But* three guardrails stop it if losses rise. *Therefore*: approve the pilot.

- Persuades alone: **yes, structurally.** It reads as an argument with no "and then".
- Connective test: **passes** at all 13 junctions.
- Nothing load-bearing missing: **conditional.** Every `[TK]` is load-bearing. The ladder
  cannot freeze until they are filled from the data inventory.

## Evidence audit (Step 4)

| Claim | Fate |
|---|---|
| "30–40% of rejected applications are recoverable" (from the earlier AI draft) | **Cut.** No source. Replaced by S09, which measures it. |
| "Bank Jago / SeaBank are taking share with faster processes" (earlier draft) | **Cut** unless a dated source exists. S05 uses our own cancel data instead. |
| "Rules in OCBC are too tight" (author's note) | Kept, made **measurable** in S06 (rule declines vs SLIK declines). |
| Process drop-outs > credit declines (S03) | **Hypothesis.** If [D2] shows the opposite, swap the order of S03–S06 (credit first) and reword S03. |
| Loss impact of option C (S08, S11) | **EST.** Method: approved-book loss rate by A-score band applied to the newly approved bands. |
| Peer decision speed (S05) | **EST/BELIEF** unless a published SLA or mystery-shop result exists. Disclose it on the slide. |

## Changelog

- v0 (2026-11-25): first compile from the author's notes. Not frozen.
- v0.1-dummy (2026-11-25): the author asked to build with dummy numbers. `[TK]` values are filled
  from ILLUSTRATIVE data in `data/*.csv` (`make_dummy_data.py`). The ladder is NOT frozen for real use:
  replace the CSVs with the real pull, re-check every title against them, then close triage.
- v0.2 (2026-11-25): review decisions applied. C01: "back-tested" became "est.; pilot tests it", and the S11
  title says "an estimated". C02: ladder synced to the as-built titles (dummy numbers). C03: S12 says
  "permanent rule change". C05: two-line titles accepted in STYLE.md. An OJK market slide was drafted, then
  cancelled by the author. Re-touch list: none beyond `deck.pptx`.
- v0.3 (2026-11-25): author asked for a deck that sells the improvement to management. Added an executive
  summary after the cover (answer first, Minto; it is a summary, not an agenda, so the Cold Open rule holds).
  Rebuilt the ask slide as approve / get / know. Pilot resourcing (2 analysts + 1 credit reviewer) is an
  ASSUMPTION in `data/pilot.csv`.
