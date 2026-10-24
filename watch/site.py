"""Build the static explorer site into _site/ (deployed to GitHub Pages).

    python -m watch.site            # then open _site/index.html via a local server:
    python -m http.server -d _site
"""

from __future__ import annotations

import json
import shutil
import sys
from datetime import timedelta

from .common import (DIGESTS_DIR, FEED_STATUS_FILE, ROOT, exclusion_rule, now_utc, read_items,
                     setup_logging, log)

WEB_DIR = ROOT / "web"
OUT_DIR = ROOT / "_site"
HISTORY_DAYS = 365


def build() -> None:
    if OUT_DIR.exists():
        shutil.rmtree(OUT_DIR)
    shutil.copytree(WEB_DIR, OUT_DIR)

    items = []
    for r in read_items(since=now_utc() - timedelta(days=HISTORY_DAYS)):
        kept = r["keep"] == "1"
        items.append({
            "id": r["id"],
            "date": (r["published"] or r["fetched_at"])[:10],
            "source": r["source"],
            "tier": int(r["tier"] or 2),
            "url": r["url"],
            "title": r["title"],
            "kept": kept,
            "category": r["category"],
            "sig": int(r["significance"] or 1),
            "story": r["story_key"],
            "summary": r["summary"],
            "why": r["why_it_matters"],
            "rule": "" if kept else exclusion_rule(r["exclusion_reason"]),
            "reason": "" if kept else r["exclusion_reason"],
        })
    items.sort(key=lambda x: x["date"], reverse=True)

    digests = []
    for path in sorted(DIGESTS_DIR.glob("20*.md"), reverse=True):
        digests.append({"date": path.stem, "markdown": path.read_text(encoding="utf-8")})

    payload = {
        "built": now_utc().isoformat(timespec="minutes"),
        "items": items,
        "digests": digests,
        "feed_status": FEED_STATUS_FILE.read_text(encoding="utf-8") if FEED_STATUS_FILE.exists() else "",
    }
    (OUT_DIR / "data.json").write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")
    log.info("site built: %d items, %d digests -> %s", len(items), len(digests), OUT_DIR)


if __name__ == "__main__":
    setup_logging()
    build()
    sys.exit(0)
