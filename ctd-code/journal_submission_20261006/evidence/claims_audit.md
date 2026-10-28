# Independent scientific-claim audit for the CTD manuscript

Audit date: 2026-10-06. Scope: supplied slide text and relationship XML, `build_weekly_progress_0809.py`, `mechanism_support_0809.png`, the GraphSAGE error-export code and CSV, and three independently checked cited papers. This is an evidence audit; no model was retrained and no missing result was reconstructed.

## Recommended scientific framing

The defensible current contribution is an **exploratory workflow for prioritizing chemical–disease associations and examining their literature and gene context**, accompanied by an explicit reproducibility audit. The supplied artifacts do not establish previously unknown causal pollutant–disease discoveries, superior GNN performance, prospective validation, or a fully implemented expanded system. A broad chemical scope is scientifically appropriate: the corpus and illustrative references include medicines, drug classes, elements, and chemical mixtures, in addition to potential environmental pollutants.

The existing literature evidence can motivate typed relationships and provenance-aware retrieval. Gene overlap is a mechanistic clue, not causal validation. In this project it also fails to show enrichment over the reported permutation comparison. These limitations belong in Results and Discussion, not only in a final disclaimer.

## Usable results, with provenance and limits

| Result | Source | Defensible wording | Limit |
|---|---|---|---|
| 9,546,982 CTD records; 108,217 records with direct evidence | `疾病污染物.pptx`, slides 2, 4, 10 | Project materials report these source-record counts | Frozen source snapshot, distinct-pair count and deduplication are absent; do not call all records verified environmental associations |
| 3,125 manually extracted epidemiological records | `疾病污染物.pptx`, slides 2/10; 20260202 slide 2 | Reported size of a literature-derived collection | Raw records, paper list, extraction protocol and inter-annotator assessment absent |
| 639 chemical/pollutant nodes and 94 disease nodes | 20251215 slide 2 | Reported node counts for the literature-derived graph | Do not assume 3,125 records are 3,125 unique edges |
| Literature-derived dataset: GCN AUC 0.9254, MLP 0.9392, GAT 0.9382 | 20251215 slide 2 | Slide-reported preliminary comparison | The MLP has the highest reported AUC; significance, seeds, split and complete prediction artifacts unavailable |
| Top-window literature yield 30.4% versus random-pair yield 7.2%, 1,000 pairs each | `疾病污染物.pptx`, slides 14–15 | Historical report of an approximately 4.22-fold difference in literature retrieval/support yield | Per-pair judgments, LLM model/prompt, search date, blinding, negative rules and comparator construction not archived; not biological validation |
| 639 of 1,000 ranked error records map to both gene resources; 128 share at least one gene | `CTD_周进展_0809.pptx`, slide 1; build script | 63.9% mapping coverage, 20.0% overlap among mappable records, and 12.8% overlap among all 1,000 records | Input is an error export, not a verified list of new positive links; exact gene snapshots absent |
| Gene overlap: observed 12.8% versus mean 18.7% over 200 disease-label permutations | Visually inspected `CTD_weekly_0809/mechanism_support_0809.png`; build script | The reported overlap does not exceed the reported null mean | No saved null distribution, confidence interval or p-value; no statistical-significance claim is warranted |
| Three article links and relation contexts independently verified | `case_reference_links.json`; NCBI PubMed efetch | Demonstrations of clinical adverse-event, hypothesized indirect, and therapeutic evidence | Abstract-level checks, not a blinded validation set; all papers precede the project |

The calculation 30.4/7.2 = 4.222 is a descriptive ratio of the reported yields. It does not make an uncontrolled literature-search experiment a valid prospective model comparison. Similarly, 128/639 = 20.03% and 128/1,000 = 12.8% are distinct denominators, both of which must be identified explicitly.

## Findings requiring correction or exclusion

### 1. The error export is not a list of new positive associations

`CTD/graphsage.py` constructs `wrong_mask = y_pred != y_true` and exports all errors. It sets the exported score to `y_prob[np.arange(len(y_pred)), y_pred]`, i.e. confidence in the predicted class. It does not filter for `predicted positive and true negative`. The CSV has 62,042 rows and only chemical name, disease name and score; true and predicted labels are absent.

`build_weekly_progress_0809.py` consumes this CSV directly and sorts its score field. Therefore the phrase “GraphSAGE top-1,000 predictions” conceals the actual selection: these are the highest-confidence records in the archived error export. A confidently predicted negative or an incorrect positive relation subtype can occur in this selection. The score cannot be treated as calibrated probability that a previously unknown chemical–disease link exists. Names and scores alone cannot recover error direction or novelty.

Use “1,000 highest-scoring records in the archived GraphSAGE error export” wherever reproducing this artifact. A future prediction export must retain source/disease identifiers, true and predicted relation types, all class probabilities, source split, model hash and evidence provenance.

### 2. The gene comparison is a negative result

The text slide emphasizes 128/639 = 20.0%, whereas the embedded plot shows 12.8% overlap for all 1,000 records and 18.7% for the mean of 200 disease-label permutations. The build script confirms both denominators and the null construction: retain the 1,000 chemical records and shuffle their disease labels with `random.Random(20260809)`.

This comparison preserves empirical chemical and disease occurrence frequencies, but not every graph property and not necessarily per-replicate mapping coverage. It is not an experiment establishing causal specificity. Observed overlap is 5.9 percentage points below the displayed null mean; no enrichment claim is supported. The permutation distribution is not saved, so neither a significance claim nor a confidence interval should be supplied from the displayed mean alone.

The script joins by normalized display names (Unicode NFKC, case folding, punctuation removal), uses human chemical–gene rows (`taxon 9606`), and uses curated gene–disease associations. The join collapses relation types, direction, dose, tissue and disease causality into set overlap. Any shared gene counts; therefore even a successful match does not show that exposure acts through that gene to cause that disease. Source provenance may overlap with the CTD chemical–disease network, creating additional circularity concerns.

### 3. The source labels are swapped in one slide

20260202 slide 3 labels CTD as 3,125 records and the pollutant collection as 9,546,982 records. This contradicts that presentation's slide 2 and multiple slides in `疾病污染物.pptx`. The consistent interpretation is CTD = 9,546,982 and extracted collection = 3,125. Record the correction rather than reproducing the erroneous table.

### 4. Filter-threshold node counts are internally inconsistent

In `疾病污染物.pptx`, slide 4, the chemical count is 507 for score >25 but 1,718 for score >50. A stricter threshold on the same records cannot increase the number of distinct chemicals. Other rows exceed the maximum possible number of distinct chemical–disease pairs: score >100 reports 395,261 records but 78 diseases × 650 chemicals = 50,700 possible pairs; score >50 reports 1,007,473 records but 198 × 1,718 = 340,164 possible pairs; score >25 reports 2,101,258 records but 507 × 507 = 257,049 possible pairs.

This could reflect transcription errors, repeated records or mixed counting units. It cannot support a graph-size table of unique edges without the source data. Omit the threshold table pending recomputation. The full-source total and direct-evidence total can remain explicitly attributed to project materials.

### 5. Early binary metrics lack compatible definitions

`疾病污染物.pptx`, slides 2/10/12, reports binary CTD GCN accuracy 0.96, recall 0.88, F1 0.74 and MLP accuracy/recall/F1 all 0.94. If all three are ordinary positive-class binary metrics from the same test set, they imply very different class prevalence. The identity

`positive_prevalence = (1 - accuracy) / [2 × recall × (1/F1 - 1)]`

yields approximately 6.47% for GCN and 50% for MLP. This is not a valid common-split comparison under that definition. The numbers could use different averaging, splits or tasks; those choices are not documented. The safest manuscript choice is to exclude the comparison or explicitly state that metric definitions and comparability remain unresolved.

The separate multi-class table also lacks averaging and class definitions. The December 2025 three-model comparison is less internally problematic, but its largest reported AUC and F1 belong to MLP, not GCN or GAT.

### 6. Spearman sign and significance cannot be asserted

`疾病污染物.pptx`, slide 14, describes six windows decreasing from 30.4% to 14.4% and quotes Spearman rho = 1.00. If the first variable is increasing rank/window index, a strictly decreasing sequence gives rho = −1. If it is descending model confidence, positive rho can be consistent. Neither exact intermediate support rates nor confidence values and analysis code are supplied. Do not silently choose a sign or reproduce a correlation coefficient without identifying both variables. “Reported support declined across the first six ranked windows” is sufficient.

Slide 13 describes 38% in a 100-pair top window, whereas slide 14 reports 30.4% in a 1,000-pair top window. Different sample sizes can explain this; it is not inherently contradictory. Both are historical exploratory checks. Avoid the slide's “significantly higher” wording because no valid significance analysis is supplied. The last window rises to 17.8%, so the entire seven-window sequence is not monotonic.

### 7. Literature support must preserve relation semantics

The case table contains medicines (sulfamethoxazole, methadone, lithium, octreotide, ritonavir, phenytoin and others), a chemical class (fibrinolytic agents), and heterogeneous endpoints. These references cannot collectively be called evidence of environmental pollutant causation. Treatment, adverse effect, biomarker/mechanism, indirect hypothesis and incidental co-mention must be distinguished.

A chemical–disease pair absent from one frozen graph can already be established in the literature. The three checked articles were published in 1991, 1998 and 2003. Their recovery is a useful retrieval/rediscovery result but does not establish a newly discovered scientific relationship. No temporal split or exclusion of training/source references is archived.

## Verified reference cases suitable for a manuscript table

1. **Sulfamethoxazole—acute generalized exanthematous pustulosis.** Anliker MD, Wüthrich B. *Journal of Investigational Allergology and Clinical Immunology*. 2003;13(1):66–68. PMID [12861854](https://pubmed.ncbi.nlm.nih.gov/12861854/). The abstract describes one patient with a positive lymphocyte transformation test. This supports a clinical adverse-drug-reaction context, not population-level environmental risk or prospective prediction validity.

2. **Lithium—hyperosmolar nonketotic coma.** Azam H, Newton RW, Morris AD, Thompson CJ. *Postgraduate Medical Journal*. 1998;74(867):39–41. DOI [10.1136/pgmj.74.867.39](https://doi.org/10.1136/pgmj.74.867.39), PMID [9538487](https://pubmed.ncbi.nlm.nih.gov/9538487/). A case report proposes that lithium-associated nephrogenic diabetes insipidus contributed to dehydration when diabetes developed. Preserve “hypothesized indirect pathway”; do not convert this into general lithium causation.

3. **Octreotide—pancreatic pseudocyst.** Gullo L, Barbara L. *The Lancet*. 1991;338(8766):540–541. DOI [10.1016/0140-6736(91)91102-z](https://doi.org/10.1016/0140-6736(91)91102-z), PMID [1678802](https://pubmed.ncbi.nlm.nih.gov/1678802/). Seven patients were treated with octreotide for two weeks; the abstract explicitly suggests a therapeutic role. It must not count as support that octreotide causes pancreatic pseudocysts. This is an especially useful example of why the system needs relation types.

All ten original slide hyperlinks were recovered from `ppt/slides/_rels/slide3.xml.rels`. The three cases above were independently checked against NCBI PubMed efetch metadata and abstracts, cross-checked with Europe PMC metadata during this audit. Their exact metadata, original links, brief evidence summaries, verification endpoint and response SHA256 are in `case_reference_links.json`. The other seven links are recovery-only, not independently content-verified. No full-text evidence appraisal was performed.

## System claims and unavailable details

The supplied requirements describe keyword/CAS/chemical-name lookup, graph display, row attributes and literature display based on `DataSource` and `PubMedIDs`. They are requirements and prototypes, not proof that all features are deployed. The user's requested broader compound coverage, deeper Acemap article/web links, gene integration, and new-relation supporting links should be separated into documented current artifacts and proposed extensions. Existing Acemap portal URLs alone do not establish working record-level integration.

Do not invent author names from group-meeting attribution. Leave manuscript authors, affiliations, corresponding author and other user-identified unavailable administrative details blank. Missing scientific information should be visibly labeled as unavailable or requiring completion; it must not be filled with plausible protocols, seeds, data releases, performance values, publication counts or experiments.

## Storage accounting for this audit

Start: `/` used 82.1525 GiB of 98.2476 GiB (83.6178%), available 16.0795 GiB; storage guard disallowed local bulk writes. `/mnt/user-ssd` was verified as the JuiceFS mount `JuiceFS:bj9-cloudml:user-ssd`; destination is group-accessible to GID 12027. All retained audit outputs were written directly to `/mnt/user-ssd/zengboyi/ctd/journal_submission_20261006/evidence/`. No datasets, packages, local caches, training jobs or old DSA files were created, changed or deleted. Outputs are small permanent evidence files; no cleanup or restoration is needed.

End measurement at 2026-10-06 02:10:58 UTC: `/` used 82.1705 GiB (83.6361%), available 16.0615 GiB. The observed whole-system increase of approximately 0.0180 GiB is not attributed to this small shared-storage audit. The two retained files totaled 23,097 bytes before this final accounting note. No persistent growth source was started.
