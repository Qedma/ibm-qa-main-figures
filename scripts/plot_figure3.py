#!/usr/bin/env python3
import json
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


ROOT = Path(__file__).resolve().parents[1]
with (ROOT / "data/figure3_quantum_dynamics.json").open() as stream:
    data = json.load(stream)

fig, axes = plt.subplots(1, 3, figsize=(12.0, 3.8), constrained_layout=True)

colors = {
    "Noisy": "#D99800", "ZNE": "#C34DFF", "Mitigated": "#0040D6",
    "BP, chi=512": "#9F9F56", "BP, chi=700": "#50502B",
    "ORQA, wt=11,delta=1e-11": "#CECECB", "ORQA, wt=20,delta=1e-9": "#585853",
    "Quantinuum mitigated": "#0070BA", "Quantinuum noisy": "#916500",
}
ax = axes[0]
for name, row in data["magnetization"].items():
    if "yerr" in row:
        ax.errorbar(row["xs"], row["ys"], yerr=row["yerr"], fmt="o-", ms=3, lw=1, capsize=2, label=name, color=colors.get(name))
    else:
        ax.plot(row["xs"], row["ys"], lw=1.2, label=name, color=colors.get(name))
ax.set(xlabel="Floquet cycle", ylabel="Magnetization", title="(a) 51-qubit dynamics")
ax.legend(fontsize=6, ncol=2)

ax = axes[1]
late = data["late_cycle"]
palette = {"21q_sim": "#585853", "28q_sim": "#FB3440", "35q_sim": "#3CBA27", "51q_exp": "#0040D6", "74q_exp": "#D99800"}
for group in ("simulations", "experiments"):
    for name, points in late[group].items():
        x = [p["cycle"] for p in points]
        y = [p["value"] for p in points]
        if group == "experiments":
            ax.errorbar(x, y, yerr=[p["error"] for p in points], fmt="o", ms=3, capsize=2, color=palette[name], label=name)
        else:
            ax.plot(x, y, "s", ms=3, color=palette[name], label=name)
        fit = late["fits"][name]["curve"]
        ax.plot(fit["cycles"], fit["value"], color=palette[name], lw=1)
ax.set(xlabel="Floquet cycle", ylabel=r"$M_{z=2}$", title="(b) Late-cycle fits", xlim=(14, 31))
ax.legend(fontsize=7, ncol=2)

ax = axes[2]
finite = data["finite_size"]
for point in finite["points"]:
    color = "#C34DFF" if point["kind"] == "experiment" else "#030300"
    ax.errorbar(point["system_size"], point["amplitude"], yerr=point["error"], fmt="o", capsize=2, color=color)
for name, color in [("classical_only", "#585853"), ("all_sizes", "#C34DFF")]:
    fit = finite["fits"][name]
    x = np.asarray(fit["system_size"])
    ax.fill_between(x, fit["band_low"], fit["band_high"], color=color, alpha=0.14)
    ax.plot(x, fit["amplitude"], color=color, lw=1.4, label=name.replace("_", " "))
ax.set(xlabel="System size", ylabel="Oscillation amplitude", title="(c) Finite-size scaling", xlim=(20, 100), ylim=(0, 0.05))
ax.legend(fontsize=8)

for ext in ("pdf", "png"):
    fig.savefig(ROOT / f"figures/figure3_quantum_dynamics.{ext}", dpi=250)

