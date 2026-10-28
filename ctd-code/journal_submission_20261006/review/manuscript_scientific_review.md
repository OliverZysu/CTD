# Scientific review of manuscript.tex

Reviewed: 2026-10-06, approximately 02:13–02:15 UTC. Source: `source/manuscript.tex`, SHA256 `31a24d7dba52b639619ded908f980b1b2b596cb2dddfe25157fe1e34da5c4d1b`. Line numbers below refer to that version. Review inputs: `claims_audit.md`, `code_results_summary.json`, the relevant loader/GraphSAGE source, and visual inspection of the original literature plots and interface mockup. The manuscript was not edited. Bibliography, forthcoming figures and supplementary cross-references are outside this bounded review.

## Overall assessment

The manuscript now separates reported metrics, directly counted CSV properties, literature recovery, gene overlap and proposed system features. The main numerical statements agree with the archived evidence. It explicitly preserves the negative gene-comparison result and does not claim a newly validated causal association or a GNN performance advantage. No additional major numerical contradiction was found.

The corrections below address the remaining small but material shifts from evidence to assertion. The document remains an exploratory working manuscript; accurate qualification does not substitute for the missing snapshots, labeled predictions and independent validation required for a stronger original-research submission.

## Corrections recommended before freezing the draft

### 1. Remove the unverified architecture adjective from the historical MLP result

**Priority: P1; location: abstract, line 19.**

Current: “In the reported exposure-data pilot, an embedding-based multilayer perceptron achieved … 0.9392”.

The December 2025 source table identifies MLP but does not establish that the reported pilot used the exact embedding-based `mlp.py` retained today. The manuscript correctly disclaims equivalence of historical runs and retained implementations elsewhere; this adjective reintroduces that equivalence in the abstract.

Suggested replacement: “In the reported exposure-data pilot, the multilayer perceptron had a reported AUROC of 0.9392 …”. In Discussion line 224, learned entity identities can remain a possible explanation if explicitly introduced as a hypothesis contingent on the pilot architecture, or can simply be removed from the speculative list.

### 2. State the provenance boundary before the model and split description

**Priority: P1; locations: Methods lines 64–85.**

The statements about negative sampling, 80/10/10 splitting, seed 42, directed edges, duplicate handling, architecture and hyperparameters accurately describe the retained source. The caveat at line 83 mentions “these values” and “historical pilot runs”, which can be read narrowly as a caveat about hyperparameter numbers alone. Readers could still attribute the complete reconstructed pipeline to all reported metrics.

Add an opening sentence before the graph/task description, for example:

> “The following task, splitting and model descriptions are obtained from static inspection of the retained implementation; no run manifest establishes that this exact code produced each historical metric or prediction export.”

Then use “The retained GraphSAGE implementation uses …” in place of “The chemical–disease predictor uses …” at line 72. This preserves useful technical details without reconstructing an undocumented experiment.

### 3. Preserve uncertainty in the lithium pathway

**Priority: P2; locations: Results lines 201 and 212.**

Current table: “Indirect pathway through nephrogenic diabetes insipidus”. The abstract of PMID 9538487 says the diabetes insipidus was likely lithium-induced and that the authors hypothesize its role in precipitating hyperosmolar dehydration. A single case does not establish the proposed mediation.

Suggested table wording: “Hypothesized indirect pathway through nephrogenic diabetes insipidus”. Suggested prose: “The lithium case report proposes an indirect pathway involving suspected lithium-associated nephrogenic diabetes insipidus.” The sulfamethoxazole and octreotide interpretations are appropriately qualified.

### 4. Avoid claiming improved access as an evaluated outcome

**Priority: P2; location: Discussion line 222.**

Current: “the most defensible current outcome is improved access to potentially relevant evidence”. No usability, retrieval-access comparison or end-to-end deployment study is supplied; the paper itself states this in Methods and Limitations.

Suggested replacement: “the most defensible current outcome is an organized set of potentially relevant literature leads and an explicit account of their evidence limits”. This avoids turning the interface intention into an observed improvement.

## Further provenance clarifications worth adding

### 5. Distinguish collection count from pilot node counts

**Priority: P2; location: Table 1, lines 54–55.**

The 3,125 record count and the pilot's 639 chemical/94 disease node counts come from different project summaries. Both are supportable as reported values, but a common frozen input snapshot is unavailable. Presenting them on one row can suggest that the exact 3,125-record corpus is known to produce those node counts.

Add a caption or footnote: “Environmental entity counts are reported for the pilot graph; a common frozen snapshot linking these counts to the collection inventory is unavailable.” This is preferable to deleting useful reported numbers.

### 6. Keep the literature and gene samples visibly separate

**Priority: P3; locations: abstract line 19; Results lines 177–189; evidence comparison figure.**

The gene script explicitly consumes the retained error export. The historical literature sample has no versioned pair list. Their membership therefore cannot be assumed identical just because both use a top-1,000 label. Methods line 103 already gives the appropriate caveat.

Use “In a separate reported shared-gene screen …” in the abstract. Ensure the comparison figure labels do not imply that its literature-supported records and gene-supported records are the same 1,000 pairs. The existing Figure 3 caption substantially addresses this.

## Checks passed

- All exposure pilot metrics match the December 2025 table. MLP is numerically highest on all four reported metrics, and the text avoids significance claims.
- The larger export has 62,042 records, 16,171 chemical names, 6,193 disease names, 61,973 name pairs and 69 exact duplicate rows, matching `code_results_summary.json`.
- First-1,000 counts, score extremes and median match the direct artifact summary. The separate top-ten mismatch is accurately described.
- The error export uses confidence in the predicted class, and the manuscript does not interpret it as a positive-association ranking.
- Visually checked original plot: seven 1,000-record literature rates are 30.4%, 19.3%, 15.8%, 15.5%, 14.5%, 14.4%, 17.8%. Its ten 100-record leading bins are 38%, 34%, 37%, 30%, 28%, 33%, 21%, 31%, 29%, 23%; their aggregate is 304/1,000. The text reports the correct range and does not reproduce the ambiguous Spearman claim.
- The original random-comparison chart explicitly reports 304/1,000 versus 72/1,000, supporting the descriptive 23.2 percentage-point difference and 4.22 ratio.
- Gene-screen denominators 128/639 and 128/1,000 are kept distinct, and the 12.8% versus 18.7% comparison is correctly interpreted as no demonstrated enrichment.
- Human taxonomy filtering, name matching, 200 permutations and seed 20260809 match the build script. The manuscript correctly avoids an unsupported permutation p-value.
- The interface mockup visually distinguishes original and predicted edges. Calling this a design artifact rather than a tested deployment is accurate.
- Broader chemical scope, Acemap record resolution and integrated gene prediction are treated as proposed extensions.
- Authors, affiliations and administrative declarations are left blank as requested.

## Storage

This follow-up generated only this small report on the verified `/mnt/user-ssd` shared mount. Start status: root used 82.1737 GiB (83.6394%), available 16.0583 GiB. No local cache, downloaded paper, training artifact or dataset was generated. Existing research artifacts were read without modification.

End status at 02:15:06 UTC: root used 82.1793 GiB (83.6452%), available 16.0526 GiB. The whole-system change is not attributed to this shared-storage report. No cleanup or recovery is necessary; the permanent report remains in `journal_submission_20261006/review/`.
