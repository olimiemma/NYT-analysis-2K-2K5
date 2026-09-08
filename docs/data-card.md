# Data card: New York Times headline analysis

This project analyzes a supplied CSV of article metadata. It does not distribute the CSV, full article bodies, subscriber data, or reader activity. The archived notebook outputs are evidence of a prior run, not independent verification of the source's completeness or a fresh reproduction.

Exact row counts, dates, annual counts, cell identifiers, and notebook hash:
[Results and provenance](results.md) and [JSON summary](../metadata/analysis-summary.json).

## Source and coverage

The original write-up attributes the input to the NYT API, but the repository contains no collector, request logs, acquisition date, source-file checksum, or documented redistribution permission. The local filename `/content/NewYorkTime_2000_2026.csv` does not establish 2026 coverage. The saved initial date audit spans 2000-01-01 through 2025-12-22.

That interval touches 26 calendar years; the companion article uses “25 Years” as a shorthand title. Low counts around 2021–2022 may reflect acquisition gaps. Their cause is unconfirmed, and no completeness guarantee is made for any year.

## Input fields

| Field | Meaning | Recorded handling and limitations |
|---|---|---|
| `date` | Publication timestamp as supplied | Parsed as UTC with pandas; invalid values become missing and are dropped. No explicit 2000–2025 boundary filter is applied. |
| `title` | Headline or article title | Missing titles are dropped; strings longer than 300 characters are later excluded. These are heuristic filters, not proof of corruption. |
| `short_desc` | Short description or abstract | Missing values become empty strings; strings longer than 1,000 characters are later excluded. This may remove legitimate records as well as anomalies. |
| `url` | Source article link used as a deduplication key | Duplicate values keep the first row. The input audit reports 12 missing URLs; pandas may collapse missing values together. No canonical-URL or missing-URL remediation is implemented. |

Derived fields include UTC year, month, day of week, text length, combined title/description text, and headline VADER compound sentiment.

## Which corpus feeds each method?

| Method or artifact | Input stage | What the output represents |
|---|---|---|
| Annual and monthly coverage charts | After initial date/title validity checks, before URL deduplication | Counts in the collected source snapshot, not an official publication ledger |
| Raw vocabulary chart | After URL deduplication and length caps | Token counts in titles; structural words remain |
| Cleaned TF-IDF and heatmap | After boilerplate-title filtering | One document per observed year, unigrams/bigrams, era-averaged scores, then per-term scaling for the heatmap |
| VADER trend | Boilerplate-filtered titles | Mean lexical compound score per year; the v2 chart uses plus/minus one standard error of the mean |
| Keyword trend | Boilerplate-filtered titles | Matching-title rate per 10,000 records in that year, subject to source coverage and matching rules |
| spaCy NER | Proportionally allocated year sample from the filtered corpus | Approximate entity extraction, followed by manual exclusions and name merging |
| RAG prototype | Targeted year-stratified subset of the filtered corpus | Experimental retrieval/generation code without a saved completed run |

The NER target is 400,000, while the saved sample is 399,988 because each year's proportional allocation is rounded down. The RAG target is 50,000; a completed sample size is not recorded. Distinguish configured targets from observed outputs when describing scale.

## Interpretation corrections

1. **Input size:** 2,217,051 rows are loaded. The 2,216,466 count is after initial validity filtering. The results file preserves every recorded stage.
2. **Daily rate:** the normalization cell pools all years by month, then divides by one nominal month length. The resulting roughly 6,000 values are not a daily publishing rate over the full interval. A defensible rate requires total calendar exposure across years, leap days and the partial final year, plus an explicit treatment of unknown collection gaps. Missing source records do not identify unobserved days reliably.
3. **Source decline:** the original narrative and summary include stronger claims about API gaps and newsroom production than the available acquisition evidence supports.
4. **Sentiment and events:** event annotations and adjacent fluctuations do not establish causation, editorial intent, or political bias. A one-SEM band is not a 95% confidence interval and excludes model and collection errors.
5. **TF-IDF and entities:** era labels, selected words, row normalization, approximate NER, and manual name merging limit interpretation. The boilerplate rule does not remove all structural terms. Values should not be read as a universal topic census.

The original code, notebook outputs, article, and PNGs remain historical artifacts. This documentation makes the limitations explicit without implying that the charts have been regenerated or the underlying analysis repaired.

## Reproduction status

Reading the README, notebook output, JSON, and charts requires no input data. The metadata builder uses Python's standard library and never executes the notebook:

```bash
python3 scripts/build_discovery.py --check
```

A complete analysis rerun requires an authorized CSV, pandas, NumPy, Matplotlib, scikit-learn, NLTK resources, spaCy with `en_core_web_sm`, and JupyterLab or Colab. Package versions are not locked. The notebook retains iterative analysis cells and runtime assumptions. Review it interactively and adapt the input path; this change does not claim a successful clean-kernel execution.

The `.py` export parses as Python but includes runtime-specific setup and package-installation commands. The RAG section references Google Drive model files and A100/CUDA installation choices. Its sampling cell does not define the `embeddings`, `embed_text`, and embedding-model setup required downstream. Local model inference is a design choice, not proof that a Colab/Drive workflow keeps all data on the user's own device.

## Rights and citation

No data license or training permission is supplied by these discovery files. Refer to the existing project notices before reuse:
https://github.com/olimiemma/NYT-analysis-2K-2K5/blob/main/README.md#legal-rights-and-attribution

Use [CITATION.cff](../CITATION.cff) for the original project and record the exact commit you inspected. The author is OLIMI EMMANUEL KASIGAZI. The project is independent of The New York Times Company.
