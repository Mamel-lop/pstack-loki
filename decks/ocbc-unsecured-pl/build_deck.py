"""Build deck.pptx from storyline + exhibit specs + data/E##.csv (loki-build, single worker).

Numbers on slides come only from data/*.csv. With dummy data present, every slide
carries an "ILLUSTRATIVE - DUMMY DATA" tag (set DUMMY = False once real data is in).
Titles below are the storyline ladder with the dummy numbers filled in; when the real
data arrives, update the [TK] values in the titles to match the new CSVs.
"""
import csv
import charts
from pathlib import Path

from pptx import Presentation
from pptx.chart.data import CategoryChartData
from pptx.dml.color import RGBColor
from pptx.enum.chart import XL_CHART_TYPE, XL_LABEL_POSITION
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.util import Inches, Pt

DUMMY = True
HERE = Path(__file__).parent
RED = RGBColor(0xE2, 0x23, 0x1A)
INK = RGBColor(0x1F, 0x1F, 0x1F)
MUTED = RGBColor(0x6E, 0x6E, 0x6E)
GREY = RGBColor(0xBF, 0xBF, 0xBF)
LIGHT = RGBColor(0xF2, 0xF2, 0xF2)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
FONT = "Arial"
ACTS = ["Situation", "Problem", "Stakes", "Answer", "Plan"]


DERIVED = []


def derive(key, value, formula):
    """Record every number computed from CSV cells, so each has a home (Law 4)."""
    DERIVED.append((key, value, formula))
    return value


def data(eid):
    with open(HERE / "data" / f"{eid}.csv") as f:
        return list(csv.DictReader(f))


prs = Presentation()
prs.slide_width, prs.slide_height = Inches(13.333), Inches(7.5)
BLANK = prs.slide_layouts[6]


def text(slide, x, y, w, h, s, size=14, bold=False, color=INK, align=PP_ALIGN.LEFT,
         anchor=MSO_ANCHOR.TOP, name=None):
    tb = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    if name:
        tb.name = name
    tf = tb.text_frame
    tf.word_wrap = True
    tf.vertical_anchor = anchor
    tf.margin_left = tf.margin_right = Inches(0.05)
    lines = s if isinstance(s, list) else [s]
    for i, line in enumerate(lines):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.alignment = align
        r = p.add_run()
        r.text = line
        r.font.size, r.font.bold, r.font.name = Pt(size), bold, FONT
        r.font.color.rgb = color
        p.space_after = Pt(6)
    return tb


def rect(slide, x, y, w, h, fill, name=None):
    s = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(x), Inches(y), Inches(w), Inches(h))
    s.fill.solid()
    s.fill.fore_color.rgb = fill
    s.line.fill.background()
    s.shadow.inherit = False
    if name:
        s.name = name
    return s


def slide(title, act, kicker=None, source=None, notes="", tag=None):
    s = prs.slides.add_slide(BLANK)
    text(s, 0.6, 0.4, 12.1, 1.15, title, 28, True, INK, anchor=MSO_ANCHOR.BOTTOM, name="Title")
    rect(s, 0.6, 1.62, 1.2, 0.06, RED, "TitleRule")
    if kicker:
        text(s, 0.6, 1.78, 12.1, 0.45, kicker, 16, False, MUTED, name="Kicker")
    if source:
        text(s, 0.6, 6.92, 6.5, 0.35, source, 9, False, MUTED, name="Source")
    if DUMMY or tag:
        tb_ = rect(s, 7.35, 6.97, 2.3, 0.28, MUTED if tag else RED, "DummyTag")
        tf = tb_.text_frame
        tf.margin_top = tf.margin_bottom = 0
        p = tf.paragraphs[0]
        p.alignment = PP_ALIGN.CENTER
        r = p.add_run()
        r.text = tag or "ILLUSTRATIVE - DUMMY DATA"
        r.font.size, r.font.bold, r.font.name = Pt(9), True, FONT
        r.font.color.rgb = WHITE
    if act:
        tb = text(s, 9.9, 6.92, 2.85, 0.35, "", 9, name="Tracker", align=PP_ALIGN.RIGHT)
        p = tb.text_frame.paragraphs[0]
        p.runs[0].text = ""
        for i, a in enumerate(ACTS):
            r = p.add_run()
            r.text = a + ("  " if i < len(ACTS) - 1 else "")
            r.font.size, r.font.name = Pt(9), FONT
            r.font.bold = a == act
            r.font.color.rgb = RED if a == act else GREY
    s.notes_slide.notes_text_frame.text = notes
    return s


def style_chart(chart, labels=True, fmt='0', value_axis=False, size=12):
    chart.has_legend = False
    chart.has_title = False
    chart.font.name, chart.font.size = FONT, Pt(size)
    chart.font.color.rgb = INK
    va = chart.value_axis
    va.has_major_gridlines = False
    va.visible = value_axis
    va.format.line.fill.background()
    ca = chart.category_axis
    ca.format.line.color.rgb = GREY
    ca.tick_labels.font.size = Pt(size)
    if labels:
        plot = chart.plots[0]
        plot.has_data_labels = True
        dl = plot.data_labels
        dl.number_format, dl.number_format_is_linked = fmt, False
        dl.font.size, dl.font.bold = Pt(size), True


def color_points(series, colors):
    for i, c in enumerate(colors):
        pt = series.points[i]
        pt.format.fill.solid()
        pt.format.fill.fore_color.rgb = c


def bar_chart(s, x, y, w, h, cats, vals, accents, kind=XL_CHART_TYPE.BAR_CLUSTERED, fmt='0',
              name="Exhibit", gap=60):
    """Chart rendered as an image (see charts.py) so it shows in every viewer."""
    f = {'0': "int", '0"%"': "pct", '#,##0': "int", '0.0"%"': "pct1"}[fmt]
    path = charts.bars(name, w, h, cats, vals, accents, horizontal=kind == XL_CHART_TYPE.BAR_CLUSTERED, fmt=f)
    pic = s.shapes.add_picture(str(path), Inches(x), Inches(y), Inches(w), Inches(h))
    pic.name = name
    return pic


def icon(s, name, x, y, size=0.6, red=True):
    """Lucide icon (ISC licence) on a round badge."""
    c = s.shapes.add_shape(MSO_SHAPE.OVAL, Inches(x), Inches(y), Inches(size), Inches(size))
    c.fill.solid()
    c.fill.fore_color.rgb = RGBColor(0xFD, 0xE8, 0xE7) if red else LIGHT
    c.line.fill.background()
    c.shadow.inherit = False
    c.name = f"bg-badge-{name}"
    pad = size * 0.2
    p_ = s.shapes.add_picture(str(HERE / "icons" / f"{name}-{'red' if red else 'ink'}.png"),
                              Inches(x + pad), Inches(y + pad), Inches(size - 2 * pad), Inches(size - 2 * pad))
    p_.name = f"bg-icon-{name}"


def callout(s, x, y, w, h, s_text, name="Annotation"):
    rect(s, x, y, 0.06, h, RED, name + "Bar")
    return text(s, x + 0.15, y, w - 0.15, h, s_text, 14, True, RED, anchor=MSO_ANCHOR.MIDDLE, name=name)


def table(s, x, y, w, rows, col_w=None, hl_col=None, size=12, row_h=0.5, name="Table"):
    nr, nc = len(rows), len(rows[0])
    gf = s.shapes.add_table(nr, nc, Inches(x), Inches(y), Inches(w), Inches(row_h * nr))
    gf.name = name
    t = gf.table
    if col_w:
        for i, cw in enumerate(col_w):
            t.columns[i].width = Inches(cw)
    for r in range(nr):
        t.rows[r].height = Inches(row_h)
        for c in range(nc):
            cell = t.cell(r, c)
            cell.margin_left = cell.margin_right = Inches(0.08)
            cell.vertical_anchor = MSO_ANCHOR.MIDDLE
            hl = hl_col is not None and c == hl_col
            cell.fill.solid()
            if r == 0:
                cell.fill.fore_color.rgb = RED if hl else INK
            else:
                cell.fill.fore_color.rgb = RGBColor(0xFD, 0xE8, 0xE7) if hl else (WHITE if r % 2 else LIGHT)
            tf = cell.text_frame
            tf.word_wrap = True
            tf.paragraphs[0].text = ""
            run = tf.paragraphs[0].add_run()
            run.text = str(rows[r][c])
            run.font.name, run.font.size = FONT, Pt(size)
            run.font.bold = r == 0 or c == 0 or hl
            run.font.color.rgb = WHITE if r == 0 else (RED if hl else INK)
    return t


# ---------------------------------------------------------------- data
e01, e02, e03, e04 = data("E01"), data("E02"), data("E03"), data("E04")
e05, e06, e07, e08, e09 = data("E05"), data("E06"), data("E07"), data("E08"), data("E09")
SRC = "Source: OCBC loan origination system, Dec-25 to Nov-26"

# ---------------------------------------------------------------- S00 cover
s = prs.slides.add_slide(BLANK)
rect(s, 0, 0, 0.35, 7.5, RED, "CoverBand")
text(s, 1.0, 2.0, 11.0, 1.6, "Recovering lost unsecured-loan approvals at OCBC", 40, True, INK,
     anchor=MSO_ANCHOR.BOTTOM, name="Title")
rect(s, 1.0, 3.75, 1.5, 0.07, RED)
text(s, 1.0, 3.95, 11.0, 0.5,
     "Where applications leak, what it costs, and a pilot to recover them at flat loss", 20, False, MUTED)
text(s, 1.0, 5.6, 11.0, 0.9, ["Graduate Program final presentation", "[Your name]  ·  [Date]"], 14, False, INK)
text(s, 1.0, 6.8, 6, 0.4, "Internal - Confidential", 9, False, MUTED)
if DUMMY:
    text(s, 7.5, 6.8, 5.3, 0.4, "ILLUSTRATIVE - DUMMY DATA, NOT FOR DECISION", 10, True, RED, PP_ALIGN.RIGHT)
s.notes_slide.notes_text_frame.text = (
    "Open with one sentence: demand for unsecured loans is rising, but our disbursements are not. "
    "Today I will show where those applications go, what that costs us, and a pilot to win part of it back.")

# ---------------------------------------------------------------- S01
a0, a1 = e01[0], e01[-1]
g_app = derive("S01 application growth %", round(float(a1["applications_index"]) - 100), "E01 applications_index[last] - 100")
g_dis = derive("S01 disbursed growth %", round(float(a1["disbursed_index"]) - 100), "E01 disbursed_index[last] - 100")
s = slide(f"Applications grew {g_app}% in 12 months; disbursed loans grew only {g_dis}%", "Situation",
          "Indexed monthly volume, Dec-25 = 100", SRC,
          f"Applications went from {int(a0['applications']):,} to {int(a1['applications']):,} a month. Disbursed loans "
          f"barely moved, from {int(a0['disbursed']):,} to {int(a1['disbursed']):,}. So demand is not our constraint: "
          "something between application and disbursement is.")
path = charts.lines("E01", 9.4, 4.5, [r["month"] for r in e01],
                    [("Applications", [float(r["applications_index"]) for r in e01], True),
                     ("Disbursed loans", [float(r["disbursed_index"]) for r in e01], False)],
                    90, 140, "Index (Dec-25 = 100); axis starts at 90")
s.shapes.add_picture(str(path), Inches(0.6), Inches(2.3), Inches(9.4), Inches(4.5)).name = "E01"
callout(s, 10.3, 3.2, 2.5, 1.4, f"Demand rose {g_app}%; loans rose {g_dis}%")

# ---------------------------------------------------------------- S02
disb = int(e02[-1]["per_100_applications"])
s = slide(f"Only {disb} of every 100 applications become a disbursed loan", "Situation",
          "Applications remaining at each stage, per 100 submitted (last 12 months)", SRC,
          f"Follow 100 applications through the funnel. Only {disb} end up as a loan. "
          "The rest of this deck is about the 70 we lose, and which of them we could keep.")
bar_chart(s, 0.6, 2.3, 9.4, 4.5, [r["stage"] for r in e02], [int(r["per_100_applications"]) for r in e02],
          [len(e02) - 1], name="E02", gap=40)
drops = [(e02[i]["stage"], int(e02[i - 1]["per_100_applications"]) - int(e02[i]["per_100_applications"]))
         for i in range(1, len(e02))]
big = max(drops, key=lambda d: d[1])
derive("S02 lost per 100", 100 - disb, "100 - E02 Disbursed")
derive("S02 biggest drop", big[1], f"E02 stage before '{big[0]}' minus '{big[0]}'")
callout(s, 10.3, 3.0, 2.5, 1.6, f"{100 - disb} of 100 lost; the biggest drop ({big[1]}) is invalid documents")

# ---------------------------------------------------------------- S03
proc = sum(int(r["lost_per_100"]) for r in e03 if r["cause_group"] == "process")
lost = sum(int(r["lost_per_100"]) for r in e03)
derive("S03 process drop-outs per 100", proc, "sum E03 lost_per_100 where cause_group=process")
derive("S03 lost per 100", lost, "sum E03 lost_per_100")
derive("S03 credit declines per 100", lost - proc, "S03 lost - S03 process")
derive("S03 process share %", round(proc / lost * 100), "process / lost x 100")
s = slide("Two in three lost applications drop out before credit review, not at it", "Problem",
          f"The {lost} lost applications per 100, by cause", SRC + "; reason codes mapped to process or credit",
          f"Of the {lost} applications we lose, {proc} never reach a credit decision: they fail on documents "
          "or the customer cancels. Only the grey part is credit risk doing its job.")
x0, y0, W, H = 0.6, 3.1, 12.1, 1.3
x = x0
for r in e03:
    w = W * int(r["lost_per_100"]) / lost
    col = RED if r["cause_group"] == "process" else GREY
    b = rect(s, x, y0, w - 0.03, H, col, "E03_" + r["cause"].replace(" ", ""))
    tf = b.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.alignment = PP_ALIGN.CENTER
    run = p.add_run()
    run.text = r["lost_per_100"]
    run.font.size, run.font.bold, run.font.name = Pt(22), True, FONT
    run.font.color.rgb = WHITE if col == RED else INK
    text(s, x, y0 + H + 0.1, w - 0.03, 0.8, r["cause"], 12, False, INK, PP_ALIGN.CENTER)
    x += w
wp = W * proc / lost
text(s, x0, y0 - 0.65, wp, 0.5, f"Process drop-outs: {proc} ({round(proc / lost * 100)}%)", 16, True, RED,
     PP_ALIGN.CENTER)
text(s, x0 + wp, y0 - 0.65, W - wp, 0.5, f"Credit declines: {lost - proc}", 16, True, MUTED, PP_ALIGN.CENTER)
callout(s, 0.6, 5.5, 8.5, 0.8, f"{round(proc / lost * 100)}% of lost applications never reach credit review")

# ---------------------------------------------------------------- S04
docs = next(int(r["lost_per_100"]) for r in e03 if r["cause"] == "Invalid documents")
doc_share = derive("S04 invalid docs share of process drop-outs %", round(docs / proc * 100),
                   "E03 Invalid documents / S03 process x 100")
top = e04[0]
s = slide(f"Invalid documents cause {doc_share}% of process drop-outs, led by {top['document_type'].lower()}s",
          "Problem", "Share of invalid-document drop-outs, by failing document (%)", SRC,
          f"{top['document_type']}s alone cause {top['pct_of_doc_failures']}% of document failures. "
          "Most of these are fixable at submission: a pre-check that tells the customer what is missing "
          "before the file enters the queue.")
text(s, 9.6, 5.0, 3.2, 1.3, f"Invalid documents: {docs} of {proc} process drop-outs per 100 applications ({doc_share}%)",
     12, False, MUTED, name="EvidenceLine")
bar_chart(s, 0.6, 2.3, 8.6, 4.5, [r["document_type"] for r in e04], [int(r["pct_of_doc_failures"]) for r in e04],
          [0], fmt='0"%"', name="E04")
callout(s, 9.6, 3.0, 3.2, 1.6, f"{top['document_type']}s: {top['pct_of_doc_failures']}% of failures. "
        "A pre-check at submission targets this")

# ---------------------------------------------------------------- S05
med = e05[0]["median_days"]
hot = [i for i, r in enumerate(e05) if int(r["cancel_rate_pct"]) >= 20]
s = slide(f"Even complete applicants cancel: our decision takes {med} days, median", "Problem",
          "Cancel rate by days from complete application to decision (%)", SRC,
          f"Our median decision time is {med} days. Once a customer waits past 8 days, roughly a quarter or more "
          "cancel, most likely because another bank answered first. [Add a peer SLA here only if you have "
          "a dated source.]")
bar_chart(s, 0.6, 2.3, 8.6, 4.05, [r["days_to_decision_bucket"] + " days" for r in e05],
          [int(r["cancel_rate_pct"]) for r in e05], hot, kind=XL_CHART_TYPE.COLUMN_CLUSTERED, fmt='0"%"',
          name="E05")
text(s, 0.6, 6.45, 8.6, 0.35, f"Median decision time: {med} days (in the 6-8 day bucket)", 11, False, MUTED,
     PP_ALIGN.CENTER, name="MedianNote")
callout(s, 9.6, 3.0, 3.2, 1.6, f"Past 8 days, cancel rate reaches {e05[hot[0]]['cancel_rate_pct']}%+")

# ---------------------------------------------------------------- S06
rule = int(e06[0]["per_100_applications"])
slik = int(e06[1]["per_100_applications"])
ratio = derive("S06 rule/SLIK ratio", round(rule / slik, 1), "E06 Internal policy rules / E06 SLIK")
s = slide(f"At credit review, internal rules decline {ratio:.1f}x more applicants than SLIK does", "Problem",
          "Credit declines per 100 applications, by reason", SRC + "; SLIK = OJK credit bureau",
          f"SLIK is a hard limit and should stay one. But SLIK declines only {slik} in 100. Our own policy "
          f"rules decline {rule}, and {e06[0]['clean_slik_pct']}% of those applicants have a clean SLIK record.")
bar_chart(s, 0.6, 2.3, 8.6, 4.2, [r["decline_reason"] for r in e06], [int(r["per_100_applications"]) for r in e06],
          [0], name="E06")
callout(s, 9.6, 3.0, 3.2, 1.6, f"{e06[0]['clean_slik_pct']}% of rule declines have clean SLIK")

# ---------------------------------------------------------------- S07
idr = sum(float(r["forgone_interest_idr_bn"]) for r in e07)
hrs = derive("S07 analyst hours (exact)", sum(int(r["analyst_hours"]) for r in e07), "sum E07 analyst_hours")
derive("S07 interest IDR bn (exact)", round(idr, 1), "sum E07 forgone_interest_idr_bn")
derive("S07 title IDR bn (rounded)", round(idr), "round(S07 exact)")
derive("S07 title hours (rounded)", round(hrs, -3), "round(S07 hours, -3)")
s = slide(f"These losses cost about IDR {round(idr)} bn interest and {round(hrs, -3):,} analyst-hours yearly",
          "Stakes", "ESTIMATE: forgone first-year interest income from recoverable applications (IDR bn)",
          SRC + "; estimate, method on slide",
          "This is an estimate, and I show the method so you can challenge each input. The recoverable shares "
          "are assumptions; the pilot will measure them.")
cats = [r["leak"] for r in e07] + ["Total"]
vals = [float(r["forgone_interest_idr_bn"]) for r in e07]
path = charts.waterfall("E07", 7.6, 4.5, cats, vals, round(idr, 1))
s.shapes.add_picture(str(path), Inches(0.6), Inches(2.3), Inches(7.6), Inches(4.5)).name = "E07"
r0 = e07[0]
text(s, 8.6, 2.4, 4.2, 4.3, [
    "Method (estimate)",
    f"Lost applications x recoverable share x IDR {r0['avg_ticket_idr_mn']} mn average ticket x "
    f"{r0['yield_pct']}% yield",
    "Recoverable share (assumed): " + "; ".join(f"{r['leak'].split(' (')[0].lower()} {r['recoverable_pct']}%"
                                                for r in e07),
    f"Analyst time: {int(e07[1]['lost_applications_per_year']):,} cancelled files x "
    f"{e07[1]['hours_per_cancelled_file']} h = {hrs:,} h",
], 12, False, INK, name="Method")

# ---------------------------------------------------------------- S08
hi = [r for r in e08 if r["ascore_band"][0] in "DE"]
s = slide("Loosening rules for everyone would add loans, but also add losses", "Stakes",
          "The obvious fix, taken seriously", None,
          "The obvious answer is to loosen the rules across the board. It is the fastest way to volume, "
          "and I want to give it a fair hearing. The problem is that rule declines span every risk band, "
          "so loosening everything lets in the riskiest bands too.")
c9 = {r["criterion"]: r for r in e09}
icon(s, "zap", 0.6, 2.4, 0.6, red=False)
icon(s, "triangle-alert", 6.9, 2.4, 0.6)
text(s, 1.35, 2.5, 5.0, 3.4, [
    "Why it is tempting",
    f"Fastest volume: {c9['Loans added per month']['C_loosen_all']} loans a month",
    f"Fast to launch: {c9['Time to launch']['C_loosen_all']}",
    "No new tooling or process",
], 16, False, INK, name="ProsText")
text(s, 7.65, 2.5, 5.0, 3.4, [
    "Why it fails",
    f"Expected loss rises {c9['Expected loss']['C_loosen_all']} (estimate)",
    "Rule declines include bands D and E, where the approved book's bad rate is "
    f"{hi[0]['approved_bad_rate_pct']}% and {hi[1]['approved_bad_rate_pct']}%",
    "Moves risk appetite, which needs Credit Risk and Board sign-off",
], 16, False, INK, name="ConsText")
for tb in (s.shapes[-2], s.shapes[-1]):  # the two text boxes just added
    tb.text_frame.paragraphs[0].runs[0].font.bold = True
s.shapes[-1].text_frame.paragraphs[0].runs[0].font.color.rgb = RED
rect(s, 6.6, 2.5, 0.02, 3.6, GREY)
callout(s, 0.6, 6.15, 12.1, 0.6, "We need to find the safe subset, not open the gate for everyone")

# ---------------------------------------------------------------- S09
tot8 = sum(int(r["rule_declined_count"]) for r in e08)
safe = [i for i, r in enumerate(e08) if float(r["approved_bad_rate_pct"]) <= float(r["book_avg_bad_rate_pct"])]
safe_n = sum(int(e08[i]["rule_declined_count"]) for i in safe)
share = round(safe_n / tot8 * 100)
derive("S09 low-risk rule declines", safe_n, "sum E08 rule_declined_count where approved_bad_rate <= book_avg")
derive("S09 low-risk share %", share, "S09 count / sum E08 rule_declined_count x 100")
s = slide(f"{share}% of rule-declined applicants score as low-risk as our approved book", "Stakes",
          "Rule-declined applicants per year, by A-score band (approved-book bad rate in brackets)",
          SRC + "; bad rate = 30+ DPD at 12 months on the approved book",
          f"The A-score ranks every applicant, including those we declined. {safe_n:,} rule-declined applicants "
          f"sit in bands A and B, where our approved book's bad rate is at or below the "
          f"{e08[0]['book_avg_bad_rate_pct']}% average. Caveat: declined applicants have no repayment history, "
          "so their risk is inferred from the band. That is why we pilot before changing rules.")
bar_chart(s, 0.6, 2.3, 8.6, 4.4, [f"{r['ascore_band']} [{r['approved_bad_rate_pct']}%]" for r in e08],
          [int(r["rule_declined_count"]) for r in e08], safe, fmt='#,##0', name="E08")
callout(s, 9.6, 2.9, 3.2, 1.8, f"{safe_n:,} applicants ({share}%) in bands at or below the "
        f"{e08[0]['book_avg_bad_rate_pct']}% book bad rate")
text(s, 9.6, 5.0, 3.2, 1.6, "Inferred risk: declined applicants have no repayment record. The pilot tests it.",
     11, False, MUTED)

# ---------------------------------------------------------------- S10
s = slide("We judge four options on loans added, loss, cost and launch time", "Answer",
          "Decision criteria, agreed before we look at the options", None,
          "Before I show the options, here are the four criteria I will judge them on. I am stating them "
          "first so the recommendation has to earn its place against them.")
crit = [("Loans added per month", "Volume we can disburse on top of today"),
        ("Expected loss", "Must stay flat; risk appetite is not on the table"),
        ("Cost", "Including the cost of doing nothing"),
        ("Time to launch", "How soon we see results")]
for i, (c, d) in enumerate(crit):
    xx = 0.6 + i * 3.05
    rect(s, xx, 2.6, 2.85, 0.08, RED)
    icon(s, ["banknote", "shield-check", "wallet", "clock"][i], xx, 2.85, 0.75)
    text(s, xx, 3.6, 2.85, 0.6, c, 18, True, INK)
    text(s, xx, 4.3, 2.85, 1.4, d, 14, False, MUTED)

# ---------------------------------------------------------------- S11
dloans = c9["Loans added per month"]["D_process_plus_ascore"].lstrip("+")
derive("S11 title loans/month (rounded)", round(int(dloans), -1), "round(E09 D loans added, -1)")
s = slide(f"Process fixes plus A-score review add an estimated {round(int(dloans), -1)} loans monthly at flat loss",
          "Answer", None, "Source: estimates from data/E07-E09; loss impact from approved-book bad rate by band",
          "Option D is the only one that adds meaningful volume without moving expected loss. Option C adds "
          "more loans, but at a cost in loss we do not want. Doing nothing is not free: we forgo about "
          f"{c9['Cost']['A_do_nothing'].replace(' forgone', '')} in interest income.")
rows = [["", "A. Do nothing", "B. Process fixes only", "C. Loosen rules for all", "D. Process fixes + A-score (recommended)"]]
for r in e09:
    rows.append([r["criterion"] + (" (est.)" if r["criterion"] in ("Loans added per month", "Expected loss") else ""),
                 r["A_do_nothing"], r["B_process_only"], r["C_loosen_all"], r["D_process_plus_ascore"]])
table(s, 0.6, 1.95, 12.1, rows, col_w=[2.3, 2.2, 2.3, 2.3, 3.0], hl_col=4, size=14, row_h=0.72, name="E09")
text(s, 0.6, 5.75, 12.1, 0.6,
     "What would change our mind: if the back-test shows rule-declined applicants in bands A-B default above "
     "the approved book's rate, or if SLIK, not internal rules, drives most credit declines.",
     12, False, MUTED, name="Falsifier")
text(s, 0.6, 6.45, 12.1, 0.4, "Loans added = recoverable loans per year (data/E07) / 12. Estimates; the pilot measures them.",
     10, False, MUTED, name="Derivation")

# ---------------------------------------------------------------- S12
s = slide("A 12-week pilot on one segment proves it before any permanent rule change", "Plan",
          "Pilot segment: salaried applicants, digital channel. Four workstreams, one per proposed solution", None,
          "The four workstreams are the four solutions I started from. Each produces a measurable output, "
          "so by week 12 we have measured evidence instead of estimates.")
rows = [["Workstream", "What we do", "Weeks", "Output"],
        ["1. Reject diagnostics", "Funnel dashboard by stage, channel and reason code", "1-2", "Weekly leak report"],
        ["2. Recover current applications", "Call back pending files; document pre-check at submission", "2-12",
         "Recovered applications"],
        ["3. Relook reject reasons", "Review rule by rule: which rules decline clean-SLIK applicants", "2-6",
         "Rule-change candidates"],
        ["4. A-score targeting", "Bands A-B rule declines go to manual review, capped volume", "4-12",
         "Approvals and early DPD vs control"]]
table(s, 1.45, 2.4, 11.25, rows, col_w=[2.75, 5.0, 0.9, 2.6], size=13, row_h=0.75, name="Workplan")
for i, nm in enumerate(["chart-column", "file-check", "list-checks", "target"]):
    icon(s, nm, 0.6, 3.15 + i * 0.75 + 0.1, 0.55, red=i == 3)

# ---------------------------------------------------------------- S13
s = slide("Three guardrails stop the pilot if early losses rise", "Plan",
          "Pre-agreed triggers: we pause first and discuss second", None,
          "These guardrails are what make the pilot safe to say yes to. If early delinquency rises, "
          "we stop automatically, before any lasting change to policy.")
g = [("Loss trigger", "Pause if 30+ DPD on pilot approvals exceeds the approved book's rate for the same band"),
     ("Volume cap", "Pilot approvals capped at a fixed monthly limit agreed with Credit Risk"),
     ("Compliance", "SLIK declines stay hard; OJK/POJK review before any permanent rule change")]
for i, (h_, d) in enumerate(g):
    xx = 0.6 + i * 4.1
    rect(s, xx, 2.6, 3.8, 3.3, LIGHT, "bg-card")
    rect(s, xx, 2.6, 3.8, 0.08, RED, "bg-cardrule")
    icon(s, ["circle-pause", "gauge", "scale"][i], xx + 0.2, 2.85, 0.65)
    text(s, xx + 0.95, 2.85, 2.7, 0.65, h_, 20, True, RED, anchor=MSO_ANCHOR.MIDDLE)
    text(s, xx + 0.2, 3.6, 3.4, 2.2, d, 15, False, INK)

# ---------------------------------------------------------------- S14 the ask
pilot = {r["item"]: r["value"] for r in data("pilot")}
s = slide("Decision today: approve the pilot, co-owned by Credit Risk and Consumer Lending", "Plan",
          None, None,
          "This is the one thing I am asking for today. It is small, reversible, and measured: "
          f"{pilot['analysts']} analysts and {pilot['credit_reviewers']} credit reviewer for {pilot['weeks']} weeks, "
          "no policy change, and a go / no-go decision at the end with real loss data.")
rect(s, 0.6, 2.2, 12.1, 1.35, LIGHT, "bg-ask")
rect(s, 0.6, 2.2, 0.1, 1.35, RED, "bg-askrule")
text(s, 1.0, 2.25, 11.5, 1.25,
     f"Approve a {pilot['weeks']}-week pilot of document pre-check, a decision-time SLA, and A-score review of "
     f"rule-based declines, co-owned by Credit Risk and Consumer Lending, starting [{pilot['start']}].",
     18, True, INK, anchor=MSO_ANCHOR.MIDDLE, name="Ask")
cols = [
    ("What you approve", [f"{pilot['weeks']} weeks, one segment: {pilot['segment'].lower()}",
                          f"Team: {pilot['analysts']} analysts + {pilot['credit_reviewers']} credit reviewer (assumed)",
                          "No policy change; SLIK stays a hard limit"]),
    ("What you get (est.)", [f"+{round(int(dloans), -1)} loans a month at full scale",
                             f"About IDR {round(idr)} bn a year in interest income",
                             f"Fewer of the ~{round(hrs, -3):,} analyst-hours a year lost to cancelled files"]),
    ("When you will know", ["Week 2: first weekly leak report",
                            "Week 6: rule-change candidates to Credit Risk",
                            f"Week {pilot['weeks']}: go / no-go, with measured loss"]),
]
for i, (h_, items) in enumerate(cols):
    xx = 0.6 + i * 4.1
    rect(s, xx, 3.85, 3.8, 0.06, RED if i == 1 else GREY, f"bg-col{i}")
    icon(s, ["circle-check", "coins", "calendar-check"][i], xx, 3.98, 0.55, red=i == 1)
    text(s, xx + 0.7, 4.0, 3.1, 0.5, h_, 18, True, RED if i == 1 else INK, name=f"AskHead{i}")
    text(s, xx, 4.55, 3.8, 2.2, items, 14, False, INK, name=f"AskBody{i}")

# ---------------------------------------------------------------- Executive summary (built last, moved to slide 2)
s = slide("We lose more good applicants to our own process than to credit risk", None,
          "Executive summary", None,
          "If you remember one slide, make it this one. Demand is there, but our own funnel loses most of it. "
          "A safe subset can be won back without raising losses, and a 12-week pilot will prove it. "
          "Today I am asking for approval of that pilot.", )
blocks = [
    ("What is happening", [f"Applications grew {g_app}% in 12 months; disbursed loans only {g_dis}%",
                           f"Only {disb} of every 100 applications become a loan"]),
    ("Why", [f"{round(proc / lost * 100)}% of lost applications never reach credit review (documents, slow decisions)",
             f"Internal rules decline {ratio}x more applicants than SLIK",
             f"{share}% of rule-declined applicants score as low-risk as our approved book"]),
    ("What we propose", [f"{pilot['weeks']}-week pilot: document pre-check, decision SLA, A-score review",
                         f"Est. +{round(int(dloans), -1)} loans a month and IDR {round(idr)} bn a year, at flat loss",
                         "Guardrails pause the pilot if early losses rise"]),
]
for i, (h_, items) in enumerate(blocks):
    yy = 2.35 + i * 1.35
    rect(s, 0.6, yy, 0.08, 1.15, RED if i == 2 else GREY, f"bg-sumbar{i}")
    icon(s, ["trending-up", "search", "lightbulb"][i], 0.85, yy + 0.25, 0.65, red=i == 2)
    text(s, 1.65, yy, 2.1, 1.15, h_, 18, True, RED if i == 2 else INK, anchor=MSO_ANCHOR.MIDDLE, name=f"SumHead{i}")
    text(s, 3.8, yy, 8.9, 1.15, items, 14, False, INK, anchor=MSO_ANCHOR.MIDDLE, name=f"SumBody{i}")
rect(s, 0.6, 6.4, 12.1, 0.42, INK, "bg-decision")
text(s, 0.75, 6.4, 11.8, 0.42, "Decision today: approve the pilot, co-owned by Credit Risk and Consumer Lending",
     14, True, WHITE, anchor=MSO_ANCHOR.MIDDLE, name="SumDecision")
lst = prs.slides._sldIdLst
el = list(lst)[-1]
lst.remove(el)
lst.insert(1, el)

# ---------------------------------------------------------------- Appendix: mind map
s = slide("Appendix: the issue tree behind the analysis", None,
          "Every lost application leaves through exactly one branch", None,
          "Use this in Q&A when someone asks whether we considered a cause.")
mm = HERE / "slides" / "mindmap_slide.png"
from PIL import Image
iw, ih = Image.open(mm).size
w_in = min(12.1, 4.5 * iw / ih)
pic = s.shapes.add_picture(str(mm), Inches(0.6 + (12.1 - w_in) / 2), Inches(2.3), width=Inches(w_in))
pic.name = "MindMap"

with open(HERE / "data" / "derived.csv", "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["number", "value", "formula"])
    w.writerows(DERIVED)

out = HERE / "deck.pptx"
prs.save(out)
print("saved", out, len(prs.slides), "slides")
