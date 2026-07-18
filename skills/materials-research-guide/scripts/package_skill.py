#!/usr/bin/env python3
"""Create a deterministic, secret-aware SkillHub upload ZIP."""

from __future__ import annotations

import argparse
import json
import re
import sys
import zipfile
from pathlib import Path


EXCLUDED_PARTS = {".git", ".idea", ".vscode", "__pycache__", "dist", "build"}
SENSITIVE_NAMES = {
    ".env",
    "credentials.json",
    "secrets.json",
    "id_rsa",
    "id_ed25519",
}
SENSITIVE_SUFFIXES = {".pem", ".key", ".p12", ".pfx"}
MAX_ZIP_BYTES = 10 * 1024 * 1024


REQUIRED_SKILLHUB_FIELDS = ("slug", "version", "displayName", "summary")


def _load_metadata(skill_dir: Path) -> dict[str, object]:
    metadata_path = skill_dir / "skillhub-metadata.json"
    try:
        metadata = json.loads(metadata_path.read_text(encoding="utf-8-sig"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError(f"Cannot read valid skillhub-metadata.json: {exc}") from exc
    if not isinstance(metadata, dict):
        raise ValueError("skillhub-metadata.json must contain a JSON object.")
    missing = [field for field in REQUIRED_SKILLHUB_FIELDS if not metadata.get(field)]
    if missing:
        raise ValueError("Missing SkillHub metadata fields: " + ", ".join(missing))
    if not re.fullmatch(r"\d+\.\d+\.\d+(?:[-+][0-9A-Za-z.-]+)?", str(metadata["version"])):
        raise ValueError("SkillHub version must be valid SemVer.")
    tags = metadata.get("tags", [])
    if not isinstance(tags, list) or any(not isinstance(tag, str) for tag in tags):
        raise ValueError("SkillHub tags must be a list of strings.")
    return metadata


def _release_skill_md(source: str, metadata: dict[str, object]) -> str:
    match = re.match(r"^(---\r?\n)(.*?)(\r?\n---\r?\n)", source, flags=re.DOTALL)
    if not match:
        raise ValueError("SKILL.md frontmatter is invalid.")
    tags = ", ".join(json.dumps(tag, ensure_ascii=False) for tag in metadata.get("tags", []))
    injected = "\n".join(
        (
            f"slug: {json.dumps(metadata['slug'], ensure_ascii=False)}",
            f"version: {json.dumps(metadata['version'], ensure_ascii=False)}",
            f"displayName: {json.dumps(metadata['displayName'], ensure_ascii=False)}",
            f"summary: {json.dumps(metadata['summary'], ensure_ascii=False)}",
            f"tags: [{tags}]",
        )
    )
    frontmatter = match.group(2).rstrip() + "\n" + injected
    return match.group(1) + frontmatter + match.group(3) + source[match.end():]


def _is_excluded(relative: Path) -> bool:
    return bool(EXCLUDED_PARTS.intersection(relative.parts)) or relative.name in {".DS_Store", "Thumbs.db"}


def _is_sensitive(relative: Path) -> bool:
    lower_name = relative.name.lower()
    return lower_name in SENSITIVE_NAMES or relative.suffix.lower() in SENSITIVE_SUFFIXES


def collect_files(skill_dir: Path) -> list[Path]:
    files: list[Path] = []
    sensitive: list[str] = []
    for path in sorted(skill_dir.rglob("*"), key=lambda item: item.as_posix().lower()):
        if not path.is_file():
            continue
        relative = path.relative_to(skill_dir)
        if _is_excluded(relative):
            continue
        if _is_sensitive(relative):
            sensitive.append(relative.as_posix())
            continue
        files.append(path)
    if sensitive:
        raise ValueError("Sensitive-looking files found: " + ", ".join(sensitive))
    return files


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("skill_dir", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    skill_dir = args.skill_dir.resolve()
    skill_md_path = skill_dir / "SKILL.md"
    if not skill_md_path.is_file():
        print("ERROR: SKILL.md is missing.", file=sys.stderr)
        return 1

    try:
        source_skill_md = skill_md_path.read_text(encoding="utf-8-sig")
        metadata = _load_metadata(skill_dir)
        version = str(metadata["version"])
        release_skill_md = _release_skill_md(source_skill_md, metadata).encode("utf-8")
        files = collect_files(skill_dir)
    except (OSError, ValueError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1

    output = args.output or skill_dir / "dist" / f"{skill_dir.name}-{version}.zip"
    output = output.resolve()
    output.parent.mkdir(parents=True, exist_ok=True)

    with zipfile.ZipFile(output, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for path in files:
            relative = path.relative_to(skill_dir).as_posix()
            info = zipfile.ZipInfo(relative, date_time=(2020, 1, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o644 << 16
            data = release_skill_md if relative == "SKILL.md" else path.read_bytes()
            archive.writestr(info, data)

    size = output.stat().st_size
    if size > MAX_ZIP_BYTES:
        output.unlink(missing_ok=True)
        print(f"ERROR: ZIP exceeds the 10 MB SkillHub upload limit ({size} bytes).", file=sys.stderr)
        return 1

    print(f"Created: {output}")
    print(f"Files: {len(files)}")
    print(f"Bytes: {size}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
