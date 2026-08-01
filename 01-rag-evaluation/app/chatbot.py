from __future__ import annotations

from dataclasses import dataclass

from app.retrieval import LexicalRetriever, SearchResult


@dataclass(frozen=True)
class ChatbotAnswer:
    question: str
    answer: str
    retrieved_documents: list[SearchResult]


def answer_question(question: str, top_k: int = 5) -> ChatbotAnswer:
    """Run the current help-center chatbot pipeline.

    This is the production-shaped baseline: retrieve candidate help articles,
    then generate a simple answer from those sources. Quest 1 evaluates the
    retrieval step, because answer generation cannot use an article that was
    never retrieved.
    """
    retriever = LexicalRetriever.from_csv()
    retrieved_documents = retriever.search(question, top_k=top_k)
    answer = generate_answer_from_results(question, retrieved_documents)
    return ChatbotAnswer(
        question=question,
        answer=answer,
        retrieved_documents=retrieved_documents,
    )


def generate_answer_from_results(question: str, results: list[SearchResult]) -> str:
    if not results:
        return (
            "I could not find a matching help-center article for that question yet. "
            "A support specialist should review it."
        )

    lines = [
        "I found these help-center articles that may answer your question:",
    ]
    for index, result in enumerate(results, start=1):
        lines.append(f"{index}. {result.title} ({result.url})")
    return "\n".join(lines)
