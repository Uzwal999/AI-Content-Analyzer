"""Visual direction generator for agency-style recommendations."""

from __future__ import annotations

from typing import Any


def generate_design_direction(
    *,
    profile: dict[str, Any],
    post_type: str,
    campaign_goal: str,
    platform: str,
) -> dict[str, object]:
    colors = profile.get("colors") or ["Brand primary", "White", "Neutral"]
    visual_style = profile.get("visual_style") or "Clean, brand-led creative direction"
    typography = profile.get("typography") or "Readable modern typography"

    if "Carousel" in post_type:
        layout = "Use a strong cover slide, 3 to 5 benefit-led slides, and a final CTA slide."
    elif "Reel" in post_type or platform == "TikTok":
        layout = "Open with a bold text hook, fast visual cuts, and a clear CTA end frame."
    elif "Story" in post_type:
        layout = "Use vertical safe spacing, one message per frame, and an interactive CTA sticker."
    else:
        layout = "Use a clean hero visual, short benefit text, and a clear CTA area."

    imagery = "Choose visuals that make the offer easy to understand within the first two seconds."
    if campaign_goal == "Brand Trust":
        imagery = "Use testimonials, proof points, team visuals, or process screenshots to build credibility."
    elif campaign_goal == "Sales":
        imagery = "Show the product or service outcome clearly with benefit text near the focal point."

    return {
        "visual_style": visual_style,
        "colors": colors,
        "typography": typography,
        "layout_suggestion": layout,
        "imagery_suggestion": imagery,
    }
