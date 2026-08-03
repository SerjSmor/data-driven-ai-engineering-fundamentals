#!/usr/bin/env python3
import argparse
import ast
import json
from copy import deepcopy
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load(path):
    return json.loads(path.read_text(encoding="utf-8"))


def save(path, value):
    path.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8")


def tasks(challenge):
    for milestone in challenge["milestones"]:
        for task in milestone["tasks"]:
            item = deepcopy(task)
            item["milestone_title"] = milestone["title"]
            yield item


def syntax_check(path):
    try:
        ast.parse(path.read_text(encoding="utf-8"))
        return True, f"Valid Python syntax: {path.relative_to(ROOT)}"
    except (OSError, SyntaxError) as exc:
        return False, f"Python check failed for {path.relative_to(ROOT)}: {exc}"


def text_signals(path, terms):
    source = path.read_text(encoding="utf-8").lower()
    found = [term for term in terms if term in source]
    return source, found


def inspect(task):
    paths = [ROOT / name for name in task.get("expected_artifacts", [])]
    evidence, risks = [], []
    missing = [p for p in paths if not p.exists() or p.stat().st_size == 0]
    if missing:
        return False, evidence, [f"Missing or empty: {p.relative_to(ROOT)}" for p in missing]
    evidence.extend(f"Found {p.relative_to(ROOT)} ({p.stat().st_size} bytes)" for p in paths)
    for path in paths:
        if path.suffix == ".py":
            ok, message = syntax_check(path)
            evidence.append(message)
            if not ok:
                risks.append(message)
        elif path.suffix == ".json":
            try:
                load(path)
                evidence.append(f"Valid JSON: {path.relative_to(ROOT)}")
            except (OSError, json.JSONDecodeError) as exc:
                risks.append(f"Invalid JSON: {exc}")

    checks = {
        "profile_dataset": (paths[0], ["wixqa_expertwritten", "wix_kb_corpus", "article_ids"]),
        "build_dataset_explorer": (paths[0], ["streamlit", "dataframe", "load_dataset"]),
        "explain_knowledge_base": (paths[0], ["article_ids", "retriev", "knowledge base"]),
        "draw_rag_flow": (paths[0], ["mermaid", "retriev", "context", "answer"]),
        "trace_example": (paths[0], ["question", "article", "context", "answer"]),
        "implement_retriever": (paths[0], ["top_k", "score", "contents", "fit"]),
        "build_search_ui": (paths[0], ["streamlit", "top_k", "score", "retriev"]),
        "design_grounded_prompt": (paths[0], ["question", "context", "insufficient", "source"]),
        "implement_rag_pipeline": (paths[0], ["retriev", "context", "question", "source"]),
        "build_chatbot_ui": (paths[0], ["streamlit", "chat", "source", "answer"]),
        "evaluate_retrieval": (paths[0], ["recall", "reciprocal", "article_ids", "top_k"]),
        "add_llm_judge": (paths[0], ["grounded", "complete", "evidence", "score"]),
    }
    if task["id"] in checks:
        path, terms = checks[task["id"]]
        _, found = text_signals(path, terms)
        evidence.append(f"Implementation signals: {', '.join(found) or 'none'}")
        threshold = max(2, len(terms) - 1)
        if len(found) < threshold:
            risks.append(f"Expected stronger evidence of: {', '.join(terms)}")

    if task["id"] == "test_retriever":
        data = load(paths[0])
        rows = data.get("results", data) if isinstance(data, dict) else data
        ok = isinstance(rows, list) and bool(rows) and isinstance(rows[0], dict)
        required = {"question", "gold_article_ids", "retrieved_article_ids"}
        if not ok or not required.issubset(rows[0]):
            risks.append("Save non-empty per-question gold and ranked retrieved article IDs.")
        else:
            evidence.append(f"Retrieval test rows: {len(rows)}")
    if task["id"] == "evaluate_retrieval":
        data = load(paths[1])
        aggregate = data.get("aggregate", {})
        keys = " ".join(aggregate).lower()
        if "mrr" not in keys or not any(name in keys for name in ("recall", "hit_rate")):
            risks.append("Aggregate results must include MRR and recall or hit rate at k.")
    if task["id"] == "evaluate_answers":
        data = load(paths[0])
        rows = data.get("results", data) if isinstance(data, dict) else data
        required = {"question", "reference_answer", "gold_article_ids", "retrieved_sources", "generated_answer"}
        if not isinstance(rows, list) or not rows or not required.issubset(rows[0]):
            risks.append("Answer results need questions, references, gold IDs, retrieved sources, and generated answers.")
    return not risks, evidence, risks


def verdict(task):
    evidence = [f"Task: {task['title']}", f"Milestone: {task['milestone_title']}", f"Judge level: {task.get('judge_level', 'medium')}"]
    try:
        ok, extra, risks = inspect(task)
    except (OSError, KeyError, TypeError, json.JSONDecodeError) as exc:
        ok, extra, risks = False, [], [f"Could not inspect artifact: {exc}"]
    return {
        "verdict": "pass" if ok else "needs_revision",
        "confidence": "high" if task.get("judge_level") == "hard" else "medium",
        "evidence": evidence + extra,
        "missing_or_risky": risks,
        "commands_run": [],
        "checked_at": datetime.now(timezone.utc).isoformat(),
    }


def main():
    parser = argparse.ArgumentParser(description="Judge ready WixQA quest tasks.")
    parser.add_argument("--task")
    parser.add_argument("--all", action="store_true")
    args = parser.parse_args()
    challenge, progress = load(ROOT / "challenge.json"), load(ROOT / "progress.json")
    judged = []
    for task in tasks(challenge):
        if args.task and task["id"] != args.task:
            continue
        state = progress["tasks"][task["id"]]
        if not args.all and state["status"] != "ready_for_judgment":
            continue
        result = verdict(task)
        state["judge"] = result
        state["status"] = "complete" if result["verdict"] == "pass" else "needs_revision"
        judged.append((task["id"], result["verdict"]))
    save(ROOT / "progress.json", progress)
    print("\n".join(f"{task_id}: {result}" for task_id, result in judged) or "No tasks judged.")


if __name__ == "__main__":
    main()
