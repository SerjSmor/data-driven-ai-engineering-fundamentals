from __future__ import annotations

import csv
import math
import re
from collections import Counter
from dataclasses import dataclass
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_ARTICLES_PATH = ROOT / "data" / "onboarding" / "articles.csv"
TOKEN_RE = re.compile(r"[A-Za-z0-9]+")


@dataclass(frozen=True)
class SearchResult:
    id: str
    title: str
    url: str
    body: str
    score: float


class LexicalRetriever:
    """Backend-owned lexical retriever used as the Quest 1 baseline."""

    def __init__(self, documents: list[dict[str, Any]]) -> None:
        self.documents = documents
        self._doc_tokens = [tokenize(document_text(document)) for document in documents]
        self._doc_term_counts = [Counter(tokens) for tokens in self._doc_tokens]
        self._idf = compute_idf(self._doc_tokens)

    @classmethod
    def from_csv(cls, path: Path = DEFAULT_ARTICLES_PATH) -> "LexicalRetriever":
        if not path.exists():
            raise FileNotFoundError(f"Missing articles CSV: {path}")
        with path.open(newline="") as handle:
            documents = [normalize_article_row(row) for row in csv.DictReader(handle)]
        return cls(documents)

    def search(self, query: str, top_k: int = 5) -> list[SearchResult]:
        query_terms = tokenize(query)
        if not query_terms:
            return []

        query_counts = Counter(query_terms)
        scored: list[SearchResult] = []
        for document, term_counts, tokens in zip(
            self.documents, self._doc_term_counts, self._doc_tokens, strict=True
        ):
            score = lexical_score(query_counts, term_counts, len(tokens), self._idf)
            if score <= 0:
                continue
            scored.append(
                SearchResult(
                    id=str(document["id"]),
                    title=str(document["title"]),
                    url=str(document["url"]),
                    body=str(document["body"]),
                    score=score,
                )
            )

        return sorted(scored, key=lambda result: result.score, reverse=True)[:top_k]


def document_text(document: dict[str, Any]) -> str:
    return f"{document.get('title', '')} {document.get('body', '')}"


def normalize_article_row(row: dict[str, str]) -> dict[str, str]:
    required = ("article_id", "title", "url", "body")
    missing = [key for key in required if key not in row]
    if missing:
        raise ValueError(f"Missing required article CSV columns: {', '.join(missing)}")
    return {
        "id": row["article_id"],
        "title": row["title"],
        "url": row["url"],
        "body": row["body"],
    }


def tokenize(text: str) -> list[str]:
    return [match.group(0).lower() for match in TOKEN_RE.finditer(text)]


def compute_idf(tokenized_documents: list[list[str]]) -> dict[str, float]:
    document_count = max(len(tokenized_documents), 1)
    document_frequency: Counter[str] = Counter()
    for tokens in tokenized_documents:
        document_frequency.update(set(tokens))
    return {
        term: math.log((document_count + 1) / (frequency + 0.5)) + 1
        for term, frequency in document_frequency.items()
    }


def lexical_score(
    query_counts: Counter[str],
    document_counts: Counter[str],
    document_length: int,
    idf: dict[str, float],
) -> float:
    score = 0.0
    length_norm = 1.0 / math.sqrt(max(document_length, 1))
    for term, query_count in query_counts.items():
        term_frequency = document_counts.get(term, 0)
        if term_frequency:
            score += query_count * (1 + math.log(term_frequency)) * idf.get(term, 1.0)
    return score * length_norm
