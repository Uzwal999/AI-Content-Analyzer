"""Rule-based improved caption generation.

This intentionally avoids external AI APIs. The function builds a polished
caption from the brand profile, selected goal, audience, and analysis signals.
"""

from __future__ import annotations

import re
from typing import Any

from .utils import contains_phrase, normalize_text, unique_preserve_order


GOAL_CTA_FALLBACKS = {
    "Awareness": "Discover more",
    "Engagement": "Tell us what you think",
    "Sales": "Shop now",
    "Hiring": "Apply today",
    "Website Traffic": "Visit our website",
    "Lead Generation": "Book a call",
    "Brand Trust": "Learn more",
    "Community Building": "Join the community",
}


def _clean_original_idea(caption: str, avoid_words: list[str]) -> str:
    """Keep the usable idea from the first sentence while stripping risky terms."""
    first_sentence = re.split(r"(?<=[.!?])\s+", caption.strip())[0] if caption.strip() else ""
    first_sentence = re.sub(r"#\w+", "", first_sentence).strip()
    first_sentence = re.sub(r"\s+", " ", first_sentence)

    for word in avoid_words:
        if word:
            first_sentence = re.sub(re.escape(word), "", first_sentence, flags=re.IGNORECASE)

    if len(first_sentence) > 140:
        first_sentence = first_sentence[:137].rstrip() + "..."

    return first_sentence


def _choose_cta(profile: dict[str, Any], campaign_goal: str) -> str:
    examples = profile.get("cta_examples") or []
    if campaign_goal == "Sales":
        for cta in examples:
            if any(word in normalize_text(cta) for word in ["shop", "buy", "range"]):
                return cta
    if campaign_goal == "Hiring":
        for cta in examples:
            if any(word in normalize_text(cta) for word in ["apply", "cv", "recruitment"]):
                return cta
    if campaign_goal in {"Lead Generation", "Website Traffic"}:
        for cta in examples:
            if any(word in normalize_text(cta) for word in ["book", "message", "contact", "visit", "enquire"]):
                return cta
    return examples[0] if examples else GOAL_CTA_FALLBACKS.get(campaign_goal, "Learn more")


def _select_keywords(profile: dict[str, Any], caption: str, limit: int = 3) -> list[str]:
    text = normalize_text(caption)
    keywords = profile.get("keywords") or []
    missing = [keyword for keyword in keywords if not contains_phrase(text, keyword)]
    selected = unique_preserve_order((missing + keywords)[:limit])
    return selected


def generate_improved_caption(
    *,
    brand_profile: dict[str, Any],
    campaign_goal: str,
    post_type: str,
    audience: str,
    original_caption: str,
    platform: str = "Instagram",
) -> str:
    """Create a practical improved caption using deterministic brand rules."""
    brand_name = brand_profile.get("brand_name", "this brand")
    industry = brand_profile.get("industry", "your brand")
    tone_words = brand_profile.get("desired_tone") or ["clear", "professional"]
    avoid_words = brand_profile.get("avoid_words") or []
    keywords = _select_keywords(brand_profile, original_caption)
    cta = _choose_cta(brand_profile, campaign_goal)
    idea = _clean_original_idea(original_caption, avoid_words)

    audience_phrase = f" for {audience.strip()}" if audience.strip() else ""
    keyword_phrase = ", ".join(keywords[:3])
    tone_phrase = ", ".join(tone_words[:2])

    if campaign_goal == "Hiring":
        body = (
            f"{brand_name} is connecting talented people with meaningful career opportunities"
            f"{audience_phrase}. Explore a clear, supportive recruitment process built around the right fit."
        )
    elif "Event" in post_type or brand_name == "TMB Bar":
        body = (
            f"Make your next event feel polished, memorable, and effortless{audience_phrase}."
            f" {brand_name} brings a premium {industry.lower()} experience designed around your guests."
        )
    elif campaign_goal == "Sales":
        body = (
            f"Bring a more {tone_phrase} experience to your routine{audience_phrase}."
            f" {brand_name} helps you choose {keyword_phrase} with confidence."
        )
    elif campaign_goal == "Engagement":
        body = (
            f"{brand_name} wants to hear from you{audience_phrase}."
            f" Share what matters most when choosing {keyword_phrase or industry.lower()}."
        )
    elif campaign_goal == "Brand Trust":
        body = (
            f"Trust is built through clarity, consistency, and real value{audience_phrase}."
            f" {brand_name} brings {keyword_phrase or industry.lower()} together with a polished, reliable approach."
        )
    elif campaign_goal == "Community Building":
        body = (
            f"Great brands grow with the people around them{audience_phrase}."
            f" {brand_name} is building a community around {keyword_phrase or industry.lower()}."
        )
    else:
        body = (
            f"Discover a more {tone_phrase} way to experience {industry.lower()}{audience_phrase}."
            f" {brand_name} brings together {keyword_phrase} in a way that feels clear and purposeful."
        )

    if idea and len(idea) > 20 and normalize_text(idea) not in normalize_text(body):
        body = f"{idea} {body}"

    if platform in {"TikTok", "X/Twitter"} and len(body) > 220:
        body = body[:217].rstrip() + "..."
    elif platform == "LinkedIn" and campaign_goal not in {"Sales", "Engagement"}:
        body = f"{body} Built for teams that need clarity before content goes live."

    improved = f"{body} {cta}."
    improved = re.sub(r"\s+", " ", improved).strip()

    for avoid_word in avoid_words:
        improved = re.sub(re.escape(avoid_word), "", improved, flags=re.IGNORECASE)

    return re.sub(r"\s+", " ", improved).strip()
