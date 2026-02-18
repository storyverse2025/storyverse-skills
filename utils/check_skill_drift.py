#!/usr/bin/env python3
"""Validate StoryVerse skill command metadata and markdown references."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Iterable, List, Set


COMMAND_REF_RE = re.compile(r"(/sv-[a-z0-9-]+)\b")


def discover_command_files(repo_root: Path) -> Set[str]:
    commands_dir = repo_root / ".claude" / "commands"
    command_files = commands_dir.glob("sv-*.md")
    return {f"/{path.stem}" for path in command_files}


def read_manifest(repo_root: Path, manifest_relpath: str) -> dict:
    manifest_path = repo_root / manifest_relpath
    with manifest_path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def markdown_files(repo_root: Path) -> Iterable[Path]:
    yield repo_root / "README.md"
    yield repo_root / "CLAUDE.md"
    commands_dir = repo_root / ".claude" / "commands"
    yield from commands_dir.glob("*.md")


def extract_command_refs(paths: Iterable[Path]) -> Set[str]:
    refs: Set[str] = set()
    for path in paths:
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        refs.update(COMMAND_REF_RE.findall(text))
    return refs


def validate_manifest(repo_root: Path, manifest: dict) -> List[str]:
    errors: List[str] = []
    commands = manifest.get("commands")
    if not isinstance(commands, list):
        return ["Manifest must contain a top-level 'commands' array."]

    seen_commands: Set[str] = set()
    for idx, entry in enumerate(commands):
        if not isinstance(entry, dict):
            errors.append(f"Manifest entry #{idx + 1} must be an object.")
            continue

        command = entry.get("command")
        file_rel = entry.get("file")
        if not command or not isinstance(command, str):
            errors.append(f"Manifest entry #{idx + 1} missing string 'command'.")
            continue
        if not file_rel or not isinstance(file_rel, str):
            errors.append(f"Manifest entry '{command}' missing string 'file'.")
            continue

        if command in seen_commands:
            errors.append(f"Duplicate manifest command: {command}")
        seen_commands.add(command)

        file_path = repo_root / file_rel
        if not file_path.exists():
            errors.append(f"Manifest file for {command} does not exist: {file_rel}")
            continue

        expected_command = f"/{file_path.stem}"
        if command != expected_command:
            errors.append(
                f"Manifest command/file mismatch: {command} vs {file_rel} (expected {expected_command})"
            )

    return errors


def main() -> int:
    repo_root = Path(__file__).resolve().parents[1]
    manifest_relpath = "context/skills-manifest.json"
    errors: List[str] = []

    manifest = read_manifest(repo_root, manifest_relpath)
    errors.extend(validate_manifest(repo_root, manifest))

    manifest_commands = {
        entry["command"]
        for entry in manifest.get("commands", [])
        if isinstance(entry, dict) and isinstance(entry.get("command"), str)
    }
    discovered_commands = discover_command_files(repo_root)

    missing_in_manifest = sorted(discovered_commands - manifest_commands)
    extra_in_manifest = sorted(manifest_commands - discovered_commands)

    if missing_in_manifest:
        errors.append(
            "Commands exist on disk but are missing in manifest: "
            + ", ".join(missing_in_manifest)
        )
    if extra_in_manifest:
        errors.append(
            "Manifest includes commands that have no command file: "
            + ", ".join(extra_in_manifest)
        )

    refs = extract_command_refs(markdown_files(repo_root))
    unknown_refs = sorted(refs - discovered_commands)
    if unknown_refs:
        errors.append(
            "Unknown /sv-* command references in markdown: "
            + ", ".join(unknown_refs)
        )

    if errors:
        print("Skill drift check failed:")
        for err in errors:
            print(f"- {err}")
        return 1

    print("Skill drift check passed.")
    print(f"- Command files: {len(discovered_commands)}")
    print(f"- Manifest commands: {len(manifest_commands)}")
    print(f"- Markdown command refs: {len(refs)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
