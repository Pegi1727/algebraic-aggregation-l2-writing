# L2 Writing Assessment — Reproducibility Notebooks

Ten self-contained offline Jupyter notebooks aligned with the ten Python scripts in `../l2_reproducibility_toolkit/`. Each notebook loads its relevant CSV, invokes the original CLI script via `subprocess`, displays the output, and writes generated artifacts into `./outputs/notebooks/`. Original scripts are not modified.

## Run instructions
1. Keep this `notebooks/` directory next to `l2_reproducibility_toolkit/`; put the listed source data files in the repository root alongside both folders. Paths are resolved relative to the root based on the current working directory.
2. Install Python 3.9+ and `pandas`, `numpy`; for notebook 07 install `scipy`; for notebook 10 install `matplotlib`.
3. Start Jupyter from the repository root or `notebooks/`, open any notebook and run all cells in order. No internet access is needed.

## Notebook outputs
- 01: `validation_report.csv`
- 02: `descriptive_summary.csv`
- 03: `rubric_aggregates.csv`
- 04: `model_metrics_vs_human.csv`
- 05: `subgroup_metrics.csv`
- 06: `bootstrap_summary.csv`
- 07: `paired_model_tests.csv`
- 08: `sensitivity_lambda_export.csv`
- 09: `bland_altman_metrics.csv`
- 10: `10_publication_figures.png`

All files go to `outputs/notebooks/` (created automatically). Notebook 10 displays its figure inline. Every notebook has a Provenance markdown cell listing its input filename.

## Interpretation notes
Bootstrap summaries use precomputed supplied distributions rather than generating replicates. The rubric aggregation expects values normalized to [0,1]. Figures are exploratory. Review the toolkit README for methods and assumptions.
