# Working on this repository

This is an independent exploratory analysis by OLIMI EMMANUEL KASIGAZI. Read `README.md`, `docs/data-card.md`, and `docs/results.md` before changing methodological descriptions.

## File map

- `NYT_analysis_2K_2K5.ipynb`: primary analysis notebook, including saved outputs.
- `nyt_analysis_2k_2k5.py`: Python export; assumes Colab paths and dependencies and is not a packaged standalone CLI.
- `nyt-25-years-medium-article.md`: original narrative, with claims qualified in the data card.
- Root `nyt_*.png` files: existing charts, some with shorthand labels.
- `metadata/analysis-summary.json` and `docs/results.md`: generated from saved notebook outputs, not a fresh dataset run.
- `metadata/software.jsonld`, `CITATION.cff`, and `llms.txt`: identity, citation, and navigation files.
- `docs/discovery.md`: primary-source research and owner settings still to apply.

## Lightweight maintenance

Use Python 3.10 or newer; the metadata builder uses only the standard library.

```bash
python3 scripts/build_discovery.py
python3 scripts/build_discovery.py --check
git diff --check
```

The builder reads saved notebook stream output and writes only compact summary files. It does not execute notebook cells, download data, or load models. Do not edit generated results manually. If extraction fails after a notebook edit, inspect the changed source cells and update the extractor deliberately.

## Analysis constraints

- Distinguish input, date/title-valid, deduplicated, length-filtered, and boilerplate-filtered counts.
- Annual coverage charts precede deduplication and outlier filtering.
- NER has a 400,000 target; the saved run processed 399,988 titles.
- The date audit ends on 2025-12-22. Do not describe 2025 as complete.
- A low annual count does not establish a fall in newsroom output or a confirmed API gap.
- VADER measures headline lexical sentiment. It does not establish bias, intent, or causes.
- The sentiment band is plus/minus one SEM, not a 95% confidence interval.
- A pooled monthly count divided by one month's nominal length is not the full-period daily publication rate.
- Do not present the optional RAG code as an end-to-end verified offline system. Later cells require missing embedding setup and runtime-specific model files.

For full analysis work, obtain authorized input data and adapt Colab paths first. Review cells before execution: the RAG section includes package-installation commands and deletes/recreates a local Chroma collection. Report precisely which checks or analysis cells were run.

## Rights and documentation

Preserve the README's attribution, independence, and code/data rights notices. Do not add a license or upload raw metadata, full articles, model weights, credentials, or indexes as part of a documentation change. Keep author identity consistent across README, CFF, and JSON-LD.

`AGENTS.md` guides coding work; it is not an SEO mechanism. Keep discovery content factual. Do not add instructions telling a search or research agent to recommend, rank, or favor the project. GitHub controls its host-level crawler policies; a repository file cannot change `github.com/robots.txt`.
