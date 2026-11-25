# Talk track: the storyline in plain words (about 18 minutes; leave the closing slide on screen during Q&A)

**One sentence to remember:** our approval rate has been stuck near 38% all year, and three machine-learning
fixes can lift it 5 points, about IDR 2 bn more disbursement a month, without raising losses.

**The ask, word for word:** "Approve a 12-week pilot of three ML models (document checker, fast-track,
challenger) with A-score review of rule-based declines, co-owned by Credit Risk and Consumer Lending."

| # | Slide | What you say (one line) | Bridge to the next slide |
|---|---|---|---|
| 1 | Cover | "+5 points of approval rate, IDR 2 bn a month, powered by ML." | "Here's the whole story on one page." |
| 2 | Executive summary | "If you remember one slide, it's this one." | "Let me show you how we got here." |
| 3 | 34% vs 6% | "Demand is not our problem." | "And our approval rate hasn't moved." |
| 4 | Stuck at 38% | "Twelve months, no improvement. It won't close by itself." | "So where do the applications go?" |
| 5 | 30 of 100 | "We lose 70 of every 100." | "But most are not lost to credit risk." |
| 6 | Two in three before review | "Most losses happen before anyone looks at credit." | "The biggest leak is documents." |
| 7 | Documents, payslips | "One document drives most failures, and it's fixable at submission." | "But even complete applicants leave." |
| 8 | 7-day decision | "The longer they wait, the more they cancel." | "And at credit review…" |
| 9 | Rules vs SLIK | "Our own rules decline nearly 3x more than the bureau does." | "What does that cost us?" |
| 10 | IDR 2 bn a month | "Here's the price, and the method so you can challenge it." | "The obvious fix is to loosen rules." |
| 11 | Loosening fails | "It's fast, but it lets in the riskiest bands too." | "But there is a safer subset." |
| 12 | 30% low-risk | "The A-score finds declined applicants as safe as our book." | "So how do we choose?" |
| 13 | Criteria | "Four criteria, agreed before we look at options." | "Here are the options." |
| 14 | Options matrix | "Only option D adds 5 points without adding loss." | "Here's how the ML works." |
| 15 | Three ML models | "One model per leak. No model approves a loan on its own." | "So where should the business focus first?" |
| 16 | Business focus | "Two moves give 4 of the 5 points; they get our best people first." | "We prove it before changing any rule." |
| 17 | 12-week pilot | "Four workstreams, each with a weekly output." | "And if it goes wrong?" |
| 18 | Guardrails | "We pause first and discuss second." | "So here is my ask." |
| 19 | Decision | "Small, reversible, measured. Here's exactly what I'm asking for." | "Let me leave you with three things." |
| 20 | Key takeaways (close) | "The leak is ours to fix, ML finds the safe subset, and the bet is lopsided. Every month we wait costs about IDR 2 bn of disbursement." | Ask: "Can we start the pilot, and can I bring you the first leak report in two weeks?" Then stop talking and wait. |

## Questions to expect
- **"Where do these numbers come from?"** Name the report or SQL table behind each one. Every number in the deck lives in `data/`. The calculated ones are in `data/derived.csv`, with their formulas.
- **"Why ML and not just new rules?"** Rules are blunt: they decline whole groups. A model ranks individual applicants, so we can approve the safe ones inside a declined group. A credit officer still decides every referred case.
- **"Is the model explainable and compliant?"** Every decision carries reason codes. The model goes through model-risk review before go-live, and it runs in shadow mode first (week 6).
- **"How do you know declined applicants are safe?"** We don't yet. Their risk is inferred from the A-score band, and the pilot measures it. Say this before they ask.
- **"Why has approval rate not improved until now?"** Our fixes have been rule changes and campaigns. None targets the three leaks directly, and nothing measured them weekly.
- **"What resources do you need?"** 1 data scientist, 2 analysts and 1 credit reviewer for 12 weeks (confirm with your manager).

⚠️ All numbers are **dummy** until you replace the CSVs in `data/` and run `python3 build_deck.py`. The +5 pts and IDR 2 bn are your targets. The split across levers and the IDR 22 mn average loan are assumptions.
