# dump.md: OCBC unsecured personal loan, graduate-program final presentation

> Transcribed from the author's notes (photo, 2026-11-25). The author's wording is
> kept below in the "Raw notes" section. Everything after it was added for loki's dump gate.

## Raw notes (author)

**Problem statement:** demand for unsecured loans keeps rising, but OCBC's
disbursement volume does not follow. The approval rate for the unsecured personal
loan is low for two reasons:

- **Application process:** invalid documents, and cancellations because other
  banks process applications faster than OCBC.
- **Credit:** credit history, SLIK, and OCBC's internal rules are too tight.

**Impact**
1. OCBC misses approvable applications.
2. Cancelled applications waste resources.
3. Revenue is lower.

**Proposed solution**
1. Investigate where and why applications are rejected.
2. Find current applications that can be improved.
3. Relook at credit history and reject reasons.
4. Identify less-risky applicants with the A-score.

## Dump gate (loki-storyline Step 0)

| # | Field | Status | What we have / assume |
|---|---|---|---|
| 1 | Audience | ASSUMED | Graduate-program panel: Consumer Lending head, Credit Risk head, a Ops/Digital rep, GP sponsor. Today they believe low disbursement is the price of prudent risk appetite. |
| 2 | The ask | ASSUMED | Approve a time-boxed pilot (document pre-check + faster decision SLA + A-score review of rule-based rejects). Owners and date are `[TK]`. |
| 3 | Budget | ASSUMED | 14 slides, 15 min talk + 10 min Q&A. |
| 4 | Data inventory | **GAP** | No numbers yet. The data list below is what to pull; every number on the slides must come from it. |
| 5 | Constraints | KNOWN | OCBC red template; OJK/POJK and SLIK rules; internal data, so the deck is confidential and uses aggregates only, with no customer-level data. |
| 6 | Stakes | ASSUMED | If nothing changes, OCBC keeps paying acquisition and processing cost for applications that never disburse, and competitors keep the applicants who leave. |
| 7 | References | NONE | No exemplar decks supplied, so loki-mobius was skipped. |

## Data inventory: pull these before triage closes

Most can come from the loan-origination system or the SSRS reports.

| ID | Data | Grain | Used by |
|---|---|---|---|
| [D1] | Application funnel: submitted, complete-docs, credit-reviewed, approved, accepted, disbursed | monthly, last 12–24 months | S01, S02, E01, E02 |
| [D2] | Reject reason codes, with each code mapped to *process* or *credit* | per application | S03, S06, E02, E04 |
| [D3] | Cancellations: timestamp, stage at cancel, stated reason | per application | S05, E03 |
| [D4] | Document check failures by document type and channel | per application | S04, E03 |
| [D5] | SLIK result (collectability), recorded for rejected and approved applicants | per application | S06, E04 |
| [D6] | A-score for **every** applicant, including rejected and cancelled | per application | S09, E05 |
| [D7] | Performance of the approved book by A-score band (e.g. 30+ DPD, NPL at 12 months) | band | S09, E05 |
| [D8] | Average ticket size, tenor, yield/NIM on the unsecured personal loan | portfolio | S07, E06 |
| [D9] | Processing effort: analyst minutes per application, cost per hour | estimate | S07, E06 |
| [D10] | Time-to-decision for OCBC (from [D1] timestamps); peer time-to-decision if a credible source exists (published SLA, mystery shop) | median, p90 | S05, E03 |
