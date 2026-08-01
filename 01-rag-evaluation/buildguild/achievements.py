from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from buildguild.state import STATE_PATH, load_state, save_state


@dataclass(frozen=True)
class Achievement:
    key: str
    name: str
    description: str
    xp: int


ACHIEVEMENTS = {
    "product_hunch": Achievement(
        key="product_hunch",
        name="Product Hunch",
        description="Turn vague stakeholder pain into measurable product requirements.",
        xp=100,
    ),
    "data_intuition": Achievement(
        key="data_intuition",
        name="Data Intuition",
        description="Understand how expert-written questions point to groundtruth articles.",
        xp=150,
    ),
    "baseline_before_optimization": Achievement(
        key="baseline_before_optimization",
        name="Baseline Before Optimization",
        description="Complete Quest 1 with a measurable retrieval baseline and failed examples.",
        xp=250,
    ),
}

QUEST_1_COMPLETE_LEVEL = 2
QUEST_1_COMPLETE_TITLE = "Baseline Builder"


def unlock_achievement(key: str, path: Path = STATE_PATH) -> dict:
    if key not in ACHIEVEMENTS:
        raise KeyError(f"Unknown achievement: {key}")

    state = load_state(path)
    player = state.setdefault("player", {})
    achievements = player.setdefault("achievements", {})
    if not achievements.get(key):
        achievements[key] = True
        player["xp"] = int(player.get("xp", 0)) + ACHIEVEMENTS[key].xp
    save_state(state, path)
    return state


def complete_quest_1(path: Path = STATE_PATH) -> dict:
    state = unlock_achievement("baseline_before_optimization", path)
    player = state.setdefault("player", {})
    player["level"] = max(int(player.get("level", 1)), QUEST_1_COMPLETE_LEVEL)
    player["title"] = QUEST_1_COMPLETE_TITLE
    save_state(state, path)
    return state


def unlocked_achievements(state: dict) -> list[Achievement]:
    player = state.get("player", {})
    achievement_state = player.get("achievements", {})
    return [
        achievement
        for key, achievement in ACHIEVEMENTS.items()
        if bool(achievement_state.get(key))
    ]
