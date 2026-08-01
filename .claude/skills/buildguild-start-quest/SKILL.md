---
name: buildguild-start-quest
description: Starts a BuildGuild quest module. Use whenever the user says "let's start module N quest", "start module 1", "start the BuildGuild game", or otherwise asks to begin/restart a quest in this repo. This is a direct action request — run the game, do not brainstorm, write design docs, or plan first.
---

# Start a BuildGuild Quest

The user wants to play. Run the game and let it drive — the quest itself supplies the
narrative, the mentors, and the next steps. Your job is to launch it and then follow the
quest's own instructions, not to invent a curriculum around it.

## 1. Resolve the module directory

| User says | Directory | Launch style |
|-----------|-----------|--------------|
| module 1 / 01 / rag evaluation | `01-rag-evaluation` | interactive terminal CLI |
| module 2 / 02 / prompt optimization | `02-few-shot-prompt-optimization` | Streamlit workspace |
| module 3 / 03 / dspy | `03-atis-few-shot-dspy` | Streamlit workspace |
| module 4 / 04 / llm judge | `04-llm-judge-calibration` | Streamlit workspace |

If the user just says "start the BuildGuild game" with no module, check which modules exist
and ask which one — don't guess.

The two launch styles are genuinely different. Only module 1 has the `buildguild` CLI;
running it in modules 2–4 will fail.

## 2a. Module 1 — run the CLI

```bash
cd 01-rag-evaluation
uv run buildguild start
```

The command prints the quest banner, then prompts for **Name** and **Difficulty**
(`easy` / `medium` / `hard`).

**These are the player's choices, not yours.** Never pass `--name` or `--difficulty` to
answer on their behalf — picking a name for someone is exactly the kind of thing they came
to the game to do. If the command aborts because it couldn't read stdin, ask the user for
their name and guidance level in chat, then re-run with those values as flags:

```bash
uv run buildguild start --name "<their answer>" --difficulty "<their answer>"
```

Guidance levels, if they ask:

- `easy` — Apprentice mode: direct hints, clear nudges, frequent check-ins.
- `medium` — Builder mode: fewer hints, the player drives the investigation.
- `hard` — Expert mode: minimal spoon-feeding, plus distracting noise.

If `.buildguild/settings.json` already exists, start offers to continue with the saved name
and level. Let the user decide.

## 2b. Modules 2–4 — run the Streamlit workspace

```bash
cd <module-directory>
uv run --no-project --with-requirements requirements.txt streamlit run app.py
```

`--no-project` matters: these modules are Streamlit apps, not importable packages, so the
workspace environment is deliberately bypassed in favour of `requirements.txt`.

Streamlit blocks the terminal, so start it in the background and hand the user the URL it
prints. `make stop-quests` (from the repo root) kills quests listening on ports 8502–8504.

## 3. Hand off to the quest

Module 1's setup writes `.buildguild/settings.json` (player name + difficulty) and tracks
progress separately in `.buildguild/state.json`. The command ends by naming the next step —
follow it immediately. For module 1 that is `skills/mike-data-onboarding.md`; read that file
and continue in character.

For modules 2–4 the app itself is the quest surface: point the user at the URL, then read
that module's `README.md` (and `AGENTS.md` if it has one — only module 1 does today) for its
own flow. Those files are the source of truth; don't assume module 1's shape applies
elsewhere.

## Troubleshooting

- **Module 1 onboarding CSVs missing** — run `uv run --extra dev invoke data` in `01-rag-evaluation`.
- **Lost track of where you are in module 1** — `uv run buildguild status` prints the current stage and next action.
- **Want to start over** — module 1 has `skills/restart-game.md`.
- **Streamlit port already in use** — `make stop-quests` from the repo root, then relaunch.
