# review.md: loki-deckreview, cycle 1 (2026-11-25)

Deck: `deck.pptx`, 16 slides, built on ILLUSTRATIVE DUMMY data.
Disposition policy (default): SEV-1 fix, SEV-2 fix, SEV-3 accept. Render faults are fixed below. Claim-side findings are never auto-fixed; they wait for the author.

**Terminal state: BLOCKED.** Render-side SEV-1 = 0. Five claim-side findings need an author decision (C01–C05).

## Fixed this cycle (render side, re-rendered and re-checked)

| ID | Slide | Pass | SEV | Finding | Fix |
|----|-------|------|-----|---------|-----|
| R01 | S01–S11 | 3 | 1 | 17 derived numbers (34%, 70, 47, 67%, 60%, 2.8×, 1,176, 30%, ~350, IDR 35 bn, 8,000 h…) had no CSV home. Three "matched" only by coincidence (60 = ticket size; 2.8 = a bad rate; 30 = funnel value) | `build_deck.py` writes `data/derived.csv`: each derived number with its formula and source cells |
| R02 | S07 | 3 | 1 | "1.5 h per cancelled file" assumption had no home | Added `hours_per_cancelled_file` to `data/E07.csv`; slide reads it from there |
| R03 | S15 | 2 (L1) | 1 | Mind map overlapped the footer and hid the dummy-data tag; text ~7 pt | Re-rendered at a larger font (~11 pt on the slide), fitted to 4.5 in height |
| R04 | S04 | 6 | 2 | Title claims 60% of process drop-outs, but the chart only shows the mix by document type | Added evidence line: "Invalid documents: 28 of 47 process drop-outs per 100 applications (60%)" |
| R05 | S08, S11 | 3 | 2 | Estimates (+60 bps; loans added) shown with FACT confidence | Labelled "(estimate)" / "(est.)" |
| R06 | S11 | 6 | 2 | Reader can't see where ~350 loans/month comes from | Derivation footnote added |
| R07 | S01, S11, S12 | 4 | 3 | Notes: missing thousands separators; garbled "costs about IDR 35 bn/yr forgone"; "each has a weekly output" was inaccurate | Rewritten |
| R08 | S05, S08, S11 | 2 (L1) | 3 | Box overlaps (caption × chart, text × callout, falsifier × footnote) | Resized |
| R09 | S13, S14 | 2 (L1) | 3 | Background cards unnamed, so they showed up as false overlaps | Named `bg-*` |

## Needs the author: claims (BLOCKED)

| ID | Slide | Pass | SEV | Finding | Recommended decision |
|----|-------|------|-----|---------|----------------------|
| C01 | S11 | 3 | 1 | Matrix cell says "Flat (back-tested)", but no back-test exists; the footnote itself says "if the back-test shows…" | Change to "Flat (est.; pilot tests it)" in `data/E09.csv`, and add "(est.)" to the S11 title |
| C02 | S01–S11 | 1 | 1 | As-built titles drift from the v0 ladder wording: S01 "last year" became "in 12 months"; S03 "Most" became "Two in three"; plus the filled `[TK]` numbers | Adopt the as-built titles into `storyline.md` as changelog v0.2 |
| C03 | S12 | 4 | 2 | "Proves it before any rule changes" overclaims: WS4 sends rule declines to manual review, which is a temporary override | "…before any permanent rule change" |
| C04 | S05 | 6 | 2 | Question-chain gap: "7 days — slow compared to whom?" Nothing answers it | Add a dated peer SLA [D10] if you have one; otherwise keep and say it aloud |
| C05 | all | 2 (L2) | 2 | Every title wraps to two lines (uatu rule: one line) | Accept two-line titles at 28 pt and record it in STYLE.md. Shortening every title would cost specificity |

## Accepted (SEV-3, per policy)
- S02 annotation wording ("biggest single drop: 28 at the 'complete documents' stage") is clunky. Suggest "the biggest drop (28) is invalid documents". It's a claim-side string, so it's left for the author.
- S13 kicker says "stop", the body says "pause": minor terminology drift.
- Callouts sit beside the charts, not on the datum. This is consistent across the deck.
- About 60 shapes have generic names (TextBox N). Geometry QA still worked.

## Pass summary
1. **Memo & flow:** connectives hold at all 13 junctions on the as-built titles. Title drift vs. ladder is C02.
2. **Visual (uatu):** Lens 1 is clean after fixes; footer furniture sits identically on every slide. Lens 2: labels, units and the axis-start disclosure (S01) are present, with no label collisions. Lens 3: reads as one deck, the accent is reserved for message carriers, and the squint test passes.
3. **Grounding:** every number on the slides now traces to `data/E##.csv` or `data/derived.csv`. The only exception is the placeholder start date. All of it is DUMMY.
4. **Clarity:** no slop lexicon hits; terminology is consistent (process drop-out / credit decline / rule decline). Clarity's lint scripts were *not* run: the sandbox blocked executing the downloaded third-party scripts. The review was done by reading.
5. **Story:** the Cold Open lands on slide 1 with no agenda; criteria come before the recommendation; "do nothing" is priced; the falsifier is present; option C is real (steelmanned on S08); the ask is restated with owners. The date is still a placeholder.
6. **Cold read (notes off):** title↔body holds on every slide after R04. Pacing: S04–S07 are four dense exhibits, relieved by S08. The argument can be stated at every act boundary.
