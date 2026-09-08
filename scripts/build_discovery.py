#!/usr/bin/env python3
"""Extract small, attributable summaries from saved notebook output, never execute it."""

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
NOTEBOOK = "NYT_analysis_2K_2K5.ipynb"
REPO = "https://github.com/olimiemma/NYT-analysis-2K-2K5"
RAW = "https://raw.githubusercontent.com/olimiemma/NYT-analysis-2K-2K5/main/"
AUTHOR = "OLIMI EMMANUEL KASIGAZI"
STAGES = [
    ("loaded", "CSV loaded", "A2pY5hFposUd", r"^Shape:\s+([\d,]+) rows"),
    ("date_title_valid", "Date/title validity filter", "YuaeYcYSpdRm", r"^Clean shape: ([\d,]+) rows"),
    ("url_deduplicated", "URL deduplication", "Sam3L8QDrfAO", r"^After dedup:\s+([\d,]+) rows"),
    ("title_length_filtered", "Title length cap", "Sam3L8QDrfAO", r"^After title cap: ([\d,]+) rows"),
    ("description_length_filtered", "Description length cap", "Sam3L8QDrfAO", r"^After desc cap:\s+([\d,]+) rows"),
    ("boilerplate_filtered", "Boilerplate-title filter", "tqPmCZd2ugSa", r"^Working set: ([\d,]+) articles"),
]


def require(condition, message):
    if not condition:
        raise ValueError(message)


def match(pattern, text):
    found = re.search(pattern, text, re.MULTILINE)
    require(found is not None, f"Expected notebook evidence missing: {pattern}")
    return found


def integer(pattern, text):
    return int(match(pattern, text).group(1).replace(",", ""))


def extract():
    raw = (ROOT / NOTEBOOK).read_bytes()
    notebook = json.loads(raw)
    cells = {}
    for index, cell in enumerate(notebook["cells"]):
        identifier = cell.get("metadata", {}).get("id") or cell.get("id")
        if identifier:
            require(identifier not in cells, f"Duplicate cell identifier: {identifier}")
            cells[identifier] = (index, cell)

    def stream(identifier):
        require(identifier in cells, f"Source cell missing: {identifier}")
        return "".join(
            "".join(out.get("text", []))
            for out in cells[identifier][1].get("outputs", [])
            if out.get("output_type") == "stream"
        )

    def source(identifier):
        return "".join(cells[identifier][1]["source"])

    stages = []
    for key, label, identifier, pattern in STAGES:
        rows = integer(pattern, stream(identifier))
        previous = stages[-1]["rows"] if stages else rows
        require(0 < rows <= previous, f"Non-monotonic corpus count: {key}")
        stages.append({"id": key, "label": label, "rows": rows,
                       "removed_since_previous": previous - rows,
                       "cell_id": identifier, "cell_index_zero_based": cells[identifier][0]})

    # Compare computed deltas to the recorded cleanup messages, not just total counts.
    cleanup = stream("Sam3L8QDrfAO")
    for stage, pattern in zip(stages[2:5], [r"\(-([\d,]+) dupes", r"\(-([\d,]+) bad titles", r"\(-([\d,]+) bloated descriptions"]):
        require(stage["removed_since_previous"] == integer(pattern, cleanup),
                f"Recorded removal count disagrees with stage: {stage['id']}")
    require(stages[-1]["removed_since_previous"] == integer(r"^Removed ([\d,]+) boilerplate", stream("tqPmCZd2ugSa")),
            "Boilerplate removal count disagrees")

    audit = stream("YuaeYcYSpdRm")
    start, end = match(r"^Date range:\s+(\d{4}-\d{2}-\d{2})\s+to\s+(\d{4}-\d{2}-\d{2})", audit).groups()
    annual = [{"year": int(y), "rows": int(n)} for y, n in
              re.findall(r"^(\d{4})(?:\.0)?\s+(\d+)\s*$", audit, re.MULTILINE)]
    require(annual and len({x['year'] for x in annual}) == len(annual), "Missing or duplicate annual counts")
    require(sum(x["rows"] for x in annual) == stages[1]["rows"], "Annual counts do not sum to the dated corpus")
    require(start[:4] == str(annual[0]["year"]) and end[:4] == str(annual[-1]["year"]), "Date/year mismatch")

    ner_id, rag_id = "ljCAfxhjygsd", "UX9oM76A13l0"
    target_pattern = r"int\((\d+)\s*\*\s*len\(x\)"
    ner_target = integer(target_pattern, source(ner_id))
    ner_actual = integer(r"^Sample size: ([\d,]+) articles", stream(ner_id))
    require(ner_actual == integer(r"^Done\. ([\d,]+) titles processed", stream(ner_id)), "NER run did not finish the sample")
    require(0 < ner_actual <= min(ner_target, stages[-1]["rows"]), "Invalid NER size")
    rag_target = integer(target_pattern, source(rag_id))
    rag_text = stream(rag_id)
    rag_actual = integer(r"^Sample size: ([\d,]+) articles", rag_text) if rag_text.strip() else None
    if rag_actual is not None:
        require(0 < rag_actual <= min(rag_target, stages[-1]["rows"]), "Invalid RAG size")

    return {
        "format_version": 1,
        "project": REPO,
        "author": AUTHOR,
        "basis": "Extraction from archived notebook stream outputs and sampling code; no analysis rerun or source-data verification.",
        "source": {"path": NOTEBOOK, "url": f"{REPO}/blob/main/{NOTEBOOK}",
                   "sha256": hashlib.sha256(raw).hexdigest(), "bytes": len(raw),
                   "cell_identifier_location": "cells[].metadata.id (Colab identifier)",
                   "citation_note": "Record the Git commit when citing; the URL follows main. The hash identifies the exact notebook bytes."},
        "date_coverage": {"start": start, "end": end, "stage": "date_title_valid",
                          "cell_id": "YuaeYcYSpdRm", "calendar_years_represented": len(annual),
                          "archive_completeness_verified": False},
        "corpus_stages": stages,
        "ner_sample": {"target": ner_target, "recorded_processed": ner_actual,
                       "allocation": "proportional by year with per-year integer truncation", "cell_id": ner_id},
        "rag_sample": {"target": rag_target, "recorded_sample": rag_actual, "cell_id": rag_id,
                       "note": "A sample target is not evidence of a completed retrieval/generation run."},
        "annual_coverage": {"stage": "date_title_valid", "cell_id": "YuaeYcYSpdRm",
                            "unit": "source records before URL deduplication and length filtering",
                            "counts": annual},
        "limitations": ["Raw CSV and acquisition logs are not distributed.",
                        "Annual source counts do not measure verified newsroom production.",
                        "The final year is partial; acquisition coverage is unverified.",
                        "This summary does not grant data-reuse or training rights."]
    }


def render(summary):
    coverage = summary["date_coverage"]
    lines = ["# Recorded results and provenance", "",
             "These counts are extracted from saved notebook output. They are not a new analysis run or a verification of the original CSV. The original notebook, source code, and charts are unchanged by this extraction.", "",
             f"Recorded dates: **{coverage['start']} to {coverage['end']}**, after initial validity filtering. The interval touches {coverage['calendar_years_represented']} calendar years; 2025 is incomplete.", "",
             "## Corpus stages", "", "| Stage | Records | Removed at this step | Notebook cell ID |", "|---|---:|---:|---|"]
    for stage in summary["corpus_stages"]:
        removed = f"{stage['removed_since_previous']:,}" if stage["id"] != "loaded" else "n/a"
        lines.append(f"| {stage['label']} | {stage['rows']:,} | {removed} | `{stage['cell_id']}` |")
    ner, rag = summary["ner_sample"], summary["rag_sample"]
    rag_size = f"{rag['recorded_sample']:,}" if rag["recorded_sample"] is not None else "not recorded"
    lines += ["", "## Sampling", "", "| Extension | Target | Recorded output | Notebook cell ID |", "|---|---:|---|---|",
              f"| spaCy NER | {ner['target']:,} | {ner['recorded_processed']:,} titles processed | `{ner['cell_id']}` |",
              f"| Optional RAG sample | {rag['target']:,} | {rag_size} | `{rag['cell_id']}` |", "",
              "The year-proportional sampling code truncates each year's allocation to an integer. A configured target and an observed sample size are different quantities. The RAG code still needs missing embedding setup and runtime-specific model assets.", "",
              "## Annual source coverage", "",
              "These counts precede URL deduplication and title/description length filtering. They sum to the date/title-valid stage. They describe the collected snapshot, not a complete archive or an official newsroom publication ledger. Collection gaps are possible but their cause is unconfirmed.", "",
              "| Year | Source records |", "|---|---:|"]
    lines += [f"| {row['year']} | {row['rows']:,} |" for row in summary["annual_coverage"]["counts"]]
    lines += ["", "## Evidence and limits", "",
              f"Notebook: {summary['source']['url']}", "",
              "Cell IDs above are the notebook's `metadata.id` values; zero-based positions are also supplied in the JSON. Capture the repository commit when citing a result. The hash below identifies the exact notebook bytes read by the extractor.", "",
              f"Notebook SHA-256: `{summary['source']['sha256']}`", "",
              "Machine-readable version: [analysis-summary.json](../metadata/analysis-summary.json).", "",
              "The [data card](data-card.md) explains denominator errors, source provenance, lexical sentiment, sampling, and incomplete RAG setup. Chart interpretations require these qualifications; the original narrative is not an independently validated findings table.", "",
              "Generated by `python3 scripts/build_discovery.py`. Check freshness with `python3 scripts/build_discovery.py --check`. No raw article rows are exported.", ""]
    return "\n".join(lines)


def check_docs(summary):
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    table_labels = {
        "loaded": "Rows loaded from the source CSV",
        "date_title_valid": "Rows after date/title validity filtering",
        "description_length_filtered": "Clean records after deduplication and outlier filtering",
        "boilerplate_filtered": "Records after the additional boilerplate-title filter",
    }
    for stage in summary["corpus_stages"]:
        if stage["id"] in table_labels:
            require(f"| {table_labels[stage['id']]} | {stage['rows']:,} |" in readme,
                    f"README table count is stale: {stage['id']}")
    require(f"{summary['ner_sample']['recorded_processed']:,}" in readme, "README NER sample is stale")
    require(summary['date_coverage']['end'] in readme, "README date is stale")
    cff = (ROOT / "CITATION.cff").read_text(encoding="utf-8")
    schema = json.loads((ROOT / "metadata/software.jsonld").read_text(encoding="utf-8"))
    require(schema["@type"] == "SoftwareSourceCode", "Schema must describe software, not a distributed dataset")
    require(schema["codeRepository"] == REPO and schema["author"]["name"] == AUTHOR, "Software identity mismatch")
    for text in [readme, (ROOT / "llms.txt").read_text(encoding="utf-8"), (ROOT / "AGENTS.md").read_text(encoding="utf-8")]:
        require(AUTHOR in text, "Inconsistent author identity")
    for field, expected in [("family-names", "KASIGAZI"), ("given-names", "OLIMI EMMANUEL"),
                            ("title", schema["name"]), ("repository-code", REPO)]:
        require(f'{field}: "{expected}"' in cff, f"CFF identity mismatch: {field}")

    documents = [ROOT / "README.md", ROOT / "llms.txt", ROOT / "AGENTS.md", *sorted((ROOT / "docs").glob("*.md"))]
    links_checked = 0
    for document in documents:
        text = document.read_text(encoding="utf-8")
        links = re.findall(r"\[[^\]\n]*\]\(([^)\s]+)\)", text)
        links += re.findall(r'(?:src|href)="([^"]+)"', text)
        for link in links:
            decoded = unquote(link)
            if decoded.startswith(RAW):
                target = ROOT / urlsplit(decoded[len(RAW):]).path
            elif decoded.startswith(REPO + "/blob/main/"):
                target = ROOT / urlsplit(decoded[len(REPO + "/blob/main/"):]).path
            elif urlsplit(decoded).scheme or decoded.startswith("#"):
                continue
            else:
                target = document.parent / urlsplit(decoded).path
            target = target.resolve()
            require(target.is_relative_to(ROOT) and target.is_file(), f"Broken local link in {document.name}: {link}")
            links_checked += 1
    return links_checked


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="Check evidence, generated-file freshness, and documentation links without writing")
    args = parser.parse_args()
    summary = extract()
    outputs = {"metadata/analysis-summary.json": json.dumps(summary, ensure_ascii=False, indent=2) + "\n",
               "docs/results.md": render(summary)}
    for path, content in outputs.items():
        target = ROOT / path
        if args.check:
            require(target.exists() and target.read_text(encoding="utf-8") == content, f"Stale generated file: {path}; run python3 scripts/build_discovery.py")
        else:
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(content, encoding="utf-8")
    links = check_docs(summary)
    stage_count = len(summary["corpus_stages"])
    year_count = len(summary["annual_coverage"]["counts"])
    print(f"{'Checked' if args.check else 'Generated'} 2 summaries; verified {stage_count} corpus stages, {year_count} annual counts, sample evidence, identity, and {links} local file links. No notebook cells executed.")


if __name__ == "__main__":
    try:
        main()
    except (ValueError, KeyError, OSError) as error:
        print(f"Discovery check failed: {error}", file=sys.stderr)
        sys.exit(1)
