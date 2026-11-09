#!/usr/bin/env python3
import runpy
from pathlib import Path


ROOT = Path(__file__).resolve().parent
for script in sorted((ROOT / "scripts").glob("plot_figure*.py")):
    print(f"Running {script.name}")
    runpy.run_path(str(script), run_name="__main__")

