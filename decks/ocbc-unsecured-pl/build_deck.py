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

# impact model (EST) from E07: author's target = approval rate +5 pts, about IDR 2 bn disbursement a month
pp = derive("target approval uplift (pts)", round(sum(float(r["approval_uplift_pp"]) for r in e07), 1),
            "sum E07 approval_uplift_pp")
bn = derive("target disbursement IDR bn/month", round(sum(float(r["disbursement_idr_bn_per_month"]) for r in e07), 1),
            "sum E07 disbursement_idr_bn_per_month, rounded")
appr0 = int(next(r["per_100_applications"] for r in e02 if r["stage"] == "Approved"))
appr1 = derive("target approval rate %", appr0 + round(pp), "E02 Approved + uplift")
loans_m = derive("extra loans per month", round(sum(float(r["extra_loans_per_month"]) for r in e07)),
                 "sum E07 extra_loans_per_month")
hrs = derive("analyst hours a year on cancelled files", sum(int(r["analyst_hours_per_year"]) for r in e07),
             "sum E07 analyst_hours_per_year")
disb_pct = derive("share of approvals disbursed %", round(float(e07[0]["disbursed_per_approved"]) * 100),
                  "E07 disbursed_per_approved x 100")
hrs_r = derive("analyst hours a year (rounded)", round(hrs, -3), "round(hours, -3)")
PP = f"{pp:g}"
BN = f"{bn:g}"

# ---------------------------------------------------------------- S00 cover
s = prs.slides.add_slide(BLANK)
rect(s, 0, 0, 0.25, 7.5, RED, "CoverBand")
text(s, 0.8, 1.3, 6.4, 2.2, "Recovering lost unsecured-loan approvals at OCBC", 38, True, INK,
     anchor=MSO_ANCHOR.BOTTOM, name="Title")
rect(s, 0.8, 3.65, 1.5, 0.07, RED)
text(s, 0.8, 3.85, 6.4, 1.0, "Three machine-learning fixes to lift the approval rate at flat loss", 20, False, MUTED,
     name="Subtitle")
text(s, 0.8, 5.5, 6.4, 0.9, ["Graduate Program final presentation", "[Your name]  ·  [Date]"], 14, False, INK)
text(s, 0.8, 6.85, 2.6, 0.4, "Internal - Confidential", 9, False, MUTED)
if DUMMY:
    text(s, 3.6, 6.85, 3.6, 0.4, "ILLUSTRATIVE - DUMMY DATA", 9, True, RED, PP_ALIGN.RIGHT)
# right visual panel
rect(s, 7.6, 0, 5.733, 7.5, RED, "bg-coverpanel")
PINK = RGBColor(0xF6, 0xB3, 0xAE)
for i, w in enumerate([4.3, 3.6, 2.9, 2.2, 1.5]):
    b_ = s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(10.47 - w / 2), Inches(0.75 + i * 0.42),
                            Inches(w), Inches(0.3))
    b_.fill.solid()
    b_.fill.fore_color.rgb = PINK if i < 4 else WHITE
    b_.line.fill.background()
    b_.shadow.inherit = False
    b_.name = f"bg-funnel{i}"
up = s.shapes.add_shape(MSO_SHAPE.UP_ARROW, Inches(12.15), Inches(1.45), Inches(0.45), Inches(1.0))
up.fill.solid()
up.fill.fore_color.rgb = WHITE
up.line.fill.background()
up.shadow.inherit = False
up.name = "bg-uparrow"
text(s, 8.2, 3.05, 4.6, 0.9, f"+{PP} pts", 44, True, WHITE, name="CoverStat1")
text(s, 8.2, 3.97, 4.6, 0.4, f"approval rate, {appr0}% to {appr1}% (target)", 14, False, WHITE, name="CoverStat1Sub")
text(s, 8.2, 4.5, 4.6, 0.9, f"IDR {BN} bn", 44, True, WHITE, name="CoverStat2")
text(s, 8.2, 5.42, 4.6, 0.4, "more disbursement a month (target)", 14, False, WHITE, name="CoverStat2Sub")
chip = s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(8.2), Inches(6.2), Inches(4.4), Inches(0.62))
chip.fill.solid()
chip.fill.fore_color.rgb = WHITE
chip.line.fill.background()
chip.shadow.inherit = False
chip.name = "bg-mlchip"
s.shapes.add_picture(str(HERE / "icons" / "brain-circuit-red.png"), Inches(8.35), Inches(6.29), Inches(0.44),
                     Inches(0.44)).name = "bg-mlicon"
text(s, 8.9, 6.2, 3.6, 0.62, "Powered by machine learning", 15, True, RED, anchor=MSO_ANCHOR.MIDDLE, name="MLChip")
s.notes_slide.notes_text_frame.text = (
    "Open with one sentence: demand for unsecured loans is rising, but our disbursements are not. "
    f"Today I will show where those applications go, and how three machine-learning fixes can lift our approval "
    f"rate by {PP} points, about IDR {BN} bn more disbursement a month, without raising losses.")

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

# ---------------------------------------------------------------- S01b approval rate flat
e11 = data("E11")
ar = [float(r["approval_rate_pct"]) for r in e11]
ar_lo = derive("approval rate min %", min(ar), "min E11 approval_rate_pct")
ar_hi = derive("approval rate max %", max(ar), "max E11 approval_rate_pct")
s = slide(f"Approval rate has stuck near {appr0}% for 12 months, despite rising demand", "Situation",
          "Approved applications per 100 submitted, monthly (%)", SRC,
          f"Here is the core problem in one line. While applications grew, our approval rate never moved: it stayed "
          f"between {ar_lo}% and {ar_hi}% every month. Nothing we are doing today is closing the gap to the "
          f"{e11[0]['target_pct']}% target, so it will not close by itself.")
path = charts.trend_vs_target("E11", 9.4, 4.5, [r["month"] for r in e11], ar, float(e11[0]["target_pct"]), 30, 50,
                              "Approval rate (%); axis starts at 30")
s.shapes.add_picture(str(path), Inches(0.6), Inches(2.3), Inches(9.4), Inches(4.5)).name = "E11"
callout(s, 10.3, 3.0, 2.5, 1.7, f"Range {ar_lo}% to {ar_hi}% all year: no improvement yet")

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
s = slide(f"The three leaks cost about IDR {BN} bn of disbursement every month", "Stakes",
          "ESTIMATE: recoverable disbursement per month, by leak (IDR bn)", SRC + "; estimate, method on slide",
          "This is an estimate, and I show the method so you can challenge each input. The uplift per leak is an "
          f"assumption; together they lift the approval rate {PP} points, from {appr0}% to {appr1}%. The pilot measures it.")
cats = [r["leak"] for r in e07] + ["Total"]
vals = [float(r["disbursement_idr_bn_per_month"]) for r in e07]
path = charts.waterfall("E07", 7.6, 4.5, cats, vals, bn)
s.shapes.add_picture(str(path), Inches(0.6), Inches(2.3), Inches(7.6), Inches(4.5)).name = "E07"
r0 = e07[0]
text(s, 8.6, 2.4, 4.2, 4.3, [
    "Method (estimate)",
    f"Applications a month ({int(r0['applications_per_month']):,}) x approval-rate uplift x {disb_pct}% of approvals "
    f"disbursed x IDR {r0['avg_ticket_idr_mn']} mn average loan",
    "Uplift (assumed): " + "; ".join(f"{r['leak'].lower()} +{r['approval_uplift_pp']} pts" for r in e07)
    + f" = +{PP} pts ({appr0}% to {appr1}%)",
    f"About {loans_m} extra loans a month",
    f"Analyst time: {hrs:,} h a year on files that later cancel ({e07[1]['hours_per_cancelled_file']} h each)",
], 12, False, INK, name="Method")
s.shapes[-1].text_frame.paragraphs[0].runs[0].font.bold = True

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
    f"Most volume: {c9['Approval rate change']['C_loosen_all']} approval rate, "
    f"{c9['Disbursement added per month']['C_loosen_all']} a month",
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
s = slide("We judge four options on volume added, loss, cost and launch time", "Answer",
          "Decision criteria, agreed before we look at the options", None,
          "Before I show the options, here are the four criteria I will judge them on. I am stating them "
          "first so the recommendation has to earn its place against them.")
crit = [("Volume added", "Approval-rate points and disbursement a month on top of today"),
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
s = slide(f"ML-assisted fixes lift approval rate {PP} points, adding IDR {BN} bn monthly (est.)",
          "Answer", None, "Source: estimates from data/E07 and E09; loss impact from approved-book bad rate by band",
          "Option D is the only one that adds meaningful volume without moving expected loss. Option C adds "
          "more, but at a cost in loss we do not want. Doing nothing is not free: we forgo about "
          f"IDR {BN} bn of disbursement every month.")
rows = [["", "A. Do nothing", "B. Process fixes only", "C. Loosen rules for all", "D. ML + process fixes + A-score (recommended)"]]
for r in e09:
    est = r["criterion"] in ("Approval rate change", "Disbursement added per month", "Expected loss")
    rows.append([r["criterion"] + (" (est.)" if est else ""),
                 r["A_do_nothing"], r["B_process_only"], r["C_loosen_all"], r["D_ml_process_ascore"]])
table(s, 0.6, 1.95, 12.1, rows, col_w=[2.4, 2.1, 2.2, 2.3, 3.1], hl_col=4, size=13, row_h=0.62, name="E09")
text(s, 0.6, 5.85, 12.1, 0.55,
     "What would change our mind: if the back-test shows rule-declined applicants in bands A-B default above "
     "the approved book's rate, or if SLIK, not internal rules, drives most credit declines.",
     12, False, MUTED, name="Falsifier")
text(s, 0.6, 6.45, 12.1, 0.4, f"Disbursement = applications a month x approval uplift x {disb_pct}% disbursed x "
     f"IDR {e07[0]['avg_ticket_idr_mn']} mn average loan (data/E07). Estimates; the pilot measures them.",
     10, False, MUTED, name="Derivation")

# ---------------------------------------------------------------- S11b how ML powers the fix
s = slide("Three ML models close the three leaks; credit officers keep the final say", "Answer",
          "One model per leak, each with an estimated approval-rate lift", None,
          "Here is how the machine learning works. One model per leak. The document checker reads uploads and "
          "flags problems before the file enters the queue. The fast-track model sends complete, low-risk files to "
          "an express decision, so fewer applicants give up waiting. The challenger model re-scores applicants our "
          "rules declined, using the A-score plus bureau and application data, and sends the low-risk ones to a "
          "credit officer. No model approves a loan on its own.")
ml = [("At submission", "scan-text", "ML document checker",
       "Reads payslips, bank statements and KTP at upload; flags missing or invalid items before the queue",
       "OCR + document classifier"),
      ("In the queue", "zap", "ML fast-track",
       "Routes complete, low-risk files to an express decision, so fewer applicants cancel while waiting",
       "Gradient-boosted routing model"),
      ("At credit review", "brain-circuit", "ML challenger model",
       "Re-scores rule-declined applicants with A-score, SLIK and application data; low-risk ones go to an officer",
       "Gradient boosting, champion vs challenger")]
for i, ((stage, ic, name_, what, tech), r) in enumerate(zip(ml, e07)):
    xx = 0.6 + i * 4.1
    text(s, xx, 2.3, 3.8, 0.35, stage.upper(), 11, True, MUTED, name=f"MLStage{i}")
    rect(s, xx, 2.7, 3.8, 2.75, LIGHT, f"bg-mlcard{i}")
    rect(s, xx, 2.7, 3.8, 0.07, RED, f"bg-mlrule{i}")
    icon(s, ic, xx + 0.2, 2.9, 0.65)
    text(s, xx + 0.95, 2.9, 2.75, 0.65, name_, 17, True, INK, anchor=MSO_ANCHOR.MIDDLE, name=f"MLName{i}")
    text(s, xx + 0.2, 3.65, 3.45, 1.05, what, 12, False, INK, name=f"MLWhat{i}")
    text(s, xx + 0.2, 4.85, 2.3, 0.5, tech, 10, False, MUTED, name=f"MLTech{i}")
    text(s, xx + 2.5, 4.75, 1.2, 0.6, f"+{r['approval_uplift_pp']} pts", 18, True, RED, PP_ALIGN.RIGHT,
         anchor=MSO_ANCHOR.MIDDLE, name=f"MLLift{i}")
    if i < 2:
        arr = s.shapes.add_shape(MSO_SHAPE.RIGHT_ARROW, Inches(xx + 3.83), Inches(3.9), Inches(0.24), Inches(0.35))
        arr.fill.solid()
        arr.fill.fore_color.rgb = GREY
        arr.line.fill.background()
        arr.shadow.inherit = False
        arr.name = f"bg-mlarrow{i}"
gov = [("user-check", "People decide", "Credit officers approve every ML-referred case"),
       ("activity", "Monitored", "Drift checks and a monthly back-test against actual repayments"),
       ("shield-check", "Governed", "Explainable reason codes; model-risk review before go-live")]
for i, (ic, h_, d) in enumerate(gov):
    xx = 0.6 + i * 4.1
    icon(s, ic, xx, 5.75, 0.55, red=False)
    text(s, xx + 0.7, 5.7, 3.1, 0.35, h_, 14, True, INK, name=f"GovHead{i}")
    text(s, xx + 0.7, 6.05, 3.1, 0.7, d, 11, False, MUTED, name=f"GovBody{i}")

# ---------------------------------------------------------------- S11c where the business must focus
order = sorted(range(len(e07)), key=lambda i: -float(e07[i]["approval_uplift_pp"]))
top2 = derive("focus: top-two lever points", round(sum(sorted([float(r["approval_uplift_pp"]) for r in e07])[-2:]), 1),
              "sum of two largest E07 approval_uplift_pp")
s = slide(f"The business should focus on documents and rule declines first: {top2:g} of {PP} points",
          "Answer", "Three moves, ranked by approval-rate impact, each with one owner and one weekly KPI", None,
          f"The opportunity is there. What matters now is focus. Two moves, fixing documents at submission and "
          f"re-scoring rule declines, deliver {top2:g} of the {PP} points, so they get our best people first. "
          "Speed is the third move. Each has one owner and one number we track every week.")
focus_rows = {
    "Invalid documents": ("Fix documents at submission", "Operations + Digital", "Invalid-document rate", "scan-text"),
    "Rule declines": ("Re-score rule declines", "Credit Risk", "Approvals from re-scored declines", "brain-circuit"),
    "Cancellations": ("Decide faster", "Consumer Lending operations", "Median days to decision", "zap"),
}
for rank, i in enumerate(order):
    r = e07[i]
    move, owner, kpi, ic = focus_rows[r["leak"]]
    yy = 2.35 + rank * 1.4
    first = rank < 2
    rect(s, 0.6, yy, 12.1, 1.2, RGBColor(0xFD, 0xE8, 0xE7) if first else LIGHT, f"bg-focus{rank}")
    text(s, 0.75, yy, 0.6, 1.2, f"{rank + 1}", 30, True, RED if first else MUTED, anchor=MSO_ANCHOR.MIDDLE,
         name=f"FocusRank{rank}")
    icon(s, ic, 1.4, yy + 0.3, 0.6, red=first)
    text(s, 2.2, yy + 0.1, 4.0, 0.5, move, 18, True, INK, name=f"FocusMove{rank}")
    text(s, 2.2, yy + 0.6, 4.0, 0.5, r["ml_lever"], 12, False, MUTED, name=f"FocusLever{rank}")
    text(s, 6.3, yy + 0.1, 2.6, 1.0, ["Owner", owner], 13, False, INK, name=f"FocusOwner{rank}")
    text(s, 9.0, yy + 0.1, 2.3, 1.0, ["Weekly KPI", kpi], 13, False, INK, name=f"FocusKPI{rank}")
    for tb in (s.shapes[-2], s.shapes[-1]):
        tb.text_frame.paragraphs[0].runs[0].font.color.rgb = MUTED
        tb.text_frame.paragraphs[0].runs[0].font.size = Pt(11)
    text(s, 11.3, yy, 1.3, 1.2, f"+{r['approval_uplift_pp']} pts", 20, True, RED if first else MUTED,
         PP_ALIGN.RIGHT, anchor=MSO_ANCHOR.MIDDLE, name=f"FocusPts{rank}")
text(s, 0.6, 6.55, 12.1, 0.35, "Owners are proposed; confirm with each function before presenting. Point lifts are estimates (data/E07).",
     10, False, MUTED, name="FocusNote")

# ---------------------------------------------------------------- S12
s = slide("A 12-week pilot on one segment proves it before any permanent rule change", "Plan",
          "Pilot segment: salaried applicants, digital channel. Four workstreams, one per proposed solution", None,
          "The four workstreams are the four solutions I started from. Each produces a measurable output, "
          "so by week 12 we have measured evidence instead of estimates.")
rows = [["Workstream", "What we do", "Weeks", "Output"],
        ["1. Diagnostics and data", "Funnel dashboard by stage and reason code; build the labelled data set for the models",
         "1-2", "Weekly leak report"],
        ["2. ML document checker", "Pre-check uploads; call back pending and incomplete files", "2-12",
         "Fewer invalid documents"],
        ["3. ML fast-track + rule relook", "Express route for low-risk files; review rules that decline clean-SLIK applicants",
         "2-8", "Shorter decision time; rule-change candidates"],
        ["4. ML challenger + A-score", "Re-score rule declines; bands A-B to manual review, capped volume", "4-12",
         "Approvals and early DPD vs control"]]
table(s, 1.45, 2.4, 11.25, rows, col_w=[2.75, 5.0, 0.9, 2.6], size=13, row_h=0.75, name="Workplan")
for i, nm in enumerate(["chart-column", "scan-text", "zap", "brain-circuit"]):
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
          f"{pilot['data_scientists']} data scientist, {pilot['analysts']} analysts and {pilot['credit_reviewers']} credit reviewer for {pilot['weeks']} weeks, "
          "no policy change, and a go / no-go decision at the end with real loss data.")
rect(s, 0.6, 2.2, 12.1, 1.35, LIGHT, "bg-ask")
rect(s, 0.6, 2.2, 0.1, 1.35, RED, "bg-askrule")
text(s, 1.0, 2.25, 11.5, 1.25,
     f"Approve a {pilot['weeks']}-week pilot of three ML models (document checker, fast-track, challenger) with "
     f"A-score review of rule-based declines, co-owned by Credit Risk and Consumer Lending, starting [{pilot['start']}].",
     18, True, INK, anchor=MSO_ANCHOR.MIDDLE, name="Ask")
cols = [
    ("What you approve", [f"{pilot['weeks']} weeks, one segment: {pilot['segment'].lower()}",
                          f"Team: {pilot['data_scientists']} data scientist, {pilot['analysts']} analysts, {pilot['credit_reviewers']} credit reviewer (assumed)",
                          "No policy change; SLIK stays a hard limit"]),
    ("What you get (est.)", [f"Approval rate +{PP} pts ({appr0}% to {appr1}%)",
                             f"About IDR {BN} bn more disbursement a month",
                             f"Fewer of the ~{hrs_r:,} analyst-hours a year lost to cancelled files"]),
    ("When you will know", ["Week 2: first weekly leak report",
                            "Week 6: models running in shadow mode",
                            f"Week {pilot['weeks']}: go / no-go, with measured loss"]),
]
for i, (h_, items) in enumerate(cols):
    xx = 0.6 + i * 4.1
    rect(s, xx, 3.85, 3.8, 0.06, RED if i == 1 else GREY, f"bg-col{i}")
    icon(s, ["circle-check", "coins", "calendar-check"][i], xx, 3.98, 0.55, red=i == 1)
    text(s, xx + 0.7, 4.0, 3.1, 0.5, h_, 18, True, RED if i == 1 else INK, name=f"AskHead{i}")
    text(s, xx, 4.55, 3.8, 2.2, items, 14, False, INK, name=f"AskBody{i}")

# ---------------------------------------------------------------- S16 closing: key takeaways
team = derive("S16 pilot team size", int(pilot["data_scientists"]) + int(pilot["analysts"]) + int(pilot["credit_reviewers"]),
              "pilot.csv data_scientists + analysts + credit_reviewers")
s = slide(f"Each month of waiting forgoes IDR {BN} bn disbursement; the pilot caps the risk",
          "Plan", "Key takeaways", None,
          "Let me close with three things to remember. First, this leak is ours to fix: most lost applications "
          "never reach a credit decision. Second, a safe subset exists, and machine learning with the A-score can "
          f"find it. Third, the bet is lopsided: we risk {pilot['weeks']} weeks and {team} people under pause "
          f"triggers, against an estimated {PP}-point lift in approval rate. Every month we wait costs about "
          f"IDR {BN} bn of disbursement. "
          "So my question is simple: can we start the pilot, and can I bring you the first leak report in two weeks?")
# left: three takeaways
tk = [("The leak is ours to fix",
       f"{round(proc / lost * 100)}% of lost applications never reach credit review"),
      ("A safe subset exists, and ML finds it",
       f"{share}% of rule-declined applicants score as low-risk as our approved book"),
      ("The bet is lopsided",
       "Small, capped and reversible downside against a measured upside")]
for i, (h_, d) in enumerate(tk):
    yy = 2.35 + i * 1.25
    text(s, 0.6, yy, 0.6, 0.6, f"{i + 1}", 30, True, RED, name=f"TkNum{i}")
    text(s, 1.2, yy, 4.6, 0.45, h_, 17, True, INK, name=f"TkHead{i}")
    text(s, 1.2, yy + 0.45, 4.6, 0.7, d, 13, False, MUTED, name=f"TkBody{i}")
# right: risk vs reward panel
rect(s, 6.3, 2.35, 3.1, 3.55, LIGHT, "bg-risk")
rect(s, 9.6, 2.35, 3.1, 3.55, RGBColor(0xFD, 0xE8, 0xE7), "bg-reward")
icon(s, "shield", 6.5, 2.5, 0.6, red=False)
text(s, 7.2, 2.5, 2.1, 0.6, "What we risk", 16, True, INK, anchor=MSO_ANCHOR.MIDDLE, name="RiskHead")
text(s, 6.5, 3.25, 2.8, 2.6, [f"{pilot['weeks']} weeks, one segment", f"{team} people (assumed)",
                              "Capped volume, pause triggers", "No policy change: fully reversible"],
     13, False, INK, name="RiskBody")
icon(s, "rocket", 9.8, 2.5, 0.6)
text(s, 10.5, 2.5, 2.1, 0.6, "What we gain (est.)", 16, True, RED, anchor=MSO_ANCHOR.MIDDLE, name="RewardHead")
text(s, 9.8, 3.25, 2.8, 2.6, [f"Approval rate +{PP} pts ({appr0}% to {appr1}%)",
                              f"About IDR {BN} bn more disbursement a month", "Fewer hours lost to cancelled files",
                              "Measured evidence for any rule change"],
     13, False, INK, name="RewardBody")
# bottom: cost of waiting + the ask
rect(s, 0.6, 6.05, 12.1, 0.75, INK, "bg-close")
icon(s, "hourglass", 0.75, 6.12, 0.6)
text(s, 1.5, 6.05, 11.1, 0.75,
     f"Cost of waiting: about IDR {BN} bn of disbursement a month (est.).  Today: approve the pilot.  "
     "Week 2: first leak report.", 14, True, WHITE, anchor=MSO_ANCHOR.MIDDLE, name="CloseBar")

# ---------------------------------------------------------------- Executive summary (built last, moved to slide 2)
s = slide("We lose more good applicants to our own process than to credit risk", None,
          "Executive summary", None,
          "If you remember one slide, make it this one. Demand is there, but our own funnel loses most of it. "
          "Three machine-learning fixes can win part of it back without raising losses, and a 12-week pilot "
          "will prove it. "
          "Today I am asking for approval of that pilot.", )
blocks = [
    ("What is happening", [f"Applications grew {g_app}% in 12 months; disbursed loans only {g_dis}%",
                           f"Only {disb} of every 100 applications become a loan"]),
    ("Why", [f"{round(proc / lost * 100)}% of lost applications never reach credit review (documents, slow decisions)",
             f"Internal rules decline {ratio}x more applicants than SLIK",
             f"{share}% of rule-declined applicants score as low-risk as our approved book"]),
    ("What we propose", [f"{pilot['weeks']}-week pilot: ML document checker, ML fast-track, ML challenger + A-score",
                         f"Target: approval rate {appr0}% to {appr1}% (+{PP} pts), about IDR {BN} bn more disbursement a month",
                         "At flat loss: guardrails pause the pilot if early losses rise"]),
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
