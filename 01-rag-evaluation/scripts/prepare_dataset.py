from __future__ import annotations

import os
import re
import csv
from collections.abc import Iterable, Mapping
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
ONBOARDING_DIR = ROOT / "data" / "onboarding"
ONBOARDING_ARTICLES_PATH = ONBOARDING_DIR / "articles.csv"
ONBOARDING_SUPPORT_QUESTIONS_PATH = ONBOARDING_DIR / "support_questions.csv"
DEFAULT_DATASET_NAME = "Wix/WixQA"
DEFAULT_DATASET_CONFIGS = ("wix_kb_corpus", "wixqa_expertwritten")
DATASET_ENV_VAR = "BUILDGUILD_WIXQA_DATASET"

QUESTION_KEYS = ("question", "query", "user_query", "prompt")
ANSWER_KEYS = ("answer", "reference_answer", "ground_truth_answer", "response")
DOC_BODY_KEYS = (
    "body",
    "content",
    "contents",
    "text",
    "article",
    "article_text",
    "html_text",
    "html_content",
)
DOC_TITLE_KEYS = ("title", "article_title", "name")
DOC_URL_KEYS = ("url", "article_url", "source_url", "link")
DOC_ID_KEYS = ("id", "doc_id", "document_id", "article_id", "kb_id")
DOC_TYPE_KEYS = ("article_type", "type")
QUESTION_ID_KEYS = ("id", "question_id", "qa_id")
SOURCE_DOC_KEYS = (
    "article_ids",
    "article_id",
    "expected_doc_ids",
    "relevant_doc_ids",
    "gold_doc_ids",
    "source_doc_ids",
    "urls",
    "url",
    "source_urls",
    "article_url",
)


def prepare_dataset(
    dataset_name: str | None = None,
    output_dir: Path = ONBOARDING_DIR,
    load_fn=None,
) -> None:
    dataset_name = dataset_name or os.environ.get(DATASET_ENV_VAR, DEFAULT_DATASET_NAME)
    load_fn = load_fn or load_wixqa
    dataset = load_fn(dataset_name)
    documents, questions = normalize_dataset(dataset)

    if not documents:
        raise ValueError("Could not find WixQA knowledge-base articles in the Hugging Face dataset.")
    if not questions:
        raise ValueError("Could not find WixQA question rows in the Hugging Face dataset.")

    write_onboarding_csvs(documents, questions, output_dir)
    print(f"Wrote {len(documents)} articles to {output_dir / 'articles.csv'}")
    print(f"Wrote {len(questions)} support questions to {output_dir / 'support_questions.csv'}")


def load_wixqa(dataset_name: str) -> DatasetDict | IterableDatasetDict | dict[str, Any]:
    from datasets import DatasetDict, IterableDatasetDict, get_dataset_config_names, load_dataset

    if dataset_name == DEFAULT_DATASET_NAME:
        return {config: load_dataset(dataset_name, config) for config in DEFAULT_DATASET_CONFIGS}

    try:
        return load_dataset(dataset_name)
    except ValueError:
        configs = get_dataset_config_names(dataset_name)
        if not configs:
            raise
        loaded: dict[str, Any] = {}
        for config in configs:
            loaded[config] = load_dataset(dataset_name, config)
        return loaded


def normalize_dataset(dataset: Any) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    documents_by_id: dict[str, dict[str, Any]] = {}
    questions: list[dict[str, Any]] = []

    for source_name, row in iter_rows(dataset):
        if is_document_row(row, source_name):
            document = normalize_document(row, len(documents_by_id) + 1)
            documents_by_id.setdefault(document["id"], document)
            continue

        if is_question_row(row, source_name):
            questions.append(normalize_question(row, len(questions) + 1))

    return list(documents_by_id.values()), questions


def iter_rows(dataset: Any, prefix: str = "") -> Iterable[tuple[str, Mapping[str, Any]]]:
    dataset_dict_types = (dict,)
    try:
        from datasets import DatasetDict, IterableDatasetDict

        dataset_dict_types = (DatasetDict, IterableDatasetDict, dict)
    except ImportError:
        pass

    if isinstance(dataset, dataset_dict_types):
        for name, value in dataset.items():
            next_prefix = f"{prefix}/{name}" if prefix else str(name)
            yield from iter_rows(value, next_prefix)
        return

    for row in dataset:
        if isinstance(row, Mapping):
            yield prefix, row


def is_document_row(row: Mapping[str, Any], source_name: str) -> bool:
    has_body = first_value(row, DOC_BODY_KEYS) is not None
    source_is_kb = "wix_kb_corpus" in source_name.lower() or any(
        token in source_name.lower() for token in ("kb", "knowledge", "article", "document")
    )
    return bool(has_body and source_is_kb)


def is_question_row(row: Mapping[str, Any], source_name: str) -> bool:
    has_question = first_value(row, QUESTION_KEYS) is not None
    source_is_qa = "wixqa_expertwritten" in source_name.lower()
    return bool(has_question and source_is_qa)


def normalize_document(row: Mapping[str, Any], index: int) -> dict[str, Any]:
    raw_id = first_value(row, DOC_ID_KEYS) or first_value(row, DOC_URL_KEYS) or f"doc_{index:05d}"
    title = first_value(row, DOC_TITLE_KEYS) or f"Untitled article {index}"
    url = first_value(row, DOC_URL_KEYS) or str(raw_id)
    body = first_value(row, DOC_BODY_KEYS) or ""
    article_type = first_value(row, DOC_TYPE_KEYS) or ""
    return {
        "id": stable_id(raw_id, "doc", index),
        "title": clean_text(title),
        "url": clean_text(url),
        "body": clean_text(body),
        "article_type": clean_text(article_type),
    }


def normalize_question(row: Mapping[str, Any], index: int) -> dict[str, Any]:
    raw_id = first_value(row, QUESTION_ID_KEYS) or f"q_{index:05d}"
    question = first_value(row, QUESTION_KEYS) or ""
    answer = first_value(row, ANSWER_KEYS) or ""
    source_doc_ids = first_list_value(row, SOURCE_DOC_KEYS)
    return {
        "id": stable_id(raw_id, "q", index),
        "question": clean_text(question),
        "answer": clean_text(answer),
        "article_ids": [
            stable_id(value, "doc", position + 1)
            for position, value in enumerate(source_doc_ids)
        ],
    }


def first_value(row: Mapping[str, Any], keys: tuple[str, ...]) -> Any | None:
    for key in keys:
        if key in row and row[key] not in (None, ""):
            return row[key]
    return None


def first_list_value(row: Mapping[str, Any], keys: tuple[str, ...]) -> list[Any]:
    for key in keys:
        if key not in row:
            continue
        value = row[key]
        if value in (None, ""):
            continue
        if isinstance(value, list):
            return value
        if isinstance(value, tuple):
            return list(value)
        if isinstance(value, str):
            return [part.strip() for part in re.split(r"[,;\n]", value) if part.strip()]
        return [value]
    return []


def stable_id(value: Any, prefix: str, index: int) -> str:
    text = clean_text(value)
    if not text:
        return f"{prefix}_{index:05d}"
    if text.startswith(f"{prefix}_"):
        return text
    if text.startswith("http"):
        return text
    return text


def clean_text(value: Any) -> str:
    if isinstance(value, list):
        return "\n".join(clean_text(item) for item in value if item not in (None, ""))
    return re.sub(r"\s+", " ", str(value)).strip()


def write_onboarding_csvs(
    documents: list[dict[str, Any]],
    questions: list[dict[str, Any]],
    output_dir: Path = ONBOARDING_DIR,
) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)

    with (output_dir / "articles.csv").open("w", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=["article_id", "title", "article_type", "url", "body"],
        )
        writer.writeheader()
        for document in documents:
            writer.writerow(
                {
                    "article_id": document["id"],
                    "title": document["title"],
                    "article_type": document.get("article_type", ""),
                    "url": document["url"],
                    "body": document["body"],
                }
            )

    with (output_dir / "support_questions.csv").open("w", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=["question_id", "question", "answer", "article_ids"],
        )
        writer.writeheader()
        for question in questions:
            writer.writerow(
                {
                    "question_id": question["id"],
                    "question": question["question"],
                    "answer": question["answer"],
                    "article_ids": ";".join(question["article_ids"]),
                }
            )


if __name__ == "__main__":
    prepare_dataset()
