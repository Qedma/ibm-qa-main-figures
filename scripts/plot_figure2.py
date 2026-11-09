#!/usr/bin/env python3
import json
from pathlib import Path

import matplotlib.pyplot as plt
import matplotlib.tri as mtri
import numpy as np


ROOT = Path(__file__).resolve().parents[1]
with (ROOT / "data/figure2_parameter_scan.json").open() as stream:
    data = json.load(stream)

points = data["scan_points"]
tx = np.asarray([p["theta_x"] for p in points])
tz = np.asarray([p["theta_z"] for p in points])
tzz = np.asarray([p["theta_zz"] for p in points])
mag = np.asarray([p["magnetization_abs"] for p in points])
ent = np.asarray([p["state_entanglement"] for p in points])
sel = data["selected_parameters"]

fig, axes = plt.subplots(2, 4, figsize=(12.0, 6.2), constrained_layout=True)

# (b) Global tradeoff cloud.
ax = axes[0, 0]
sc = ax.scatter(ent / np.nanmax(ent), mag, c=np.sqrt((tx-sel["theta_x"])**2 + (tz-sel["theta_z"])**2 + (tzz-sel["theta_zz"])**2), s=10, cmap="viridis")
ax.set(xlabel="Normalized state entanglement", ylabel="Magnetization", title="(b) Tradeoff")
fig.colorbar(sc, ax=ax, label="Parameter distance")

def slice_plot(ax, fixed_name, fixed_value, x_values, values, title, cmap, operators=False):
    fixed = tzz if fixed_name == "theta_zz" else tz
    mask = np.abs(fixed - fixed_value) < 0.011
    tri = mtri.Triangulation(tx[mask], x_values[mask])
    contour = ax.tricontourf(tri, values[mask], levels=18, cmap=cmap)
    ax.scatter(sel["theta_x"], sel["theta_z" if fixed_name == "theta_zz" else "theta_zz"], marker="*", s=100, c="#65DB51", edgecolors="black")
    ax.set(xlabel=r"$\theta_x$", ylabel=r"$\theta_z$" if fixed_name == "theta_zz" else r"$\theta_{zz}$", title=title)
    fig.colorbar(contour, ax=ax)
    if operators:
        op = data["operator_entanglement_points"]
        op_fixed = np.asarray([p[fixed_name] for p in op])
        op_mask = np.abs(op_fixed - fixed_value) < 0.011
        op_x = np.asarray([p["theta_x"] for p in op])[op_mask]
        op_y = np.asarray([p["theta_z" if fixed_name == "theta_zz" else "theta_zz"] for p in op])[op_mask]
        op_v = np.asarray([p["operator_entanglement"] for p in op])[op_mask]
        ax.scatter(op_x, op_y, c=op_v, s=18, cmap="Greens", edgecolors="black", linewidths=0.25)

slice_plot(axes[0, 1], "theta_zz", sel["theta_zz"], tz, mag, "(c) Magnetization", "Blues")
slice_plot(axes[0, 2], "theta_zz", sel["theta_zz"], tz, ent, "(d) State/operator entanglement", "Reds", True)
slice_plot(axes[0, 3], "theta_z", sel["theta_z"], tzz, mag, "(e) Magnetization", "Blues")
slice_plot(axes[1, 0], "theta_z", sel["theta_z"], tzz, ent, "(f) State/operator entanglement", "Reds", True)

for ax, row, label in zip(axes[1, 1:], data["dynamics"], ["(g)", "(h)", "(i)"]):
    twin = ax.twinx()
    ax.plot(row["cycles"], row["magnetization_abs"], "o-", ms=2.5, lw=1.0, color="#0040D6", label="Magnetization")
    twin.plot(row["cycles"], row["state_entanglement"], lw=1.2, color="#DF0412", label="State entanglement")
    ax.set(xlabel="Floquet cycle", ylabel="Magnetization", title=f"{label} {row['name'].replace('_', ' ')}")
    twin.set_ylabel("Normalized entanglement")
    twin.set_ylim(0, 1)

for ext in ("pdf", "png"):
    fig.savefig(ROOT / f"figures/figure2_parameter_scan.{ext}", dpi=250)
