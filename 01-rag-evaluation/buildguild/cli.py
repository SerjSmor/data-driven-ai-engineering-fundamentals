from __future__ import annotations

from typing import Annotated

import typer

from buildguild.banner import print_banner
from buildguild.settings import player_settings
from buildguild.start import DIFFICULTIES, configure_player, print_difficulty_intro
from buildguild.status import print_status


app = typer.Typer(no_args_is_help=True)
run_app = typer.Typer(no_args_is_help=True)
app.add_typer(run_app, name="run")


@app.command()
def start(
    name: Annotated[str | None, typer.Option("--name", help="Player name.")] = None,
    difficulty: Annotated[
        str | None,
        typer.Option("--difficulty", help="Quest difficulty: easy, medium, or hard."),
    ] = None,
) -> None:
    """Start Quest 1 by choosing a player name and difficulty."""
    print_banner(compact=True)
    print_difficulty_intro()
    existing_settings = player_settings()
    chosen_name = name
    chosen_difficulty = difficulty

    if not chosen_name and not chosen_difficulty and existing_settings:
        existing_name = existing_settings.get("name")
        existing_difficulty = existing_settings.get("difficulty", "easy")
        use_existing = typer.confirm(
            f"Continue as {existing_name} on {existing_difficulty} difficulty?",
            default=True,
        )
        if use_existing:
            chosen_name = existing_name
            chosen_difficulty = existing_difficulty

    chosen_name = chosen_name or typer.prompt("Name")
    chosen_difficulty = chosen_difficulty or typer.prompt("Difficulty", default="easy")
    if chosen_difficulty.strip().lower() not in DIFFICULTIES:
        allowed = ", ".join(DIFFICULTIES)
        raise typer.BadParameter(f"Choose one of: {allowed}", param_hint="--difficulty")

    state = configure_player(name=chosen_name, difficulty=chosen_difficulty)
    player = state["player"]
    typer.echo(
        f"Quest setup complete: {player['name']} chose {player['difficulty']} difficulty."
    )
    typer.echo("Next: use skills/mike-data-onboarding.md")


@app.command()
def status() -> None:
    """Show the current quest stage and next action."""
    print_status()


@app.command()
def banner() -> None:
    """Show the Quest 1 opening screen."""
    print_banner()


@run_app.command("skill")
def run_skill(
    skill_name: str,
    quest: Annotated[str, typer.Option("--quest")],
) -> None:
    """Run a BuildGuild skill for a quest."""
    if quest != "quest-01":
        raise typer.BadParameter("Only quest-01 is available in this POC.", param_hint="--quest")

    if skill_name == "maya-tests-outputs":
        from buildguild.skills.maya_tests_outputs import run

        run()
        return

    raise typer.BadParameter(
        "Unknown skill. Available skills: maya-tests-outputs.",
        param_hint="skill_name",
    )


def main() -> None:
    app()


if __name__ == "__main__":
    main()
