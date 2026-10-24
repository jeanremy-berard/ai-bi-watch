"""Fetch candidate entries from the configured sources."""

from __future__ import annotations

import calendar
import html
import re
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone

import feedparser
import requests

from .common import USER_AGENT, log, normalize_url

TIMEOUT = 25


@dataclass
class Entry:
    source: str
    tier: int
    group: str
    url: str
    title: str
    text: str            # whatever text the feed provides (cleaned)
    published: datetime | None


@dataclass
class FetchResult:
    source: dict
    ok: bool
    entries: list[Entry]
    error: str = ""
    newest: datetime | None = None
    total: int = 0       # entries in the feed before filtering


_TAG = re.compile(r"<[^>]+>")
_WS = re.compile(r"\s+")


def clean_html(s: str) -> str:
    return _WS.sub(" ", html.unescape(_TAG.sub(" ", s or ""))).strip()


def _entry_date(e) -> datetime | None:
    for key in ("published_parsed", "updated_parsed", "created_parsed"):
        t = e.get(key)
        if t:
            return datetime.fromtimestamp(calendar.timegm(t), tz=timezone.utc)
    return None


def _entry_text(e) -> str:
    parts = []
    for c in e.get("content") or []:
        parts.append(c.get("value", ""))
    if not parts:
        parts.append(e.get("summary", ""))
    return clean_html(" ".join(parts))


BROWSER_UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
              "(KHTML, like Gecko) Chrome/130.0 Safari/537.36")


def _get(url: str) -> requests.Response:
    r = requests.get(url, headers={"User-Agent": USER_AGENT}, timeout=TIMEOUT)
    if r.status_code == 403:
        # some hosts (e.g. *.substack.com) refuse non-browser user agents
        r = requests.get(url, headers={"User-Agent": BROWSER_UA,
                                       "Accept": "application/rss+xml, application/xml;q=0.9, */*;q=0.8"},
                         timeout=TIMEOUT)
    r.raise_for_status()
    return r


def fetch_rss(src: dict) -> FetchResult:
    try:
        resp = _get(src["url"])
    except Exception as exc:  # network, HTTP status
        return FetchResult(src, False, [], error=f"{type(exc).__name__}: {exc}"[:200])
    feed = feedparser.parse(resp.content)
    if not feed.entries:
        why = "no entries"
        if feed.bozo:
            why += f" (parse error: {feed.bozo_exception})"
        return FetchResult(src, False, [], error=why[:200])
    entries = []
    for e in feed.entries:
        link = e.get("link") or ""
        if not link.startswith("http"):
            continue
        entries.append(
            Entry(
                source=src["name"],
                tier=int(src.get("tier", 2)),
                group=src.get("group", ""),
                url=normalize_url(link),
                title=clean_html(e.get("title", "")),
                text=_entry_text(e),
                published=_entry_date(e),
            )
        )
    dates = [x.published for x in entries if x.published]
    return FetchResult(src, True, entries, newest=max(dates) if dates else None, total=len(entries))


def fetch_hf_papers(src: dict) -> FetchResult:
    try:
        data = _get(src["url"]).json()
    except Exception as exc:
        return FetchResult(src, False, [], error=f"{type(exc).__name__}: {exc}"[:200])
    min_up = int(src.get("min_upvotes", 0))
    entries = []
    for row in data:
        paper = row.get("paper") or {}
        pid = paper.get("id")
        if not pid:
            continue
        upvotes = int(paper.get("upvotes") or 0)
        if upvotes < min_up:
            continue
        published = row.get("publishedAt") or paper.get("publishedAt")
        try:
            pub_dt = datetime.fromisoformat(published.replace("Z", "+00:00")) if published else None
        except ValueError:
            pub_dt = None
        abstract = paper.get("summary") or row.get("summary") or ""
        orgs = paper.get("organization", {}) or {}
        org = orgs.get("fullname") or orgs.get("name") or ""
        text = f"[{upvotes} upvotes on Hugging Face daily papers{', ' + org if org else ''}] {abstract}"
        entries.append(
            Entry(
                source=src["name"],
                tier=int(src.get("tier", 3)),
                group=src.get("group", "ai_research"),
                url=f"https://arxiv.org/abs/{pid}",
                title=clean_html(row.get("title") or paper.get("title", "")),
                text=clean_html(text),
                published=pub_dt,
            )
        )
    entries.sort(key=lambda x: -int(re.search(r"\[(\d+) upvotes", x.text).group(1)))
    dates = [x.published for x in entries if x.published]
    return FetchResult(src, True, entries, newest=max(dates) if dates else None, total=len(data))


def fetch_source(src: dict) -> FetchResult:
    kind = src.get("type", "rss")
    if kind == "hf_papers":
        return fetch_hf_papers(src)
    return fetch_rss(src)


def select_new(result: FetchResult, settings: dict, seen: set[str], since: datetime,
               id_fn) -> list[Entry]:
    """Apply date window, include-regex prefilter, dedupe and per-source cap."""
    src = result.source
    include = [re.compile(p, re.I) for p in src.get("include", [])]
    cap = int(src.get("max_items", settings.get("max_items_per_source", 15)))
    picked: list[Entry] = []
    for e in result.entries:
        if e.published and e.published < since:
            continue
        if include and not any(p.search(f"{e.title} {e.text[:2000]}") for p in include):
            continue
        if id_fn(e.url) in seen:
            continue
        picked.append(e)
        if len(picked) >= cap:
            break
    if result.entries and not any(e.published for e in result.entries):
        log.info("%s: feed has no dates, relying on dedupe + cap", src["name"])
    return picked


def window_start(settings: dict, first_run: bool) -> datetime:
    days = settings.get("bootstrap_days", 7) if first_run else settings.get("lookback_days", 3)
    return datetime.now(timezone.utc) - timedelta(days=int(days))
