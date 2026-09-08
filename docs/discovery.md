# Discovery strategy and research

Reviewed September 8, 2026. This document records how the repository was made easier to find, inspect, and cite, and separates implemented files from settings and website work that remain outside this change.

## What the research supports

Clear content, working links, identifiable authorship, and traceable evidence help readers and software understand a project. Search eligibility, an agent's ability to read a file, and an agent choosing to cite it are different outcomes. None is guaranteed by a special filename.

| Guidance | Implication for this repository | Primary source |
|---|---|---|
| Google applies its existing search fundamentals to AI search and explicitly says it ignores `llms.txt` for rankings | Prioritize an accurate README, useful text, links, and original evidence; do not claim a Google ranking boost from an AI index | https://developers.google.com/search/docs/fundamentals/ai-optimization-guide |
| The `llms.txt` proposal describes a small Markdown index linking to useful content | Provide an optional raw-text entry point; it is not a universal crawler requirement | https://llmstxt.org/ |
| GitHub surfaces README content as the repository introduction | State the subject, author, methods, scope, and entry points near the top | https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-readmes |
| GitHub topics let users find related projects; repository search can search README text using `in:readme` | Use precise subject terms in normal prose and configure accurate topics in About | https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/classifying-your-repository-with-topics and https://docs.github.com/en/search-github/searching-on-github/searching-for-repositories |
| GitHub recognizes `CITATION.cff` on the default branch | Supply real author and software citation information without inventing a release, DOI, or license | https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-citation-files |
| Schema.org defines `SoftwareSourceCode` and `codeRepository` | Publish structured identity for this software project; do not advertise an unavailable source CSV as a downloadable dataset | https://schema.org/SoftwareSourceCode |
| GitHub sanitizes rendered Markdown, including script tags | A JSON-LD file is directly readable metadata; it is not JSON-LD automatically injected into GitHub's rendered page | https://github.com/github/markup |
| OpenAI distinguishes search crawling from model-training crawling | Search visibility and permission for training are separate decisions; this change grants no training rights | https://developers.openai.com/api/docs/bots |
| Robots rules must live at the service's top-level `/robots.txt` | A file in this repository cannot control `github.com` crawling | https://www.rfc-editor.org/rfc/rfc9309.html#section-2.3 |
| `AGENTS.md` supplies project instructions to coding agents | Use it for source navigation, maintenance commands, and methodological constraints, not search ranking | https://agents.md/ |

The attached ideas were useful prompts, but “most web crawlers are LLM agents,” guaranteed citation uplift, and a universal 40–60-word answer format are not established by this research. No traffic-share assumption is needed for these changes.

## Implemented in this change

| File or change | Practical purpose |
|---|---|
| Revised `README.md` | Descriptive project title, concise summary, author identity, linked entry points, corrected counts, and specific run limitations |
| `llms.txt` | Small file index with direct raw links; avoids forcing an agent to fetch the full notebook first |
| `CITATION.cff` | GitHub-native citation metadata for the original project |
| `metadata/software.jsonld` | Schema.org software and author identity, with explicit access and rights boundaries |
| `metadata/analysis-summary.json` | Exact archived counts, corpus stages, sampling target versus result, and source provenance |
| `docs/results.md` | Human-readable version of the same evidence, generated from saved output |
| `docs/data-card.md` | Field dictionary, corpus-to-method mapping, source gaps, denominator corrections, and reproduction status |
| `AGENTS.md` | Instructions for coding agents working on this repository |
| `scripts/build_discovery.py` | Deterministic summary generation and consistency checks without raw data or notebook execution |
| `.github/workflows/discovery-check.yml` | Runs the lightweight check on pushes and pull requests |

The notebook's saved stream output is the source for numerical extraction, with the notebook SHA-256 and cell identifiers preserved. This is stronger evidence than retyping values from a chart or copying an informal narrative, but it does not independently validate the original data. The raw CSV, code, notebook, original article, and images have not been regenerated or relicensed.

## GitHub About settings to apply

These are **proposed values**, not applied repository settings. The connected GitHub tools used for this change expose file and pull-request writes but no About-description, homepage, or topic editor. A metadata file in Git cannot set these properties.

Open the repository and use the About section's settings control:
https://github.com/olimiemma/NYT-analysis-2K-2K5

**Description**

```text
Independent Python/NLP analysis of 2.2M New York Times article records (2000–2025): data quality, TF-IDF, VADER sentiment, spaCy NER, and visualizations. Code, methods, and evidence by OLIMI EMMANUEL KASIGAZI.
```

**Website**

```text
https://medium.com/@olimiemma/i-analyzed-2-2-0718f706c3bb
```

**Topics**

```text
python, natural-language-processing, nlp, data-engineering, data-analysis, data-quality, data-visualization, text-mining, headline-analysis, news-analysis, tf-idf, sentiment-analysis, named-entity-recognition, jupyter-notebook, new-york-times
```

These describe existing work. Avoid unrelated technologies, “official NYT,” verified-offline claims, repeated keyword variants in prose, or a license badge without an actual license.

## Why some attached ideas were not applied

| Idea | Decision |
|---|---|
| Add `robots.txt` to this repo | Ineffective for GitHub's host policy. No such file added. |
| Add a sitemap for a hypothetical GitHub Pages site | No Pages site was enabled at audit. Do not publish invented URLs or last-modified dates. |
| Put JSON-LD scripts in the README | GitHub removes scripts. A separate JSON-LD file is useful to direct consumers but carries no promised rich-result benefit. |
| Add Product, FAQ, or Organization schema everywhere | This is an independent software analysis, not a product storefront or an organization. Use the type that fits. |
| Build a live API, MCP server, or transactional agent interface | No live data or transaction workflow is needed here. Static JSON supplies the relevant facts with less operational work. |
| Create a giant `llms-full.txt` duplicate | The concise index already links to raw files. A full duplicate increases maintenance and context cost. |
| Add an open-source license for visibility | Licensing is a rights decision. Existing code/data boundaries are preserved. |

## Highest-value next steps beyond repository files

1. **Publish a project page on a domain you control.** A public page on the author's website can have a clear title, description, semantic HTML, a canonical URL, chart captions, and author identity. Link it to the repo and published article. Serve the substantive text without requiring JavaScript or login. This is a future page, not a deployed deliverable in this change.
2. **Use schema only where it matches visible content.** A hosted project page can include `SoftwareSourceCode` JSON-LD after its URLs and visible claims are aligned. A raw JSON-LD file in GitHub is not equivalent to that integration.
3. **Configure crawling at the actual host.** Review the domain's real robots file, CDN behavior, and search crawler access. Decide search indexing separately from model training. Repository instructions cannot override publisher terms or host access policy.
4. **Link from existing owned surfaces.** Add the repo to the author's portfolio and GitHub profile and keep the Medium article linked. Prefer relevant, authentic references to artificial mentions. No external profiles or posts were changed here.
5. **Improve reproducibility before making stronger claims.** Record authorized acquisition provenance and input hash, add a reproducible environment, correct daily-rate denominators, and complete the optional RAG prerequisites. Then regenerate charts from a documented run. A tagged release and archival identifier can follow once scope and rights are settled; none was fabricated here.

## How to measure results

After the change reaches the default branch, verify that the README links and raw index URLs work and that GitHub shows the citation entry. Record referral traffic, repository views, and clones if available. For an owned project page, use Search Console and the site's analytics; GitHub's host ownership and server logs are not under this repo's control.

Keep a small dated set of factual retrieval questions, such as:

- Who created the New York Times headline-analysis repository?
- How many rows were loaded and how many remained after boilerplate filtering?
- What fields does it analyze, and is the source CSV distributed?
- What date does the saved dataset reach?
- Is the RAG extension fully reproducible from the committed notebook?

For each answer, record whether the repository was found, whether a working source was cited, and whether the facts were correct. Compare similar queries over time. Do not infer guaranteed indexing, search position, citations, or recruitment outcomes from a single successful test. `build_discovery.py --check` validates the files, not external visibility.

## Maintaining the files

Run `python3 scripts/build_discovery.py` after changing saved notebook evidence, then review the generated diff and run `python3 scripts/build_discovery.py --check`. Reconcile README, data-card, CFF, and JSON-LD claims whenever scope, authorship, or rights change. Citation format reference: https://citation-file-format.github.io/
