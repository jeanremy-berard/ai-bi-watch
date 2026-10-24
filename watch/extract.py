"""Full-text extraction for entries whose feed only carries a teaser."""

from __future__ import annotations

import requests
import trafilatura

from .common import USER_AGENT, log

TIMEOUT = 20


def fetch_fulltext(url: str, max_chars: int) -> str:
    """Return the main text of the page, or "" on any failure (never raises)."""
    if "arxiv.org/abs/" in url:
        return ""  # abstract from the API is what we want; the page adds nothing
    try:
        r = requests.get(url, headers={"User-Agent": USER_AGENT}, timeout=TIMEOUT)
        r.raise_for_status()
        if "html" not in r.headers.get("content-type", "html"):
            return ""
        text = trafilatura.extract(r.text, include_comments=False, include_tables=False,
                                   favor_precision=True) or ""
    except Exception as exc:
        log.info("fulltext failed for %s: %s", url, type(exc).__name__)
        return ""
    return text[:max_chars]
