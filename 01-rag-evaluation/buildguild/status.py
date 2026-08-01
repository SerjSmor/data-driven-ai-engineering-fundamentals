from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from rich.console import Console

from buildguild.achievements import unlocked_achievements
from buildguild.onboarding import (
    ARTICLE_TYPE_FREQUENCY_PATH,
    article_type_frequency_is_valid,
)
from buildguild.settings import player_settings
from buildguild.state import load_state


QUEST_KEY = "quest_01"
PRODUCT_REQUIREMENTS_PATH = Path("analysis/quest_01_product_requirements.md")
IMPLEMENTATION_SPEC_PATH = Path("analysis/quest_01_implementation_spec.md")
REPORT_PATH = Path("analysis/baseline_report.md")
IMPLEMENTATION_FILES = [
    Path("analysis/ask.py"),
    Path("analysis/rag.py"),
    Path("app/retrieval.py"),
    Path("app/chatbot.py"),
    Path("analysis/run_baseline.py"),
    Path("analysis/metrics.py"),
]


@dataclass(frozen=True)
class Status:
    stage: str
    completed: list[str]
    missing: list[str]
    next_action: str
    player_name: str | None
    player_difficulty: str
    player_level: int
    player_title: str
    player_xp: int
    achievements: list[str]


def inspect_status() -> Status:
    state = load_state()
    quest = state.get(QUEST_KEY, {})
    player = state.get("player", {})
    settings_player = player_settings()

    setup_done = bool(player.get("setup_completed"))
    customer_pain_onboarding_done = bool(quest.get("customer_pain_onboarding_completed"))
    article_type_frequency_valid = article_type_frequency_is_valid()
    onboarding_done = bool(quest.get("product_onboarding_completed"))
    product_requirements_found = PRODUCT_REQUIREMENTS_PATH.exists()
    implementation_spec_found = IMPLEMENTATION_SPEC_PATH.exists()
    implementation_spec_completed = bool(quest.get("implementation_spec_completed"))
    implementation_complete = all(path.exists() for path in IMPLEMENTATION_FILES)
    report_found = REPORT_PATH.exists()
    maya_report_review_passed = bool(quest.get("maya_report_review_passed"))

    completed: list[str] = []
    missing: list[str] = []

    _record(completed, missing, setup_done, "Player setup completed")
    _record(completed, missing, customer_pain_onboarding_done, "Mike data onboarding completed")
    _record(
        completed,
        missing,
        article_type_frequency_valid,
        "Article type frequency CSV valid",
    )
    _record(completed, missing, onboarding_done, "Product onboarding completed")
    _record(completed, missing, product_requirements_found, "Product requirements found")
    _record(completed, missing, implementation_spec_found, "Implementation spec found")
    _record(completed, missing, implementation_spec_completed, "Implementation spec completed")
    _record(completed, missing, implementation_complete, "Baseline implementation detected")
    _record(completed, missing, report_found, "Baseline report found")
    _record(completed, missing, maya_report_review_passed, "Maya report review passed")

    player_name = player.get("name") or settings_player.get("name")
    if player_name is not None:
        player_name = str(player_name)
    player_difficulty = str(player.get("difficulty") or settings_player.get("difficulty", "easy"))
    player_level = int(player.get("level", 1))
    player_title = str(player.get("title", "New Builder"))
    player_xp = int(player.get("xp", 0))
    achievement_names = [achievement.name for achievement in unlocked_achievements(state)]

    if not setup_done:
        return Status(
            stage="Quest setup",
            completed=completed,
            missing=missing,
            next_action="Run: uv run buildguild start",
            player_name=player_name,
            player_difficulty=player_difficulty,
            player_level=player_level,
            player_title=player_title,
            player_xp=player_xp,
            achievements=achievement_names,
        )

    if not customer_pain_onboarding_done or not article_type_frequency_valid:
        return Status(
            stage="Mike data onboarding",
            completed=completed,
            missing=missing,
            next_action=f"Ask your coding agent to use skills/mike-data-onboarding.md and create {ARTICLE_TYPE_FREQUENCY_PATH}.",
            player_name=player_name,
            player_difficulty=player_difficulty,
            player_level=player_level,
            player_title=player_title,
            player_xp=player_xp,
            achievements=achievement_names,
        )

    if not onboarding_done or not product_requirements_found:
        return Status(
            stage="Product discovery",
            completed=completed,
            missing=missing,
            next_action="Ask your coding agent to use skills/maya-product-lead.md, complete the four discovery checkboxes, and create analysis/quest_01_product_requirements.md.",
            player_name=player_name,
            player_difficulty=player_difficulty,
            player_level=player_level,
            player_title=player_title,
            player_xp=player_xp,
            achievements=achievement_names,
        )
    if not implementation_spec_found or not implementation_spec_completed:
        return Status(
            stage="Tour data and write implementation spec",
            completed=completed,
            missing=missing,
            next_action="Ask your coding agent to use skills/ari-data-guide.md, inspect the dataset, and create analysis/quest_01_implementation_spec.md with a Data Tour Findings section.",
            player_name=player_name,
            player_difficulty=player_difficulty,
            player_level=player_level,
            player_title=player_title,
            player_xp=player_xp,
            achievements=achievement_names,
        )
    if not implementation_complete:
        return Status(
            stage="Implement baseline evaluation",
            completed=completed,
            missing=missing,
            next_action='Implement: python analysis/ask.py "How do I connect a domain?" and python analysis/run_baseline.py',
            player_name=player_name,
            player_difficulty=player_difficulty,
            player_level=player_level,
            player_title=player_title,
            player_xp=player_xp,
            achievements=achievement_names,
        )
    if not report_found:
        return Status(
            stage="Run baseline evaluation",
            completed=completed,
            missing=missing,
            next_action="Run: python analysis/run_baseline.py",
            player_name=player_name,
            player_difficulty=player_difficulty,
            player_level=player_level,
            player_title=player_title,
            player_xp=player_xp,
            achievements=achievement_names,
        )
    if not maya_report_review_passed:
        return Status(
            stage="Maya report review",
            completed=completed,
            missing=missing,
            next_action="Ask your coding agent to use skills/maya-tests-outputs.md so Maya can review analysis/baseline_report.md.",
            player_name=player_name,
            player_difficulty=player_difficulty,
            player_level=player_level,
            player_title=player_title,
            player_xp=player_xp,
            achievements=achievement_names,
        )
    return Status(
        stage="Quest complete",
        completed=completed,
        missing=missing,
        next_action="Quest 1 complete. Quest 2 is not available yet; watch the repo for updates.",
        player_name=player_name,
        player_difficulty=player_difficulty,
        player_level=player_level,
        player_title=player_title,
        player_xp=player_xp,
        achievements=achievement_names,
    )


def print_status(console: Console | None = None) -> None:
    console = console or Console()
    status = inspect_status()
    console.print("[bold]BuildGuild Status[/bold]")
    console.print("Current quest:")
    console.print("Quest 1 - The Bot Works. Nobody Knows If It Is Good.")
    console.print(f"Stage: {status.stage}")
    console.print("Progress:")
    for item in status.completed:
        console.print(f"\\[x] {item}")
    for item in status.missing:
        console.print(f"\\[ ] {item}")
    console.print("Player:")
    if status.player_name:
        console.print(f"Name: {status.player_name}")
    console.print(f"Difficulty: {status.player_difficulty}")
    console.print(f"Level {status.player_level} - {status.player_title} ({status.player_xp} XP)")
    if status.achievements:
        console.print("Achievements:")
        for achievement in status.achievements:
            console.print(f"\\[x] {achievement}")
    console.print("Next action:")
    console.print(status.next_action)


def _record(completed: list[str], missing: list[str], condition: bool, label: str) -> None:
    if condition:
        completed.append(label)
    else:
        missing.append(label)
