# Data files

All four files are ordinary UTF-8 JSON and can be read without project-specific libraries.

- `figure1_runtime_frontier.json` contains measured/estimated classical runtimes, measured QESEM runtimes, and evaluated QESEM runtime-model curves with uncertainty envelopes.
- `figure2_parameter_scan.json` contains the 21-qubit parameter scan at cycle 30, operator-entanglement scan points, and three selected 28-qubit dynamics series.
- `figure3_quantum_dynamics.json` contains the magnetization series (including separate Quantinuum H2 and Helios points), late-cycle oscillation fits, fitted amplitudes, and finite-size fit curves.
- `figure4_classical_methods.json` contains SPP, PEPO-BP, PEPS-BP, and separate 51q/74q TDVP and heuristic-corrected TEBD results together with the corresponding QESEM, PEPS, and exact-statevector references.

The files intentionally omit notebook-only diagnostics, unused fit parameters, undisplayed bond dimensions, and cycles outside the plotted ranges.

