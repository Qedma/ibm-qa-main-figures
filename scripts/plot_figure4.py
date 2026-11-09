#!/usr/bin/env python3
import json
from pathlib import Path

import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1.inset_locator import inset_axes


ROOT = Path(__file__).resolve().parents[1]
with (ROOT / "data/figure4_classical_methods.json").open() as stream:
    data = json.load(stream)

fig, axes = plt.subplots(2, 3, figsize=(12.0, 7.0), constrained_layout=True)
method_colors = ["#50502B", "#9F9F56", "#CDCDA2", "#D99800", "#FFBD22"]

def references(ax):
    for name, color in [("QESEM-Unbiased", "#0040D6"), ("QESEM-Extrapolated", "#C34DFF")]:
        row = data["references"][name]
        ax.errorbar(row["xs"], row["ys"], yerr=row.get("yerr"), fmt="o-", ms=3, lw=1, capsize=2, color=color, label=name)

ax = axes[0, 0]
for (name, row), color in zip(data["spp"].items(), method_colors):
    ax.plot(row["xs"], row["ys"], color=color, lw=1.2, label=name)
references(ax)
ax.set_title("(a) SPP")

def tensor_panel(ax, key, title):
    inset = inset_axes(ax, width="40%", height="38%", loc="lower right")
    for (name, row), color in zip(data[key].items(), method_colors):
        ax.plot(row["steps"], row["value"], color=color, lw=1.2, label=name)
        inset.plot(row["steps"], list(row["fidelity"].values()) if isinstance(row["fidelity"], dict) else row["fidelity"], color=color, lw=0.8)
    references(ax)
    ax.set_title(title)
    inset.set_title("Fidelity", fontsize=7)
    inset.tick_params(labelsize=6)

tensor_panel(axes[0, 1], "pepo_bp", "(b) PEPO-BP")
tensor_panel(axes[0, 2], "peps_bp", "(c) PEPS-BP")

ax = axes[1, 0]
for (name, row), color in zip(data["tdvp"].items(), method_colors * 2):
    ax.plot(row["xs"], row["ys"], lw=1.0, color=color, label=name)
references(ax)
ax.set_title("(d) TDVP, 51q and 74q")

ax = axes[1, 1]
for (name, row), color in zip(data["heuristic_corrected_tebd"].items(), method_colors * 4):
    ax.plot(row["cycles"], row["corrected"], lw=1.0, color=color, label=name)
for name, row in data["exact_references"].items():
    ax.plot(row["xs"], row["ys"], linestyle="--", lw=0.9, label=name)
references(ax)
ax.set_title("(e) Heuristic-corrected TEBD")

axes[1, 2].axis("off")
for ax in axes.flat[:5]:
    ax.set(xlabel="Floquet cycle", ylabel=r"$M_{z=2}$", xlim=(0, 31))
    ax.grid(True, alpha=0.18)
    ax.legend(fontsize=5.5, ncol=2)

for ext in ("pdf", "png"):
    fig.savefig(ROOT / f"figures/figure4_classical_methods.{ext}", dpi=250)

