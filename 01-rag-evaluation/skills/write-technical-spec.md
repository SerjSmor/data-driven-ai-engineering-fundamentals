# Write Technical Spec

Use this skill only if the learner asks specifically for the standalone technical-spec instructions. The preferred Quest 1 path is `skills/ari-data-guide.md`, which combines the data tour and technical spec into one step.

Use after:

- `analysis/quest_01_product_requirements.md` exists.
- The learner has toured the data with Ari or equivalent EDA.

The learner and coding agent should collaboratively create:

```text
analysis/quest_01_implementation_spec.md
```

This is the actual implementation ticket for Quest 1.

## Workshop Rules

- Do not jump straight to code.
- Ask one engineering question at a time.
- Keep scope aligned with Maya's product requirements.
- Make the learner decide the baseline approach.
- Keep agentic RAG, reranking, hybrid search, dashboards, Slack, and GitHub API out of scope.

## Required Sections

```text
# Quest 1 Technical Spec: Baseline RAG Evaluation

## Product Requirement Source
## Goal
## Data Tour Findings
## User-Facing Commands
## Files To Implement
## Data Contracts
## Baseline Retrieval Approach
## Evaluation Plan
## Report Format
## Acceptance Criteria
## Out of Scope
## Implementation Order
```

## Evaluation Plan Must Include

- Command: `python analysis/run_baseline.py`
- Retrieval uses the existing backend lexical retriever in `app/retrieval.py`.
- The current chatbot path is `app/chatbot.py`: customer question -> top 5 retrieved articles -> simple source-based answer.
- Data comes from `data/onboarding/articles.csv` and `data/onboarding/support_questions.csv`.
- The learner implements the retrieval evaluation harness, CLI path, and report.
- Retrieval evaluates whether the expected WixQA source article appears in the top 5 retrieved documents.
- Metrics:
  - `retrieval_hit_rate@5`
  - `num_failed_questions`
- Report path: `analysis/baseline_report.md`
- Positive examples.
- Negative failed examples.

When the spec is complete, update `.buildguild/state.json`:

```json
{
  "quest_01": {
    "implementation_spec_completed": true
  }
}
```
