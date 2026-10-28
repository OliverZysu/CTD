# CTD manuscript figure manifest

All four figures are original vector redraws made for manuscript preparation on 2026-10-06. They are 6.4 inches wide, use embedded TrueType fonts, and also have 300 dpi PNG previews. `build_figures.py` is the editable, rerunnable source. `figure_values.json` records the plotted summaries. No source artifact was modified.

The numerical figures reconstruct reported slide/table labels. They are **not** row-level reanalysis, independent replication, prospective evaluation, or causal validation. No confidence intervals, p-values, or unknown model metrics were manufactured.

## Figure 1 — workflow.pdf / workflow.png

Conceptual workflow with an explicit dashed **Proposed extension** area. CTD and ED appear as separate dataset graphs: only the CTD row leads to the retained GraphSAGE implementation and its ranked model–label discordances, while the ED row leads to the reported GCN/MLP/GAT pilot. The graph-node label describes chemical / disease nodes without asserting bidirectional implementation. The retained ranked export contains errors only, so these records are not labeled as an unrestricted set of novel positive candidates. Raw CTD and ED datasets were not supplied. The chemical–disease baseline code and an interface specification exist. The figure does not establish a deployed or tested end-to-end system. Literature retrieval, gene-node integration, Acemap navigation and links to evidence are presented as components of the proposed integrated extension, with literature and gene context shown as parallel evidence views; preliminary offline evidence checks are summarized separately in Figure 2.

Sources:

- `/mnt/user-ssd/zengboyi/ctd/ctd_ppt_data/ctd_ppt_data/CTD/graphsage.py` — GraphSAGE implementation.
- `/mnt/user-ssd/zengboyi/ctd/ctd_ppt_data/ctd_ppt_data/CTD/data_utils.py` — chemical–disease data-processing code.
- `/mnt/user-ssd/zengboyi/ctd/ctd_ppt_data/ctd_ppt_data/环境污染物需求/环境污染物需求.md` — interface requirements, CTD/ED fields and bibliographic fields; not proof of implementation.
- `/mnt/user-ssd/zengboyi/ctd/ctd_ppt_data/ctd_ppt_data/DDE组会文档20260105_环境.pptx`, slide 3 — reported system prototype/development coordination.
- User's current extension request — broader chemical coverage, Acemap links, gene nodes/relations and linked literature for candidate relations.

## Figure 2 — evidence_support.pdf / evidence_support.png

Panel A: preliminary literature retrieval yield, ranked sample **304 / 1,000 = 30.4%**, random sample **72 / 1,000 = 7.2%**. These values were transcribed from the source chart. The source chart's stronger “better than chance” title is not adopted, because independent screening and evaluation details were not supplied.

Sources:

- `/mnt/user-ssd/zengboyi/ctd/ctd_ppt_data/ctd_ppt_data/疾病污染物.pptx`, slide 15, embedded chart.
- Extracted source chart: `/mnt/user-ssd/zengboyi/ctd/journal_submission_20261006/evidence/slide15_image10.png`, panel A.

Panel B: shared-gene-path yield **128 / 1,000 = 12.8%**, compared with the chart-reported **18.7%** mean over **200** disease-label permutations. The 12.8% observation is lower than the displayed permutation mean; the figure does not claim gene-path enrichment. The raw permutation distribution was not available, so no error bars, variance estimate or significance test is drawn. The historical script describes permutation of disease labels over the same 1,000 chemicals with an all-record denominator.

Panel C: a separate conditional result, **639 / 1,000** records mappable and **128 / 639 = 20.0%** with at least one shared gene. The displayed percentage follows the source rounding (128/639 × 100 = approximately 20.031%). This conditional percentage is not placed on the all-record comparison axis. Mappability is based on chemical–gene and curated gene–disease lookup availability. The historic analysis uses human chemical–gene interactions and CTD curated gene–disease associations.

Sources:

- `/mnt/user-ssd/zengboyi/ctd/ctd_ppt_data/ctd_ppt_data/CTD_周进展_0809.pptx`, slide 1.
- `/mnt/user-ssd/zengboyi/ctd/ctd_ppt_data/ctd_ppt_data/CTD_weekly_0809/mechanism_support_0809.png` — visible 12.8% and 18.7% chart labels and the 200-permutation mean label.
- `/mnt/user-ssd/zengboyi/ctd/build_weekly_progress_0809.py`, functions `load_stats` and `make_chart` — historical algorithm and denominator description; not rerun because its original CTD public-data files were not supplied as current frozen evidence.
- Text extraction: `/mnt/user-ssd/zengboyi/ctd/journal_submission_20261006/evidence/CTD_周进展_0809.txt`.

## Figure 3 — pilot_metrics.pdf / pilot_metrics.png

Dot plots show **F1-score** and **AUROC** only, for the literature-extracted disease–pollutant (ED) pilot. Source graph size: 639 pollutant nodes and 94 disease nodes. Axes show their numerical limits clearly; points have no uncertainty bars because repetitions and uncertainty were not reported. GraphSAGE has no plotted ED metric because no such result was supplied.

| Model | Accuracy | Recall | F1-score | AUROC |
|---|---:|---:|---:|---:|
| GCN | 0.8342 | 0.8517 | 0.8430 | 0.9254 |
| MLP | 0.8542 | 0.8631 | 0.8587 | 0.9392 |
| GAT | 0.8474 | 0.8473 | 0.8474 | 0.9382 |

Sources:

- `/mnt/user-ssd/zengboyi/ctd/ctd_ppt_data/ctd_ppt_data/DDE组会文档20251215_环境.pptx`, slide 2, metrics table.
- Text extraction: `/mnt/user-ssd/zengboyi/ctd/journal_submission_20261006/evidence/DDE组会文档20251215_环境.txt`.

## Figure 4 — literature_rank.pdf / literature_rank.png

Panel A shows seven sampled windows of 1,000 ranked records, starting at ranks **1, 10,001, 20,001, 30,001, 40,001, 50,001, 60,001**, respectively. Retrieval yields: **30.4, 19.3, 15.8, 15.5, 14.5, 14.4, 17.8%**. The axis uses the explicitly labeled rank starts from the source chart; model probabilities are not inferred from plotted coordinates.

Panel B shows ten consecutive bins of 100 records within the first 1,000 ranked records. Retrieval yields: **38, 34, 37, 30, 28, 33, 21, 31, 29, 23%**. These counts sum to 304 / 1,000 and are arithmetically consistent with Figure 2A. The figure omits source-chart fitted lines and correlation claims because the underlying screening records and full numerical inputs were not available.

Sources:

- `/mnt/user-ssd/zengboyi/ctd/ctd_ppt_data/ctd_ppt_data/疾病污染物.pptx`, slide 14, embedded chart.
- Extracted source chart: `/mnt/user-ssd/zengboyi/ctd/journal_submission_20261006/evidence/slide14_image9.png`, panels A and B.

## Storage and regeneration

Run `python3 build_figures.py` from any working directory. The script writes only its named products under this figures directory and uses a temporary directory here for Matplotlib and temporary-file state. That disposable cache is removed when rendering finishes. It does not call the historical analysis script or access its `/tmp` paths.

Destination verified as `/mnt/user-ssd` on `JuiceFS:bj9-cloudml:user-ssd`, mounted read/write with `allow_other`. The output directory inherits group 12027 from the manuscript task; output figure files are group-readable/writable without world-write access. Expected shared-storage peak is below 30 MiB, with no intentional local bulk write. The parent task maintains the overall storage ledger. Root disk usage before this subtask: **82.159 GiB (83.625%)**, available **16.073 GiB**. No existing data or other tasks' files were removed.

Verification at 2026-10-06 02:15 UTC: all four PDFs contain one page, are exactly **460.8 pt (6.4 in)** wide, and embed their DejaVu Sans / DejaVu Sans Bold TrueType subsets with Unicode mappings. PNG previews were visually checked; all labels and numerical values are legible, and the workflow connector was adjusted to avoid crossing text. All rendering temporary directories were removed. Final figure products and source occupy approximately **0.86 MiB** on shared storage. No continuing task-owned cache growth remains.

Whole-machine root usage after rendering was **82.180 GiB (83.645%)**, available **16.052 GiB**. The approximately 0.020 GiB increase is a whole-machine observation during concurrent work, not a measured local footprint of these shared-storage figures. No local data were removed; the recovery/regeneration location is this figures directory and `build_figures.py`.

Scientific-label revision: all four figures were regenerated after the retained-export audit. Record counts and percentages are unchanged; CTD and ED training paths are distinct, the export is labeled as discordances, and literature/gene evidence views run in parallel. Figure 4 retains vertically stacked panels A (top) and B (bottom).
