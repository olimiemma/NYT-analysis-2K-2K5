# New York Times Headline Analysis (2000–2025): Python, NLP, and Data Quality

An independent data engineering and natural language processing case study by **OLIMI EMMANUEL KASIGAZI**. The saved notebook loads **2,217,051 article-metadata records**, producing **2,071,261 records** after cleaning and boilerplate filtering. It uses Python, pandas, TF-IDF, VADER sentiment analysis, spaCy named-entity recognition, and Matplotlib to explore headline language and source coverage.

The input fields are publication dates, titles, short descriptions, and article URLs. This is headline and content-metadata analysis, not subscriber behavior, reader engagement, advertising performance, or full-article analysis. The recorded date range is **January 1, 2000 through December 22, 2025**; the snapshot does not cover all of 2025.

An optional RAG prototype references BGE-M3, ChromaDB, and a Gemma GGUF model. Its saved setup uses Google Colab and Google Drive and has missing embedding prerequisites, so a complete offline run is not established by this repository.

> **Independent project:** This repository is not affiliated with, sponsored by, or endorsed by The New York Times Company. Findings are the author's interpretations of the available dataset and are not statements by The New York Times.

## Start here

| Goal | Entry point |
|---|---|
| Inspect exact counts and notebook evidence | [Results and provenance](docs/results.md) |
| Understand fields, methods, and run requirements | [Data card](docs/data-card.md) |
| Retrieve counts as JSON | [Analysis summary](metadata/analysis-summary.json) |
| Identify the software and author programmatically | [Software metadata](metadata/software.jsonld) |
| Find a small index of useful files | [llms.txt](llms.txt) |
| Cite the project | [CITATION.cff](CITATION.cff) |
| Work on the repository with a coding agent | [AGENTS.md](AGENTS.md) |

Published article:
https://medium.com/@olimiemma/i-analyzed-2-2-0718f706c3bb

The notebook and original article preserve an exploratory workflow. Use the data card and evidence-linked results for current interpretations, including corrections to input counts, sampling, and monthly-rate claims. `llms.txt` is an optional navigation aid, not a guarantee of indexing or AI citations.

<p align="center">
  <img src="nyt_sentiment_trend_v2.png" alt="Average VADER sentiment of New York Times article titles by year from 2000 through 2025, with a standard-error band" width="100%">
</p>

## Project at a glance

| Item | Scope |
|---|---:|
| Recorded date range after initial parsing | 2000-01-01 to 2025-12-22 |
| Rows loaded from the source CSV | 2,217,051 |
| Rows after date/title validity filtering | 2,216,466 |
| Clean records after deduplication and outlier filtering | 2,184,483 |
| Records after the additional boilerplate-title filter | 2,071,261 |
| Named-entity sample in saved output | 399,988 titles; 400,000 target, allocated proportionally by year |
| Optional semantic-search sample | 50,000 target; no saved completed sample output |
| Primary environment | Python / Jupyter / Google Colab |

The source CSV is intentionally **not included** in this repository. Anyone reproducing the analysis must obtain article metadata through a source they are authorized to use and comply with all applicable terms.

## Questions explored

- How complete and consistent is the dataset across years?
- Which words dominate the raw headline corpus, and which are publication boilerplate?
- Which terms distinguish the pre-9/11, War on Terror, Obama, Trump/COVID, and post-COVID periods?
- How does headline-level lexical sentiment vary over time?
- Which people, places, and organizations appear most often in a stratified sample?
- Are apparent monthly publishing patterns real, or artifacts of unequal month length and source coverage?
- Can local embeddings and a local language model support semantic retrieval over a sample of the corpus?

## Selected results

### Raw headline vocabulary

Structural terms such as “paid,” “notice,” “briefing,” and “corrections” dominate the unfiltered counts. The chart separates likely publication boilerplate from content words and named entities so the result is not mistaken for a simple topic ranking.

<p align="center">
  <img src="nyt_top_keywords_lollipop.png" alt="Lollipop chart of the 25 most frequent words in article titles, categorized as content words, named entities, or NYT structural boilerplate" width="100%">
</p>

### Era-distinctive terms

The TF-IDF analysis treats each year as a document, aggregates those scores into five researcher-defined eras, and displays each term relative to its own peak. Darker cells indicate that a term was more distinctive in that era; they do **not** mean that different terms have equal absolute frequency.

<p align="center">
  <img src="nyt_tfidf_era_heatmap.png" alt="Heatmap of relative TF-IDF prominence for headline terms across five eras from 2000 through 2025" width="100%">
</p>

### Named entities

spaCy named-entity recognition processed 399,988 titles, with a 400,000-title target allocated proportionally by year. Integer rounding in each year's allocation explains the difference. The result is useful for exploration but should not be treated as a definitive census: single-pass NER cannot reliably disambiguate every person, organization, or place.

<p align="center">
  <img src="nyt_ner_entities.png" alt="Bar charts of the most frequently extracted people, places, and organizations in a stratified sample of article titles" width="100%">
</p>

### Publication coverage

The source contains substantially more records in some years than others. A collection or API-coverage gap is a hypothesis for the 2021–2022 decline, especially the 2022 low; this repository has no acquisition logs that confirm its cause. The saved annual chart is calculated before URL deduplication and length filtering and is not an official newsroom publication ledger.

<p align="center">
  <img src="nyt_articles_per_year.png" alt="Collected article-metadata records by year before URL deduplication, showing a 2006 peak and lower observed counts around 2022; collection completeness is unverified" width="100%">
</p>

## Repository contents

| Path | Purpose |
|---|---|
| `NYT_analysis_2K_2K5.ipynb` | Main notebook and narrative workflow |
| `nyt_analysis_2k_2k5.py` | Colab-exported Python script |
| `nyt-25-years-medium-article.md` | Long-form project write-up |
| `nyt_articles_per_year.png` | Annual source-coverage audit |
| `nyt_monthly_seasonality.png` | Raw monthly totals |
| `nyt_top_keywords_lollipop.png` | Raw vocabulary with manual categories |
| `nyt_tfidf_era_heatmap.png` | Era-level TF-IDF comparison |
| `nyt_sentiment_trend.png` | Original sentiment chart |
| `nyt_sentiment_trend_v2.png` | Sentiment chart with uncertainty band |
| `nyt_keyword_bump_chart.png` | Yearly keyword rates per 10,000 articles |
| `nyt_ner_entities.png` | Named-entity summary |

Full notebook:

https://github.com/olimiemma/NYT-analysis-2K-2K5/blob/main/NYT_analysis_2K_2K5.ipynb

Long-form write-up:

https://github.com/olimiemma/NYT-analysis-2K-2K5/blob/main/nyt-25-years-medium-article.md

## Data pipeline

1. Load the source CSV and inspect its schema.
2. Parse `date` as UTC, coercing invalid timestamps to missing values.
3. Remove records without a valid date or title.
4. Fill missing short descriptions with empty strings.
5. Drop duplicate URLs.
6. Remove extreme title and description lengths (`title > 300` characters; `short_desc > 1,000` characters).
7. Derive year, month, day-of-week, title length, and description length.
8. Create a second analytical corpus by filtering recurring structural and boilerplate titles.
9. Run frequency, TF-IDF, VADER sentiment, keyword-rate, and sampled NER analyses.
10. Optionally build a local embedding index and retrieval-augmented-generation prototype over a smaller sample.

The workflow deliberately retains two corpus sizes:

- **2,184,483 clean records** for raw-frequency analysis. The earlier saved annual and monthly charts use the **2,216,466-row** intermediate corpus before URL deduplication and length filtering.
- **2,071,261 filtered records** for analyses that would otherwise be dominated by recurring title templates.

## Expected data schema

The notebook expects a CSV containing at least these fields:

| Column | Meaning |
|---|---|
| `date` | Publication timestamp |
| `title` | Article title or headline |
| `short_desc` | Short description or abstract |
| `url` | Article URL and deduplication key |

Do not commit the raw CSV, credentials, API responses, full article text, or any other content unless you have confirmed that redistribution is permitted.

## Reproducing the core analysis

### 1. Clone the repository

```bash
git clone https://github.com/olimiemma/NYT-analysis-2K-2K5.git
cd NYT-analysis-2K-2K5
```

### 2. Create an environment

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install pandas numpy matplotlib nltk scikit-learn spacy jupyterlab
python -m spacy download en_core_web_sm
```

On Windows PowerShell, activate the environment with:

```powershell
.venv\Scripts\Activate.ps1
```

### 3. Provide your own lawful data source

The current notebook was developed in Google Colab and expects:

```text
/content/NewYorkTime_2000_2026.csv
```

Upload your authorized CSV to that location in Colab, or replace the hard-coded path before running locally. Keep API keys in environment variables or a secrets manager; never place them in the notebook or commit them to Git.

### 4. Run the notebook in order

```bash
jupyter lab
```

Open `NYT_analysis_2K_2K5.ipynb` and review the cells in order through the core analysis, stopping before the `RAG` section. The original notebook includes iterative analysis cells, Colab-specific paths, and unpinned dependencies; a fresh clean-kernel reproduction has not been verified. NLTK resources and the spaCy model may require network downloads. See the data card for specific prerequisites and known limitations.

### Optional semantic search / RAG

The semantic-search section references BGE-M3 embeddings, ChromaDB, `llama.cpp`, and a Gemma-family GGUF model. It is an experimental extension. The committed sampling cell does not create `embeddings` or `embed_text`, which later cells require, and no completed RAG outputs are saved. Model paths, GPU installation commands, and the Drive mount also require adaptation. The exported `.py` file parses as Python but assumes the original runtime and unprovided files; it is not a packaged standalone command-line application.

Do not use this dataset or the optional RAG workflow to train, fine-tune, or distribute a model unless your data rights expressly allow that use.

## Tools and techniques

- **Data engineering:** pandas, NumPy, schema inspection, UTC parsing, deduplication, derived date fields, and rule-based quality checks
- **Visualization:** Matplotlib
- **Text analysis:** NLTK stopwords, VADER sentiment, scikit-learn TF-IDF
- **Named entities:** spaCy `en_core_web_sm`
- **Optional retrieval:** dense embeddings, ChromaDB, `llama-cpp-python`, and a local GGUF model
- **Environment:** Jupyter Notebook / Google Colab

## Interpretation limits

These results are descriptive and exploratory.

- **Source coverage is not newsroom output.** Missing or uneven API/data-collection coverage can change counts and trends. The annual chart is a coverage audit, not an official publication ledger.
- **Headline-only analysis is narrow.** Titles and short descriptions do not represent complete articles, editorial intent, reader response, or the full range of journalism published.
- **Sentiment is lexical, not editorial.** VADER reacts to words associated with negative or positive affect. A headline about an improving murder rate can still score negatively because it contains “murder.” The result must not be interpreted as proof of political bias or institutional mood.
- **The uncertainty band is limited.** The standard-error band describes uncertainty around the yearly sample mean; it does not capture model error, source-selection bias, temporal dependence, or headline-template effects.
- **The TF-IDF heatmap is row-normalized.** A value of `1.00` marks a term's peak era, not a universal score comparable across all rows.
- **NER is approximate.** “Clinton” may combine Bill and Hillary Clinton; “Trump” may refer to a person or brand; the small spaCy model does not perform full entity resolution or co-reference resolution.
- **Monthly totals need correct exposure denominators.** `nyt_monthly_seasonality.png` shows raw totals. A later cell divides totals pooled across years by one month's nominal length. Its roughly 6,000 values are not a valid daily publishing rate across the full period. A real rate needs total covered calendar days per month across the included years, accounting for leap years, partial years, and unresolved collection gaps.
- **Counts and rates answer different questions.** The keyword trend uses mentions per 10,000 articles by year to reduce distortion from uneven yearly coverage.
- **Era boundaries are analytical choices.** They are useful for comparison but are not objective divisions of history.
- **2025 is incomplete.** The saved initial date audit ends on December 22, 2025. The interval touches 26 calendar years, despite the original article's shorthand title, “25 Years.”

## Ethical use

- This project analyzes public-facing article metadata, not reader or subscriber data.
- Do not use the outputs to profile individual journalists, readers, or private persons.
- Avoid causal claims about political events, editorial decisions, or institutional bias from descriptive headline statistics alone.
- Preserve links and attribution when presenting examples so readers can inspect the original context where permitted.
- Document filters, exclusions, sampling choices, model versions, and known coverage gaps when extending the analysis.
- Review sensitive named-entity outputs manually before publication.

## Legal, rights, and attribution

This section is a project notice, not legal advice. A README cannot grant rights that the repository owner does not possess or override a data provider's terms.

### New York Times content and API terms

Headlines, short descriptions, article text, URLs, trademarks, and other New York Times materials remain subject to the rights of The New York Times Company and/or the relevant authors and licensors. They are **not** covered by any license that may later be applied to this project's original code.

If you obtain data from The New York Times Developer Network or another NYT service, review and comply with the terms that apply to your account, endpoint, storage, display, attribution, redistribution, and intended use:

https://developer.nytimes.com/

https://developer.nytimes.com/terms

https://help.nytimes.com/hc/en-us/articles/115014893428-Terms-of-service

The repository does not include an NYT API key, the raw CSV, full article text, or a license to republish NYT content. Obtain your own credentials and permission where required. Do not remove copyright notices, bypass access controls, evade rate limits, or use the project as a substitute for an NYT product or subscription.

“The New York Times,” “The Times,” “NYTimes.com,” and related names and logos are trademarks or service marks associated with The New York Times Company. Their use here is solely descriptive and nominative. No NYT logo is included, and no endorsement is claimed.

### Original project materials

Unless a separate `LICENSE` file is added, no open-source license is granted for the original code, prose, or visualizations in this repository. Under the default copyright position, reuse beyond rights supplied by law requires permission from the copyright holder.

Copyright © 2026 OLIMI EMMANUEL KASIGAZI. All rights reserved for original project materials, excluding third-party content and software.

Any future code license should clearly apply only to original code and expressly exclude:

- New York Times content and metadata;
- the source dataset and API responses;
- third-party model weights and tokenizers;
- third-party libraries and assets; and
- names, logos, and trademarks.

Third-party Python packages and models retain their own licenses and terms. Review them before redistribution or commercial use.

### Citation

When referencing this analysis, use `CITATION.cff`, cite the repository, and include the commit and date you accessed. Citation metadata identifies the original project; it grants no rights to the source data.

```text
OLIMI EMMANUEL KASIGAZI. “New York Times Headline Analysis (2000–2025).”
GitHub repository, 2026.
https://github.com/olimiemma/NYT-analysis-2K-2K5
```

## Corrections and reproducibility reports

If you find a data-quality issue, methodological error, or result you cannot reproduce, open a GitHub issue with:

- the affected notebook cell or script section;
- the package and model versions used;
- the relevant date range and row counts;
- a minimal reproducible example that does not expose credentials or restricted data; and
- the expected and observed results.

Issues:

https://github.com/olimiemma/NYT-analysis-2K-2K5/issues

## Author

OLIMI EMMANUEL KASIGAZI

https://github.com/olimiemma

https://olimiemma.com/


## Maintaining discovery information

Regenerate the compact results from saved notebook output without running the analysis:

```bash
python3 scripts/build_discovery.py
python3 scripts/build_discovery.py --check
```

The check verifies count arithmetic, source hashes, generated-file freshness, metadata agreement, and local documentation links. It does not validate the underlying dataset or prove that a crawler indexed the repository.

Research, hosting boundaries, suggested GitHub topics, and next steps:
[Discovery strategy](docs/discovery.md)
