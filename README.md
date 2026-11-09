# Main-figure data for *Resolving Structure in Prethermal Floquet Dynamics with Precision Quantum Computation*

This repository contains the numerical data and minimal plotting scripts needed to reproduce the quantitative panels of the manuscript's four main figures.

The original publication figures use a more elaborate layout and styling. The scripts here intentionally use simple Matplotlib formatting so the data and scientific content are easy to inspect.

## Contents

| Manuscript figure | Data | Script | Coverage |
|---|---|---|---|
| Figure 1 | `data/figure1_runtime_frontier.json` | `scripts/plot_figure1.py` | Runtime-frontier panel (b) |
| Figure 2 | `data/figure2_parameter_scan.json` | `scripts/plot_figure2.py` | Quantitative panels (b)-(i) |
| Figure 3 | `data/figure3_quantum_dynamics.json` | `scripts/plot_figure3.py` | Panels (a)-(c) |
| Figure 4 | `data/figure4_classical_methods.json` | `scripts/plot_figure4.py` | Panels (a)-(e), with separate 51q/74q TDVP and TEBD axes |

Figure 1a and Figure 2a/2c are conceptual or circuit/system schematics rather than plots of numerical data, so they are not regenerated here.

Each JSON file is self-contained. It includes the plotted measurements or simulation results, uncertainties where applicable, and the evaluated fit/model curves needed by its corresponding script.

## Reproduce all plots

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python plot_all.py
```

The scripts write PDF and PNG files to `figures/`.

To reproduce a single figure, run its script directly, for example:

```bash
python scripts/plot_figure3.py
```

## Data conventions

- Floquet-cycle indices are integers unless a model curve uses a dense evaluation grid.
- Runtime is reported in hours.
- Experimental uncertainties are one standard deviation.
- State entanglement in the Figure 2 dynamics panels is normalized by 12, matching the manuscript plotting convention.
- Figure 3 finite-size curves use the manuscript ansatz `A(N) = a exp(-sqrt(N)/xi) + c`.
- Figure 3 separates the Quantinuum H2 and Helios measurements; the Helios series includes the cycle-21 point.
- Figure 4 stores and plots the 51q and 74q TDVP/TEBD results separately. Only the three displayed bond dimensions and cycles through 30 are included.

## Provenance

The JSON files were exported from the analysis data used for the manuscript version dated 9 November 2026. They are deliberately flattened into public, dependency-free records so reproducing the plots does not require the original research notebooks or internal software packages.

