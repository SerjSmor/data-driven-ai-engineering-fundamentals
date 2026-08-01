from __future__ import annotations

import argparse
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from buildguild.achievements import ACHIEVEMENTS
from buildguild.state import DEFAULT_STATE, load_state, save_state

CONFIRMATION = "RESET_QUEST_01"
ARI_CONFIRMATION = "RESET_ARI"
QUEST_OUTPUT_PATHS = [
    Path("analysis/article_type_frequency.csv"),
    Path("analysis/quest_01_product_requirements.md"),
    Path("analysis/quest_01_implementation_spec.md"),
    Path("analysis/baseline_report.md"),
    Path("analysis/quest_01_eda.py"),
    Path("analysis/quest_01_eda.ipynb"),
    Path("analysis/quest_01_eda.md"),
    Path("analysis/rag.py"),
    Path("analysis/ask.py"),
    Path("analysis/run_baseline.py"),
    Path("analysis/metrics.py"),
    Path("analysis/test_baseline_evaluation.py"),
]
ARI_OUTPUT_PATHS = [
    Path("analysis/quest_01_implementation_spec.md"),
    Path("analysis/baseline_report.md"),
    Path("analysis/quest_01_eda.py"),
    Path("analysis/quest_01_eda.ipynb"),
    Path("analysis/quest_01_eda.md"),
    Path("analysis/rag.py"),
    Path("analysis/ask.py"),
    Path("analysis/run_baseline.py"),
    Path("analysis/metrics.py"),
    Path("analysis/test_baseline_evaluation.py"),
]
EMPTY_OUTPUT_DIRS = [
    Path("analysis"),
]


def restart_quest(root: Path = ROOT) -> list[Path]:
    removed = remove_outputs(QUEST_OUTPUT_PATHS, root)
    remove_empty_output_dirs(root, removed)
    save_state(DEFAULT_STATE, root / ".buildguild" / "state.json")
    return removed


def restart_ari(root: Path = ROOT) -> list[Path]:
    removed = remove_outputs(ARI_OUTPUT_PATHS, root)
    remove_empty_output_dirs(root, removed)

    state_path = root / ".buildguild" / "state.json"
    state = load_state(state_path)
    quest = state.setdefault("quest_01", {})
    quest["implementation_spec_completed"] = False
    quest["maya_report_review_passed"] = False

    player = state.setdefault("player", {})
    achievements = player.setdefault("achievements", {})
    achievements["data_intuition"] = False
    achievements["baseline_before_optimization"] = False
    player["level"] = 1
    player["title"] = "New Builder"
    player["xp"] = sum(
        achievement.xp
        for key, achievement in ACHIEVEMENTS.items()
        if bool(achievements.get(key))
    )
    save_state(state, state_path)
    return removed


def remove_outputs(output_paths: list[Path], root: Path) -> list[Path]:
    removed: list[Path] = []
    for relative_path in output_paths:
        path = root / relative_path
        if path.exists():
            path.unlink()
            removed.append(relative_path)
    return removed


def remove_empty_output_dirs(root: Path, removed: list[Path]) -> None:
    for relative_path in EMPTY_OUTPUT_DIRS:
        path = root / relative_path
        if path.exists() and path.is_dir() and not any(path.iterdir()):
            path.rmdir()
            removed.append(relative_path)


def main() -> None:
    parser = argparse.ArgumentParser(description="Reset BuildGuild Quest 1 outputs and state.")
    parser.add_argument(
        "--stage",
        choices=("quest", "ari"),
        default="quest",
        help="Reset the whole quest or only Ari's EDA/spec stage and downstream outputs.",
    )
    parser.add_argument(
        "--confirm",
        required=True,
        help=f"Required confirmation token. Use {CONFIRMATION} for --stage quest or {ARI_CONFIRMATION} for --stage ari.",
    )
    args = parser.parse_args()

    expected_confirmation = ARI_CONFIRMATION if args.stage == "ari" else CONFIRMATION
    if args.confirm != expected_confirmation:
        raise SystemExit(f"Refusing to reset. Pass --confirm {expected_confirmation}")

    if args.stage == "ari":
        removed = restart_ari()
        print("Ari stage reset complete.")
        print("Preserved: Mike onboarding, Maya product discovery, and player settings.")
        print("State reset: quest_01.implementation_spec_completed=false")
        print("State reset: quest_01.maya_report_review_passed=false")
    else:
        removed = restart_quest()
        print("Quest 1 reset complete.")
        print("State reset: .buildguild/state.json")
        print("Settings preserved: .buildguild/settings.json")
    if removed:
        print("Removed:")
        for path in removed:
            print(f"- {path}")
    else:
        print("No quest output files were present.")


if __name__ == "__main__":
    main()
