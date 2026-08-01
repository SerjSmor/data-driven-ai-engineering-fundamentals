from __future__ import annotations

import csv
from collections import Counter
from pathlib import Path


ARTICLES_PATH = Path("data/onboarding/articles.csv")
SUPPORT_QUESTIONS_PATH = Path("data/onboarding/support_questions.csv")
ARTICLE_TYPE_FREQUENCY_PATH = Path("analysis/article_type_frequency.csv")


def expected_article_type_counts(
    articles_path: Path = ARTICLES_PATH,
    support_questions_path: Path = SUPPORT_QUESTIONS_PATH,
) -> Counter[str]:
    article_types = _load_article_types(articles_path)
    counts: Counter[str] = Counter()

    with support_questions_path.open(newline="") as handle:
        for row in csv.DictReader(handle):
            for article_id in _split_article_ids(row.get("article_ids", "")):
                article_type = article_types.get(article_id)
                if article_type:
                    counts[article_type] += 1

    return counts


def article_type_frequency_is_valid(
    output_path: Path = ARTICLE_TYPE_FREQUENCY_PATH,
    articles_path: Path = ARTICLES_PATH,
    support_questions_path: Path = SUPPORT_QUESTIONS_PATH,
) -> bool:
    if not output_path.exists():
        return False

    try:
        expected = expected_article_type_counts(articles_path, support_questions_path)
        actual = _load_frequency_counts(output_path)
    except (OSError, csv.Error, ValueError):
        return False

    return actual == expected


def _load_article_types(path: Path) -> dict[str, str]:
    article_types: dict[str, str] = {}
    with path.open(newline="") as handle:
        for row in csv.DictReader(handle):
            article_id = (row.get("article_id") or "").strip()
            article_type = (row.get("article_type") or "").strip()
            if article_id and article_type:
                article_types[article_id] = article_type
    return article_types


def _load_frequency_counts(path: Path) -> Counter[str]:
    counts: Counter[str] = Counter()
    with path.open(newline="") as handle:
        reader = csv.DictReader(handle)
        if not reader.fieldnames:
            return counts

        article_type_key = _find_column(reader.fieldnames, "article_type", "type")
        count_key = _find_column(reader.fieldnames, "count", "frequency", "uses")
        if article_type_key is None or count_key is None:
            raise ValueError("Missing article_type or count column")

        for row in reader:
            article_type = (row.get(article_type_key) or "").strip()
            count_text = (row.get(count_key) or "").strip()
            if article_type:
                counts[article_type] = int(count_text)
    return counts


def _find_column(fieldnames: list[str], *candidates: str) -> str | None:
    normalized = {fieldname.strip().lower(): fieldname for fieldname in fieldnames}
    for candidate in candidates:
        if candidate in normalized:
            return normalized[candidate]
    return None


def _split_article_ids(raw_value: str) -> list[str]:
    return [article_id.strip() for article_id in raw_value.split(";") if article_id.strip()]
