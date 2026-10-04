# L2 Writing Assessment Reproducibility Toolkit

This archive contains exactly 10 Python (`.py`) and 10 R (`.R`) analysis entry points, plus one shared helper per language. Helpers are not analysis entry points. CSV inputs are read only; results are written to the requested output path.

## Data and column names

Designed to work with CSVs such as `lukasiewicz_analysis_results.csv`, `raw_deidentified_l2_writing_corpus.csv`, `subgroup_profile_metrics.csv`, `bootstrap_distributions_2000.csv`, `sensitivity_analysis_weights.csv`, `residual_and_error_diagnostics.csv`, and `final_model_comparison_APA.csv`. Schemas vary. Scripts attempt limited transparent detection; specify actual names when detection is ambiguous. `--input` and `--output` are required. Multi-file-style operations accept an output directory; otherwise output is the given file path.

## Python

Requires Python 3.9+, pandas, numpy. `07_paired_model_tests.py` additionally requires scipy; `10_publication_figures.py` requires matplotlib. Run from this directory, for example:

```bash
python 01_validate_files.py --input /path/lukasiewicz_analysis_results.csv --output /path/results/validation.csv
python 04_model_metrics_vs_human.py --input /path/lukasiewicz_analysis_results.csv --output /path/results/model_metrics.csv --human-col Human_Global --models Additive,Min,Luk_4D
python 03_aggregate_rubric_dimensions.py --input /path/raw_deidentified_l2_writing_corpus.csv --output /path/results/aggregates.csv --columns Linguistic_Accuracy_L,Intelligibility_I,Communicative_Adequacy_C,Academic_Appropriateness_A --lambda 0.5
```

## R

Requires R 4.0+; analysis uses base R only. Run from this directory:

```bash
Rscript 01_validate_files.R --input /path/lukasiewicz_analysis_results.csv --output /path/results/validation.csv
Rscript 05_subgroup_metrics.R --input /path/lukasiewicz_analysis_results.csv --output /path/results/subgroups.csv --human-col Human_Global --group-col Profile --models Additive,Min,Luk_4D
```

## Methods and interpretation

`03_aggregate_rubric_dimensions` requires at least two finite normalized rubric values in [0,1]. Arithmetic mean and minimum are reported, along with the n-ary Łukasiewicz t-norm `max(0, sum(x_i) - (k - 1))`. Configurable Composite Min-Add is `lambda * minimum + (1 - lambda) * mean`, with `lambda` constrained to [0,1]. The range claim follows only when every dimension is in [0,1]. Do not apply this formula to unnormalized rubric scores without a defensible normalization step.

Metric comparisons use complete paired rows; bias is prediction minus human score. Bland-Altman limits are mean difference +/- 1.96 sample SD, a descriptive approximation requiring suitable distributional assumptions. Paired tests use Wilcoxon signed-rank on provided paired columns and Holm correction across tested pairs; the input columns must genuinely be paired measurements. Bootstrap summary reports empirical quantiles of supplied numeric distributions; it does not create new bootstrap replicates. Sensitivity operation exports numeric data, preserving supplied values rather than inferring an unverified objective. Figure output is exploratory, not a claim of publication-ready inference.

Scripts do not fabricate findings or infer unverified column definitions. Review missingness, score scale, pairing, independence, subgroup sizes, and model-comparison design before interpreting outputs. R execution is not claimed as tested; Python files are syntax-checked. Adjust column options to match the source CSV headers.
