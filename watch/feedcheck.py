"""Check every configured source and write data/feed_status.md.

Runs as part of every ingest, and on its own via:
    python -m watch.feedcheck
No API key needed.
"""

from __future__ import annotations

import sys
from concurrent.futures import ThreadPoolExecutor
from datetime import timedelta

from .common import DATA_DIR, FEED_STATUS_FILE, load_sources, now_utc, setup_logging

STALE_DAYS = 120


def write_status(results) -> list[str]:
    """Write the status table; return the names of dead sources."""
    now = now_utc()
    dead, lines = [], []
    for res in sorted(results, key=lambda r: (r.ok, r.source["name"])):
        name = res.source["name"]
        if not res.ok:
            dead.append(name)
            lines.append(f"| ❌ | {name} | {res.error.replace('|', '/')} | | |")
            continue
        newest = res.newest.date().isoformat() if res.newest else "no dates"
        stale = res.newest is not None and now - res.newest > timedelta(days=STALE_DAYS)
        lines.append(f"| {'⚠️ stale' if stale else '✅'} | {name} | ok | {res.total} | {newest} |")
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    FEED_STATUS_FILE.write_text(
        f"# Feed status\n\nChecked {now:%Y-%m-%d %H:%M} UTC. "
        f"{len(results) - len(dead)}/{len(results)} sources reachable.\n\n"
        "| | Source | Status | Entries | Newest entry |\n|---|---|---|---|---|\n"
        + "\n".join(lines) + "\n",
        encoding="utf-8",
    )
    return dead


def dead_sources() -> list[str]:
    """Read back the dead sources from the last status file."""
    if not FEED_STATUS_FILE.exists():
        return []
    return [line.split("|")[2].strip() for line in FEED_STATUS_FILE.read_text().splitlines()
            if line.startswith("| ❌")]


def main() -> int:
    setup_logging()
    from .sources import fetch_source

    _, sources = load_sources()
    with ThreadPoolExecutor(8) as pool:
        results = list(pool.map(fetch_source, sources))
    dead = write_status(results)
    print(FEED_STATUS_FILE.read_text())
    return 1 if len(dead) == len(results) else 0


if __name__ == "__main__":
    sys.exit(main())
