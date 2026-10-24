"""Shared helpers: paths, config, item storage."""

from __future__ import annotations

import csv
import hashlib
import logging
import re
from datetime import datetime, timedelta, timezone
from pathlib import Path
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit

import yaml

ROOT = Path(__file__).resolve().parent.parent
CONFIG_DIR = ROOT / "config"
DATA_DIR = ROOT / "data"
ITEMS_DIR = DATA_DIR / "items"
DIGESTS_DIR = ROOT / "digests"
FEATURED_FILE = DATA_DIR / "featured.txt"
FEED_STATUS_FILE = DATA_DIR / "feed_status.md"

USER_AGENT = "ai-bi-watch/0.1 (personal news monitor; +https://github.com/jeanremy-berard/ai-bi-watch)"

CATEGORIES = [
    "ai_releases",
    "ai_engineering",
    "ai_research",
    "bi_microsoft",
    "bi_market",
    "bi_practice",
    "access_licensing",
    "none",
]

EXCLUSION_RULES = [
    "kept",
    "funding or business news",
    "minor feature",
    "marketing or case study",
    "tutorial or listicle",
    "societal debate or opinion",
    "regulation without direct impact",
    "event or webinar",
    "safety research",
    "off-topic",
    "low significance",
    "other",
]

_LEGACY_RULES = [  # free-text reasons written before exclusion_rule existed
    ("funding or business news", ("funding", "ipo", "valuation", "acquisition", "hiring", "executive", "governance", "philanthrop")),
    ("marketing or case study", ("marketing", "case study", "customer", "partner", "promo")),
    ("minor feature", ("minor", "small", "ui tweak", "incremental")),
    ("tutorial or listicle", ("tutorial", "how-to", "listicle", "beginner")),
    ("societal debate or opinion", ("societal", "debate", "opinion", "ethic", "politic", "philosoph")),
    ("regulation without direct impact", ("regulat", "policy", "legislat")),
    ("event or webinar", ("event", "webinar", "conference", "recap")),
    ("safety research", ("safety", "alignment")),
    ("off-topic", ("off-topic", "off topic", "unrelated", "not relevant")),
    ("low significance", ("significance", "threshold", "marginal")),
]


def exclusion_rule(reason: str) -> str:
    """Map a stored exclusion_reason to one of EXCLUSION_RULES."""
    head = (reason or "").split(":", 1)[0].strip().lower()
    if head in EXCLUSION_RULES:
        return head
    text = (reason or "").lower()
    for rule, keys in _LEGACY_RULES:
        if any(k in text for k in keys):
            return rule
    return "other"


ITEM_FIELDS = [
    "id",
    "fetched_at",
    "published",
    "source",
    "tier",
    "group",
    "url",
    "title",
    "keep",
    "category",
    "significance",
    "story_key",
    "summary",
    "why_it_matters",
    "exclusion_reason",
    "text_chars",
    "model",
]

log = logging.getLogger("watch")


def setup_logging() -> None:
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")


def now_utc() -> datetime:
    return datetime.now(timezone.utc)


def load_sources() -> tuple[dict, list[dict]]:
    cfg = yaml.safe_load((CONFIG_DIR / "sources.yaml").read_text(encoding="utf-8"))
    sources = [s for s in cfg["sources"] if s.get("enabled", True)]
    names = [s["name"] for s in sources]
    dupes = {n for n in names if names.count(n) > 1}
    if dupes:
        raise ValueError(f"Duplicate source names: {dupes}")
    return cfg["settings"], sources


def load_profile() -> str:
    return (CONFIG_DIR / "profile.md").read_text(encoding="utf-8")


_TRACKING_PARAMS = re.compile(r"^(utm_|mc_|ref$|ref_src$|source$|fbclid$|gclid$)")


def normalize_url(url: str) -> str:
    """Strip tracking parameters and fragments so the same article dedupes."""
    parts = urlsplit(url.strip())
    query = [(k, v) for k, v in parse_qsl(parts.query) if not _TRACKING_PARAMS.match(k)]
    path = parts.path.rstrip("/") or "/"
    return urlunsplit((parts.scheme.lower(), parts.netloc.lower(), path, urlencode(query), ""))


def item_id(url: str) -> str:
    return hashlib.sha1(normalize_url(url).encode("utf-8")).hexdigest()[:16]


def month_file(dt: datetime) -> Path:
    return ITEMS_DIR / f"{dt:%Y-%m}.csv"


def read_items(since: datetime | None = None) -> list[dict]:
    """Read stored items, optionally only those fetched since a date."""
    rows: list[dict] = []
    if not ITEMS_DIR.exists():
        return rows
    for path in sorted(ITEMS_DIR.glob("*.csv")):
        if since is not None:
            # skip whole months that end before `since`
            y, m = map(int, path.stem.split("-"))
            month_end = datetime(y + (m == 12), m % 12 + 1, 1, tzinfo=timezone.utc)
            if month_end < since:
                continue
        with path.open(newline="", encoding="utf-8") as f:
            for row in csv.DictReader(f):
                if since is None or parse_iso(row["fetched_at"]) >= since:
                    rows.append(row)
    return rows


def seen_ids(days: int = 62) -> set[str]:
    return {r["id"] for r in read_items(since=now_utc() - timedelta(days=days))}


def append_items(items: list[dict]) -> None:
    ITEMS_DIR.mkdir(parents=True, exist_ok=True)
    by_file: dict[Path, list[dict]] = {}
    for it in items:
        by_file.setdefault(month_file(parse_iso(it["fetched_at"])), []).append(it)
    for path, rows in by_file.items():
        new = not path.exists()
        with path.open("a", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=ITEM_FIELDS, extrasaction="ignore")
            if new:
                w.writeheader()
            w.writerows(rows)


def parse_iso(s: str) -> datetime:
    dt = datetime.fromisoformat(s)
    return dt if dt.tzinfo else dt.replace(tzinfo=timezone.utc)


def read_featured() -> set[str]:
    if not FEATURED_FILE.exists():
        return set()
    return {line.split()[0] for line in FEATURED_FILE.read_text().splitlines() if line.strip()}


def add_featured(ids: list[str], date: str) -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    with FEATURED_FILE.open("a", encoding="utf-8") as f:
        for i in ids:
            f.write(f"{i} {date}\n")
