from __future__ import annotations

import json
import csv
from collections import Counter
from pathlib import Path
from typing import Any


QUEST_KEY = "quest_01"
STATE_PATH = Path(".buildguild/state.json")
ARTICLES_PATH = Path("data/onboarding/articles.csv")
SUPPORT_QUESTIONS_PATH = Path("data/onboarding/support_questions.csv")
ARTICLE_TYPE_FREQUENCY_PATH = Path("analysis/article_type_frequency.csv")
PRODUCT_REQUIREMENTS_PATH = Path("analysis/quest_01_product_requirements.md")
IMPLEMENTATION_SPEC_PATH = Path("analysis/quest_01_implementation_spec.md")
REPORT_PATH = Path("analysis/baseline_report.md")
IMPLEMENTATION_FILES = [
    Path("analysis/ask.py"),
    Path("analysis/rag.py"),
    Path("app/retrieval.py"),
    Path("analysis/run_baseline.py"),
    Path("analysis/metrics.py"),
]


def build_status_line(root: Path) -> str:
    checks = inspect_checks(root)
    completed = sum(1 for value in checks.values() if value)
    total = len(checks)

    stage, next_hint = resolve_stage(checks)
    return f"BuildGuild Q1 [{completed}/{total}] {stage} -> {next_hint}"


def inspect_checks(root: Path) -> dict[str, bool]:
    state = load_state(root)
    quest = state.get(QUEST_KEY, {})
    player = state.get("player", {})
    return {
        "setup": bool(player.get("setup_completed")),
        "mike_onboarding": bool(quest.get("customer_pain_onboarding_completed")),
        "article_type_frequency": article_type_frequency_is_valid(root),
        "product_onboarding": bool(quest.get("product_onboarding_completed")),
        "product_requirements": (root / PRODUCT_REQUIREMENTS_PATH).exists(),
        "implementation_spec_file": (root / IMPLEMENTATION_SPEC_PATH).exists(),
        "implementation_spec_done": bool(quest.get("implementation_spec_completed")),
        "implementation": all((root / path).exists() for path in IMPLEMENTATION_FILES),
        "baseline_report": (root / REPORT_PATH).exists(),
        "maya_review": bool(quest.get("maya_report_review_passed")),
    }


def resolve_stage(checks: dict[str, bool]) -> tuple[str, str]:
    if not checks["setup"]:
        return "Quest setup", "buildguild start"
    if not checks["mike_onboarding"] or not checks["article_type_frequency"]:
        return "Mike onboarding", "mike-data-onboarding"
    if not checks["product_onboarding"] or not checks["product_requirements"]:
        return "Product discovery", "/quest-status"
    if not checks["implementation_spec_file"] or not checks["implementation_spec_done"]:
        return "Tour + spec", "ari-data-guide"
    if not checks["implementation"]:
        return "Implement baseline", "analysis scripts"
    if not checks["baseline_report"]:
        return "Run evaluation", "baseline report"
    if not checks["maya_review"]:
        return "Maya review", "maya-tests-outputs"
    return "Complete", "watch repo"


def load_state(root: Path) -> dict[str, Any]:
    state_path = root / STATE_PATH
    if not state_path.exists():
        return {}

    try:
        data = json.loads(state_path.read_text())
    except json.JSONDecodeError:
        return {}

    if isinstance(data, dict):
        return data
    return {}


def article_type_frequency_is_valid(root: Path) -> bool:
    output_path = root / ARTICLE_TYPE_FREQUENCY_PATH
    if not output_path.exists():
        return False

    try:
        expected = expected_article_type_counts(root)
        actual = load_frequency_counts(output_path)
    except (OSError, csv.Error, ValueError):
        return False

    return actual == expected


def expected_article_type_counts(root: Path) -> Counter[str]:
    article_types: dict[str, str] = {}
    with (root / ARTICLES_PATH).open(newline="") as handle:
        for row in csv.DictReader(handle):
            article_id = (row.get("article_id") or "").strip()
            article_type = (row.get("article_type") or "").strip()
            if article_id and article_type:
                article_types[article_id] = article_type

    counts: Counter[str] = Counter()
    with (root / SUPPORT_QUESTIONS_PATH).open(newline="") as handle:
        for row in csv.DictReader(handle):
            for article_id in (row.get("article_ids") or "").split(";"):
                article_type = article_types.get(article_id.strip())
                if article_type:
                    counts[article_type] += 1
    return counts


def load_frequency_counts(path: Path) -> Counter[str]:
    counts: Counter[str] = Counter()
    with path.open(newline="") as handle:
        reader = csv.DictReader(handle)
        if not reader.fieldnames:
            return counts
        fieldnames = {name.lower(): name for name in reader.fieldnames}
        article_type_key = fieldnames.get("article_type") or fieldnames.get("type")
        count_key = fieldnames.get("count") or fieldnames.get("frequency") or fieldnames.get("uses")
        if not article_type_key or not count_key:
            raise ValueError("Missing article type or count column")
        for row in reader:
            article_type = (row.get(article_type_key) or "").strip()
            if article_type:
                counts[article_type] = int((row.get(count_key) or "").strip())
    return counts


def repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def main() -> None:
    print(build_status_line(repo_root()))


if __name__ == "__main__":
    main()
