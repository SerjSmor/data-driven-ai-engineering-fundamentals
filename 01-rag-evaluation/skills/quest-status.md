# Quest Status

Use this skill whenever the player asks for Quest 1 status, uses `/quest-status`, or asks what to do next.

This skill is agent-agnostic. Codex, Claude Code, OpenCode, and a plain chat agent should all follow the same status contract.

## Preferred Path

If it is safe and available, run:

```text
uv run buildguild status
```

If running `uv` would trigger cache, permission, environment, or approval friction, do not request permission just for status. Inspect files directly instead.

## Direct Inspection

Read:

- `.buildguild/settings.json`
- `.buildguild/state.json`
- `player.name` from settings first, then state fallback.
- `player.difficulty` from settings first, then state fallback.
- `player.setup_completed`
- `player.level`
- `player.title`
- `player.xp`
- `player.achievements`

Check whether these files exist:

- `analysis/article_type_frequency.csv`
- `analysis/quest_01_product_requirements.md`
- `analysis/quest_01_implementation_spec.md`
- `analysis/baseline_report.md`
- `analysis/ask.py`
- `analysis/rag.py`
- `app/retrieval.py`
- `app/chatbot.py`
- `analysis/run_baseline.py`
- `analysis/metrics.py`

## Stage Order

Report the first incomplete stage:

1. Quest setup
   - Needs `player.setup_completed = true`.
   - Next action: run `uv run buildguild start`.
   - This asks: "What is your name, brave adventurer?" and "How much guidance do you want on this quest?"

2. Mike data onboarding
   - Needs `quest_01.customer_pain_onboarding_completed = true`.
   - Needs valid `analysis/article_type_frequency.csv`.
   - Next action: ask the coding agent to use `skills/mike-data-onboarding.md`.

3. Product discovery
   - Needs `quest_01.product_onboarding_completed = true`.
   - Needs `analysis/quest_01_product_requirements.md`.

4. Tour data and write implementation spec
   - Needs `analysis/quest_01_implementation_spec.md`.
   - Needs `quest_01.implementation_spec_completed = true`.
   - Next action: ask the coding agent to use `skills/ari-data-guide.md`; if using Streamlit, Ari should build the EDA app with the player.

5. Implement baseline evaluation
   - Needs `analysis/ask.py`.
   - Needs `analysis/rag.py`.
   - Needs `app/retrieval.py`.
   - Needs `app/chatbot.py`.
   - Needs `analysis/run_baseline.py`.
   - Needs `analysis/metrics.py`.

6. Run baseline evaluation
   - Needs `analysis/baseline_report.md`.

7. Maya report review
   - Needs `quest_01.maya_report_review_passed = true`.

8. Quest complete
   - Show unlocked achievements.
   - Say Quest 2 is not available yet and the player should watch the repo for updates.

## Response Format

Keep it short:

```text
Quest 1 Status
Stage: <stage>

Done:
- ...

Missing:
- ...

Next:
<one concrete next action>

Player:
Name: <name if known>
Difficulty: <easy|medium|hard>
Level <level> - <title> (<xp> XP)

Achievements:
- ...
```

Do not role-play Maya in status output. Do not start product discovery. Only report current state and the next action.
