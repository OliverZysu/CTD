# Scientific code and artifact audit

Audit date: 2026-10-06. Source root for relative `file:line` citations below:
`/mnt/user-ssd/zengboyi/ctd/ctd_ppt_data/ctd_ppt_data/CTD`.

This audit used static source inspection, Python AST parsing, streaming TSV counts, CSV parsing, and whitelisted checkpoint metadata inspection. No model was trained, executed, or evaluated. No packages were installed. Descriptive counts are reproducible with `python3 code_evidence_analysis.py` in this evidence directory. The resulting `code_results_summary.json` contains file identities, SHA256 checksums for the tabular artifacts, exact counts, source constants and tensor shapes. It is not a model-results reproduction.

## 1. Findings that govern manuscript claims

1. **The supplied top-10 and all-error CSV files are inconsistent.** The all-error file contains 62,042 records, its maximum score is 0.9964913726, and the separate top-10 file contains scores from 0.9999141693 to 0.9999955893. None of the ten compound–disease name pairs occurs in the all-error file. Yet the supplied exporter creates `df_top10 = df_all.head(10)` (`graphsage.py:300–303`). These files therefore cannot be represented as an intact all-errors/top-10 pair produced by that code invocation. Their actual run or edit history is unknown.
2. **These are errors, not a validated discovery list.** The exporter selects `y_pred != y_true`, sorts by the probability of the predicted class, and discards true labels, predicted labels, stable entity IDs and all other class probabilities (`graphsage.py:266–293`). In a binary run the reported score is `max(p(no association), p(association))`, so it may describe a confident prediction of no association. Neither false-positive/false-negative direction nor biological novelty can be recovered from the CSV alone.
3. **No completed numerical training log is present.** Both `gat_improved_training.log:1–4` and `gat_optimized_training.log:1–4` end in `ModuleNotFoundError: No module named 'torch_geometric'`. Checkpoints and loss-curve images also exist, but are not linked to these failed invocations by a run manifest. The logs do not prove that no successful run ever occurred; they do not substantiate numerical performance.
4. **Archived models represent different node populations and class counts.** Metadata in `best_gat_final.pt` shows 728 embedding rows and 2 output classes; `best_graphsage.pt` has 25,018 embedding rows and 2 classes; optimized and improved GAT each have 13,942 embedding rows and 3 classes. Treating these as checkpoints from one common benchmark is unsupported. Tensor dimensions alone do not identify their data sources or splits.
5. **The code snapshot is not directly reproducible.** `gcn.py` fails parsing at line 42. Six other model entry points unpack four loader values while the supplied shared loader returns five. All four explicitly referenced CTD/environment source files are missing at their configured paths and absent from the audited CTD subtree.
6. **The supplied graph code is a learned-ID, two-part link predictor.** It is not evidence of a implemented heterogeneous chemical–gene–disease explanation model or literature retrieval/acemap integration. Gene support in the loader is an alternative input-column alias (`data_utils.py:80–100`), not a separate third node type.

## 2. Descriptive results measured directly from the files

### All-error CSV

Source: `CTD/graphsage_wrong_predictions_all.csv:1`; first nonempty record at line 3. The blank second line explains why the file has 62,044 newline-terminated lines but only 62,042 parsed data records. There are no empty values in the three exported fields.

| Quantity | Directly measured value |
|---|---:|
| Parsed error records | 62,042 |
| Distinct compound names | 16,171 |
| Distinct disease names | 6,193 |
| Distinct compound-name/disease-name pairs | 61,973 |
| Repeated rows beyond the first identical row | 69 |
| Name pairs that occur more than once | 69 |
| Minimum reported predicted-class probability | 0.5000077486 |
| Median probability | 0.7536072433 |
| Mean probability | 0.7483805419 |
| Maximum probability | 0.9964913726 |
| Records with probability ≥ 0.90 | 12,413 |
| Records with probability ≥ 0.95 | 4,844 |
| Records with probability ≥ 0.99 | 200 |

All rows are sorted by descending score. Duplicate counts concern the exported names and scores: entity IDs are absent, so name collisions cannot be distinguished from repeated sampled pairs. The full test denominator and correctly predicted records are absent; accuracy, precision, recall, F1, AUROC, calibration and discovery yield cannot be calculated from this export.

Among the first 1,000 error records there are 805 compound names, 739 disease names and 998 distinct name pairs; scores range from 0.9793844223 to 0.9964913726. Ozone and bisphenol F each occur eight times, while decamethrin, Tobacco Smoke Pollution and methylmercuric chloride each occur six times. The most common disease label is “Diabetes Mellitus, Experimental” (11 records); Autistic Disorder, Cell Transformation, Neoplastic, Lung Neoplasms, Prostatic Neoplasms and Carcinoma, Hepatocellular each occur nine times. These are distributions within selected model errors, not disease-risk frequencies, association enrichment or a confirmed new-relation cohort. Exact top-20 name counts are in `code_results_summary.json:98`.

The separate top-10 file (`CTD/graphsage_top10_wrong_predictions.csv:2–11`) begins with Baclofen–Decerebrate State and Ceftriaxone–Cerebral Ventriculitis. All ten are absent from the all-error file, and all ten scores exceed its maximum. Do not merge the files for analyses or label either one a supported set of novel relations.

### SIDER-format adverse-event tables

The two TSV files use drug IDs, UMLS-style concept IDs and MedDRA LLT/PT vocabulary fields, matching the SIDER distribution format (`meddra_all_se.tsv:1–5`, `meddra_freq.tsv:2–5`). Their filenames and schema are consistent with SIDER; no local download manifest/version or processing script establishes a release history. These are drug-side-effect records, not a CTD environmental-exposure relation table.

| File | Nonblank rows | Distinct flat drug IDs | PT rows | Distinct mapped PT concepts | Distinct flat-drug/mapped-PT pairs |
|---|---:|---:|---:|---:|---:|
| `meddra_all_se.tsv` | 309,849 | 1,430 | 163,206 | 4,251 | 145,321 |
| `meddra_freq.tsv` | 291,632 | 968 | 154,507 | 2,964 | 59,542 |

PT means the value in column 4 for `meddra_all_se.tsv` or column 8 for `meddra_freq.tsv`; mapped PT concept means column 5 or 9, respectively. Flat drug ID is column 1. These definitions matter: using original concepts, LLT rows, stereospecific IDs, names or all terminology levels gives different counts. `meddra_freq.tsv` also has one leading blank physical line; its repeated rows represent frequency/terminology records rather than unique associations.

No audited Python file refers to either TSV file. Consequently these counts may describe available data resources but cannot be called the trained model's sample sizes, CTD graph statistics, or an external validation result. Drug adverse effects, therapeutic associations, marker/mechanism annotations, inferred CTD links and environmental exposures require separate relation semantics and validation.

## 3. Exact shared preprocessing protocol expressed by the current source

The shared implementation is `data_utils.py`; MLP and GCN include similar local copies. These are **source defaults**, not recovered run configurations.

* It reads CSV ChemicalID/DiseaseID/DirectEvidence columns and can use GeneID as a substitute source identifier. The GeneID column is renamed ChemicalID. It creates a source-node index block followed by a disease-node index block (`data_utils.py:80–103`, `158–177`). It does not create simultaneous chemical and gene node types or chemical–gene edges.
* Non-binary mode drops rows without recognized direct evidence, maps marker/mechanism to class 1 and therapeutic to class 2, and folds the combined string `marker/mechanism|therapeutic` into therapeutic (`data_utils.py:128–148`, `182–190`). This is a modeling decision; it is not a biological proof that the combined category is purely therapeutic.
* In forced-binary mode every retained CSV row becomes positive regardless of direct evidence (`data_utils.py:145–148`, `155–156`, `185–186`). With the full CTD chemical–disease CSV configured, this can conflate curated marker/mechanism, therapeutic and inferred relations unless the input itself was filtered. The input is unavailable, so the actual composition cannot be counted.
* JSON ingestion retains only the Chinese `污染物` and `疾病` fields, treating their stripped strings as source/disease IDs (`data_utils.py:110–124`). There is no explicit crosswalk reconciling CTD identifiers, PubChem identifiers and free-text names. In three-class mode **all environmental JSON rows are assigned class 2**, which is therapeutic for CSV rows (`data_utils.py:192–196`). This is a concrete label-semantic defect in the optional combined-data path; current GraphSAGE/final-GAT defaults disable JSON.
* Missing CSV/JSON paths generate warnings and can silently change the available source mixture (`data_utils.py:107–108`, `125–126`); no positive records causes an early return (`202–204`). A reproducible pipeline should require the declared source manifest to match, rather than switch task interpretation when a source is absent.
* NumPy random generator seed is 42 by default (`data_utils.py:18`, `32`). Negative ratio is 1.0; validation and test proportions are each 0.1 (`15–17`). Candidate negative source/disease IDs are sampled uniformly and excluded if they belong to any retained positive pair (`206–225`). The code **does not exclude a candidate already accepted as a negative**, so sampling is with replacement over absent pairs. Absence from a curated resource is an unlabeled state rather than experimental evidence of no relationship.
* The code shuffles all records, then performs class-stratified record splitting using the same seed; per class `n_val=floor(0.1n)`, `n_test=floor(0.1n)` and all remaining records go to training (`235–274`). There is no pair-grouped, entity-disjoint, temporal or publication-disjoint split.
* The message-passing adjacency is built only from positive training records (`276–279`), and the same training adjacency is used for training, validation and test objects (`287–298`). This correctly avoids deliberately adding every held-out edge to the graph, but does not prevent pair-level overlap caused by duplicate records. Positive deduplication occurs on `(ChemicalID, DiseaseID, DirectEvidence)` before label normalization, rather than the final relation identity (`131`). JSON positives are not deduplicated; cross-source positives are concatenated. Actual cross-split overlap cannot be quantified without original inputs and split records.
* Only source-to-disease edges are constructed. There is no reverse-edge concatenation or `to_undirected` operation. The current source therefore does not support describing bidirectional chemical/disease message propagation (`276–279`). Node features are integer indices consumed by learned embedding tables, rather than chemical structures, gene expression, molecular descriptors or text embeddings (`281`, `graphsage.py:86–101`).

## 4. Model settings and evaluation

All rows below describe supplied source defaults. The absence of run manifests prevents assuming that the checkpoints, figures or slides were generated with those defaults.

| Model source | Configured input/task | Dimensions and training settings | Selection/evidence |
|---|---|---|---|
| `graphsage.py` | full `CTD_chemicals_diseases.csv`; binary; JSON off | learned embedding 128, two SAGEConv layers 128→256→128; concatenation decoder 256→128→2; dropout 0.1; Adam lr 0.005, weight decay 1e-4; 80 epochs; unweighted CE | best validation macro-F1 checkpoint; source `70–107`, `151–170`, `192–206`, `232–243` |
| `gat_final.py` | full CTD CSV; binary; JSON off | embedding/hidden/output base dimensions 192; GAT heads 4 and 4, first concatenated (768-wide), second averaged; decoder with BatchNorm; dropout 0.1; AdamW lr 0.005, decay 1e-4; 150 epochs; unweighted CE | LinkNeighborLoader batch 2,048 and fanouts [15,10], workers 0; clip gradient norm 1.0; ReduceLROnPlateau on validation F1, factor 0.5, patience 10; best validation F1. `26–95`, `180–208`, `229–259`, `279–335` |
| `gat.py` | direct-evidence CSV; three classes | embedding/hidden/output 128; heads 4 and 4; dropout/attention dropout 0.1; AdamW lr 0.005, decay 1e-4; 100 epochs; CE | final epoch evaluated; loader return-arity defect. `24–68`, `105–178` |
| `gat_optimized.py` | direct-evidence CSV; three classes | embedding 256, hidden 256, output 128; heads 8 and 1; dropout 0.3, attention dropout 0.1; AdamW lr 0.002, decay 1e-4; 150 epochs; CE weighted by inverse class frequency | best validation F1; LR plateau factor 0.5, patience 10 on F1; loader return-arity defect. `119–194`, `209–233` |
| `gat_improved.py` | direct-evidence CSV; three classes | embedding/hidden/output 256; three GAT layers with heads 8/8/4, residual projections, LayerNorm, learned node-type and degree features; dropout/attention dropout 0.2; AdamW lr 0.001, decay 5e-4; at most 150 epochs | hardcoded chemical boundary 10,622; custom focal loss gamma 2 with class weights; LR plateau on loss, factor 0.5/patience 10; best-F1 selection and early-stop patience 20; loader return-arity defect. `32–168`, `171–205`, `232–349` |
| `lightgcn.py` | direct-evidence CSV; three classes | embedding 128; three LGConv layers; mean of initial and layer embeddings; concatenation MLP; dropout 0.1; AdamW lr 0.005, decay 5e-5; 100 epochs; CE | final epoch; loader return-arity defect. `24–65`, `92–157` |
| `node2vec_baseline.py` | direct-evidence CSV; three classes | Node2Vec embedding 128, walk length 20, context size 10, 10 walks/node, 1 negative sample, batch 256, SparseAdam lr 0.01, 20 embedding epochs; frozen embeddings, MLP hidden128/dropout0.1, AdamW lr0.01/decay5e-5, 80 classifier epochs | final epoch; loader return-arity defect. `18–52`, `89–160`, `166–189` |
| `degree_logreg_baseline.py` | direct-evidence CSV; three classes | features: source degree, target degree, degree product, all from training graph; train-fitted StandardScaler; multinomial LogisticRegression, lbfgs, C=1, max_iter=200 | loader return-arity defect. `18–35`, `54–95` |
| `mlp.py` | `high_inference_score_relationships.csv`; binary; JSON off | embedding64; concatenated pair→hidden128→2; dropout0.1; Adam lr0.01; 100 epochs; CE | final epoch; local loader, no checkpoint selection. `230–258`, `290–335`, `345–365` |
| `gcn.py` | high-inference CSV; binary; JSON off | intended embedding128, GCN hidden256/output128; dropout0.1; Adam lr0.005/decay1e-4;100 epochs | syntax-invalid snapshot; settings are intentions only. `246–286`, `330–381`; first parse failure at42 |

Standard metrics are accuracy and macro-averaged precision, recall and F1; AUROC uses class-1 probability for binary GraphSAGE/final-GAT/MLP and one-vs-rest for multiclass (`graphsage.py:129–146`; `gat_final.py:153–175`; `mlp.py:270–287`). Several evaluators catch any AUROC `ValueError` and replace it with 0.5; this value can therefore be an error fallback rather than a computed statistic. There is no AUPRC, candidate retrieval metric, calibration evaluation, confidence interval or multi-seed aggregation in the supplied entry points. PyTorch initialization/dropout/neighborhood sampling seeds are not set in these files; the NumPy split seed alone does not establish full run determinism.

The custom focal loss computes `pt = exp(-weighted_cross_entropy)` (`gat_improved.py:181–184`); this is not equivalent to applying an alpha weight outside the conventional unweighted-probability focal factor. Report the implemented formula if that model is retained.

## 5. Reproducibility and artifact mismatches

### Code execution defects

`data_utils.py:303` returns `(train_data, val_data, test_data, num_nodes, num_classes)`, while these callers expect only four values:

* `degree_logreg_baseline.py:62`
* `node2vec_baseline.py:116`
* `lightgcn.py:107`
* `gat.py:124`
* `gat_optimized.py:142`
* `gat_improved.py:254`

The mismatch is visible statically and would prevent those entry points from reaching training with this loader. `gcn.py:42` produces `IndentationError: expected an indented block after 'if' statement on line 41`; further broken indentation is visible at `75`, `78` and `323`. Eleven other Python sources parse successfully; syntax success is not a runtime or scientific-validity test.

### Missing inputs

All of these absolute paths are nonexistent and their basenames are absent from the audited CTD subtree:

* `/home/byzeng/hjwrw_all_data/CTD_chemicals_diseases.csv`
* `/home/byzeng/hjwrw_all_data/direct_evidence_relationships.csv`
* `/home/byzeng/hjwrw_all_data/high_inference_score_relationships.csv`
* `/home/byzeng/hjwrw_all_data/环境污染物_pubchemCID.json`

The configured paths appear in `graphsage.py:153–155`, `gat_final.py:182–184`, `mlp.py:292–294`, `gat.py:106`. This is a statement about the current machine and audited subtree, not proof that the files never existed elsewhere. A high-inference-score threshold, CTD release, retrieval date and filtering pipeline cannot be recovered from the filenames alone.

### Checkpoint dimensions

Only the small ZIP member `data.pkl` was inspected through a strict whitelist returning tensor metadata; tensor-storage bytes were not loaded and pickle-specified code was not imported. Details are in `code_results_summary.json:272`.

| Archived file | Embedding shape | Final classifier weight shape |
|---|---|---|
| `CTD/best_gat_final.pt` | [728,192] | [2,192] |
| `CTD/best_graphsage.pt` | [25018,128] | [2,128] |
| `CTD/best_gat_optimized.pt` | [13942,256] | [3,128] |
| `CTD/best_gat_improved.pt` | [13942,256] | [3,256] |

No checkpoint contains the source-data hashes, node-ID dictionary, complete split ledger, code revision or training metrics needed to link these dimensions to a named experiment. The 728-node final-GAT checkpoint is especially incompatible with treating it as a direct comparator on the same complete node population as the 25,018-node GraphSAGE checkpoint. It may be from another dataset or experiment; the archive does not establish which one.

### Publication packaging

`gcn_train.sh:35` contains a plaintext access credential. The value is intentionally not reproduced here. Exclude or sanitize that line before distributing a code supplement; the manuscript package must not copy the original script unchanged. The script's active invocation is GraphSAGE (`gcn_train.sh:44`) despite its filename and SLURM job name referring to GCN; the filename is not a reliable run-model identifier.

## 6. What a manuscript can and cannot currently claim

Supported now: the existence and described source design of the link-prediction prototypes; exploratory records/plots supplied separately; the descriptive CSV and SIDER-format counts above; the stated artifact inconsistencies; and a proposed system extension with typed compounds, genes, diseases and provenance-aware literature links.

Not established by this code bundle: a reproducible ranking of models, statistically significant discovery performance, validated new disease–pollutant links, causal exposure effects, biological mechanistic explanations, improved performance from genes, live acemap links, or a fully deployed combined chemical–gene–disease system. Planned extensions must be described as a design or future work until their implementations and outcomes are available.

For a new results-bearing submission, recover the versioned data and current working code; deduplicate and group splits by stable relation identity; keep sampled unobserved negatives distinct from verified negatives; record binary versus typed-relation tasks; preserve the complete labeled test predictions and independent run IDs; evaluate calibrated association probabilities and prospective/published evidence with leakage controls; and run all compared methods on common splits with multiple seeds. Gene-path validation must prevent gene-mediated CTD inference from appearing simultaneously in the target labels and the validating evidence.

## 7. Storage accounting

At start, `/` usage was 82.1493 GiB used of 98.2476 GiB (83.6146%), available 16.0826 GiB. Local bulk writes were disallowed by the storage guard. This audit wrote only small scripts and evidence reports to the verified JuiceFS `/mnt/user-ssd` mount; it created no local model/data/cache copy, installed environment or training output. Original artifacts were read in place and preserved. The root agent aggregates final storage accounting for the submission package. These evidence files are persistent deliverables and should be retained with the manuscript's audit trail.

At audit handoff (2026-10-06 02:12 UTC), `/` used 82.1718 GiB (83.6375%), available 16.0601 GiB. The system-wide change was +0.0225 GiB; this is not attributable to any local bulk output from this audit. Its three small persistent outputs total approximately 60 KiB on shared storage, with no disposable task cache to remove and no audit process left running.
