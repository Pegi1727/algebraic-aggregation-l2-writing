# Research data release

This release packages the available raw, processed, and statistical-analysis data files supplied in the inventory. It contains one Excel workbook, individual CSV exports, and a source-to-output manifest. Source files were not modified.

## Contents and provenance
The `csv/` directory includes direct copies of supplied CSV tables; JSON-to-CSV conversions; and two-column `section,text` CSV representations of supplied TXT summaries. JSON object values that are nested arrays or objects are serialized as compact JSON strings to retain their complete content. The workbook has one worksheet per supplied data file.

All contents are derived only from the supplied data files listed in `manifest.csv`; no images or unrelated documents are included. No SPSS `.sav` or `.sps` file was present in the provided inventory. This release makes no claim that SPSS analyses were run.
