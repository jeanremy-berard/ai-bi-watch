"""Weekly run: turn the week's kept items into a markdown digest in digests/.

Usage:
    python -m watch.digest              # needs ANTHROPIC_API_KEY
    python -m watch.digest --dry-run    # writes the model input instead of calling it
    python -m watch.digest --days 7     # window (default 7)
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from collections import Counter
from datetime import timedelta
from zoneinfo import ZoneInfo

import anthropic

from .common import (DIGESTS_DIR, add_featured, exclusion_rule, load_profile, load_sources,
                     log, now_utc, read_featured, read_items, setup_logging)
from .feedcheck import dead_sources

SECTION_ORDER = [
    ("access_licensing", "Access & licensing"),
    ("ai_releases", "AI: releases & platforms"),
    ("ai_engineering", "AI: tooling & engineering"),
    ("bi_microsoft", "BI: Microsoft Fabric & Power BI"),
    ("bi_market", "BI: market"),
    ("ai_research", "Research corner"),
    ("bi_practice", "BI practice"),
]

INSTRUCTIONS = """You write a weekly AI & BI digest for one reader. The reader profile
below says who they are and what matters to them. The items were already triaged by a
smaller model; you now edit them into a digest that respects the reader's time.

Editing rules:
1. Group items about the same underlying event into one story (story_key helps but is
   not always consistent: use judgment). Several outlets covering a story is a signal of
   importance: say so ("covered by N sources").
2. You may demote or cut items the triage over-rated. Do not invent items or facts.
   Use only the URLs given in the input, exactly as given.
3. Order stories within each section by significance. Keep the digest scannable: a
   heavy week is still at most ~20 stories in total. Cut the weakest rather than pile up.
4. Research corner: at most 2 papers, popularized (what, why it might matter and when,
   how solid). BI practice: at most 3 reads; these can be a few weeks old.
5. Write plainly, no hype words, no exclamation marks. Never explain basics of data, BI
   or AI to this reader.

Output markdown with exactly this structure (omit a section entirely if it has no story):

# AI & BI Watch: week ending {date}

## This week in five lines
- (3 to 5 bullets: the most significant stories across all sections, one line each)

## <Section title>
### <Story title>
<2-4 sentence summary>
**Why it matters:** <one sentence for this reader>
<significance as ●●●○○ out of 5> · [<source name>](<url>) · [<source name>](<url>) (best source first; at most 3 links; add "covered by N sources" when N > 1)

Section titles, in this order: {sections}

<reader_profile>
{profile}
</reader_profile>"""


def collect(days: int, practice_days: int) -> tuple[list[dict], list[dict], list[dict]]:
    now = now_utc()
    week = read_items(since=now - timedelta(days=days))
    featured = read_featured()
    kept = [r for r in week if r["keep"] == "1" and r["category"] != "bi_practice"]
    practice = [r for r in read_items(since=now - timedelta(days=practice_days))
                if r["keep"] == "1" and r["category"] == "bi_practice" and r["id"] not in featured]
    return week, kept, practice


def model_input(kept: list[dict], practice: list[dict]) -> str:
    lines = []
    for r in sorted(kept + practice, key=lambda r: (-int(r["significance"]), r["category"])):
        lines.append(json.dumps({
            "category": r["category"],
            "significance": int(r["significance"]),
            "story_key": r["story_key"],
            "source": r["source"],
            "source_tier": int(r["tier"]),
            "published": r["published"][:10],
            "url": r["url"],
            "title": r["title"],
            "summary": r["summary"],
            "why_it_matters": r["why_it_matters"],
        }, ensure_ascii=False))
    return "Items (one JSON object per line):\n" + "\n".join(lines)


def footer(week: list[dict], kept: list[dict], practice: list[dict], dead: list[str]) -> str:
    dropped = [r for r in week if r["keep"] != "1"]
    reasons = Counter(exclusion_rule(r["exclusion_reason"]) for r in dropped)
    borderline = sorted((r for r in dropped if int(r["significance"] or 0) >= 3),
                        key=lambda r: -int(r["significance"]))[:15]
    out = ["\n---\n", "## Under the hood\n",
           f"{len(week)} items triaged this week, {len(kept)} kept"
           f" (+{len(practice)} BI practice reads in the pool), {len(dropped)} dropped.\n"]
    if reasons:
        out.append("Top drop reasons: " + ", ".join(f"{k} ({v})" for k, v in reasons.most_common(6)) + ".\n")
    if borderline:
        out.append("\n<details><summary>Borderline drops (significance ≥ 3 but excluded): "
                   "check these to calibrate the filter</summary>\n")
        for r in borderline:
            out.append(f"- [{r['title']}]({r['url']}) · {r['source']} · "
                       f"sig {r['significance']} · {r['exclusion_reason']}")
        out.append("\n</details>\n")
    if dead:
        out.append(f"\n⚠️ Feeds unreachable at last check: {', '.join(dead)}. "
                   "See data/feed_status.md.\n")
    return "\n".join(out)


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--days", type=int, default=7)
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args(argv)
    setup_logging()

    settings, _ = load_sources()
    week, kept, practice = collect(args.days, int(settings.get("practice_window_days", 28)))
    today = week_ending()
    DIGESTS_DIR.mkdir(parents=True, exist_ok=True)
    out_path = DIGESTS_DIR / f"{today}.md"
    log.info("%d items this week, %d kept, %d practice candidates", len(week), len(kept), len(practice))

    if not kept and not practice:
        body = f"# AI & BI Watch: week ending {today}\n\nNothing passed the filter this week.\n"
    else:
        system = (INSTRUCTIONS.replace("{profile}", load_profile())
                  .replace("{date}", today)
                  .replace("{sections}", "; ".join(t for _, t in SECTION_ORDER)))
        user = model_input(kept, practice)
        if args.dry_run:
            body = f"<!-- dry run: model input below -->\n\n```\n{user}\n```\n"
        else:
            if not os.environ.get("ANTHROPIC_API_KEY"):
                log.error("ANTHROPIC_API_KEY is not set")
                return 1
            client = anthropic.Anthropic(max_retries=4)
            resp = client.messages.create(
                model=settings["digest_model"],
                max_tokens=16000,
                system=system,
                messages=[{"role": "user", "content": user}],
            )
            body = "".join(b.text for b in resp.content if b.type == "text").strip() + "\n"
            log.info("digest tokens: in %d, out %d", resp.usage.input_tokens, resp.usage.output_tokens)
            check_links(body, kept + practice)

    body += footer(week, kept, practice, dead_sources())
    out_path.write_text(body, encoding="utf-8")
    (DIGESTS_DIR / "latest.md").write_text(body, encoding="utf-8")
    if not args.dry_run:
        add_featured([r["id"] for r in practice if r["url"] in body], today)
    log.info("wrote %s", out_path)
    return 0


def week_ending() -> str:
    """Label digests by the Saturday they are meant for (Paris time).

    The scheduled run starts on Friday evening because GitHub fires scheduled
    workflows hours late; a run on Friday must still be labelled Saturday.
    """
    local = now_utc().astimezone(ZoneInfo("Europe/Paris")).date()
    return (local + timedelta(days=(5 - local.weekday()) % 7)).isoformat()


def check_links(body: str, items: list[dict]) -> None:
    known = {r["url"] for r in items}
    for url in re.findall(r"\]\((https?://[^)\s]+)\)", body):
        if url not in known:
            log.warning("digest links to a URL not in the input: %s", url)


if __name__ == "__main__":
    sys.exit(main())
