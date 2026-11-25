# Talk track: the storyline in plain words (about 15 minutes)

**One sentence to remember:** we lose more good applicants to our own process than to credit risk,
and a safe, measured pilot can win part of them back.

**The ask, word for word:** "Approve a 12-week pilot of document pre-check, a decision-time SLA, and A-score
review of rule-based declines, co-owned by Credit Risk and Consumer Lending."

| # | Slide | What you say (one line) | Bridge to the next slide |
|---|---|---|---|
| 1 | Executive summary | "If you remember one slide, it's this one." | "Let me show you how we got here." |
| 2 | 34% vs 6% | "Demand is not our problem." | "So where do the applications go?" |
| 3 | 30 of 100 | "We lose 70 of every 100." | "But most are not lost to credit risk." |
| 4 | Two in three before review | "Most losses happen before anyone looks at credit." | "The biggest leak is documents." |
| 5 | Documents, payslips | "One document drives most failures, and it's fixable at submission." | "But even complete applicants leave." |
| 6 | 7-day decision | "The longer they wait, the more they cancel." | "And at credit review…" |
| 7 | Rules vs SLIK | "Our own rules decline nearly 3x more than the bureau does." | "What does all this cost us?" |
| 8 | IDR 35 bn | "Here's the price, and here's the method so you can challenge it." | "The obvious fix is to loosen rules." |
| 9 | Loosening fails | "It's fast, but it lets in the riskiest bands too." | "But there is a safer subset." |
| 10 | 30% low-risk | "The A-score finds declined applicants as safe as our book." | "So how do we choose what to do?" |
| 11 | Criteria | "Four criteria, agreed before we look at options." | "Here are the options." |
| 12 | Options matrix | "Only option D adds loans without adding loss." | "We prove it before changing any rule." |
| 13 | 12-week pilot | "Four workstreams: the four fixes I started with." | "And if it goes wrong?" |
| 14 | Guardrails | "We pause first and discuss second." | "So here is my ask." |
| 15 | Decision | "Small, reversible, measured. Can I have your approval?" | — |

## Questions to expect
- **"Where do these numbers come from?"** Name the report or SQL table behind each one. Every number in the deck lives in `data/`. The calculated ones are in `data/derived.csv`, with their formulas.
- **"Isn't loosening rules risky?"** Yes. That's why slide 9 rejects it, and slide 14 shows the guardrails.
- **"How do you know declined applicants are safe?"** We don't yet. Their risk is inferred from the A-score band, and the pilot measures it. Say this before they ask.
- **"Is 7 days slow?"** Have a competitor benchmark ready if you can find a dated source; otherwise say the pilot measures our own cancel rate against waiting time.
- **"What resources do you need?"** 2 analysts and 1 credit reviewer for 12 weeks (confirm this with your manager before presenting).

⚠️ All numbers are **dummy** until you replace the CSVs in `data/` and run `python3 build_deck.py`.
