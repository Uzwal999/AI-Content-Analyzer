"""Brand profile definitions used by the analyzer and API."""

from __future__ import annotations

from copy import deepcopy
from typing import Any


BRAND_PROFILES: dict[str, dict[str, Any]] = {
    "The ISMA": {
        "brand_name": "The ISMA",
        "industry": "Natural skincare and wellness",
        "desired_tone": ["premium", "natural", "calm", "clean", "trustworthy", "soft"],
        "keywords": [
            "natural",
            "skincare",
            "glow",
            "clean",
            "self-care",
            "soft",
            "fresh",
            "gentle",
            "premium",
            "clay",
            "serum",
            "wellness",
            "routine",
            "nourish",
        ],
        "avoid_words": [
            "cheap",
            "fake",
            "guaranteed results",
            "miracle cure",
            "aggressive",
            "too many emojis",
            "pushy sales",
            "instant cure",
            "must buy",
            "hurry",
        ],
        "cta_examples": ["Discover the range", "Shop now", "Upgrade your skincare routine"],
        "visual_style": (
            "Soft beige backgrounds, clean product photography, natural textures, clay elements, "
            "warm lighting, minimal typography, spa-style mood"
        ),
        "colors": ["Beige", "White", "Soft Brown", "Warm Cream"],
        "typography": "Minimal premium typography with calm spacing",
    },
    "TMB Bar": {
        "brand_name": "TMB Bar",
        "industry": "Mobile bar and event services",
        "desired_tone": ["elegant", "energetic", "professional", "event-focused", "memorable", "premium"],
        "keywords": [
            "event",
            "mobile bar",
            "cocktails",
            "celebration",
            "guests",
            "party",
            "wedding",
            "corporate",
            "premium",
            "experience",
            "unforgettable",
            "service",
        ],
        "avoid_words": ["boring wording", "unclear CTA", "weak event benefit", "too generic", "cheap"],
        "cta_examples": ["Book your event", "Create an unforgettable experience", "Enquire today"],
        "visual_style": (
            "Black and gold tones, cocktail closeups, event photography, elegant typography, "
            "premium lighting, celebration atmosphere"
        ),
        "colors": ["Black", "Gold", "Champagne", "White"],
        "typography": "Elegant high-contrast typography with premium event styling",
    },
    "AESN": {
        "brand_name": "AESN",
        "industry": "Recruitment and staffing",
        "desired_tone": ["professional", "helpful", "clear", "trustworthy", "career-focused"],
        "keywords": [
            "hiring",
            "jobs",
            "recruitment",
            "candidates",
            "employers",
            "apply",
            "career",
            "opportunity",
            "staff",
            "workforce",
            "CV",
            "role",
            "vacancy",
        ],
        "avoid_words": ["slang", "unclear role details", "too casual tone", "missing pay", "missing location"],
        "cta_examples": ["Apply today", "Send your CV", "Contact our recruitment team"],
        "visual_style": (
            "Clean corporate layout, blue and white palette, clear job details, professional icons, "
            "readable typography"
        ),
        "colors": ["Blue", "White", "Navy", "Light Grey"],
        "typography": "Readable professional typography with clear hierarchy",
    },
    "EverVFX": {
        "brand_name": "EverVFX",
        "industry": "Creative agency, branding, AI content, design, social media",
        "desired_tone": ["modern", "creative", "strategic", "premium", "growth-focused", "confident"],
        "keywords": [
            "branding",
            "content",
            "design",
            "strategy",
            "growth",
            "reels",
            "social media",
            "AI",
            "creative",
            "digital",
            "campaigns",
            "visuals",
            "storytelling",
        ],
        "avoid_words": ["generic wording", "weak value proposition", "unclear offer", "overused buzzwords", "cheap design"],
        "cta_examples": ["Let's build your brand", "Message us", "Book a free strategy call"],
        "visual_style": (
            "Dark premium background, gradient accents, modern typography, creative visuals, "
            "AI-inspired design, bold layout"
        ),
        "colors": ["Black", "Electric Blue", "Purple", "Cyan", "White"],
        "typography": "Bold modern typography with clean agency spacing",
    },
}


def get_brand_profiles() -> dict[str, dict[str, Any]]:
    """Return a copy so API callers cannot mutate the shared profiles."""
    return deepcopy(BRAND_PROFILES)


def build_custom_profile(custom_brand: dict[str, Any] | None) -> dict[str, Any]:
    """Normalize a custom brand payload into the same profile shape as presets."""
    custom_brand = custom_brand or {}
    visual_style = custom_brand.get("visual_style") or custom_brand.get("visual_style_preference") or "Clean brand-led creative direction"
    return {
        "brand_name": custom_brand.get("brand_name") or "Custom Brand",
        "industry": custom_brand.get("industry") or "General brand",
        "desired_tone": custom_brand.get("desired_tone") or ["clear", "professional"],
        "keywords": custom_brand.get("keywords") or [],
        "avoid_words": custom_brand.get("avoid_words") or [],
        "cta_examples": custom_brand.get("cta_examples") or ["Learn more"],
        "visual_style": visual_style,
        "colors": custom_brand.get("colors") or ["Brand primary", "White", "Neutral"],
        "typography": custom_brand.get("typography") or "Clean readable typography",
        "target_audience": custom_brand.get("target_audience") or "",
        "brand_personality": custom_brand.get("brand_personality") or "",
    }


def get_profile(brand: str, custom_brand: dict[str, Any] | None = None) -> dict[str, Any]:
    """Resolve a preset or custom brand profile."""
    if brand == "Custom Brand":
        return build_custom_profile(custom_brand)

    profiles = get_brand_profiles()
    return profiles.get(brand, build_custom_profile(custom_brand))
