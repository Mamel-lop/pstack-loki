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

# E07: impact bridge (EST). Author's target: approval rate +5 percentage points (38% -> 43%)
# and about IDR 2 bn more disbursement a month. Lever split and ticket size are ASSUMPTIONS.
ticket_mn, hours_per_cancel = 22, 1.5
apps_month = total_apps / 12
disb_per_approved = 30 / 38                      # from E02: disbursed / approved
levers = [  # (leak, ML lever, approval uplift in percentage points)
    ("Invalid documents", "ML document checker at submission", 2.0),
    ("Cancellations", "ML fast-track for low-risk complete files", 1.0),
    ("Rule declines", "ML challenger model + A-score review", 2.0),
]
e07 = []
for leak, lever, pp in levers:
    approvals = apps_month * pp / 100
    loans = approvals * disb_per_approved
    hrs = round(total_apps * 19 / 100 * hours_per_cancel) if leak == "Cancellations" else 0
    e07.append([leak, lever, pp, round(apps_month), round(approvals, 1), round(disb_per_approved, 3),
                round(loans, 1), ticket_mn, round(loans * ticket_mn / 1000, 2), hrs, hours_per_cancel])
write("E07.csv", ["leak", "ml_lever", "approval_uplift_pp", "applications_per_month", "extra_approvals_per_month",
                  "disbursed_per_approved", "extra_loans_per_month", "avg_ticket_idr_mn",
                  "disbursement_idr_bn_per_month", "analyst_hours_per_year", "hours_per_cancelled_file"], e07)


def disb_bn(pp):
    return round(apps_month * pp / 100 * disb_per_approved * ticket_mn / 1000, 1)


# E09: options matrix (EST)
write("E09.csv", ["criterion", "A_do_nothing", "B_process_only", "C_loosen_all", "D_ml_process_ascore"], [
    ["Approval rate change", "0", "+3.0 pts", "+7.0 pts", "+5.0 pts"],
    ["Disbursement added per month", "0", f"IDR {disb_bn(3.0)} bn", f"IDR {disb_bn(7.0)} bn", f"IDR {disb_bn(5.0)} bn"],
    ["Expected loss", "Unchanged", "Unchanged", "+60 bps", "Flat (est.; pilot tests it)"],
    ["Cost", f"IDR {disb_bn(5.0)} bn/month forgone", "Low", "Low", "Moderate (ML build + pilot)"],
    ["Time to launch", "-", "4-6 weeks", "2 weeks", "8-12 weeks"],
])
loans_total = round(sum(r[6] for r in e07), 1)
# Pilot resourcing (ASSUMPTION, to be agreed with Credit Risk / Consumer Lending)
write("pilot.csv", ["item", "value"], [
    ["weeks", 12], ["data_scientists", 1], ["analysts", 2], ["credit_reviewers", 1], ["segment", "Salaried applicants, digital channel"],
    ["start", "January 2027"]])
print("dummy data written; apps/yr =", total_apps, "; extra loans/month =", loans_total, "; IDR bn/month =", disb_bn(5.0))

# E11: monthly approval rate (approved per 100 submitted), flat all year (DUMMY)
rates = [37.6, 38.1, 37.2, 38.4, 37.9, 38.0, 37.5, 38.3, 37.8, 38.2, 37.7, 38.1]
write("E11.csv", ["month", "approval_rate_pct", "target_pct"], [[m, r, 43] for m, r in zip(months, rates)])
