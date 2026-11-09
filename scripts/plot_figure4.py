#!/usr/bin/env python3
import json
from pathlib import Path

import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1.inset_locator import inset_axes


ROOT = Path(__file__).resolve().parents[1]
with (ROOT / "data/figure4_classical_methods.json").open() as stream:
    data = json.load(stream)

fig = plt.figure(figsize=(14.0, 7.2), constrained_layout=True)
grid = fig.add_gridspec(2, 12, height_ratios=(1.0, 1.05))
top_axes = [fig.add_subplot(grid[0, start:start + 4]) for start in (0, 4, 8)]
bottom_axes = [fig.add_subplot(grid[1, start:start + 3]) for start in (0, 3, 6, 9)]
method_colors = ["#50502B", "#9F9F56", "#CDCDA2", "#D99800", "#FFBD22"]
chi_colors = {"4096": "#50502B", "2048": "#9F9F56", "1024": "#D99800"}


def references(ax, system):
    reference_colors = {"QESEM-Unbiased": "#0040D6", "QESEM-Extrapolated": "#C34DFF"}
    for name, row in data["references"][system].items():
        ax.errorbar(
            row["xs"], row["ys"], yerr=row["yerr"], fmt="o", ms=3,
            capsize=2, color=reference_colors[name], label=name, zorder=10,
        )


def exact_references(ax):
    exact_colors = {"Exact 28q": "#FB3440", "Exact 35q": "#3CBA27"}
    for name, row in data["exact_references"].items():
        ax.plot(
            row["xs"], row["ys"], linestyle=(0, (2, 1.5)), lw=1.0,
            color=exact_colors[name], label=name,
        )


def format_top(ax, title):
    ax.set(title=title, xlabel="Floquet cycle", xlim=(0, 31), ylim=(0.23, 0.47))
    ax.grid(True, alpha=0.18)
    ax.legend(fontsize=6, ncol=2)


ax = top_axes[0]
for (name, row), color in zip(data["spp"].items(), method_colors):
    ax.plot(row["xs"], row["ys"], color=color, lw=1.2, label=name)
references(ax, "51q")
format_top(ax, "(a) SPP, 51q")
ax.set_ylabel(r"$M_{z=2}$")


def tensor_panel(ax, key, title):
    inset = inset_axes(ax, width="47%", height="40%", loc="lower right", borderpad=1.0)
    diagnostic = inset.twinx()
    for (name, row), color in zip(data[key].items(), method_colors):
        ax.plot(row["steps"], row["value"], color=color, lw=1.2, label=name)
        if "fidelity" not in row:
            continue
        fidelity = list(row["fidelity"].values()) if isinstance(row["fidelity"], dict) else row["fidelity"]
        error = list(row["cumulative_error"].values()) if isinstance(row["cumulative_error"], dict) else row["cumulative_error"]
        inset.plot(row["steps"], fidelity, color=color, lw=0.8)
        diagnostic.plot(row["steps"], error, color=color, lw=0.8, linestyle="--")
    references(ax, "51q")
    format_top(ax, title)
    inset.set(xlim=(0, 30), ylim=(-0.05, 1.05), ylabel="Fidelity")
    diagnostic.set_ylabel(r"Cum. $L_2$ error")
    inset.tick_params(labelsize=5)
    diagnostic.tick_params(labelsize=5)
    inset.yaxis.label.set_size(6)
    diagnostic.yaxis.label.set_size(6)


tensor_panel(top_axes[1], "pepo_bp", "(b) PEPO-BP, 51q")
tensor_panel(top_axes[2], "peps_bp", "(c) PEPS-BP, 51q")


def peps_reference(ax, section):
    row = section["peps_reference"]
    ax.plot(
        row["steps"], row["value"], lw=1.3, color="#0070BA",
        label=f"PEPS, D={row['bond_dimension']}", zorder=8,
    )


def format_bottom(ax, title, system, y_limits, show_legend=True):
    ax.set(title=f"{title}, {system}", xlabel="Floquet cycle", xlim=(0, 31), ylim=y_limits)
    ax.grid(True, alpha=0.18)
    if show_legend:
        ax.legend(fontsize=5.3, ncol=2, loc="best")


def tdvp_panel(ax, system, label):
    section = data["tdvp"][system]
    exact_references(ax)
    for chi in ("4096", "2048", "1024"):
        row = section[chi]
        ax.plot(row["xs"], row["ys"], lw=1.2, color=chi_colors[chi], label=rf"TDVP, $\chi={chi}$")
    peps_reference(ax, section)
    references(ax, system)
    format_bottom(ax, f"({label}) TDVP", system, (0.33, 0.41))


def tebd_panel(ax, system, label):
    section = data["heuristic_corrected_tebd"][system]
    exact_references(ax)
    for chi in ("4096", "2048", "1024"):
        row = section[chi]
        ax.plot(row["cycles"], row["corrected"], lw=1.2, color=chi_colors[chi], label=rf"corrected, $\chi={chi}$")
        ax.plot(row["cycles"], row["raw"], lw=0.9, linestyle="--", alpha=0.6, color=chi_colors[chi])
    peps_reference(ax, section)
    references(ax, system)
    format_bottom(ax, f"({label}) corrected TEBD", system, (0.2, 0.5), show_legend=False)
    if system == "51q":
        ax.legend(fontsize=4.8, ncol=2, loc="upper left")

    zoom = inset_axes(ax, width="48%", height="38%", loc="lower right", borderpad=0.9)
    exact_references(zoom)
    for chi in ("4096", "2048", "1024"):
        row = section[chi]
        zoom.plot(row["cycles"], row["corrected"], lw=0.9, color=chi_colors[chi])
        zoom.plot(row["cycles"], row["raw"], lw=0.7, linestyle="--", alpha=0.5, color=chi_colors[chi])
    references(zoom, system)
    zoom.set(xlim=(15, 30), ylim=(0.33, 0.41))
    zoom.grid(True, alpha=0.15)
    zoom.tick_params(labelsize=5)


tdvp_panel(bottom_axes[0], "51q", "d")
tdvp_panel(bottom_axes[1], "74q", "d")
tebd_panel(bottom_axes[2], "51q", "e")
tebd_panel(bottom_axes[3], "74q", "e")
bottom_axes[0].set_ylabel(r"$M_{z=2}$")
bottom_axes[2].set_ylabel(r"$M_{z=2}$")

for ext in ("pdf", "png"):
    fig.savefig(ROOT / f"figures/figure4_classical_methods.{ext}", dpi=250)
