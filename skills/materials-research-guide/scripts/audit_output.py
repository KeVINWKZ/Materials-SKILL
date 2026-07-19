#!/usr/bin/env python3
"""Audit a complete-mode ten-section Markdown report.

This script is not suitable for compact-mode outputs. Use
references/compact-audit-checklist.md for compact-mode review.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


REQUIRED_HEADINGS = (
    "研究问题与边界",
    "文献证据表",
    "证据缺口与置信度",
    "实验方案",
    "表征方案",
    "机理假设与证伪",
    "创新点评估",
    "论文框架",
    "安全与局限",
    "已核验参考文献",
)

DOI_RE = re.compile(r"10\.\d{4,9}/[-._;()/:A-Z0-9]+", re.IGNORECASE)
PMID_RE = re.compile(r"\bPMID\s*:?\s*(\d{6,9})\b", re.IGNORECASE)
ARXIV_RE = re.compile(r"\barXiv\s*:?\s*(\d{4}\.\d{4,5}(?:v\d+)?)\b", re.IGNORECASE)
EVIDENCE_RE = re.compile(r"\bE\d+\b")
OVERCLAIM_TERMS = ("首次实现", "世界首创", "完全证明", "必然导致", "100%有效")


def _read_stdin_markdown() -> str:
    data = sys.stdin.buffer.read()
    candidates: list[str] = []
    for encoding in ("utf-8-sig", "utf-16", "utf-16-le", "gb18030"):
        try:
            candidates.append(data.decode(encoding))
        except UnicodeDecodeError:
            continue
    if not candidates:
        return data.decode("utf-8", errors="replace")
    return max(
        candidates,
        key=lambda text: text.count("##") + sum(heading in text for heading in REQUIRED_HEADINGS) * 10,
    )


def _section_names(markdown: str) -> set[str]:
    return {
        match.group(1).strip()
        for match in re.finditer(r"^##\s+(.+?)\s*$", markdown, flags=re.MULTILINE)
    }


def audit(markdown: str, minimum_sources: int) -> tuple[list[str], list[str], dict[str, int]]:
    errors: list[str] = []
    warnings: list[str] = []
    headings = _section_names(markdown)
    for heading in REQUIRED_HEADINGS:
        if heading not in headings:
            errors.append(f"Missing required section: {heading}")

    dois = {match.group(0).rstrip(".,;)").lower() for match in DOI_RE.finditer(markdown)}
    pmids = {match.group(1) for match in PMID_RE.finditer(markdown)}
    arxiv_ids = {match.group(1).lower() for match in ARXIV_RE.finditer(markdown)}
    source_count = len(dois) + len(pmids) + len(arxiv_ids)
    if source_count < minimum_sources:
        errors.append(
            f"Only {source_count} distinct DOI/PMID/arXiv identifiers found; "
            f"minimum is {minimum_sources}."
        )

    evidence_labels = set(EVIDENCE_RE.findall(markdown))
    if not evidence_labels:
        errors.append("No evidence labels such as E1 or E2 were found.")

    for term in OVERCLAIM_TERMS:
        if term in markdown:
            warnings.append(f"Potential overclaim requires explicit evidence and scope: {term}")

    if "待核验" in markdown and "已核验参考文献" in headings:
        warnings.append("Check that items marked 待核验 are not mixed into the verified reference list.")

    metrics = {
        "required_sections_found": len(set(REQUIRED_HEADINGS) & headings),
        "verified_identifier_count": source_count,
        "evidence_label_count": len(evidence_labels),
    }
    return errors, warnings, metrics


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Audit a complete-mode ten-section Markdown report only.",
        epilog=(
            "Compact-mode outputs must use references/compact-audit-checklist.md "
            "instead of this script."
        ),
    )
    parser.add_argument("report", help="Markdown report path, or - to read UTF-8 text from stdin")
    parser.add_argument(
        "--mode",
        choices=("complete",),
        required=True,
        help="Required safety gate confirming that the report uses complete mode.",
    )
    parser.add_argument("--min-sources", type=int, default=3)
    args = parser.parse_args()
    if args.min_sources < 1:
        parser.error("--min-sources must be >= 1")

    if args.report == "-":
        markdown = _read_stdin_markdown()
    else:
        try:
            markdown = Path(args.report).read_text(encoding="utf-8-sig")
        except OSError as exc:
            print(f"ERROR: cannot read report: {exc}", file=sys.stderr)
            return 2

    errors, warnings, metrics = audit(markdown, args.min_sources)
    for key, value in metrics.items():
        print(f"{key}: {value}")
    for warning in warnings:
        print(f"WARNING: {warning}")
    for error in errors:
        print(f"ERROR: {error}")

    if errors:
        return 1
    print("Output audit passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
