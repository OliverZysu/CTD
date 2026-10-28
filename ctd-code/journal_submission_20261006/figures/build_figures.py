#!/usr/bin/env python3
"""Rebuild the four CTD manuscript figures from documented slide summaries.

Run: python3 build_figures.py
All outputs and temporary/cache files stay beside this script. The source
project is read-only; no training, data retrieval, or statistical reanalysis is
performed. Values transcribed from charts are identified in figure_manifest.md.
"""

from __future__ import annotations

from datetime import datetime, timezone
import json
import os
from pathlib import Path
import sys
import tempfile

sys.dont_write_bytecode = True
OUTPUT = Path(__file__).resolve().parent

NAVY = "#203C59"
TEAL = "#177E89"
AMBER = "#D09B40"
TEXT = "#253746"
MUTED = "#617180"
GRID = "#DFE6EC"
PALE = "#F4F7F9"
PALE_TEAL = "#EFF7F7"
WHITE = "#FFFFFF"

VALUES = {
    "literature_retrieval": {
        "ranked": {"retrieved": 304, "denominator": 1000, "percent": 30.4},
        "random": {"retrieved": 72, "denominator": 1000, "percent": 7.2},
        "status": "Transcribed from slide chart labels; no row-level audit.",
    },
    "gene_paths": {
        "all_ranked_records": {"supported": 128, "denominator": 1000, "percent": 12.8},
        "mappable_records": {"supported": 128, "denominator": 639, "percent": 20.0},
        "permutation_control": {"reported_mean_percent": 18.7, "permutations": 200},
        "status": "Reported summaries only; the raw null distribution is unavailable.",
    },
    "ed_pilot": {
        "GCN": {"accuracy": 0.8342, "recall": 0.8517, "f1": 0.8430, "auroc": 0.9254},
        "MLP": {"accuracy": 0.8542, "recall": 0.8631, "f1": 0.8587, "auroc": 0.9392},
        "GAT": {"accuracy": 0.8474, "recall": 0.8473, "f1": 0.8474, "auroc": 0.9382},
    },
    "literature_rank_windows": {
        "start_ranks": [1, 10001, 20001, 30001, 40001, 50001, 60001],
        "denominator_per_window": 1000,
        "percent": [30.4, 19.3, 15.8, 15.5, 14.5, 14.4, 17.8],
    },
    "literature_top_1000_bins": {
        "start_ranks": [1, 101, 201, 301, 401, 501, 601, 701, 801, 901],
        "denominator_per_bin": 100,
        "percent": [38, 34, 37, 30, 28, 33, 21, 31, 29, 23],
    },
}


def main() -> None:
    # TemporaryDirectory removes this task's disposable font cache on exit.
    with tempfile.TemporaryDirectory(prefix=".figure-render-", dir=OUTPUT) as scratch:
        os.environ["MPLCONFIGDIR"] = str(Path(scratch) / "mplconfig")
        os.environ["TMPDIR"] = scratch
        tempfile.tempdir = scratch
        import matplotlib

        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        from matplotlib.patches import FancyArrowPatch, FancyBboxPatch

        plt.rcParams.update({
            "font.family": "DejaVu Sans",
            "font.size": 8,
            "text.color": TEXT,
            "axes.labelcolor": TEXT,
            "axes.edgecolor": GRID,
            "xtick.color": MUTED,
            "ytick.color": MUTED,
            "axes.linewidth": 0.7,
            "pdf.fonttype": 42,
            "ps.fonttype": 42,
            "savefig.facecolor": WHITE,
            "figure.facecolor": WHITE,
            "axes.facecolor": WHITE,
            "axes.unicode_minus": True,
        })

        def save(fig, stem: str) -> None:
            metadata = {
                "Title": stem.replace("_", " "),
                "Author": "CTD manuscript preparation",
                "Subject": "Preliminary reported results and proposed workflow",
                "CreationDate": datetime(2026, 10, 6, tzinfo=timezone.utc),
                "ModDate": datetime(2026, 10, 6, tzinfo=timezone.utc),
            }
            fig.savefig(OUTPUT / f"{stem}.pdf", metadata=metadata)
            fig.savefig(OUTPUT / f"{stem}.png", dpi=300)
            plt.close(fig)

        def header(fig, title: str, subtitle: str) -> None:
            fig.text(0.035, 0.962, title, fontsize=12, weight="bold", color=NAVY, va="top")
            fig.text(0.035, 0.902, subtitle, fontsize=7.6, color=MUTED, va="top")

        def plot_style(ax, upper: float, ticks) -> None:
            ax.set_ylim(0, upper)
            ax.set_yticks(ticks)
            ax.grid(axis="y", color=GRID, linewidth=0.65)
            ax.set_axisbelow(True)
            ax.spines[["top", "right", "left"]].set_visible(False)
            ax.tick_params(axis="both", length=0, labelsize=7.4)
            ax.tick_params(axis="x", pad=6)

        def box(ax, x, y, w, h, label, fill=WHITE, edge=GRID, fontsize=8.3):
            patch = FancyBboxPatch(
                (x, y), w, h, boxstyle="round,pad=0.006,rounding_size=0.012",
                linewidth=0.8, facecolor=fill, edgecolor=edge,
            )
            ax.add_patch(patch)
            ax.text(x + w / 2, y + h / 2, label, ha="center", va="center",
                    fontsize=fontsize, color=TEXT, linespacing=1.45)
            return patch

        def arrow(ax, start, end, color=NAVY, dashed=False):
            ax.add_patch(FancyArrowPatch(
                start, end, arrowstyle="-|>", mutation_scale=9,
                linewidth=1.1, color=color,
                linestyle=(0, (4, 3)) if dashed else "-",
                shrinkA=1.5, shrinkB=2,
            ))

        # Figure 1: conceptual workflow. The proposed system extension is explicit.
        fig = plt.figure(figsize=(6.4, 4.05))
        ax = fig.add_axes([0, 0, 1, 1])
        ax.set(xlim=(0, 1), ylim=(0, 1))
        ax.axis("off")
        header(fig, "From association ranking to linked evidence",
               "Conceptual workflow grounded in the available code and project specifications")
        box(ax, .031, .488, .938, .357, "", fill=PALE)
        ax.text(.05, .81, "Reported data / retained baseline", fontsize=9.5, weight="bold", color=NAVY)
        box(ax, .053, .667, .20, .104, "CTD chemical–disease\nrecords", edge="#BACAD7", fontsize=7.5)
        box(ax, .305, .667, .17, .104, "CTD graph", edge="#BACAD7", fontsize=8.3)
        box(ax, .525, .667, .18, .104, "GraphSAGE\nretained CTD code", edge="#BACAD7", fontsize=7.8)
        box(ax, .75, .667, .205, .104, "Ranked discordances\nfor review", edge="#BACAD7", fontsize=7.6)
        arrow(ax, (.259, .719), (.305, .719))
        arrow(ax, (.481, .719), (.525, .719))
        arrow(ax, (.711, .719), (.75, .719))
        ax.text(.39, .642, "chemical / disease nodes", ha="center", fontsize=6.9, color=MUTED)
        box(ax, .053, .523, .20, .104, "Manually extracted\nexposure records (ED)", edge="#BACAD7", fontsize=7.5)
        box(ax, .305, .523, .17, .104, "Separate ED\ngraph", edge="#BACAD7", fontsize=8.0)
        box(ax, .525, .523, .18, .104, "GCN · MLP · GAT\nreported pilot", edge="#BACAD7", fontsize=7.6)
        arrow(ax, (.259, .575), (.305, .575))
        arrow(ax, (.481, .575), (.525, .575))
        ax.text(.05, .453, "Separate datasets; the retained ranked export contains discordant records only.",
                fontsize=7.05, color=MUTED)
        proposed = box(ax, .031, .112, .938, .291, "", fill=PALE_TEAL, edge=TEAL)
        proposed.set_linestyle((0, (4, 3)))
        ax.text(.05, .368, "Proposed extension", fontsize=9.5, weight="bold", color=TEAL)
        box(ax, .087, .263, .296, .075, "Literature evidence\nPMIDs and source records", edge="#B5D5D6", fontsize=7.5)
        box(ax, .087, .147, .296, .075, "Gene context\nchemical–gene–disease", edge="#B5D5D6", fontsize=7.5)
        box(ax, .624, .18, .327, .133, "Linked evidence interface\nAcemap · PubMed · source pages", edge="#B5D5D6", fontsize=7.7)
        ax.plot([.389, .49, .49], [.3005, .3005, .2465], color=TEAL, lw=1.0, linestyle=(0, (4, 3)))
        ax.plot([.389, .49, .49], [.1845, .1845, .2465], color=TEAL, lw=1.0, linestyle=(0, (4, 3)))
        arrow(ax, (.49, .2465), (.624, .2465), color=TEAL, dashed=True)
        # Parallel evidence views, fed by the retained discordance ranking.
        ax.plot([.8525, .8525, .012, .012], [.661, .424, .424, .1845],
                color=TEAL, lw=1.0, linestyle=(0, (4, 3)))
        arrow(ax, (.012, .3005), (.087, .3005), color=TEAL, dashed=True)
        arrow(ax, (.012, .1845), (.087, .1845), color=TEAL, dashed=True)
        ax.text(.035, .049,
                "The evidence interface remains proposed; gene paths provide context without establishing causality.",
                fontsize=6.95, color=MUTED)
        save(fig, "workflow")

        # Figure 2: unconditional comparisons plus a separate conditional summary.
        fig = plt.figure(figsize=(6.4, 4.05))
        header(fig, "Preliminary evidence checks",
               "Reconstructed from reported summaries; denominators are kept explicit")
        fig.text(.10, .836, "A  Literature retrieval", fontsize=9.8, weight="bold", color=NAVY)
        fig.text(.60, .836, "B  Shared-gene paths", fontsize=9.8, weight="bold", color=NAVY)
        ax_a = fig.add_axes([.10, .394, .37, .392])
        ax_b = fig.add_axes([.60, .394, .36, .392])
        plot_style(ax_a, 40, [0, 10, 20, 30, 40])
        plot_style(ax_b, 25, [0, 5, 10, 15, 20, 25])
        ax_a.bar([0, 1], [30.4, 7.2], color=[NAVY, AMBER], width=.57, zorder=3)
        ax_b.bar([0, 1], [12.8, 18.7], color=[NAVY, AMBER], width=.57, zorder=3)
        ax_a.set_xticks([0, 1], ["Ranked sample\nn = 1,000", "Random sample\nn = 1,000"])
        ax_b.set_xticks([0, 1], ["Ranked sample\nn = 1,000", "Permuted labels\n200 runs"])
        ax_a.set_ylabel("Retrieval yield (%)", fontsize=8.0, labelpad=5)
        ax_b.set_ylabel("Records with a path (%)", fontsize=8.0, labelpad=5)
        ax_a.set_xlim(-.55, 1.55)
        ax_b.set_xlim(-.55, 1.55)
        for x, value, count in [(0, 30.4, "304 / 1,000"), (1, 7.2, "72 / 1,000")]:
            ax_a.text(x, value + 1.2, f"{value:.1f}%", ha="center", va="bottom",
                      weight="bold", fontsize=9.2, color=NAVY)
            ax_a.text(x, value * .46, count, ha="center", va="center", fontsize=7.1,
                      color=WHITE if x == 0 else TEXT)
        for x, value, label in [(0, 12.8, "128 / 1,000"), (1, 18.7, "reported\nmean")]:
            ax_b.text(x, value + .9, f"{value:.1f}%", ha="center", va="bottom",
                      weight="bold", fontsize=9.2, color=NAVY)
            ax_b.text(x, value * .46, label, ha="center", va="center", fontsize=7.0,
                      color=WHITE if x == 0 else TEXT)
        card_ax = fig.add_axes([0, 0, 1, 1], zorder=-1)
        card_ax.set(xlim=(0, 1), ylim=(0, 1))
        card_ax.axis("off")
        box(card_ax, .059, .145, .9, .126, "", fill=PALE_TEAL, edge="#C9DFE0")
        fig.text(.079, .238, "C  Conditional result among mapped records", fontsize=8.8, weight="bold", color=TEAL)
        fig.text(.079, .186, "639 / 1,000 records mappable", fontsize=8.0)
        fig.text(.527, .186, "128 / 639 = 20.0% with a shared gene", fontsize=8.0)
        fig.text(.035, .094, "Raw retrieval decisions and the permutation distribution were unavailable.", fontsize=7.25, color=MUTED)
        fig.text(.035, .055, "Literature retrieval and shared-gene paths are preliminary checks; they do not establish causality.", fontsize=7.25, color=MUTED)
        save(fig, "evidence_support")

        # Figure 3: only the ED metrics actually supplied in the slide table.
        fig = plt.figure(figsize=(6.4, 2.85))
        header(fig, "ED pilot: preliminary reported benchmark",
               "Disease–pollutant graph: 639 pollutant nodes and 94 disease nodes")
        models = ["GCN", "MLP", "GAT"]
        model_colors = [NAVY, TEAL, AMBER]
        for left, metric, title, limits, ticks in [
            (.13, "f1", "A  F1-score", (.82, .89), [.82, .84, .86, .88]),
            (.62, "auroc", "B  AUROC", (.91, .96), [.91, .93, .95]),
        ]:
            ax = fig.add_axes([left, .23, .35, .5])
            ax.set(xlim=limits, ylim=(-.55, 2.55))
            ax.set_yticks([2, 1, 0], models)
            ax.set_xticks(ticks)
            ax.spines[["top", "right", "left"]].set_visible(False)
            ax.tick_params(axis="both", length=0, labelsize=8.1)
            ax.tick_params(axis="y", pad=8)
            ax.tick_params(axis="x", pad=7)
            ax.grid(axis="x", color=GRID, linewidth=.65)
            for y in [2, 1, 0]:
                ax.axhline(y, color=GRID, linewidth=.6, zorder=1)
            for y, model, color in zip([2, 1, 0], models, model_colors):
                value = VALUES["ed_pilot"][model][metric]
                ax.scatter(value, y, s=42, color=color, edgecolor=WHITE, linewidth=.7, zorder=4)
                ax.text(value + (limits[1] - limits[0]) * .038, y, f"{value:.4f}",
                        va="center", fontsize=8.2, color=TEXT,
                        bbox={"facecolor": WHITE, "edgecolor": "none", "pad": 1.2}, zorder=5)
            ax.text(-.155, 1.10, title, transform=ax.transAxes,
                    fontsize=9.8, weight="bold", color=NAVY)
        fig.text(.035, .065,
                 "Single reported summaries; data splits, repeated runs and uncertainty were not documented.",
                 fontsize=7.2, color=MUTED)
        save(fig, "pilot_metrics")

        # Figure 4: rank positions and exact labels, with no fabricated probabilities.
        fig = plt.figure(figsize=(6.4, 4.7))
        header(fig, "Literature retrieval yield across ranked records",
               "Reported chart labels; each window or bin has an explicit sample size")
        fig.text(.105, .843, "A  Sampled windows across the ranking (n = 1,000 per window)",
                 fontsize=9.2, weight="bold", color=NAVY)
        fig.text(.105, .455, "B  Within the first 1,000 records (n = 100 per bin)",
                 fontsize=9.2, weight="bold", color=NAVY)
        ax_a = fig.add_axes([.105, .585, .86, .221])
        ax_b = fig.add_axes([.105, .195, .86, .221])
        for ax in [ax_a, ax_b]:
            plot_style(ax, 45, [0, 20, 40])
            ax.set_ylabel("Yield (%)", fontsize=8.0, labelpad=6)
        windows = VALUES["literature_rank_windows"]
        rates = windows["percent"]
        ax_a.bar(range(7), rates, width=.57, color=NAVY, zorder=3)
        ax_a.set_xticks(range(7), [f"{r:,}" for r in windows["start_ranks"]])
        ax_a.set_xlabel("Start rank of each window of 1,000 records", fontsize=8.0, labelpad=7)
        ax_a.set_xlim(-.58, 6.58)
        for x, value in enumerate(rates):
            ax_a.text(x, value + 1.5, f"{value:.1f}%", ha="center", va="bottom", fontsize=8.0, color=NAVY,
                      bbox={"facecolor": WHITE, "edgecolor": "none", "pad": .5})
        bins = VALUES["literature_top_1000_bins"]
        ax_b.bar(range(10), bins["percent"], width=.57, color=TEAL, zorder=3)
        ax_b.set_xticks(range(10), [f"{r:,}–{r+99:,}" for r in bins["start_ranks"]])
        ax_b.tick_params(axis="x", labelsize=6.9)
        ax_b.set_xlabel("Rank interval", fontsize=8.0, labelpad=7)
        ax_b.set_xlim(-.58, 9.58)
        for x, value in enumerate(bins["percent"]):
            ax_b.text(x, value + 1.5, f"{value:g}%", ha="center", va="bottom", fontsize=8.0, color=TEAL,
                      bbox={"facecolor": WHITE, "edgecolor": "none", "pad": .5})
        fig.text(.035, .057,
                 "Rates were transcribed from slide charts. Literature identities and screening decisions require audit.",
                 fontsize=7.1, color=MUTED)
        save(fig, "literature_rank")

        (OUTPUT / "figure_values.json").write_text(
            json.dumps(VALUES, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )
        for path in OUTPUT.iterdir():
            if path.is_file() and path.name in {
                "workflow.pdf", "workflow.png", "evidence_support.pdf", "evidence_support.png",
                "pilot_metrics.pdf", "pilot_metrics.png", "literature_rank.pdf", "literature_rank.png",
                "figure_values.json",
            }:
                path.chmod(0o660)
        print("Generated workflow, evidence_support, pilot_metrics and literature_rank (PDF + PNG).")


if __name__ == "__main__":
    main()
