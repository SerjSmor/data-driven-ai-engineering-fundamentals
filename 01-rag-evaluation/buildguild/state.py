from __future__ import annotations

import json
from pathlib import Path
from typing import Any


DEFAULT_STATE: dict[str, Any] = {
    "quest_01": {
        "customer_pain_onboarding_completed": False,
        "product_onboarding_completed": False,
        "implementation_spec_completed": False,
        "maya_report_review_passed": False,
    },
    "player": {
        "name": None,
        "difficulty": "easy",
        "setup_completed": False,
        "level": 1,
        "title": "New Builder",
        "xp": 0,
        "achievements": {
            "product_hunch": False,
            "data_intuition": False,
            "baseline_before_optimization": False,
        },
    }
}

STATE_PATH = Path(".buildguild/state.json")


def load_state(path: Path = STATE_PATH) -> dict[str, Any]:
    if not path.exists():
        save_state(DEFAULT_STATE.copy(), path)
        return json.loads(json.dumps(DEFAULT_STATE))

    try:
        data = json.loads(path.read_text())
    except json.JSONDecodeError:
        data = {}

    return _with_defaults(data)


def save_state(state: dict[str, Any], path: Path = STATE_PATH) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(state, indent=2, sort_keys=True) + "\n")


def update_quest_state(quest_key: str, updates: dict[str, Any], path: Path = STATE_PATH) -> dict[str, Any]:
    state = load_state(path)
    quest_state = state.setdefault(quest_key, {})
    quest_state.update(updates)
    save_state(state, path)
    return state


def update_player_state(updates: dict[str, Any], path: Path = STATE_PATH) -> dict[str, Any]:
    state = load_state(path)
    player_state = state.setdefault("player", {})
    for key, value in updates.items():
        if isinstance(value, dict) and isinstance(player_state.get(key), dict):
            player_state[key].update(value)
        else:
            player_state[key] = value
    save_state(state, path)
    return state


def _with_defaults(data: dict[str, Any]) -> dict[str, Any]:
    state = json.loads(json.dumps(DEFAULT_STATE))
    for key, value in data.items():
        if isinstance(value, dict) and isinstance(state.get(key), dict):
            _deep_update(state[key], value)
        else:
            state[key] = value
    return state


def _deep_update(target: dict[str, Any], updates: dict[str, Any]) -> None:
    for key, value in updates.items():
        if isinstance(value, dict) and isinstance(target.get(key), dict):
            _deep_update(target[key], value)
        else:
            target[key] = value
