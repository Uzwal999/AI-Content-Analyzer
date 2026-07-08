"""Campaign brief generator."""

from __future__ import annotations

from typing import Any

from .cta_analyzer import recommended_ctas


GOAL_ANGLES = {
    "Awareness": "Brand discovery and positioning",
    "Engagement": "Audience interaction and conversation",
    "Sales": "Product benefit and purchase intent",
    "Hiring": "Role clarity and candidate motivation",
    "Website Traffic": "Insight-led click-through",
    "Lead Generation": "Clear offer and enquiry intent",
    "Brand Trust": "Proof, credibility, and expertise",
    "Community Building": "Shared values and audience belonging",
}


def generate_campaign_brief(
    *,
    profile: dict[str, Any],
    campaign_goal: str,
    audience: str,
    post_type: str,
    platform: str,
) -> dict[str, str]:
    cta = recommended_ctas(profile, campaign_goal)[0]
    tones = profile.get("desired_tone") or ["clear", "professional"]
    key_message = (
        f"Position {profile.get('brand_name', 'the brand')} for {audience or 'the target audience'} "
        f"with a {', '.join(tones[:2])} message that supports {campaign_goal.lower()}."
    )
    return {
        "campaign_goal": campaign_goal,
        "target_audience": audience or profile.get("target_audience") or "Target audience",
        "recommended_post_type": post_type,
        "content_angle": GOAL_ANGLES.get(campaign_goal, "Clear brand-led communication"),
        "caption_tone": " and ".join(tones[:2]).title(),
        "recommended_cta": cta,
        "key_message": key_message,
        "suggested_follow_up_content": f"Use a follow-up {platform} post to reinforce proof, benefits, and the next action.",
    }
