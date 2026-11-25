"""Render deck charts as PNG images (matplotlib), styled to STYLE.md.

Images display identically in PowerPoint, Keynote and Google Slides (including mobile),
which do not all render native pptx charts. Chart data stays in data/E##.csv.
"""
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

RED, INK, MUTED, GREY = "#E2231A", "#1F1F1F", "#6E6E6E", "#BFBFBF"
plt.rcParams.update({"font.family": "Liberation Sans", "font.size": 13, "text.color": INK,
                     "axes.edgecolor": GREY, "axes.labelcolor": MUTED,
                     "xtick.color": INK, "ytick.color": INK})
OUT = Path(__file__).parent / "slides" / "charts"
OUT.mkdir(parents=True, exist_ok=True)
DPI = 220


def _fmt(fmt, v):
    return {"pct": f"{v:.0f}%", "pct1": f"{v:.1f}%", "int": f"{v:,.0f}", "dec1": f"{v:.1f}"}[fmt]


def _clean(ax, keep="bottom"):
    for side in ("top", "right", "left", "bottom"):
        ax.spines[side].set_visible(side == keep)
    ax.tick_params(length=0)


def bars(name, w, h, cats, vals, accents, horizontal=True, fmt="int"):
    fig, ax = plt.subplots(figsize=(w, h), dpi=DPI)
    colors = [RED if i in accents else GREY for i in range(len(vals))]
    top = max(vals)
    if horizontal:
        y = list(range(len(vals)))[::-1]
        ax.barh(y, vals, color=colors, height=0.62)
        ax.set_yticks(y, cats)
        ax.set_xticks([])
        ax.set_xlim(0, top * 1.15)
        for yi, v in zip(y, vals):
            ax.text(v + top * 0.015, yi, _fmt(fmt, v), va="center", fontweight="bold")
        _clean(ax, "left")
    else:
        x = range(len(vals))
        ax.bar(x, vals, color=colors, width=0.62)
        ax.set_xticks(list(x), cats)
        ax.set_yticks([])
        ax.set_ylim(0, top * 1.15)
        for xi, v in zip(x, vals):
            ax.text(xi, v + top * 0.02, _fmt(fmt, v), ha="center", fontweight="bold")
        _clean(ax, "bottom")
    fig.tight_layout()
    path = OUT / f"{name}.png"
    fig.savefig(path, transparent=False, facecolor="white")
    plt.close(fig)
    return path


def lines(name, w, h, cats, series, ymin, ymax, ylabel):
    """series: list of (label, values, emphasised: bool)"""
    fig, ax = plt.subplots(figsize=(w, h), dpi=DPI)
    x = list(range(len(cats)))
    for label, vals, emph in series:
        col = RED if emph else GREY
        ax.plot(x, vals, color=col, linewidth=3.5 if emph else 2.5)
        ax.text(x[-1] + 0.15, vals[-1], f"{label}: {vals[-1]:.0f}", va="center", fontweight="bold",
                color=RED if emph else MUTED)
    ax.set_xticks(x, cats, fontsize=11)
    ax.set_ylim(ymin, ymax)
    ax.set_yticks([t for t in range(ymin, ymax + 1, 10) if t > ymin])
    ax.set_xlim(-0.3, len(cats) + 2.2)
    ax.set_ylabel(ylabel, fontsize=11)
    ax.grid(axis="y", color="#E5E5E5", linewidth=0.6)
    ax.set_axisbelow(True)
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)
    ax.tick_params(length=0)
    fig.tight_layout()
    path = OUT / f"{name}.png"
    fig.savefig(path, facecolor="white")
    plt.close(fig)
    return path


def waterfall(name, w, h, cats, vals, total):
    fig, ax = plt.subplots(figsize=(w, h), dpi=DPI)
    run = 0
    for i, v in enumerate(vals):
        ax.bar(i, v, bottom=run, color=GREY, width=0.62)
        ax.text(i, run + v + total * 0.02, f"{v:.1f}", ha="center", fontweight="bold")
        run += v
    i = len(vals)
    ax.bar(i, total, color=RED, width=0.62)
    ax.text(i, total + total * 0.02, f"{total:.1f}", ha="center", fontweight="bold", color=RED, fontsize=15)
    ax.set_xticks(range(len(cats)), [c.replace(" (", "\n(") for c in cats], fontsize=11)
    ax.set_yticks([])
    ax.set_ylim(0, total * 1.15)
    _clean(ax, "bottom")
    fig.tight_layout()
    path = OUT / f"{name}.png"
    fig.savefig(path, facecolor="white")
    plt.close(fig)
    return path


def trend_vs_target(name, w, h, cats, vals, target, ymin, ymax, ylabel):
    fig, ax = plt.subplots(figsize=(w, h), dpi=DPI)
    x = list(range(len(cats)))
    ax.plot(x, vals, color=RED, linewidth=3.5, marker="o", markersize=5)
    ax.axhline(target, color=MUTED, linewidth=1.5, linestyle="--")
    ax.text(x[-1] + 0.2, target + 0.5, f"Target {target:g}%", va="bottom", color=MUTED, fontweight="bold")
    ax.text(x[-1] + 0.2, vals[-1], f"{vals[-1]:g}%", va="center", color=RED, fontweight="bold")
    ax.set_xticks(x, cats, fontsize=11)
    ax.set_ylim(ymin, ymax)
    ax.set_yticks([t for t in range(ymin, ymax + 1, 5) if t > ymin])
    ax.set_xlim(-0.3, len(cats) + 1.4)
    ax.set_ylabel(ylabel, fontsize=11)
    ax.grid(axis="y", color="#E5E5E5", linewidth=0.6)
    ax.set_axisbelow(True)
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)
    ax.tick_params(length=0)
    fig.tight_layout()
    path = OUT / f"{name}.png"
    fig.savefig(path, facecolor="white")
    plt.close(fig)
    return path
