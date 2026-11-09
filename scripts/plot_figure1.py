#!/usr/bin/env python3
import json
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


ROOT = Path(__file__).resolve().parents[1]
with (ROOT / "data/figure1_runtime_frontier.json").open() as stream:
    data = json.load(stream)

fig, ax = plt.subplots(figsize=(7.0, 4.3), constrained_layout=True)

styles = {
    "pepsbp": ("PEPS-BP", "s", "#50502B"),
    "pps": ("SPP measured", "o", "#585853"),
    "pps_estimate": ("SPP estimate", None, "#84847D"),
    "tebd_estimate": ("TEBD", "^", "#D99800"),
    "statevector": ("Statevector", "x", "#95030C"),
    "unbiased_emp": ("QESEM-Unbiased measured", "o", "#0040D6"),
    "heuristic_emp": ("QESEM-Extrapolated measured", "D", "#C34DFF"),
}
for key, (label, marker, color) in styles.items():
    method = data["methods"].get(key)
    if not method or not method.get("points"):
        continue
    x_key, y_key = method["x_key"], method["y_key"]
    points = method["points"]
    ax.plot(
        [point[x_key] for point in points],
        [point[y_key] for point in points],
        marker=marker,
        markersize=4,
        linewidth=1.2,
        color=color,
        label=label,
    )

model_styles = {
    "qesem_unbiased_eps_0.015": ("QESEM-Unbiased model", "#0040D6", "-"),
    "qesem_extrapolated_eps_0.005": ("QESEM-Extrapolated model, eps=0.005", "#C34DFF", "-"),
    "qesem_extrapolated_eps_0.015": ("QESEM-Extrapolated model, eps=0.015", "#C34DFF", ":"),
}
for key, (label, color, linestyle) in model_styles.items():
    model = data["qesem_runtime_models"][key]
    x = np.asarray(model["cycles"])
    y = np.asarray(model["runtime_hours"])
    ax.fill_between(x, model["band_low"], model["band_high"], color=color, alpha=0.10)
    ax.plot(x, y, color=color, linestyle=linestyle, linewidth=1.7, label=label)

ax.axvline(data["unmitigated_accuracy_limit_cycle"], color="#D99800", linestyle="--", linewidth=1.0)
ax.set(yscale="log", xlim=(0, 35), ylim=(1e-3, 4e2), xlabel="Floquet cycle", ylabel="Run time [hours]", title="Figure 1b - runtime frontier")
ax.grid(True, which="major", alpha=0.2)
ax.legend(fontsize=7, ncol=2)

for ext in ("pdf", "png"):
    fig.savefig(ROOT / f"figures/figure1_runtime_frontier.{ext}", dpi=250)

