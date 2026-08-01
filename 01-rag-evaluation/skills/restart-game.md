# Restart Game

Use this skill when the player asks to restart Quest 1, reset the game, restart Ari's step, or clear generated quest outputs.

This is destructive. Do not run any reset immediately.

There are two supported reset scopes:

- Full Quest 1 reset: use when the player asks to restart the whole game or Quest 1.
- Ari stage reset: use when the player asks to restart Ari, replay the EDA, redo the technical spec, or reset from the data-tour/spec step.

## Full Quest 1 Reset

First explain exactly what will happen:

- Delete generated Quest 1 output files:
  - `analysis/article_type_frequency.csv`
  - `analysis/quest_01_product_requirements.md`
  - `analysis/quest_01_implementation_spec.md`
  - `analysis/baseline_report.md`
  - `analysis/quest_01_eda.py`
  - `analysis/quest_01_eda.ipynb`
  - `analysis/quest_01_eda.md`
  - `analysis/ask.py`
  - `analysis/rag.py`
  - `analysis/run_baseline.py`
  - `analysis/metrics.py`
  - `analysis/test_baseline_evaluation.py`
- Reset `.buildguild/state.json` to the default Quest 1 flags.
- Keep `.buildguild/settings.json` so the player name and difficulty survive restart.
- Keep starter files, including `app/retrieval.py`, `app/chatbot.py`, skills, docs, and any prepared WixQA data.

Then ask the player to confirm full reset with this exact phrase:

```text
RESET_QUEST_01
```

If the player confirms full reset, run:

```text
python3 scripts/restart_quest.py --confirm RESET_QUEST_01
```

After the script succeeds, tell the player to ask their coding agent to start the BuildGuild game again.

## Ari Stage Reset

First explain exactly what will happen:

- Preserve:
  - `.buildguild/settings.json`
  - `analysis/article_type_frequency.csv`
  - `analysis/quest_01_product_requirements.md`
  - `quest_01.customer_pain_onboarding_completed`
  - `quest_01.product_onboarding_completed`
  - the Product Hunch achievement
- Delete Ari and downstream generated files:
  - `analysis/quest_01_implementation_spec.md`
  - `analysis/baseline_report.md`
  - `analysis/quest_01_eda.py`
  - `analysis/quest_01_eda.ipynb`
  - `analysis/quest_01_eda.md`
  - `analysis/ask.py`
  - `analysis/rag.py`
  - `analysis/run_baseline.py`
  - `analysis/metrics.py`
  - `analysis/test_baseline_evaluation.py`
- Reset Ari and downstream flags:
  - `quest_01.implementation_spec_completed = false`
  - `quest_01.maya_report_review_passed = false`
  - Data Intuition achievement locked again
  - Baseline Before Optimization achievement locked again

Then ask the player to confirm Ari reset with this exact phrase:

```text
RESET_ARI
```

If the player confirms Ari reset, run:

```text
python3 scripts/restart_quest.py --stage ari --confirm RESET_ARI
```

After the script succeeds, tell the player the expected next stage is Ari's data tour and technical spec:

```text
Use skills/ari-data-guide.md
```

If `analysis/quest_01_product_requirements.md` is missing after an Ari reset, do not continue to Ari. Tell the player to replay Maya product discovery because Ari needs Maya's handoff artifact.

## Confirmation Rule

If the player does not provide the exact phrase for the selected scope, do not reset anything.

Do not delete files manually. `scripts/restart_quest.py` is the source of truth for what gets reset.

## Completion

After either reset, it is useful to check:

```text
uv run buildguild status
```
