"""Write ILLUSTRATIVE DUMMY data into data/E##.csv.

Every number here is invented so the deck can be built and reviewed.
Replace each CSV with the real pull (see dump.md data inventory) before presenting.
"""
import csv
from pathlib import Path

D = Path(__file__).parent / "data"


def write(name, header, rows):
    with open(D / name, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(header)
        w.writerows(rows)


# E01: monthly applications vs disbursed (last 12 months)
months = ["Dec-25", "Jan-26", "Feb-26", "Mar-26", "Apr-26", "May-26",
          "Jun-26", "Jul-26", "Aug-26", "Sep-26", "Oct-26", "Nov-26"]
rows = []
for i, m in enumerate(months):
    apps = round(2000 * 1.34 ** (i / 11))
    disb = round(680 * 1.06 ** (i / 11))
    rows.append([m, apps, disb, round(apps / 2000 * 100, 1), round(disb / 680 * 100, 1)])
write("E01.csv", ["month", "applications", "disbursed", "applications_index", "disbursed_index"], rows)
total_apps = sum(r[1] for r in rows)

# E02: funnel per 100 applications (last 12 months)
write("E02.csv", ["stage", "per_100_applications"], [
    ["Submitted", 100], ["Complete documents", 72], ["Credit reviewed", 61],
    ["Approved", 38], ["Accepted by customer", 33], ["Disbursed", 30]])

# E03: the 70 lost applications per 100, by cause
lost = [["process", "Invalid documents", 28], ["process", "Cancellations", 19],
        ["credit", "Internal rule declines", 14], ["credit", "SLIK", 5],
        ["credit", "No history", 4]]
tot = sum(r[2] for r in lost)
write("E03.csv", ["cause_group", "cause", "lost_per_100", "pct_of_lost"],
      [r + [round(r[2] / tot * 100)] for r in lost])

# E04: document failures by type (share of invalid-document drop-outs)
write("E04.csv", ["document_type", "pct_of_doc_failures"], [
    ["Payslip", 38], ["Bank statement", 24], ["ID card (KTP)", 14],
    ["Tax ID (NPWP)", 12], ["Employment letter", 8], ["Other", 4]])

# E05: cancel rate by days-to-decision bucket
write("E05.csv", ["days_to_decision_bucket", "cancel_rate_pct", "median_days"], [
    ["0-2", 4, 7], ["3-5", 8, 7], ["6-8", 15, 7], ["9-11", 24, 7], ["12+", 31, 7]])

# E06: credit declines per 100 applications, by reason
write("E06.csv", ["decline_reason", "per_100_applications", "clean_slik_pct"], [
    ["Internal policy rules", 14, 81], ["SLIK (collectability 2+)", 5, 0],
    ["Thin or no credit history", 4, ""]])

# E08: rule-declined applicants by A-score band, with approved-book bad rate
write("E08.csv", ["ascore_band", "rule_declined_count", "approved_bad_rate_pct", "book_avg_bad_rate_pct"], [
    ["A (lowest risk)", 480, 1.2, 2.8], ["B", 696, 2.0, 2.8], ["C", 980, 3.1, 2.8],
    ["D", 1000, 5.5, 2.8], ["E (highest risk)", 764, 9.8, 2.8]])

# E07: forgone interest by leak (EST). Recoverable share is an assumption.
ticket_mn, yield_pct, hours_per_cancel = 60, 14, 1.5
leaks = [("Invalid documents", 28, 25), ("Cancellations", 19, 20)]
e07 = []
for name, per100, rec in leaks:
    lost_n = round(total_apps * per100 / 100)
    loans = round(lost_n * rec / 100)
    hrs = round(lost_n * hours_per_cancel) if name == "Cancellations" else 0
    e07.append([name, lost_n, rec, loans, ticket_mn, yield_pct,
                round(loans * ticket_mn * yield_pct / 100 / 1000, 1), hrs, hours_per_cancel])
rule_declines = round(total_apps * 14 / 100)
low_risk_share = round((480 + 696) / (480 + 696 + 980 + 1000 + 764) * 100)
loans = round(rule_declines * low_risk_share / 100)
e07.append(["Rule declines (low-risk A-score)", rule_declines, low_risk_share, loans,
            ticket_mn, yield_pct, round(loans * ticket_mn * yield_pct / 100 / 1000, 1), 0, hours_per_cancel])
write("E07.csv", ["leak", "lost_applications_per_year", "recoverable_pct", "recoverable_loans",
                  "avg_ticket_idr_mn", "yield_pct", "forgone_interest_idr_bn", "analyst_hours", "hours_per_cancelled_file"], e07)
loans_total = sum(r[3] for r in e07)

# E09: options matrix
b = round((e07[0][3] + e07[1][3]) / 12)
d = round(loans_total / 12)
idr = round(sum(r[6] for r in e07))
write("E09.csv", ["criterion", "A_do_nothing", "B_process_only", "C_loosen_all", "D_process_plus_ascore"], [
    ["Loans added per month", "0", f"+{b}", "+420", f"+{d}"],
    ["Expected loss", "Unchanged", "Unchanged", "+60 bps", "Flat (est.; pilot tests it)"],
    ["Cost", f"IDR {idr} bn/yr forgone", "Low", "Low", "Moderate"],
    ["Time to launch", "-", "4-6 weeks", "2 weeks", "8-12 weeks"],
])
print("dummy data written; total applications/yr =", total_apps, "; loans recoverable =", loans_total)
