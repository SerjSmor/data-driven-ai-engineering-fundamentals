from __future__ import annotations

import json
from pathlib import Path
from typing import Any


SETTINGS_PATH = Path(".buildguild/settings.json")


def load_settings(path: Path = SETTINGS_PATH) -> dict[str, Any]:
    if not path.exists():
        return {}

    try:
        data = json.loads(path.read_text())
    except json.JSONDecodeError:
        return {}

    if isinstance(data, dict):
        return data
    return {}


def save_settings(
    *,
    name: str,
    difficulty: str,
    path: Path = SETTINGS_PATH,
) -> dict[str, Any]:
    settings = {
        "player": {
            "name": name,
            "difficulty": difficulty,
        }
    }
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(settings, indent=2, sort_keys=True) + "\n")
    return settings


def player_settings(path: Path = SETTINGS_PATH) -> dict[str, str]:
    settings = load_settings(path)
    player = settings.get("player", {})
    if not isinstance(player, dict):
        return {}

    name = player.get("name")
    difficulty = player.get("difficulty")
    result: dict[str, str] = {}
    if isinstance(name, str) and name.strip():
        result["name"] = name.strip()
    if isinstance(difficulty, str) and difficulty.strip():
        result["difficulty"] = difficulty.strip().lower()
    return result
