"""Pydantic request and response models for the FastAPI app."""

from __future__ import annotations

from pydantic import BaseModel, Field


class ClientDetails(BaseModel):
    client_name: str = ""
    campaign_name: str = ""
    prepared_by: str = "EverVFX"
    report_notes: str = ""
    brand_manager_name: str = ""
    date_generated: str = ""


class CustomBrand(BaseModel):
    brand_name: str = ""
    industry: str = ""
    desired_tone: list[str] = Field(default_factory=list)
    keywords: list[str] = Field(default_factory=list)
    avoid_words: list[str] = Field(default_factory=list)
    cta_examples: list[str] = Field(default_factory=list)
    target_audience: str = ""
    brand_personality: str = ""
    visual_style: str = ""
    visual_style_preference: str = ""


class AnalyzeRequest(BaseModel):
    brand: str
    platform: str = "Instagram"
    post_type: str
    campaign_goal: str
    caption: str
    audience: str = ""
    hashtags: str = ""
    competitor_caption: str = ""
    agency_mode: bool = False
    client_details: ClientDetails = Field(default_factory=ClientDetails)
    custom_brand: CustomBrand | None = None


class HookAnalysis(BaseModel):
    hook_score: int
    hook_strength: str
    first_line: str
    comment: str
    suggestions: list[str]


class ToneAnalysis(BaseModel):
    detected_tone: list[str]
    tone_score: int
    comment: str


class CTAAnalysis(BaseModel):
    cta_found: bool
    cta_strength: int
    detected_cta: str
    recommended_ctas: list[str]
    comment: str


class KeywordAnalysis(BaseModel):
    keyword_score: int
    matched_keywords: list[str]
    missing_keywords: list[str]


class HashtagAnalysis(BaseModel):
    hashtag_score: int
    hashtag_count: int
    relevant_hashtags: list[str]
    keyword_hashtags: list[str]
    generic_hashtags: list[str]
    suggestions: list[str]
    comment: str


class CaptionQuality(BaseModel):
    clarity_score: int
    length_status: str
    word_count: int
    character_count: int
    emoji_count: int
    has_excessive_punctuation: bool
    comment: str


class PlatformSuggestions(BaseModel):
    platform: str
    suggestions: list[str]


class CampaignGoalRelevance(BaseModel):
    score: int
    comment: str


class ScoreBreakdownItem(BaseModel):
    score: int
    max_score: int


class ReadabilityAnalysis(BaseModel):
    word_count: int
    sentence_count: int
    average_words_per_sentence: float
    readability_score: int
    reading_level: str
    comment: str


class PlatformFit(BaseModel):
    score: int
    recommended_length: str
    comment: str
    tips: list[str]


class RiskAnalysis(BaseModel):
    risk_level: str
    risky_terms: list[str]
    comment: str


class BeforeAfter(BaseModel):
    original: str
    improved: str
    key_improvements: list[str]


class CampaignBrief(BaseModel):
    campaign_goal: str
    target_audience: str
    recommended_post_type: str
    content_angle: str
    caption_tone: str
    recommended_cta: str
    key_message: str
    suggested_follow_up_content: str


class DesignDirection(BaseModel):
    visual_style: str
    colors: list[str]
    typography: str
    layout_suggestion: str
    imagery_suggestion: str


class CalendarSuggestion(BaseModel):
    suggested_day: str
    content_role: str
    follow_up_posts: list[str]
    weekly_sequence: list[str]


class CompetitorComparison(BaseModel):
    available: bool
    summary: str
    your_strengths: list[str]
    competitor_strengths: list[str]
    recommendation: str


class AnalyzeResponse(BaseModel):
    overall_score: int
    score_label: str
    publish_readiness: str
    brand_voice_score: int
    hook_analysis: HookAnalysis
    tone_analysis: ToneAnalysis
    cta_analysis: CTAAnalysis
    keyword_analysis: KeywordAnalysis
    hashtag_analysis: HashtagAnalysis
    caption_quality: CaptionQuality
    platform_suggestions: PlatformSuggestions
    content_type: str
    content_pillar: str
    campaign_goal_relevance: CampaignGoalRelevance
    score_breakdown: dict[str, ScoreBreakdownItem]
    readability_analysis: ReadabilityAnalysis
    platform_fit: PlatformFit
    risk_analysis: RiskAnalysis
    problems: list[str]
    suggestions: list[str]
    improved_caption: str
    before_after: BeforeAfter
    campaign_brief: CampaignBrief
    design_direction: DesignDirection
    calendar_suggestion: CalendarSuggestion
    competitor_comparison: CompetitorComparison
    final_recommendation: str
