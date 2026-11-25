
## S00
- [Title] Recovering lost unsecured-loan approvals at OCBC
- [Subtitle] Three machine-learning fixes to lift the approval rate at flat loss
- [TextBox 5] Graduate Program final presentation / [Your name]  ·  [Date]
- [TextBox 6] Internal - Confidential
- [TextBox 7] ILLUSTRATIVE - DUMMY DATA
- [CoverStat1] +5 pts
- [CoverStat1Sub] approval rate, 38% to 43% (target)
- [CoverStat2] IDR 2 bn
- [CoverStat2Sub] more disbursement a month (target)
- [MLChip] Powered by machine learning
- [NOTES] Open with one sentence: demand for unsecured loans is rising, but our disbursements are not. Today I will show where those applications go, and how three machine-learning fixes can lift our approval rate by 5 points, about IDR 2 bn more disbursement a month, without raising losses.

## S01
- [Title] We lose more good applicants to our own process than to credit risk
- [Kicker] Executive summary
- [DummyTag] ILLUSTRATIVE - DUMMY DATA
- [SumHead0] What is happening
- [SumBody0] Applications grew 34% in 12 months; disbursed loans only 6% / Only 30 of every 100 applications become a loan
- [SumHead1] Why
- [SumBody1] 67% of lost applications never reach credit review (documents, slow decisions) / Internal rules decline 2.8x more applicants than SLIK / 30% of rule-declined applicants score as low-risk as our approved book
- [SumHead2] What we propose
- [SumBody2] 12-week pilot: ML document checker, ML fast-track, ML challenger + A-score / Target: approval rate 38% to 43% (+5 pts), about IDR 2 bn more disbursement a month / At flat loss: guardrails pause the pilot if early losses rise
- [SumDecision] Decision today: approve the pilot, co-owned by Credit Risk and Consumer Lending
- [NOTES] If you remember one slide, make it this one. Demand is there, but our own funnel loses most of it. Three machine-learning fixes can win part of it back without raising losses, and a 12-week pilot will prove it. Today I am asking for approval of that pilot.

## S02
- [Title] Applications grew 34% in 12 months; disbursed loans grew only 6%
- [Kicker] Indexed monthly volume, Dec-25 = 100
- [Source] Source: OCBC loan origination system, Dec-25 to Nov-26
- [DummyTag] ILLUSTRATIVE - DUMMY DATA
- [Tracker] Situation  Problem  Stakes  Answer  Plan
- [Annotation] Demand rose 34%; loans rose 6%
- [NOTES] Applications went from 2,000 to 2,680 a month. Disbursed loans barely moved, from 680 to 721. So demand is not our constraint: something between application and disbursement is.

## S03
- [Title] Approval rate has stuck near 38% for 12 months, despite rising demand
- [Kicker] Approved applications per 100 submitted, monthly (%)
- [Source] Source: OCBC loan origination system, Dec-25 to Nov-26
- [DummyTag] ILLUSTRATIVE - DUMMY DATA
- [Tracker] Situation  Problem  Stakes  Answer  Plan
- [Annotation] Range 37.2% to 38.4% all year: no improvement yet
- [NOTES] Here is the core problem in one line. While applications grew, our approval rate never moved: it stayed between 37.2% and 38.4% every month. Nothing we are doing today is closing the gap to the 43% target, so it will not close by itself.

## S04
- [Title] Only 30 of every 100 applications become a disbursed loan
- [Kicker] Applications remaining at each stage, per 100 submitted (last 12 months)
- [Source] Source: OCBC loan origination system, Dec-25 to Nov-26
- [DummyTag] ILLUSTRATIVE - DUMMY DATA
- [Tracker] Situation  Problem  Stakes  Answer  Plan
- [Annotation] 70 of 100 lost; the biggest drop (28) is invalid documents
- [NOTES] Follow 100 applications through the funnel. Only 30 end up as a loan. The rest of this deck is about the 70 we lose, and which of them we could keep.

## S05
- [Title] Two in three lost applications drop out before credit review, not at it
- [Kicker] The 70 lost applications per 100, by cause
- [Source] Source: OCBC loan origination system, Dec-25 to Nov-26; reason codes mapped to process or credit
- [DummyTag] ILLUSTRATIVE - DUMMY DATA
- [Tracker] Situation  Problem  Stakes  Answer  Plan
- [E03_Invaliddocuments] 28
- [TextBox 8] Invalid documents
- [E03_Cancellations] 19
- [TextBox 10] Cancellations
- [E03_Internalruledeclines] 14
- [TextBox 12] Internal rule declines
- [E03_SLIK] 5
- [TextBox 14] SLIK
- [E03_Nohistory] 4
- [TextBox 16] No history
- [TextBox 17] Process drop-outs: 47 (67%)
- [TextBox 18] Credit declines: 23
- [Annotation] 67% of lost applications never reach credit review
- [NOTES] Of the 70 applications we lose, 47 never reach a credit decision: they fail on documents or the customer cancels. Only the grey part is credit risk doing its job.

## S06
- [Title] Invalid documents cause 60% of process drop-outs, led by payslips
- [Kicker] Share of invalid-document drop-outs, by failing document (%)
- [Source] Source: OCBC loan origination system, Dec-25 to Nov-26
- [DummyTag] ILLUSTRATIVE - DUMMY DATA
- [Tracker] Situation  Problem  Stakes  Answer  Plan
- [EvidenceLine] Invalid documents: 28 of 47 process drop-outs per 100 applications (60%)
- [Annotation] Payslips: 38% of failures. A pre-check at submission targets this
- [NOTES] Payslips alone cause 38% of document failures. Most of these are fixable at submission: a pre-check that tells the customer what is missing before the file enters the queue.

## S07
- [Title] Even complete applicants cancel: our decision takes 7 days, median
- [Kicker] Cancel rate by days from complete application to decision (%)
- [Source] Source: OCBC loan origination system, Dec-25 to Nov-26
- [DummyTag] ILLUSTRATIVE - DUMMY DATA
- [Tracker] Situation  Problem  Stakes  Answer  Plan
- [MedianNote] Median decision time: 7 days (in the 6-8 day bucket)
- [Annotation] Past 8 days, cancel rate reaches 24%+
- [NOTES] Our median decision time is 7 days. Once a customer waits past 8 days, roughly a quarter or more cancel, most likely because another bank answered first. [Add a peer SLA here only if you have a dated source.]

## S08
- [Title] At credit review, internal rules decline 2.8x more applicants than SLIK does
- [Kicker] Credit declines per 100 applications, by reason
- [Source] Source: OCBC loan origination system, Dec-25 to Nov-26; SLIK = OJK credit bureau
- [DummyTag] ILLUSTRATIVE - DUMMY DATA
- [Tracker] Situation  Problem  Stakes  Answer  Plan
- [Annotation] 81% of rule declines have clean SLIK
- [NOTES] SLIK is a hard limit and should stay one. But SLIK declines only 5 in 100. Our own policy rules decline 14, and 81% of those applicants have a clean SLIK record.

## S09
- [Title] The three leaks cost about IDR 2 bn of disbursement every month
- [Kicker] ESTIMATE: recoverable disbursement per month, by leak (IDR bn)
- [Source] Source: OCBC loan origination system, Dec-25 to Nov-26; estimate, method on slide
- [DummyTag] ILLUSTRATIVE - DUMMY DATA
- [Tracker] Situation  Problem  Stakes  Answer  Plan
- [Method] Method (estimate) / Applications a month (2,325) x approval-rate uplift x 79% of approvals disbursed x IDR 22 mn average loan / Uplift (assumed): invalid documents +2.0 pts; cancellations +1.0 pts; rule declines +2.0 pts = +5 pts (38% to 43%) / About 92 extra loans a month / Analyst time: 7,951 h a year on files that later cancel (1.5 h each)
- [NOTES] This is an estimate, and I show the method so you can challenge each input. The uplift per leak is an assumption; together they lift the approval rate 5 points, from 38% to 43%. The pilot measures it.

## S10
- [Title] Loosening rules for everyone would add loans, but also add losses
- [Kicker] The obvious fix, taken seriously
- [DummyTag] ILLUSTRATIVE - DUMMY DATA
- [Tracker] Situation  Problem  Stakes  Answer  Plan
- [ProsText] Why it is tempting / Most volume: +7.0 pts approval rate, IDR 2.8 bn a month / Fast to launch: 2 weeks / No new tooling or process
- [ConsText] Why it fails / Expected loss rises +60 bps (estimate) / Rule declines include bands D and E, where the approved book's bad rate is 5.5% and 9.8% / Moves risk appetite, which needs Credit Risk and Board sign-off
- [Annotation] We need to find the safe subset, not open the gate for everyone
- [NOTES] The obvious answer is to loosen the rules across the board. It is the fastest way to volume, and I want to give it a fair hearing. The problem is that rule declines span every risk band, so loosening everything lets in the riskiest bands too.

## S11
- [Title] 30% of rule-declined applicants score as low-risk as our approved book
- [Kicker] Rule-declined applicants per year, by A-score band (approved-book bad rate in brackets)
- [Source] Source: OCBC loan origination system, Dec-25 to Nov-26; bad rate = 30+ DPD at 12 months on the approved book
- [DummyTag] ILLUSTRATIVE - DUMMY DATA
- [Tracker] Situation  Problem  Stakes  Answer  Plan
- [Annotation] 1,176 applicants (30%) in bands at or below the 2.8% book bad rate
- [TextBox 10] Inferred risk: declined applicants have no repayment record. The pilot tests it.
- [NOTES] The A-score ranks every applicant, including those we declined. 1,176 rule-declined applicants sit in bands A and B, where our approved book's bad rate is at or below the 2.8% average. Caveat: declined applicants have no repayment history, so their risk is inferred from the band. That is why we pilot before changing rules.

## S12
- [Title] We judge four options on volume added, loss, cost and launch time
- [Kicker] Decision criteria, agreed before we look at the options
- [DummyTag] ILLUSTRATIVE - DUMMY DATA
- [Tracker] Situation  Problem  Stakes  Answer  Plan
- [TextBox 9] Volume added
- [TextBox 10] Approval-rate points and disbursement a month on top of today
- [TextBox 14] Expected loss
- [TextBox 15] Must stay flat; risk appetite is not on the table
- [TextBox 19] Cost
- [TextBox 20] Including the cost of doing nothing
- [TextBox 24] Time to launch
- [TextBox 25] How soon we see results
- [NOTES] Before I show the options, here are the four criteria I will judge them on. I am stating them first so the recommendation has to earn its place against them.

## S13
- [Title] ML-assisted fixes lift approval rate 5 points, adding IDR 2 bn monthly (est.)
- [Source] Source: estimates from data/E07 and E09; loss impact from approved-book bad rate by band
- [DummyTag] ILLUSTRATIVE - DUMMY DATA
- [Tracker] Situation  Problem  Stakes  Answer  Plan
- [E09]  | A. Do nothing | B. Process fixes only | C. Loosen rules for all | D. ML + process fixes + A-score (recommended)
- [E09] Approval rate change (est.) | 0 | +3.0 pts | +7.0 pts | +5.0 pts
- [E09] Disbursement added per month (est.) | 0 | IDR 1.2 bn | IDR 2.8 bn | IDR 2.0 bn
- [E09] Expected loss (est.) | Unchanged | Unchanged | +60 bps | Flat (est.; pilot tests it)
- [E09] Cost | IDR 2.0 bn/month forgone | Low | Low | Moderate (ML build + pilot)
- [E09] Time to launch | - | 4-6 weeks | 2 weeks | 8-12 weeks
- [Falsifier] What would change our mind: if the back-test shows rule-declined applicants in bands A-B default above the approved book's rate, or if SLIK, not internal rules, drives most credit declines.
- [Derivation] Disbursement = applications a month x approval uplift x 79% disbursed x IDR 22 mn average loan (data/E07). Estimates; the pilot measures them.
- [NOTES] Option D is the only one that adds meaningful volume without moving expected loss. Option C adds more, but at a cost in loss we do not want. Doing nothing is not free: we forgo about IDR 2 bn of disbursement every month.

## S14
- [Title] Three ML models close the three leaks; credit officers keep the final say
- [Kicker] One model per leak, each with an estimated approval-rate lift
- [DummyTag] ILLUSTRATIVE - DUMMY DATA
- [Tracker] Situation  Problem  Stakes  Answer  Plan
- [MLStage0] AT SUBMISSION
- [MLName0] ML document checker
- [MLWhat0] Reads payslips, bank statements and KTP at upload; flags missing or invalid items before the queue
- [MLTech0] OCR + document classifier
- [MLLift0] +2.0 pts
- [MLStage1] IN THE QUEUE
- [MLName1] ML fast-track
- [MLWhat1] Routes complete, low-risk files to an express decision, so fewer applicants cancel while waiting
- [MLTech1] Gradient-boosted routing model
- [MLLift1] +1.0 pts
- [MLStage2] AT CREDIT REVIEW
- [MLName2] ML challenger model
- [MLWhat2] Re-scores rule-declined applicants with A-score, SLIK and application data; low-risk ones go to an officer
- [MLTech2] Gradient boosting, champion vs challenger
- [MLLift2] +2.0 pts
- [GovHead0] People decide
- [GovBody0] Credit officers approve every ML-referred case
- [GovHead1] Monitored
- [GovBody1] Drift checks and a monthly back-test against actual repayments
- [GovHead2] Governed
- [GovBody2] Explainable reason codes; model-risk review before go-live
- [NOTES] Here is how the machine learning works. One model per leak. The document checker reads uploads and flags problems before the file enters the queue. The fast-track model sends complete, low-risk files to an express decision, so fewer applicants give up waiting. The challenger model re-scores applicants our rules declined, using the A-score plus bureau and application data, and sends the low-risk ones to a credit officer. No model approves a loan on its own.

## S15
- [Title] The business should focus on documents and rule declines first: 4 of 5 points
- [Kicker] Three moves, ranked by approval-rate impact, each with one owner and one weekly KPI
- [DummyTag] ILLUSTRATIVE - DUMMY DATA
- [Tracker] Situation  Problem  Stakes  Answer  Plan
- [FocusRank0] 1
- [FocusMove0] Fix documents at submission
- [FocusLever0] ML document checker at submission
- [FocusOwner0] Owner / Operations + Digital
- [FocusKPI0] Weekly KPI / Invalid-document rate
- [FocusPts0] +2.0 pts
- [FocusRank1] 2
- [FocusMove1] Re-score rule declines
- [FocusLever1] ML challenger model + A-score review
- [FocusOwner1] Owner / Credit Risk
- [FocusKPI1] Weekly KPI / Approvals from re-scored declines
- [FocusPts1] +2.0 pts
- [FocusRank2] 3
- [FocusMove2] Decide faster
- [FocusLever2] ML fast-track for low-risk complete files
- [FocusOwner2] Owner / Consumer Lending operations
- [FocusKPI2] Weekly KPI / Median days to decision
- [FocusPts2] +1.0 pts
- [FocusNote] Owners are proposed; confirm with each function before presenting. Point lifts are estimates (data/E07).
- [NOTES] The opportunity is there. What matters now is focus. Two moves, fixing documents at submission and re-scoring rule declines, deliver 4 of the 5 points, so they get our best people first. Speed is the third move. Each has one owner and one number we track every week.

## S16
- [Title] A 12-week pilot on one segment proves it before any permanent rule change
- [Kicker] Pilot segment: salaried applicants, digital channel. Four workstreams, one per proposed solution
- [DummyTag] ILLUSTRATIVE - DUMMY DATA
- [Tracker] Situation  Problem  Stakes  Answer  Plan
- [Workplan] Workstream | What we do | Weeks | Output
- [Workplan] 1. Diagnostics and data | Funnel dashboard by stage and reason code; build the labelled data set for the models | 1-2 | Weekly leak report
- [Workplan] 2. ML document checker | Pre-check uploads; call back pending and incomplete files | 2-12 | Fewer invalid documents
- [Workplan] 3. ML fast-track + rule relook | Express route for low-risk files; review rules that decline clean-SLIK applicants | 2-8 | Shorter decision time; rule-change candidates
- [Workplan] 4. ML challenger + A-score | Re-score rule declines; bands A-B to manual review, capped volume | 4-12 | Approvals and early DPD vs control
- [NOTES] The four workstreams are the four solutions I started from. Each produces a measurable output, so by week 12 we have measured evidence instead of estimates.

## S17
- [Title] Three guardrails stop the pilot if early losses rise
- [Kicker] Pre-agreed triggers: we pause first and discuss second
- [DummyTag] ILLUSTRATIVE - DUMMY DATA
- [Tracker] Situation  Problem  Stakes  Answer  Plan
- [TextBox 10] Loss trigger
- [TextBox 11] Pause if 30+ DPD on pilot approvals exceeds the approved book's rate for the same band
- [TextBox 16] Volume cap
- [TextBox 17] Pilot approvals capped at a fixed monthly limit agreed with Credit Risk
- [TextBox 22] Compliance
- [TextBox 23] SLIK declines stay hard; OJK/POJK review before any permanent rule change
- [NOTES] These guardrails are what make the pilot safe to say yes to. If early delinquency rises, we stop automatically, before any lasting change to policy.

## S18
- [Title] Decision today: approve the pilot, co-owned by Credit Risk and Consumer Lending
- [DummyTag] ILLUSTRATIVE - DUMMY DATA
- [Tracker] Situation  Problem  Stakes  Answer  Plan
- [Ask] Approve a 12-week pilot of three ML models (document checker, fast-track, challenger) with A-score review of rule-based declines, co-owned by Credit Risk and Consumer Lending, starting [January 2027].
- [AskHead0] What you approve
- [AskBody0] 12 weeks, one segment: salaried applicants, digital channel / Team: 1 data scientist, 2 analysts, 1 credit reviewer (assumed) / No policy change; SLIK stays a hard limit
- [AskHead1] What you get (est.)
- [AskBody1] Approval rate +5 pts (38% to 43%) / About IDR 2 bn more disbursement a month / Fewer of the ~8,000 analyst-hours a year lost to cancelled files
- [AskHead2] When you will know
- [AskBody2] Week 2: first weekly leak report / Week 6: models running in shadow mode / Week 12: go / no-go, with measured loss
- [NOTES] This is the one thing I am asking for today. It is small, reversible, and measured: 1 data scientist, 2 analysts and 1 credit reviewer for 12 weeks, no policy change, and a go / no-go decision at the end with real loss data.

## S19
- [Title] Each month of waiting forgoes IDR 2 bn disbursement; the pilot caps the risk
- [Kicker] Key takeaways
- [DummyTag] ILLUSTRATIVE - DUMMY DATA
- [Tracker] Situation  Problem  Stakes  Answer  Plan
- [TkNum0] 1
- [TkHead0] The leak is ours to fix
- [TkBody0] 67% of lost applications never reach credit review
- [TkNum1] 2
- [TkHead1] A safe subset exists, and ML finds it
- [TkBody1] 30% of rule-declined applicants score as low-risk as our approved book
- [TkNum2] 3
- [TkHead2] The bet is lopsided
- [TkBody2] Small, capped and reversible downside against a measured upside
- [RiskHead] What we risk
- [RiskBody] 12 weeks, one segment / 4 people (assumed) / Capped volume, pause triggers / No policy change: fully reversible
- [RewardHead] What we gain (est.)
- [RewardBody] Approval rate +5 pts (38% to 43%) / About IDR 2 bn more disbursement a month / Fewer hours lost to cancelled files / Measured evidence for any rule change
- [CloseBar] Cost of waiting: about IDR 2 bn of disbursement a month (est.).  Today: approve the pilot.  Week 2: first leak report.
- [NOTES] Let me close with three things to remember. First, this leak is ours to fix: most lost applications never reach a credit decision. Second, a safe subset exists, and machine learning with the A-score can find it. Third, the bet is lopsided: we risk 12 weeks and 4 people under pause triggers, against an estimated 5-point lift in approval rate. Every month we wait costs about IDR 2 bn of disbursement. So my question is simple: can we start the pilot, and can I bring you the first leak report in two weeks?

## S20
- [Title] Appendix: the issue tree behind the analysis
- [Kicker] Every lost application leaves through exactly one branch
- [DummyTag] ILLUSTRATIVE - DUMMY DATA
- [NOTES] Use this in Q&A when someone asks whether we considered a cause.
