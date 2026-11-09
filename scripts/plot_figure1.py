#!/usr/bin/env python3
import json
import math
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import to_rgb
from matplotlib.lines import Line2D
from matplotlib.ticker import FuncFormatter, LogLocator, MultipleLocator, NullFormatter


ROOT = Path(__file__).resolve().parents[1]
with (ROOT / "data/figure1_runtime_frontier.json").open() as stream:
    data = json.load(stream)

QEDMA = {
    "ink": "#030300",
    "blue": "#0040D6",
    "purple": "#C34DFF",
    "gold": "#D99800",
    "gold_dark": "#916500",
    "red_dark": "#95030C",
    "gray_dark": "#585853",
    "olive_dark": "#50502B",
    "grid": "#CECECB",
}

plt.rcParams.update({
    "font.family": "sans-serif",
    "font.sans-serif": ["Arial", "Helvetica", "DejaVu Sans"],
    "font.size": 8.0,
    "axes.labelsize": 8.0,
    "xtick.labelsize": 8.0,
    "ytick.labelsize": 8.0,
    "legend.fontsize": 6.2,
    "axes.edgecolor": QEDMA["ink"],
    "axes.labelcolor": QEDMA["ink"],
    "xtick.color": QEDMA["ink"],
    "ytick.color": QEDMA["ink"],
    "axes.linewidth": 0.75,
    "xtick.direction": "in",
    "ytick.direction": "in",
    "pdf.fonttype": 42,
    "ps.fonttype": 42,
})


def xy(name):
    method = data["methods"][name]
    return (
        np.asarray([point[method["x_key"]] for point in method["points"]], dtype=float),
        np.asarray([point[method["y_key"]] for point in method["points"]], dtype=float),
    )


def resource_limit(ax, x, y, color):
    ax.scatter(x, y, marker="o", s=54, facecolors="white", edgecolors=color, linewidths=1.1, zorder=12)
    ax.scatter(x, y, marker="x", s=34, color=color, linewidths=1.3, zorder=13)


def add_frontier_background(ax):
    gold = np.asarray(to_rgb("#FFF2D3"))
    blue = np.asarray(to_rgb("#C4D6FF"))
    x_values = np.linspace(0, 35, 1200)
    image = np.empty((8, len(x_values), 3))
    for index, x in enumerate(x_values):
        if x <= 11:
            mix = 0.0
        elif x >= 15:
            mix = 1.0
        else:
            t = (x - 11) / 4
            mix = 3 * t**2 - 2 * t**3
        color = gold * (1 - mix) + blue * mix
        alpha = 0.30 * (1 - mix) + 0.42 * mix
        image[:, index, :] = color * alpha + (1 - alpha)
    ax.imshow(image, extent=(0, 35, 1e-3, 4e2), origin="lower", aspect="auto", zorder=-20)
    ax.text(
        6.2, 30, "Classically\naccessible", color=QEDMA["gold_dark"],
        ha="center", va="center", fontsize=8.0, fontweight="semibold", linespacing=0.92,
    )


fig, ax = plt.subplots(figsize=(7.05, 4.35), constrained_layout=True, facecolor="white")
ax.set_facecolor("white")
ax.set(yscale="log", xlim=(0, 35), ylim=(1e-3, 4e2))
add_frontier_background(ax)

# Classical methods. Solid segments are directly measured; dashed segments
# are the estimates used in the manuscript. Crossed circles mark resource limits.
x, y = xy("pps")
ax.plot(x, y, "o-", ms=3.1, lw=1.25, color=QEDMA["gray_dark"], zorder=5)
resource_limit(ax, x[-1], y[-1], QEDMA["gray_dark"])

x, y = xy("pps_estimate")
y_zero = math.exp(2 * math.log(y[0]) - math.log(y[1]))
x = np.concatenate(([0.0], x))
y = np.concatenate(([y_zero], y))
ax.plot(x, y, linestyle=(0, (5, 3)), lw=1.15, color=QEDMA["gray_dark"], zorder=4)

x, y = xy("tebd_estimate")
measured = x <= 6
ax.plot(x[measured], y[measured], "o-", ms=3.1, lw=1.25, color=QEDMA["gold_dark"], zorder=5)
ax.plot(x[x >= 6], y[x >= 6], linestyle=(0, (5, 3)), lw=1.15, color=QEDMA["gold_dark"], zorder=4)
resource_limit(ax, x[measured][-1], y[measured][-1], QEDMA["gold_dark"])

x, y = xy("statevector")
ax.plot(x, y, linestyle=(0, (6, 2, 1.5, 2)), lw=1.25, color=QEDMA["red_dark"], zorder=5)
resource_limit(ax, x[-1], y[-1], QEDMA["red_dark"])

x, y = xy("pepsbp")
measured = x <= 13
ax.plot(x[measured], y[measured], "s-", ms=3.1, lw=1.25, color=QEDMA["olive_dark"], zorder=6)
ax.plot(x[x >= 13], y[x >= 13], linestyle=(0, (5, 3)), lw=1.15, color=QEDMA["olive_dark"], zorder=4)
resource_limit(ax, x[measured][-1], y[measured][-1], QEDMA["olive_dark"])

# Experimental runtimes. Early low-cycle points are de-emphasized exactly as
# in the source plot because they are not part of the late-time comparison.
for name, color, marker in (
    ("unbiased_emp", QEDMA["blue"], "o"),
    ("heuristic_emp", QEDMA["purple"], "D"),
):
    x, y = xy(name)
    early = (x < 5) & (x != 4)
    ax.scatter(x[early], y[early], s=12, marker=marker, color=color, alpha=0.28, zorder=7)
    ax.scatter(x[~early], y[~early], s=14, marker=marker, color=color, alpha=0.95, zorder=8)

# QESEM runtime models and uncertainty bands.
model_styles = {
    "qesem_unbiased_eps_0.015": (QEDMA["blue"], "-", 0.16),
    "qesem_extrapolated_eps_0.005": (QEDMA["purple"], "-", 0.16),
    "qesem_extrapolated_eps_0.015": (QEDMA["purple"], (0, (1.2, 2.0)), 0.08),
}
for name, (color, linestyle, alpha) in model_styles.items():
    model = data["qesem_runtime_models"][name]
    x = np.asarray(model["cycles"])
    y = np.asarray(model["runtime_hours"])
    ax.fill_between(x, model["band_low"], model["band_high"], color=color, alpha=alpha, linewidth=0, zorder=1)
    ax.plot(x, y, color=color, linestyle=linestyle, lw=1.35, zorder=3)

ax.scatter(
    [data["unmitigated_accuracy_limit_cycle"]], [1e-3], marker="^", s=72,
    facecolors=QEDMA["gold"], edgecolors="white", linewidths=0.8,
    zorder=14, clip_on=False,
)
ax.text(26.5, 0.105, r"$\epsilon=0.005$", color=QEDMA["purple"], fontsize=7.2, rotation=8)
ax.text(23.0, 0.024, r"$\epsilon=0.015$", color=QEDMA["purple"], fontsize=7.2, rotation=8)

handles = [
    Line2D([], [], linestyle="none", label="Quantum (ibm_boston)"),
    Line2D([], [], marker="o", linestyle="none", color=QEDMA["blue"], markersize=4, label="QESEM-Unbiased: measured"),
    Line2D([], [], color=QEDMA["blue"], lw=1.35, label="QESEM-Unbiased: runtime model"),
    Line2D([], [], marker="D", linestyle="none", color=QEDMA["purple"], markersize=3.8, label="QESEM-Extrapolated: measured"),
    Line2D([], [], color=QEDMA["purple"], lw=1.35, label="QESEM-Extrapolated: runtime model"),
    Line2D([], [], marker="^", linestyle="none", markerfacecolor=QEDMA["gold"], markeredgecolor="white", markersize=6, label="Unmitigated accuracy limit"),
    Line2D([], [], linestyle="none", label="Classical"),
    Line2D([], [], color=QEDMA["olive_dark"], marker="s", lw=1.25, markersize=3.5, label="PEPS-BP, H100 80GB (dashed: estimated)"),
    Line2D([], [], color=QEDMA["gray_dark"], marker="o", lw=1.25, markersize=3.5, label="SPP, Fugaku (measured, fixed resources)"),
    Line2D([], [], color=QEDMA["gray_dark"], linestyle=(0, (5, 3)), lw=1.15, label=r"SPP, Fugaku (estimated $\epsilon=0.015$ lower bound)"),
    Line2D([], [], color=QEDMA["gold_dark"], marker="o", lw=1.25, markersize=3.5, label="TEBD, A100 40GB (dashed: estimated)"),
    Line2D([], [], color=QEDMA["red_dark"], linestyle=(0, (6, 2, 1.5, 2)), lw=1.25, label="Statevector, Fugaku (estimated)"),
    Line2D([], [], marker=r"$\otimes$", linestyle="none", color=QEDMA["gray_dark"], markersize=7, label="Resource limit"),
]
legend = ax.legend(
    handles=handles, loc="upper right", frameon=True, facecolor="white",
    edgecolor=QEDMA["grid"], framealpha=0.95, handlelength=2.0,
    handletextpad=0.45, labelspacing=0.18, borderpad=0.35,
)
for text in legend.get_texts():
    if text.get_text() in {"Quantum (ibm_boston)", "Classical"}:
        text.set_fontweight("bold")

ax.set_xlabel("Floquet cycle", fontweight="semibold")
ax.set_ylabel("Run time [hours]", fontweight="semibold")
ax.xaxis.set_major_locator(MultipleLocator(5))
ax.xaxis.set_minor_locator(MultipleLocator(1))
ax.yaxis.set_major_locator(LogLocator(base=10))
ax.yaxis.set_minor_locator(LogLocator(base=10, subs=np.arange(2, 10) * 0.1))
ax.yaxis.set_major_formatter(FuncFormatter(lambda value, _: f"{value:g}"))
ax.yaxis.set_minor_formatter(NullFormatter())
ax.tick_params(which="major", length=3.0, width=0.65)
ax.tick_params(which="minor", length=1.6, width=0.45)

fig.savefig(ROOT / "figures/figure1_runtime_frontier.pdf", transparent=False)
fig.savefig(ROOT / "figures/figure1_runtime_frontier.png", dpi=500, transparent=False)
