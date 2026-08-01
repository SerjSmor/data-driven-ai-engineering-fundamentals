# Quest 1: RAG Evaluation - Agent Context

See `challenge.json` for milestones, tasks, and artifacts. This file covers quest-specific narrative and mechanics.

## Quest Flow

```
start -> Mike data onboarding -> Maya product discovery -> Ari technical spec -> learner implementation -> Maya report review
```

## Key Mechanics

**Characters & Progressive Guidance:**
- **Mike** (data lead): Explains drag-and-drop builder company context, data relationships, article schema. Produces `analysis/article_type_frequency.csv`.
- **Maya** (product manager): Product discovery via hidden checkboxes (`???` labels). Reveals labels only after qualifying questions. Produces `analysis/quest_01_product_requirements.md`.
- **Ari** (coding agent): EDA mode. Creates `analysis/quest_01_implementation_spec.md` with `## Data Tour Findings` section. Does NOT implement the baseline.

**State & Unlocks:**
- Player name and difficulty stored in `.buildguild/settings.json`.
- Quest progress in `.buildguild/state.json`.
- Unlock `product_hunch` after product discovery, `data_intuition` after Ari's spec, `baseline_before_optimization` after Maya accepts report.

## Quest-Specific Rules

- Start with `uv run buildguild start`. Complete setup, then immediately start Mike's onboarding.
- Do not rush end-to-end; use guided pair-programming loops.
- Show compact table previews, not raw wide CSV lines, unless explicitly asked.
- Do not ship a complete baseline RAG solution in starter repo.
- Keep scope narrow: no agentic RAG, reranking, hybrid retrieval, Slack, GitHub API, or dashboards.
- After product discovery, use `skills/ari-data-guide.md` for EDA and technical spec writing.

## Completion

Quest 1 complete only after:
- `quest_01.maya_report_review_passed = true` (Maya accepts baseline report)
- Player levels to Level 2, title "Baseline Builder"
- Quest 2 not yet available; direct player to watch repo for updates

## Quick Start

**When you say "start module 1 quest":** Your agent will run `uv run buildguild start` to initialize your player profile and set difficulty level.

## Reference Commands

```text
uv run buildguild start    # Start the game (player setup)
uv run buildguild status   # Show current quest stage
uv run --extra dev invoke data # Prepare dataset CSVs
```
