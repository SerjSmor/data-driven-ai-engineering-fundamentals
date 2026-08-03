#!/usr/bin/env python3
import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load(path):
    return json.loads(path.read_text(encoding="utf-8"))


def save(path, value):
    path.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8")


def main():
    parser = argparse.ArgumentParser(description="Mark BuildGuild work ready for judgment.")
    parser.add_argument("task_id", nargs="?")
    parser.add_argument("--milestone")
    parser.add_argument("--all", action="store_true")
    parser.add_argument("--notes", default="")
    args = parser.parse_args()
    if sum(bool(x) for x in (args.task_id, args.milestone, args.all)) != 1:
        raise SystemExit("Pass exactly one task id, --milestone, or --all.")

    challenge = load(ROOT / "challenge.json")
    progress = load(ROOT / "progress.json")
    milestones = {item["id"]: item for item in challenge["milestones"]}
    if args.all:
        ids = [t["id"] for m in challenge["milestones"] for t in m["tasks"] if not t.get("optional")]
    elif args.milestone:
        if args.milestone not in milestones:
            raise SystemExit(f"Unknown milestone: {args.milestone}")
        ids = [t["id"] for t in milestones[args.milestone]["tasks"] if not t.get("optional")]
    else:
        ids = [args.task_id]

    unknown = [task_id for task_id in ids if task_id not in progress["tasks"]]
    if unknown:
        raise SystemExit(f"Unknown task id: {', '.join(unknown)}")
    now = datetime.now(timezone.utc).isoformat()
    for task_id in ids:
        progress["tasks"][task_id].update(
            status="ready_for_judgment", builder_notes=args.notes, judge=None, ready_at=now
        )
    save(ROOT / "progress.json", progress)
    print(f"{len(ids)} task(s) ready_for_judgment: {', '.join(ids)}")


if __name__ == "__main__":
    main()
