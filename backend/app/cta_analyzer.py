"""CTA detection and recommendation logic."""

from __future__ import annotations

from typing import Any

from .utils import clamp, contains_phrase, normalize_text, unique_preserve_order


CTA_PHRASES = [
    "shop now",
    "book now",
    "apply today",
    "learn more",
    "contact us",
    "send us a message",
    "visit our website",
    "enquire today",
    "discover more",
    "discover the range",
    "send your cv",
    "book a free strategy call",
    "message us",
    "order now",
    "get started",
    "get in touch",
    "book your event",
    "upgrade your skincare routine",
    "contact our recruitment team",
    "let's build your brand",
]

GOAL_CTA_OPTIONS: dict[str, list[str]] = {
    "Awareness": ["Discover more", "Explore the story", "Meet the brand"],
    "Engagement": ["Tell us what you think", "Comment below", "Save this for later"],
    "Sales": ["Shop now", "Discover the range", "Explore the collection"],
    "Hiring": ["Apply today", "Send your CV", "View the role"],
    "Website Traffic": ["Visit our website", "Learn more", "Read the full guide"],
    "Lead Generation": ["Book a free strategy call", "Send us a message", "Enquire today"],
    "Brand Trust": ["Learn more", "See how we work", "Explore our approach"],
    "Community Building": ["Join the community", "Share your thoughts", "Connect with us"],
}


def recommended_ctas(profile: dict[str, Any], campaign_goal: str) -> list[str]:
    profile_ctas = profile.get("cta_examples") or []
    goal_ctas = GOAL_CTA_OPTIONS.get(campaign_goal, ["Learn more"])
    return unique_preserve_order(profile_ctas + goal_ctas)[:4]


def analyze_cta(text: str, profile: dict[str, Any], campaign_goal: str) -> dict[str, Any]:
    profile_ctas = [normalize_text(cta) for cta in profile.get("cta_examples", [])]
    all_ctas = unique_preserve_order(CTA_PHRASES + profile_ctas)
    detected = next((cta for cta in all_ctas if contains_phrase(text, cta)), "")

    if detected:
        profile_match = any(contains_phrase(detected, cta) or contains_phrase(cta, detected) for cta in profile_ctas)
        score = 15 if profile_match else 13
        comment = "The CTA is clear and action-oriented."
    else:
        soft_actions = ["discover", "explore", "join", "start", "read", "watch", "visit", "message", "contact"]
        soft_match = next((action for action in soft_actions if contains_phrase(text, action)), "")
        detected = soft_match
        score = 9 if soft_match else 3
        comment = "The CTA is present but could be more specific." if soft_match else "The caption needs a clearer direct CTA."

    return {
        "cta_found": bool(detected),
        "cta_strength": clamp(score, 0, 15),
        "detected_cta": detected.title() if detected else "",
        "recommended_ctas": recommended_ctas(profile, campaign_goal),
        "comment": comment,
    }
