from __future__ import annotations

from pathlib import Path

from rich.console import Console

from buildguild.settings import SETTINGS_PATH, save_settings
from buildguild.state import STATE_PATH, load_state, save_state


DIFFICULTIES = ("easy", "medium", "hard")


def configure_player(
    *,
    name: str,
    difficulty: str = "easy",
    path: Path = STATE_PATH,
) -> dict:
    normalized_name = name.strip()
    normalized_difficulty = difficulty.strip().lower()

    if not normalized_name:
        raise ValueError("Player name is required.")
    if normalized_difficulty not in DIFFICULTIES:
        allowed = ", ".join(DIFFICULTIES)
        raise ValueError(f"Difficulty must be one of: {allowed}.")

    state = load_state(path)
    player = state.setdefault("player", {})
    player["name"] = normalized_name
    player["difficulty"] = normalized_difficulty
    player["setup_completed"] = True
    save_state(state, path)
    save_settings(name=normalized_name, difficulty=normalized_difficulty, path=SETTINGS_PATH)
    return state


def print_difficulty_intro(console: Console | None = None) -> None:
    console = console or Console()
    console.print("[bold cyan]What is your name, brave adventurer?[/bold cyan]")
    console.print("[bold cyan]How much guidance do you want on this quest?[/bold cyan]")
    console.print("[green]easy[/green]   - Apprentice mode: direct hints, clear nudges, and frequent check-ins.")
    console.print("[yellow]medium[/yellow] - Builder mode: fewer hints; you drive the investigation.")
    console.print("[red]hard[/red]   - Expert mode: minimal spoon-feeding. Beware: the dungeon may distract you from the clean path.")
