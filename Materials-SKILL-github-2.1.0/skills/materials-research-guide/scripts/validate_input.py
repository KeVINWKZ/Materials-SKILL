#!/usr/bin/env python3
"""Validate and normalize structured input for the materials-research skill."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


REQUIRED_TEXT_FIELDS = ("material_system", "research_goal")
LIST_FIELDS = ("known_processes", "available_equipment")
OBJECT_FIELDS = ("constraints", "evidence_preferences")


def _clean_text(value: str) -> str:
    return " ".join(value.split())


def validate(payload: Any) -> tuple[dict[str, Any], list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    if not isinstance(payload, dict):
        return {}, ["Top-level input must be a JSON object."], []

    normalized = dict(payload)
    for field in REQUIRED_TEXT_FIELDS:
        value = payload.get(field)
        if not isinstance(value, str) or not value.strip():
            errors.append(f"{field} must be a non-empty string.")
        else:
            normalized[field] = _clean_text(value)

    application = payload.get("application")
    if application is not None:
        if not isinstance(application, str):
            errors.append("application must be a string when provided.")
        else:
            normalized["application"] = _clean_text(application)

    for field in LIST_FIELDS:
        value = payload.get(field, [])
        if not isinstance(value, list) or any(not isinstance(item, str) for item in value):
            errors.append(f"{field} must be a list of strings.")
        else:
            normalized[field] = [_clean_text(item) for item in value if item.strip()]

    for field in OBJECT_FIELDS:
        value = payload.get(field, {})
        if not isinstance(value, dict):
            errors.append(f"{field} must be a JSON object.")
        else:
            normalized[field] = value

    preferences = normalized.get("evidence_preferences", {})
    minimum = preferences.get("minimum_verified_sources", 3)
    if not isinstance(minimum, int) or minimum < 1:
        errors.append("evidence_preferences.minimum_verified_sources must be an integer >= 1.")
    elif minimum < 3:
        warnings.append("Fewer than three verified sources may be insufficient for strong claims.")

    for recommended in ("application", "available_equipment", "constraints"):
        if not normalized.get(recommended):
            warnings.append(f"Recommended field is missing or empty: {recommended}.")

    normalized["schema_version"] = "1.0"
    return normalized, errors, warnings


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path, help="UTF-8 JSON input file")
    parser.add_argument("--output", type=Path, help="Optional normalized JSON output")
    args = parser.parse_args()

    try:
        payload = json.loads(args.input.read_text(encoding="utf-8-sig"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"ERROR: cannot read valid JSON: {exc}", file=sys.stderr)
        return 2

    normalized, errors, warnings = validate(payload)
    for warning in warnings:
        print(f"WARNING: {warning}", file=sys.stderr)
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1

    rendered = json.dumps(normalized, ensure_ascii=False, indent=2) + "\n"
    if args.output:
        args.output.write_text(rendered, encoding="utf-8")
    else:
        sys.stdout.write(rendered)
    print("Input validation passed.", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
