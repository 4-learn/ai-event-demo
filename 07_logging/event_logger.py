import csv
from pathlib import Path
from uuid import uuid4

CSV_PATH = Path(__file__).parent / "events.csv"
FIELDS = ["event_id", "zone", "started_at", "ended_at", "duration_seconds"]


def save_event(zone, started_at, ended_at):
    event = {
        "event_id": uuid4().hex,
        "zone": zone,
        "started_at": started_at.isoformat(timespec="milliseconds"),
        "ended_at": ended_at.isoformat(timespec="milliseconds"),
        "duration_seconds": round((ended_at - started_at).total_seconds(), 3),
    }
    needs_header = not CSV_PATH.exists() or CSV_PATH.stat().st_size == 0

    with CSV_PATH.open("a", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=FIELDS)
        if needs_header:
            writer.writeheader()
        writer.writerow(event)
