"""Optional competitor caption comparison."""

from __future__ import annotations

from typing import Any

from .cta_analyzer import analyze_cta
from .hook_analyzer import analyze_hook
from .utils import contains_phrase, normalize_text, word_count


def _keyword_count(text: str, profile: dict[str, Any]) -> int:
    normalized = normalize_text(text)
    return sum(1 for keyword in profile.get("keywords", []) if contains_phrase(normalized, keyword))


def compare_competitor(
    *,
    your_caption: str,
    competitor_caption: str,
    profile: dict[str, Any],
    platform: str,
    campaign_goal: str,
) -> dict[str, object]:
    if not competitor_caption.strip():
        return {
            "available": False,
            "summary": "No competitor caption was provided.",
            "your_strengths": [],
            "competitor_strengths": [],
            "recommendation": "Add a competitor caption to compare hook, CTA, tone, clarity, and keyword strength.",
        }

    your_hook = analyze_hook(your_caption, platform)["hook_score"]
    competitor_hook = analyze_hook(competitor_caption, platform)["hook_score"]
    your_cta = analyze_cta(normalize_text(your_caption), profile, campaign_goal)["cta_strength"]
    competitor_cta = analyze_cta(normalize_text(competitor_caption), profile, campaign_goal)["cta_strength"]
    your_keywords = _keyword_count(your_caption, profile)
    competitor_keywords = _keyword_count(competitor_caption, profile)
    your_words = word_count(your_caption)
    competitor_words = word_count(competitor_caption)

    your_strengths: list[str] = []
    competitor_strengths: list[str] = []

    if your_hook >= competitor_hook:
        your_strengths.append("Stronger or equal first-line hook")
    else:
        competitor_strengths.append("Stronger opening line")

    if your_cta >= competitor_cta:
        your_strengths.append("Clearer CTA")
    else:
        competitor_strengths.append("Clearer CTA")

    if your_keywords >= competitor_keywords:
        your_strengths.append("More brand keyword alignment")
    else:
        competitor_strengths.append("More keyword coverage")

    if 12 <= your_words <= 90:
        your_strengths.append("Good caption length")
    if 12 <= competitor_words <= 90:
        competitor_strengths.append("Good caption length")

    if competitor_strengths and your_strengths:
        summary = "Your caption has clear strengths, but the competitor caption wins in a few areas."
        recommendation = "Keep your brand tone while improving the competitor's strongest hook or clarity tactic."
    elif competitor_strengths:
        summary = "The competitor caption currently performs better in the comparison signals."
        recommendation = "Strengthen your opening line, CTA, and keyword usage before publishing."
    else:
        summary = "Your caption is stronger than the competitor caption across the main comparison signals."
        recommendation = "Use your current direction and test small improvements to the hook or CTA."

    return {
        "available": True,
        "summary": summary,
        "your_strengths": your_strengths,
        "competitor_strengths": competitor_strengths,
        "recommendation": recommendation,
    }
