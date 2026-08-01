#!/usr/bin/env python3
"""Read-only smoke checks for the BuildGuild workspace."""

from __future__ import annotations

import ast
import json
import subprocess
import sys
import tomllib
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
QUESTS = (
    "01-rag-evaluation",
    "02-few-shot-prompt-optimization",
    "03-atis-few-shot-dspy",
    "04-llm-judge-calibration",
)


def fail(message: str) -> None:
    print(f"FAIL: {message}", file=sys.stderr)
    raise SystemExit(1)


def load_json(path: Path) -> dict:
    try:
        with path.open("r", encoding="utf-8") as handle:
            return json.load(handle)
    except (OSError, json.JSONDecodeError) as exc:
        fail(f"{path.relative_to(ROOT)} is not valid JSON: {exc}")


def parse_python(path: Path) -> None:
    try:
        ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    except (OSError, SyntaxError) as exc:
        fail(f"{path.relative_to(ROOT)} is not valid Python: {exc}")


def check_help(path: Path, cwd: Path = ROOT) -> None:
    result = subprocess.run(
        [sys.executable, str(path), "--help"],
        cwd=cwd,
        capture_output=True,
        text=True,
    )
    if result.returncode:
        fail(f"{path.relative_to(ROOT)} --help failed: {result.stderr.strip()}")


def main() -> None:
    with (ROOT / "pyproject.toml").open("rb") as handle:
        workspace = tomllib.load(handle).get("tool", {}).get("uv", {}).get("workspace", {})
    if workspace.get("members") != list(QUESTS):
        fail("root uv workspace members do not match the supported quests")

    result = subprocess.run(["make", "--dry-run", "install"], cwd=ROOT, capture_output=True, text=True)
    if result.returncode:
        fail(f"documented make install command is unavailable: {result.stderr.strip()}")

    for quest in QUESTS:
        quest_root = ROOT / quest
        if not quest_root.is_dir():
            fail(f"missing quest directory: {quest}")
        for required in ("README.md", "pyproject.toml", "challenge.json"):
            if not (quest_root / required).is_file():
                fail(f"{quest} is missing {required}")

        challenge = load_json(quest_root / "challenge.json")
        if not isinstance(challenge.get("milestones"), list):
            fail(f"{quest}/challenge.json must contain milestones")

        if quest == "01-rag-evaluation":
            for source in sorted((quest_root / "app").glob("*.py")):
                parse_python(source)
            for source in sorted((quest_root / "buildguild").glob("*.py")):
                parse_python(source)
            parse_python(quest_root / "tasks.py")
            check_help(quest_root / "scripts" / "restart_quest.py", quest_root)
            continue

        for required in ("progress.json", "app.py"):
            if not (quest_root / required).is_file():
                fail(f"{quest} is missing {required}")
        progress = load_json(quest_root / "progress.json")
        if not isinstance(progress.get("tasks"), dict):
            fail(f"{quest}/progress.json must contain tasks")
        parse_python(quest_root / "app.py")

        scripts = quest_root / "scripts"
        for script in sorted(scripts.glob("*.py")):
            parse_python(script)
            check_help(script)

    print(f"Workspace smoke checks passed for {len(QUESTS)} quests.")


if __name__ == "__main__":
    main()
