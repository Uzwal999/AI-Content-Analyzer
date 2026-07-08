"""Reusable rule-based NLP analyzer for EverVFX AI Brand Content Analyzer."""

from __future__ import annotations

from typing import Any

from .brand_profiles import get_profile
from .calendar_suggestions import generate_calendar_suggestion
from .campaign_brief import generate_campaign_brief
from .caption_generator import generate_improved_caption
from .competitor_analyzer import compare_competitor
from .cta_analyzer import analyze_cta
from .design_direction import generate_design_direction
from .hashtag_analyzer import analyze_hashtags
from .hook_analyzer import analyze_hook
from .tone_detector import analyze_tone
from .utils import (
    clamp,
    contains_phrase,
    count_emojis,
    find_matches,
    has_excessive_punctuation,
    normalize_text,
    parse_list_text,
    unique_preserve_order,
    word_count,
)


CAMPAIGN_GOAL_TERMS: dict[str, list[str]] = {
    "Awareness": ["discover", "introduce", "meet", "brand", "story", "new"],
    "Engagement": ["comment", "share", "tell us", "what do you think", "tag", "save"],
    "Sales": ["shop", "buy", "order", "offer", "product", "range", "collection"],
    "Hiring": ["hiring", "apply", "cv", "opportunity", "role", "job", "vacancy"],
    "Website Traffic": ["visit", "website", "link", "learn more", "read more"],
    "Lead Generation": ["contact", "message", "enquiry", "consultation", "book a call", "book"],
    "Brand Trust": ["trusted", "reliable", "experience", "quality", "reviews", "proven"],
    "Community Building": ["community", "together", "join", "share", "support", "connect"],
}

PLATFORM_SUGGESTIONS: dict[str, list[str]] = {
    "Instagram": ["Use a strong first-line hook.", "Keep the caption benefit-driven.", "Use focused hashtags."],
    "LinkedIn": ["Keep the tone professional.", "Lead with insight or business value.", "Use fewer emojis."],
    "Facebook": ["Use a conversational tone.", "Make the CTA clear.", "Community-led copy can perform well."],
    "TikTok": ["Keep the caption short and punchy.", "Make the hook immediate.", "Use trend-aware language carefully."],
    "X/Twitter": ["Keep the message concise.", "Use one clear hook.", "Use minimal hashtags."],
}

PLATFORM_LENGTH_GUIDES: dict[str, tuple[int, int]] = {
    "Instagram": (80, 350),
    "LinkedIn": (180, 1200),
    "Facebook": (80, 600),
    "TikTok": (30, 180),
    "X/Twitter": (20, 260),
}


def _prepare_custom_brand(custom_brand: dict[str, Any] | None) -> dict[str, Any] | None:
    if not custom_brand:
        return None

    prepared = dict(custom_brand)
    for key in ["desired_tone", "keywords", "avoid_words", "cta_examples"]:
        prepared[key] = parse_list_text(prepared.get(key))
    return prepared


def _score_label(score: int) -> str:
    if score >= 80:
        return "Strong"
    if score >= 60:
        return "Good"
    if score >= 40:
        return "Needs Improvement"
    return "Weak"


def _publish_readiness(score: int) -> str:
    if score >= 80:
        return "Ready to Publish"
    if score >= 60:
        return "Good, Minor Improvements"
    if score >= 40:
        return "Needs Revision"
    return "Not Ready"


def _recommendation(score: int) -> str:
    if score >= 80:
        return "Ready to Publish. This caption is strong enough for client or brand use with minor refinements."
    if score >= 60:
        return "Good with minor improvements. Strengthen the hook, CTA, or brand keywords before posting."
    if score >= 40:
        return "Needs revision before posting. Improve brand fit, clarity, and campaign alignment."
    return "Not ready for client publishing. Rewrite the caption with a clearer hook, value proposition, and CTA."


def _analyze_keywords(text: str, profile: dict[str, Any]) -> dict[str, Any]:
    keywords = profile.get("keywords") or []
    matched = find_matches(text, keywords)
    missing = [keyword for keyword in keywords if keyword not in matched]
    expected_matches = max(3, min(6, len(keywords))) if keywords else 1
    score = 14 if not keywords else clamp((len(matched) / expected_matches) * 20, 0, 20)
    return {
        "keyword_score": score,
        "matched_keywords": matched,
        "missing_keywords": missing[:8],
    }


def _analyze_caption_quality(caption: str, text: str, cta_found: bool, audience_focused: bool) -> dict[str, Any]:
    character_count = len(caption.strip())
    words = word_count(caption)
    emojis = count_emojis(caption)
    excessive_punctuation = has_excessive_punctuation(caption)

    score = 11
    length_status = "Good"
    if character_count < 30:
        length_status = "Too short"
        score -= 6
    elif character_count > 600:
        length_status = "Too long"
        score -= 5

    if words < 8:
        score -= 2
    if emojis > 6:
        score -= 3
    if excessive_punctuation:
        score -= 3
    if cta_found:
        score += 1
    if audience_focused:
        score += 1
    if any(contains_phrase(text, word) for word in ["because", "so you can", "designed for", "helps", "benefits", "built for"]):
        score += 1

    score = clamp(score, 0, 15)
    if score >= 12:
        comment = "The caption is clear, readable, and structured for social media."
    elif score >= 8:
        comment = "The caption is understandable but needs stronger structure or audience benefit."
    else:
        comment = "The caption needs clearer value, cleaner formatting, and stronger direction."

    return {
        "clarity_score": score,
        "length_status": length_status,
        "word_count": words,
        "character_count": character_count,
        "emoji_count": emojis,
        "has_excessive_punctuation": excessive_punctuation,
        "comment": comment,
    }


def _analyze_campaign_goal(text: str, campaign_goal: str, cta_found: bool) -> dict[str, Any]:
    terms = CAMPAIGN_GOAL_TERMS.get(campaign_goal, [])
    matches = find_matches(text, terms)
    score = clamp(len(matches) * 2.5 + (2 if cta_found else 0), 0, 10)

    if score >= 7:
        comment = f"The caption supports the selected {campaign_goal.lower()} goal."
    elif score >= 4:
        comment = f"The caption partially supports {campaign_goal.lower()}, but the intent could be clearer."
    else:
        comment = f"The selected {campaign_goal.lower()} goal is not clear enough in the caption."

    return {
        "score": score,
        "comment": comment,
    }


def _score_avoided_bad_words(text: str, profile: dict[str, Any]) -> tuple[int, list[str]]:
    avoid_words = profile.get("avoid_words") or []
    found = find_matches(text, avoid_words)
    risky_claims = find_matches(text, ["guaranteed results", "miracle", "instant cure", "best ever", "100%", "no risk"])
    all_found = unique_preserve_order(found + risky_claims)
    return clamp(10 - len(all_found) * 4, 0, 10), all_found


def _risk_analysis(bad_words_found: list[str], tone_analysis: dict[str, Any]) -> dict[str, Any]:
    detected = tone_analysis["detected_tone"]
    if bad_words_found or "Aggressive" in detected:
        risk_level = "High"
        comment = "Brand safety risk is high because the caption uses risky wording or aggressive tone."
    elif "Sales-heavy" in detected:
        risk_level = "Medium"
        comment = "The caption may feel too sales-heavy for some brand contexts."
    else:
        risk_level = "Low"
        comment = "No major brand safety risk was detected."
    return {
        "risk_level": risk_level,
        "risky_terms": bad_words_found,
        "comment": comment,
    }


def _mentions_audience(text: str, audience: str) -> bool:
    if not audience.strip():
        return True
    audience_terms = [
        term for term in normalize_text(audience).replace("-", " ").split()
        if len(term) > 3 and term not in {"your", "with", "from", "this", "that"}
    ]
    return any(contains_phrase(text, term) for term in audience_terms) or any(
        contains_phrase(text, term) for term in ["you", "your", "for you", "designed for", "built for"]
    )


def _detect_content_type(text: str, post_type: str, campaign_goal: str) -> str:
    if any(contains_phrase(text, term) for term in ["testimonial", "review", "client said", "case study"]):
        return "Testimonial"
    if any(contains_phrase(text, term) for term in ["behind the scenes", "bts", "process", "studio"]):
        return "Behind the Scenes"
    if any(contains_phrase(text, term) for term in ["hiring", "apply", "job", "role", "cv", "vacancy"]):
        return "Hiring"
    if any(contains_phrase(text, term) for term in ["event", "wedding", "corporate", "guests", "party"]):
        return "Event Promotion"
    if "Service Promotion" in post_type or any(contains_phrase(text, term) for term in ["service", "solution", "strategy call"]):
        return "Service Promotion"
    if any(contains_phrase(text, term) for term in ["tips", "guide", "how", "benefits", "learn"]):
        return "Educational"
    if any(contains_phrase(text, term) for term in ["shop", "buy", "order", "product", "range", "collection"]):
        return "Sales" if campaign_goal == "Sales" else "Product Awareness"
    if campaign_goal == "Community Building":
        return "Community Post"
    return "Brand Awareness"


def _detect_content_pillar(content_type: str, campaign_goal: str) -> str:
    if content_type in {"Educational", "Product Awareness"}:
        return "Educational/Product Awareness"
    if content_type in {"Sales", "Service Promotion"}:
        return "Promotional"
    if content_type == "Testimonial" or campaign_goal == "Brand Trust":
        return "Trust-building"
    if content_type == "Hiring":
        return "Recruitment"
    if content_type == "Event Promotion":
        return "Event"
    if content_type == "Community Post":
        return "Community"
    return "Brand Story"


def _platform_suggestions(platform: str, caption_quality: dict[str, Any], hook_analysis: dict[str, Any]) -> dict[str, Any]:
    suggestions = list(PLATFORM_SUGGESTIONS.get(platform, ["Keep the caption clear and action-oriented."]))
    if caption_quality["character_count"] > PLATFORM_LENGTH_GUIDES.get(platform, (0, 600))[1]:
        suggestions.append(f"Shorten the caption for better {platform} performance.")
    if hook_analysis["hook_score"] < 7:
        suggestions.append(f"Strengthen the first line for {platform}.")
    return {
        "platform": platform,
        "suggestions": unique_preserve_order(suggestions)[:4],
    }


def _readability_analysis(caption: str) -> dict[str, Any]:
    sentences = [part.strip() for part in caption.replace("!", ".").replace("?", ".").split(".") if part.strip()]
    sentence_count = max(1, len(sentences))
    words = word_count(caption)
    average_words = round(words / sentence_count, 1) if words else 0
    score = 8
    if words < 8:
        score -= 4
    if average_words > 25:
        score -= 3
    elif average_words > 18:
        score -= 1
    return {
        "word_count": words,
        "sentence_count": sentence_count,
        "average_words_per_sentence": average_words,
        "readability_score": clamp(score, 0, 10),
        "reading_level": "Easy to scan" if average_words <= 18 else "Moderate" if average_words <= 25 else "Dense",
        "comment": "Sentence length is easy to scan." if average_words <= 18 else "Shorter sentences would improve mobile readability.",
    }


def _platform_fit(caption: str, platform: str, cta_found: bool) -> dict[str, Any]:
    minimum, maximum = PLATFORM_LENGTH_GUIDES.get(platform, (80, 350))
    count = len(caption.strip())
    tips: list[str] = []
    score = 8
    if count < minimum:
        score -= 2
        tips.append(f"Add slightly more context for {platform}.")
    elif count > maximum:
        score -= 2
        tips.append(f"Shorten the caption for {platform}.")
    if not cta_found:
        score -= 2
        tips.append("Add a clear CTA.")
    if not tips:
        tips.append("Length and structure fit the selected platform.")
    return {
        "score": clamp(score, 0, 10),
        "recommended_length": f"{minimum}-{maximum} characters",
        "comment": f"This caption is {count} characters for {platform}.",
        "tips": tips,
    }


def _build_feedback(
    *,
    keyword_analysis: dict[str, Any],
    tone_analysis: dict[str, Any],
    cta_analysis: dict[str, Any],
    hook_analysis: dict[str, Any],
    hashtag_analysis: dict[str, Any],
    caption_quality: dict[str, Any],
    campaign_goal_relevance: dict[str, Any],
    bad_words_found: list[str],
    audience_focused: bool,
    platform_suggestions: dict[str, Any],
) -> tuple[list[str], list[str]]:
    problems: list[str] = []
    suggestions: list[str] = []

    if hook_analysis["hook_score"] < 6:
        problems.append("Hook is weak.")
        suggestions.append("Add a stronger first-line hook that mentions the benefit or creates curiosity.")
    if cta_analysis["cta_strength"] < 7:
        problems.append("CTA is missing or too weak.")
        suggestions.append("Add a clearer CTA that matches the campaign goal.")
    if keyword_analysis["keyword_score"] < 12:
        problems.append("Caption does not include enough brand keywords.")
        suggestions.append("Use more brand-specific keywords naturally.")
    if tone_analysis["tone_score"] < 8:
        problems.append("Tone does not match the selected brand strongly enough.")
        suggestions.append("Adjust the caption to match the selected brand tone.")
    if "Aggressive" in tone_analysis["detected_tone"]:
        problems.append("Caption sounds too aggressive for this brand.")
        suggestions.append("Make the caption less pushy and more brand-appropriate.")
    if bad_words_found:
        problems.append(f"Caption includes risky words or phrases: {', '.join(bad_words_found)}.")
        suggestions.append("Remove risky wording that conflicts with the brand guidelines.")
    if hashtag_analysis["hashtag_score"] < 3:
        problems.append("Hashtags are too generic or not strong enough.")
        suggestions.extend(hashtag_analysis["suggestions"])
    if caption_quality["length_status"] == "Too short":
        problems.append("Caption is too short to communicate value.")
        suggestions.append("Mention the audience benefit earlier.")
    elif caption_quality["length_status"] == "Too long":
        problems.append("Caption is too long for most social feeds.")
        suggestions.append("Shorten the caption around one main message.")
    if caption_quality["emoji_count"] > 6:
        problems.append("Too many emojis.")
        suggestions.append("Reduce emojis to keep the caption polished.")
    if caption_quality["has_excessive_punctuation"]:
        problems.append("Excessive punctuation is reducing quality.")
        suggestions.append("Remove repeated punctuation such as !!! or ???.")
    if campaign_goal_relevance["score"] < 5:
        problems.append("Campaign goal is unclear.")
        suggestions.append("Align the copy and CTA more clearly with the selected campaign goal.")
    if not audience_focused:
        problems.append("Caption is not audience-focused.")
        suggestions.append("Mention the audience or their benefit more clearly.")

    suggestions.extend(platform_suggestions["suggestions"][:2])

    if not problems:
        suggestions.append("Caption is strong. Test a small hook or CTA variation before publishing.")

    return unique_preserve_order(problems), unique_preserve_order(suggestions)


def _key_improvements(problems: list[str], suggestions: list[str]) -> list[str]:
    improvements = []
    if any("Hook" in problem for problem in problems):
        improvements.append("Stronger opening hook")
    if any("CTA" in problem for problem in problems):
        improvements.append("Clearer CTA")
    if any("keyword" in problem.lower() for problem in problems):
        improvements.append("More brand keywords")
    if any("tone" in problem.lower() for problem in problems):
        improvements.append("Better brand tone")
    if not improvements:
        improvements = ["Polished structure", "Clearer brand fit", "Improved campaign alignment"]
    return unique_preserve_order(improvements + suggestions[:1])[:5]


def analyze_caption(payload: dict[str, Any]) -> dict[str, Any]:
    """Analyze a caption and return a frontend-ready JSON-compatible result."""
    caption = payload.get("caption", "")
    hashtags = payload.get("hashtags", "")
    audience = payload.get("audience", "")
    platform = payload.get("platform", "Instagram")
    post_type = payload.get("post_type", "Static Post")
    campaign_goal = payload.get("campaign_goal", "Awareness")
    competitor_caption = payload.get("competitor_caption", "")
    custom_brand = _prepare_custom_brand(payload.get("custom_brand"))
    brand_profile = get_profile(payload.get("brand", ""), custom_brand)

    combined_text = normalize_text(f"{caption} {hashtags}")
    audience_focused = _mentions_audience(combined_text, audience)

    keyword_analysis = _analyze_keywords(combined_text, brand_profile)
    tone_analysis = analyze_tone(combined_text, brand_profile)
    cta_analysis = analyze_cta(combined_text, brand_profile, campaign_goal)
    hook_analysis = analyze_hook(caption, platform)
    hashtag_analysis = analyze_hashtags(caption, hashtags, brand_profile)
    caption_quality = _analyze_caption_quality(caption, combined_text, cta_analysis["cta_found"], audience_focused)
    campaign_goal_relevance = _analyze_campaign_goal(combined_text, campaign_goal, cta_analysis["cta_found"])
    avoided_bad_words_score, bad_words_found = _score_avoided_bad_words(combined_text, brand_profile)
    content_type = _detect_content_type(combined_text, post_type, campaign_goal)
    content_pillar = _detect_content_pillar(content_type, campaign_goal)
    platform_suggestions = _platform_suggestions(platform, caption_quality, hook_analysis)
    risk_analysis = _risk_analysis(bad_words_found, tone_analysis)

    overall_score = clamp(
        keyword_analysis["keyword_score"]
        + tone_analysis["tone_score"]
        + cta_analysis["cta_strength"]
        + caption_quality["clarity_score"]
        + campaign_goal_relevance["score"]
        + hook_analysis["hook_score"]
        + hashtag_analysis["hashtag_score"]
        + avoided_bad_words_score,
        0,
        100,
    )

    brand_voice_score = clamp(
        (keyword_analysis["keyword_score"] / 20) * 35
        + (tone_analysis["tone_score"] / 15) * 35
        + (avoided_bad_words_score / 10) * 20
        + (10 if audience_focused else 0),
        0,
        100,
    )

    problems, suggestions = _build_feedback(
        keyword_analysis=keyword_analysis,
        tone_analysis=tone_analysis,
        cta_analysis=cta_analysis,
        hook_analysis=hook_analysis,
        hashtag_analysis=hashtag_analysis,
        caption_quality=caption_quality,
        campaign_goal_relevance=campaign_goal_relevance,
        bad_words_found=bad_words_found,
        audience_focused=audience_focused,
        platform_suggestions=platform_suggestions,
    )

    improved_caption = generate_improved_caption(
        brand_profile=brand_profile,
        campaign_goal=campaign_goal,
        post_type=post_type,
        audience=audience,
        original_caption=caption,
        platform=platform,
    )

    campaign_brief = generate_campaign_brief(
        profile=brand_profile,
        campaign_goal=campaign_goal,
        audience=audience,
        post_type=post_type,
        platform=platform,
    )
    design_direction = generate_design_direction(
        profile=brand_profile,
        post_type=post_type,
        campaign_goal=campaign_goal,
        platform=platform,
    )
    calendar_suggestion = generate_calendar_suggestion(campaign_goal, content_type)
    competitor_comparison = compare_competitor(
        your_caption=caption,
        competitor_caption=competitor_caption,
        profile=brand_profile,
        platform=platform,
        campaign_goal=campaign_goal,
    )

    return {
        "overall_score": overall_score,
        "score_label": _score_label(overall_score),
        "publish_readiness": _publish_readiness(overall_score),
        "brand_voice_score": brand_voice_score,
        "hook_analysis": hook_analysis,
        "tone_analysis": tone_analysis,
        "cta_analysis": cta_analysis,
        "keyword_analysis": keyword_analysis,
        "hashtag_analysis": hashtag_analysis,
        "caption_quality": caption_quality,
        "platform_suggestions": platform_suggestions,
        "content_type": content_type,
        "content_pillar": content_pillar,
        "campaign_goal_relevance": campaign_goal_relevance,
        "score_breakdown": {
            "Brand keyword match": {"score": keyword_analysis["keyword_score"], "max_score": 20},
            "Tone match": {"score": tone_analysis["tone_score"], "max_score": 15},
            "CTA strength": {"score": cta_analysis["cta_strength"], "max_score": 15},
            "Caption quality": {"score": caption_quality["clarity_score"], "max_score": 15},
            "Campaign relevance": {"score": campaign_goal_relevance["score"], "max_score": 10},
            "Hook strength": {"score": hook_analysis["hook_score"], "max_score": 10},
            "Hashtag quality": {"score": hashtag_analysis["hashtag_score"], "max_score": 5},
            "Brand safety": {"score": avoided_bad_words_score, "max_score": 10},
        },
        "readability_analysis": _readability_analysis(caption),
        "platform_fit": _platform_fit(caption, platform, cta_analysis["cta_found"]),
        "risk_analysis": risk_analysis,
        "problems": problems,
        "suggestions": suggestions,
        "improved_caption": improved_caption,
        "before_after": {
            "original": caption,
            "improved": improved_caption,
            "key_improvements": _key_improvements(problems, suggestions),
        },
        "campaign_brief": campaign_brief,
        "design_direction": design_direction,
        "calendar_suggestion": calendar_suggestion,
        "competitor_comparison": competitor_comparison,
        "final_recommendation": _recommendation(overall_score),
    }
