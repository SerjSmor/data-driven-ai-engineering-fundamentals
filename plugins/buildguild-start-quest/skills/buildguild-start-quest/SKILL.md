---
name: buildguild-start-quest
description: Starts a BuildGuild quest module. Use whenever the user says "let's start module N quest", "start module 1", "start the BuildGuild game", or otherwise asks to begin or restart a quest in this repo. This is a direct action request. Run the game rather than planning first.
---

# Start a BuildGuild Quest

## Resolve the module

| User says | Directory |
| --- | --- |
| module 1 / 01 / rag evaluation | `01-rag-evaluation` |
| module 2 / 02 / prompt optimization | `02-few-shot-prompt-optimization` |
| module 3 / 03 / dspy | `03-atis-few-shot-dspy` |
| module 4 / 04 / llm judge | `04-llm-judge-calibration` |

If no module is specified, ask the user which available module to start.

## Start the quest

Run from the selected module directory. Quest 1 has an interactive terminal
onboarding flow; Quests 2–4 are Streamlit workspaces.

```bash
# Quest 1 only
uv run buildguild start

# Quests 2–4
uv run --no-project --with-requirements requirements.txt streamlit run app.py
```

For Quest 1, the command asks for the player's name and difficulty (`easy`,
`medium`, or `hard`). Do not choose either value for the user. If stdin is
unavailable, ask in chat and rerun with `--name` and `--difficulty`.

For Quests 2–4, open the Streamlit URL printed by the command. Read the
selected module's `AGENTS.md` (if present) and `README.md` for its specific
workflow.

## Troubleshooting

- If Quest 1 onboarding CSVs are missing, run `uv run --extra dev invoke data` from `01-rag-evaluation`.
- Run `uv run buildguild status` to find the current Quest 1 stage and next action.
- Quest 1 restart instructions are in `skills/restart-game.md`.
