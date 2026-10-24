"""Per-item triage with a small model: keep/drop, category, significance, summary."""

from __future__ import annotations

import json

import anthropic

from .common import CATEGORIES, EXCLUSION_RULES, log

SCHEMA = {
    "type": "object",
    "properties": {
        "keep": {"type": "boolean"},
        "category": {"type": "string", "enum": CATEGORIES},
        "significance": {"type": "integer"},
        "story_key": {"type": "string"},
        "summary": {"type": "string"},
        "why_it_matters": {"type": "string"},
        "exclusion_rule": {"type": "string", "enum": EXCLUSION_RULES},
        "exclusion_reason": {"type": "string"},
    },
    "required": ["keep", "category", "significance", "story_key", "summary",
                 "why_it_matters", "exclusion_rule", "exclusion_reason"],
    "additionalProperties": False,
}

INSTRUCTIONS = """You triage articles for a personal weekly AI & BI news digest.
Apply the reader profile below strictly. Most items should be dropped: a feed full of
vendor marketing should produce very few keeps.

Return:
- keep: true only if the item passes the Keep/Drop rules AND significance >= 3.
- category: the best category (use "none" when nothing fits).
- significance: 1-5 per the scale in the profile. Score the underlying news, not the
  enthusiasm of the writing. Vendor self-description ("revolutionary") is not evidence.
- story_key: a short neutral label for the underlying event, the same one other outlets
  covering it would get, e.g. "OpenAI releases GPT-6", "Fabric: Direct Lake on OneLake GA".
  For opinion or practice pieces: "<author>: <topic>".
- summary: 2-4 sentences, plain and factual, what actually happened or what the piece
  argues. For research, popularize: what was done, in plain words; why it might matter
  and on what timescale; how solid it looks. Empty string if dropped.
- why_it_matters: one sentence for this reader specifically (what it changes for
  someone running Fabric/Power BI and building with LLMs). Empty string if dropped.
- exclusion_rule: if dropped, the Drop rule that applies ("kept" if kept; "low significance"
  if it passes the rules but scores below 3).
- exclusion_reason: if dropped, a few words of detail. Empty string if kept.

Write in English. Do not invent facts that are not in the text; if the text is only a
teaser, say less rather than guess.

<reader_profile>
{profile}
</reader_profile>"""


def build_message(entry, text: str) -> str:
    published = entry.published.date().isoformat() if entry.published else "unknown"
    return (
        f"Source: {entry.source} (tier {entry.tier}; source group hint: {entry.group})\n"
        f"Published: {published}\n"
        f"URL: {entry.url}\n"
        f"Title: {entry.title}\n\n"
        f"Text:\n{text or '(no text available, judge from title and source only)'}"
    )


def classify(client: anthropic.Anthropic, model: str, profile: str, entry, text: str) -> dict:
    resp = client.messages.create(
        model=model,
        max_tokens=1200,
        system=INSTRUCTIONS.replace("{profile}", profile),
        messages=[{"role": "user", "content": build_message(entry, text)}],
        output_config={"format": {"type": "json_schema", "schema": SCHEMA}},
    )
    raw = next(b.text for b in resp.content if b.type == "text")
    out = json.loads(raw)
    out["significance"] = max(1, min(5, int(out.get("significance", 1))))
    if out["keep"] and out["significance"] < 3:
        out["keep"] = False
        out["exclusion_rule"] = "low significance"
    # stored as "<rule>: <detail>" so the CSV schema stays unchanged
    if out["keep"]:
        out["exclusion_reason"] = ""
    else:
        rule = out.get("exclusion_rule") or "other"
        rule = "other" if rule == "kept" else rule
        detail = (out.get("exclusion_reason") or "").strip()
        out["exclusion_reason"] = f"{rule}: {detail}" if detail else rule
    return out


def heuristic(entry, text: str) -> dict:
    """Dry-run stand-in for the model: keeps everything at significance 3."""
    return {
        "keep": True,
        "category": entry.group if entry.group in CATEGORIES else "none",
        "significance": 3,
        "story_key": entry.title[:80],
        "summary": (text or entry.title)[:300],
        "why_it_matters": "(dry run, no model call)",
        "exclusion_reason": "",
    }


def safe_classify(client, model, profile, entry, text) -> dict | None:
    try:
        return classify(client, model, profile, entry, text)
    except anthropic.APIStatusError as exc:
        log.warning("classify failed for %s: %s %s", entry.url, exc.status_code, exc.message)
        if exc.status_code in (401, 403):
            raise
    except Exception as exc:
        log.warning("classify failed for %s: %s", entry.url, exc)
    return None
