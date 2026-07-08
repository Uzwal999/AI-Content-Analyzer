"""Rule-based tone detection for caption analysis."""

from __future__ import annotations

from typing import Any

from .utils import clamp, contains_phrase, normalize_text


TONE_PATTERNS: dict[str, list[str]] = {
    "Premium": ["premium", "refined", "elegant", "crafted", "elevated", "luxury", "sophisticated", "polished"],
    "Natural": ["natural", "clean", "gentle", "soft", "fresh", "wellness", "self-care", "calm", "nourish"],
    "Professional": ["professional", "trusted", "reliable", "support", "solution", "team", "service", "expertise"],
    "Friendly": ["you", "your", "welcome", "join", "together", "help", "let's", "we"],
    "Educational": ["tips", "learn", "guide", "why", "how", "benefits", "improve", "understand"],
    "Casual": ["hey", "fun", "vibes", "chill", "quick", "simple", "easy"],
    "Sales-heavy": ["buy now", "limited offer", "hurry", "cheap", "best ever", "guaranteed", "don't miss out"],
    "Aggressive": ["must buy", "insane", "crazy", "unbelievable", "massive", "urgent"],
    "Generic": ["amazing", "best", "great", "quality", "perfect", "new post"],
    "Strategic": ["strategy", "growth", "positioning", "campaign", "audience", "insight", "brand"],
    "Trustworthy": ["trusted", "reliable", "proven", "clear", "transparent", "experience", "quality"],
}


def detect_tones(text: str) -> list[str]:
    detected = [
        tone for tone, patterns in TONE_PATTERNS.items()
        if any(contains_phrase(text, pattern) for pattern in patterns)
    ]
    return detected or ["Generic"]


def analyze_tone(text: str, profile: dict[str, Any]) -> dict[str, Any]:
    detected = detect_tones(text)
    desired = [normalize_text(tone) for tone in profile.get("desired_tone", [])]

    desired_hits = 0
    for desired_tone in desired:
        if contains_phrase(text, desired_tone):
            desired_hits += 1
            continue
        for detected_tone in detected:
            normalized_detected = normalize_text(detected_tone)
            if normalized_detected in desired_tone or desired_tone in normalized_detected:
                desired_hits += 1
                break

    score = 6
    if desired:
        score += (desired_hits / len(desired)) * 9
    if "Aggressive" in detected:
        score -= 5
    if "Sales-heavy" in detected and not any(tone in desired for tone in ["sales", "energetic", "confident"]):
        score -= 3
    if "Generic" in detected and len(detected) == 1:
        score -= 2

    score = clamp(score, 0, 15)
    if score >= 12:
        comment = "The tone matches the selected brand well."
    elif score >= 8:
        comment = "The tone is usable, but it could sound more brand-specific."
    else:
        comment = "The tone does not strongly match the selected brand identity."

    return {
        "detected_tone": detected,
        "tone_score": score,
        "comment": comment,
    }
