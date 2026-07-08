"""Content calendar suggestion generator."""

from __future__ import annotations


DAY_BY_GOAL = {
    "Awareness": "Monday",
    "Engagement": "Wednesday",
    "Sales": "Friday",
    "Hiring": "Tuesday",
    "Website Traffic": "Thursday",
    "Lead Generation": "Thursday",
    "Brand Trust": "Wednesday",
    "Community Building": "Sunday",
}


def generate_calendar_suggestion(campaign_goal: str, content_type: str) -> dict[str, object]:
    follow_up_map = {
        "Sales": ["Educational carousel", "Customer testimonial", "Sales CTA post"],
        "Hiring": ["Role details post", "Team culture post", "Application reminder"],
        "Lead Generation": ["Problem-awareness post", "Case study post", "Consultation CTA post"],
        "Engagement": ["Question post", "Poll or story prompt", "Community response post"],
    }
    follow_ups = follow_up_map.get(campaign_goal, ["Educational carousel", "Trust-building proof post", "CTA reminder post"])
    return {
        "suggested_day": DAY_BY_GOAL.get(campaign_goal, "Monday"),
        "content_role": content_type,
        "follow_up_posts": follow_ups,
        "weekly_sequence": [
            f"Monday: {content_type}",
            "Wednesday: Educational or proof-led content",
            f"Friday: {campaign_goal} CTA post",
        ],
    }
