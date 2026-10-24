"""Daily run: fetch sources, triage new items, append them to data/items/YYYY-MM.csv.

Usage:
    python -m watch.ingest             # needs ANTHROPIC_API_KEY
    python -m watch.ingest --dry-run   # no API calls, keeps everything (for testing)
"""

from __future__ import annotations

import argparse
import os
import sys
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed

import anthropic

from . import classify as clf
from .common import (ITEMS_DIR, append_items, item_id, load_profile, load_sources, log,
                     now_utc, seen_ids, setup_logging)
from .extract import fetch_fulltext
from .feedcheck import write_status
from .sources import fetch_source, select_new, window_start

WORKERS = 6
MAX_CONSECUTIVE_FAILURES = 8


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true", help="no API calls, no full-text fetch")
    ap.add_argument("--limit", type=int, default=0, help="max items to triage (testing)")
    args = ap.parse_args(argv)
    setup_logging()

    settings, sources = load_sources()
    profile = load_profile()
    first_run = not any(ITEMS_DIR.glob("*.csv"))
    since = window_start(settings, first_run)
    seen = seen_ids()
    log.info("%d sources, window since %s%s, %d known items", len(sources), since.date(),
             " (first run)" if first_run else "", len(seen))

    # 1. fetch all feeds in parallel
    with ThreadPoolExecutor(WORKERS) as pool:
        results = list(pool.map(fetch_source, sources))
    write_status(results)
    candidates = []
    batch_ids: set[str] = set()
    for res in results:
        if not res.ok:
            log.warning("FEED DOWN %s: %s", res.source["name"], res.error)
            continue
        for e in select_new(res, settings, seen | batch_ids, since, item_id):
            batch_ids.add(item_id(e.url))
            candidates.append(e)
    if args.limit:
        candidates = candidates[: args.limit]
    log.info("%d new candidate items", len(candidates))
    if not candidates:
        return 0

    # 2. full text + triage
    client = None
    if not args.dry_run:
        if not os.environ.get("ANTHROPIC_API_KEY"):
            log.error("ANTHROPIC_API_KEY is not set (add it as a repository secret)")
            return 1
        client = anthropic.Anthropic(max_retries=4)
    model = settings["classify_model"]
    min_chars = int(settings.get("fulltext_min_chars", 1500))
    max_chars = int(settings.get("fulltext_max_chars", 8000))
    failures = {"consecutive": 0}
    lock = threading.Lock()
    abort = threading.Event()

    def work(entry):
        if abort.is_set():
            return None
        text = entry.text
        if not args.dry_run and len(text) < min_chars:
            full = fetch_fulltext(entry.url, max_chars)
            if len(full) > len(text):
                text = full
        text = text[:max_chars]
        if args.dry_run:
            verdict = clf.heuristic(entry, text)
        else:
            verdict = clf.safe_classify(client, model, profile, entry, text)
        with lock:
            if verdict is None:
                failures["consecutive"] += 1
                if failures["consecutive"] >= MAX_CONSECUTIVE_FAILURES:
                    abort.set()
                return None
            failures["consecutive"] = 0
        return {
            "id": item_id(entry.url),
            "fetched_at": now_utc().isoformat(timespec="seconds"),
            "published": entry.published.isoformat(timespec="seconds") if entry.published else "",
            "source": entry.source,
            "tier": entry.tier,
            "group": entry.group,
            "url": entry.url,
            "title": entry.title,
            "keep": "1" if verdict["keep"] else "0",
            "category": verdict["category"],
            "significance": verdict["significance"],
            "story_key": verdict["story_key"],
            "summary": verdict["summary"],
            "why_it_matters": verdict["why_it_matters"],
            "exclusion_reason": verdict["exclusion_reason"],
            "text_chars": len(text),
            "model": "dry-run" if args.dry_run else model,
        }

    rows = []
    with ThreadPoolExecutor(WORKERS) as pool:
        futures = [pool.submit(work, e) for e in candidates]
        for fut in as_completed(futures):
            try:
                row = fut.result()
            except anthropic.APIStatusError as exc:  # auth problems: stop everything
                abort.set()
                log.error("API error, aborting: %s %s", exc.status_code, exc.message)
                continue
            if row:
                rows.append(row)

    rows.sort(key=lambda r: (r["source"], r["published"]))
    append_items(rows)
    kept = sum(r["keep"] == "1" for r in rows)
    log.info("stored %d items (%d kept, %d dropped)", len(rows), kept, len(rows) - kept)
    if abort.is_set():
        log.error("aborted after repeated API failures (check the key and the credit balance)")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
