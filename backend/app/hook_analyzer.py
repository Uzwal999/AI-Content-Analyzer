"""First-line hook analysis."""

from __future__ import annotations

import re

from .utils import clamp, contains_phrase, word_count


BENEFIT_TERMS = ["save", "grow", "improve", "build", "discover", "transform", "help", "designed for", "so you can"]
CURIOUS_TERMS = ["why", "how", "what if", "did you know", "ready to", "looking for", "struggling"]
GENERIC_TERMS = ["new post", "amazing", "best", "great", "check this out"]


def first_line(caption: str) -> str:
    clean = caption.strip()
    if not clean:
        return ""
    return re.split(r"[\n.!?]+", clean)[0].strip()


def analyze_hook(caption: str, platform: str) -> dict[str, object]:
    line = first_line(caption)
    suggestions: list[str] = []
    words = word_count(line)
    lower = line.lower()
    score = 5

    if not line:
        score = 0
        suggestions.append("Add a strong first line that introduces the main benefit.")
    else:
        if any(term in lower for term in BENEFIT_TERMS):
            score += 2
        else:
            suggestions.append("Make the opening more benefit-driven.")

        if any(term in lower for term in CURIOUS_TERMS):
            score += 1

        if words <= 14:
            score += 1
        else:
            score -= 2
            suggestions.append("Shorten the opening line so it is easier to scan.")

        if any(contains_phrase(lower, term) for term in GENERIC_TERMS):
            score -= 2
            suggestions.append("Avoid generic opening phrases and make the hook more specific.")

        if platform in {"Instagram", "TikTok", "X/Twitter"} and words > 12:
            suggestions.append(f"Make the first line punchier for {platform}.")
        if platform == "LinkedIn" and not any(term in lower for term in ["strategy", "business", "growth", "hiring", "career", "brand"]):
            suggestions.append("For LinkedIn, add a clearer business or professional insight in the first line.")

    score = clamp(score, 0, 10)
    if score >= 8:
        strength = "Strong"
        comment = "The hook is clear, specific, and likely to stop the scroll."
    elif score >= 5:
        strength = "Good"
        comment = "The hook is clear, but it can be more specific or benefit-driven."
    else:
        strength = "Weak"
        comment = "The hook needs a sharper opening benefit or curiosity angle."

    if not suggestions:
        suggestions.append("The opening is strong. Consider testing a slightly more specific first line.")

    return {
        "hook_score": score,
        "hook_strength": strength,
        "first_line": line,
        "comment": comment,
        "suggestions": suggestions[:3],
    }
