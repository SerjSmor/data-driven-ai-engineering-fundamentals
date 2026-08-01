# Project Setup

Use this skill when the player asks what this repo is, how the pieces fit together, or what to run.

Keep it minimal. Do not start a roleplay scene.

## Explain The Setup

BuildGuild Quest 1 is a repo-based game:

- Mike introduces the company data relationship: `skills/mike-data-onboarding.md`.
- Maya handles product discovery: `skills/maya-product-lead.md`.
- Ari handles data tour plus technical spec: `skills/ari-data-guide.md`.
- The backend starter retriever is `app/retrieval.py`.
- The current chatbot-shaped pipeline is `app/chatbot.py`: question -> retrieve top 5 articles -> draft a simple source-based answer.
- The player implements the evaluator/report around that retriever.
- Quest progress can unlock achievements: Product Hunch, Data Intuition, and Baseline Before Optimization.
- Quest 1 completion levels the player to Baseline Builder; Quest 2 is not available yet.

## Key Commands

```text
uv run buildguild start
uv run --extra dev invoke data
uv run buildguild status
```

`uv run buildguild start` asks for the player name and guidance level. These settings are stored in `.buildguild/settings.json`; quest progress is stored separately in `.buildguild/state.json`.

If `.buildguild/settings.json` already exists, start asks whether to continue with the same name and guidance level.

The selected difficulty controls how much help the quest gives:

- easy: Apprentice mode with direct hints, clear nudges, and frequent check-ins.
- medium: Builder mode with fewer hints; the player drives the investigation.
- hard: Expert mode with minimal spoon-feeding and distracting noise while keeping the quest solvable.

## Main Artifacts

```text
analysis/article_type_frequency.csv
analysis/quest_01_product_requirements.md
analysis/quest_01_implementation_spec.md
analysis/baseline_report.md
.buildguild/state.json
.buildguild/settings.json
```

## Flow

```text
start -> Mike -> Maya -> Ari -> implementation -> evaluation report -> Maya review
```

If the onboarding CSVs are missing, run `uv run --extra dev invoke data` before the tour.
