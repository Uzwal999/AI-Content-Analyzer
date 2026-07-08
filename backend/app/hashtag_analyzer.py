"""Hashtag quality checker."""

from __future__ import annotations

import re
from typing import Any

from .utils import clamp, normalize_text, unique_preserve_order


GENERIC_HASHTAGS = {
    "love",
    "instagood",
    "photooftheday",
    "viral",
    "trending",
    "best",
    "amazing",
    "business",
    "marketing",
    "follow",
}


def extract_hashtags(caption: str, hashtags: str) -> list[str]:
    tags = re.findall(r"#([A-Za-z0-9_]+)", f"{caption} {hashtags}")
    return [f"#{tag}" for tag in unique_preserve_order(tags)]


def _compact(value: str) -> str:
    return normalize_text(value).replace("#", "").replace("-", "").replace("_", "").replace(" ", "")


def analyze_hashtags(caption: str, hashtags: str, profile: dict[str, Any]) -> dict[str, Any]:
    tags = extract_hashtags(caption, hashtags)
    compact_keywords = {_compact(keyword) for keyword in profile.get("keywords", [])}

    relevant = [tag for tag in tags if _compact(tag) in compact_keywords]
    generic = [tag for tag in tags if _compact(tag) in GENERIC_HASHTAGS]
    suggestions: list[str] = []

    score = 3
    if len(tags) == 0:
        score = 1
        suggestions.append("Add 2 to 6 relevant hashtags for discoverability.")
    elif 2 <= len(tags) <= 6:
        score = 4
    elif len(tags) > 10:
        score = 2
        suggestions.append("Reduce hashtag count to keep the caption premium.")

    if relevant:
        score += 1
    else:
        suggestions.append("Add at least one niche hashtag linked to the brand or industry.")

    if generic:
        score -= 1
        suggestions.append("Replace generic hashtags with more specific brand, service, or audience hashtags.")

    score = clamp(score, 0, 5)
    if score >= 4:
        comment = "Hashtags are focused and support the brand context."
    elif score >= 2:
        comment = "Hashtags are usable, but they could be more brand-specific."
    else:
        comment = "Hashtags need refinement for better discoverability and brand fit."

    return {
        "hashtag_score": score,
        "hashtag_count": len(tags),
        "relevant_hashtags": relevant,
        "keyword_hashtags": relevant,
        "generic_hashtags": generic,
        "suggestions": unique_preserve_order(suggestions),
        "comment": comment,
    }
