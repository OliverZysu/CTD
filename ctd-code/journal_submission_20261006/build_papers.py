#!/usr/bin/env python3
"""Build the reading, line-numbered review, and supplementary PDFs.

Requires an existing pdflatex installation. No network access or shell escape.
Run from any directory. Final files are saved here; small temporary TeX inputs may use bounded /dev/shm staging.
"""
from pathlib import Path
import os
import json
import shutil
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parent
BUILD = ROOT / "build"
SOURCE = ROOT / "source"
BUILD.mkdir(exist_ok=True)
jobs = [
    ("manuscript", "manuscript.tex"),
    ("manuscript_submission", r"\def\submissionformat{1}\input{manuscript.tex}"),
    ("supplementary", "supplementary.tex"),
]
staging_parent = Path("/dev/shm") if Path("/dev/shm").is_dir() else BUILD
# Only this task's small, reconstructible document inputs are staged. Original
# research data and weight files are never copied. The context removes staging.
with tempfile.TemporaryDirectory(prefix="ctd-paper-build-", dir=staging_parent) as temp:
    stage = Path(temp)
    shutil.copytree(SOURCE, stage / "source")
    (stage / "figures").mkdir()
    for figure in (ROOT / "figures").glob("*.pdf"):
        shutil.copy2(figure, stage / "figures" / figure.name)
    work = stage / "build"
    work.mkdir()
    env = os.environ.copy()
    observed_staging_peak = 0
    for key, directory in (("TMPDIR", "tmp"), ("TEXMFVAR", "tex-cache"), ("TEXMFCONFIG", "tex-config")):
        destination = stage / directory
        destination.mkdir()
        env[key] = str(destination)
    for name, entry in jobs:
        for run in (1, 2):
            command = ["pdflatex", "-no-shell-escape", "-halt-on-error", "-interaction=nonstopmode",
                       "-output-directory", str(work), "-jobname", name, entry]
            result = subprocess.run(command, cwd=stage / "source", env=env, text=True,
                                    stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=300)
            (BUILD / f"{name}.pass{run}.txt").write_text(result.stdout)
            observed_staging_peak = max(observed_staging_peak, sum(p.stat().st_size for p in stage.rglob("*") if p.is_file()))
            if result.returncode:
                print(result.stdout[-6000:])
                raise SystemExit(result.returncode)
        shutil.copy2(work / f"{name}.pdf", ROOT / f"{name}.pdf")
        shutil.copy2(work / f"{name}.log", BUILD / f"{name}.log")
        print(f"Built {ROOT / (name + '.pdf')}", flush=True)
    (BUILD / "build_metadata.json").write_text(json.dumps({
        "observed_staging_peak_bytes": observed_staging_peak,
        "staging_parent": str(staging_parent),
        "staging_cleanup": "TemporaryDirectory removes staging on context exit",
        "compiler": subprocess.run(["pdflatex", "--version"], text=True, stdout=subprocess.PIPE).stdout.splitlines()[0],
        "shell_escape": False,
        "passes_per_document": 2,
    }, indent=2))
