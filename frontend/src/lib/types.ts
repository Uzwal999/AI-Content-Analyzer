export type BrandName = "The ISMA" | "TMB Bar" | "AESN" | "EverVFX" | "Custom Brand";

export type Platform = "Instagram" | "LinkedIn" | "Facebook" | "TikTok" | "X/Twitter";

export type PostType =
  | "Static Post"
  | "Carousel"
  | "Reel"
  | "Story"
  | "LinkedIn Post"
  | "Product Post"
  | "Hiring Post"
  | "Event Post"
  | "Service Promotion"
  | "Testimonial Post";

export type CampaignGoal =
  | "Awareness"
  | "Engagement"
  | "Sales"
  | "Hiring"
  | "Website Traffic"
  | "Lead Generation"
  | "Brand Trust"
  | "Community Building";

export interface BrandProfile {
  brand_name: string;
  industry: string;
  desired_tone: string[];
  keywords: string[];
  avoid_words: string[];
  cta_examples: string[];
  visual_style?: string;
  colors?: string[];
  typography?: string;
}

export interface ClientDetails {
  client_name: string;
  campaign_name: string;
  prepared_by: string;
  report_notes: string;
  brand_manager_name: string;
  date_generated: string;
}

export interface CustomBrandInput {
  brand_name: string;
  industry: string;
  desired_tone: string[];
  keywords: string[];
  avoid_words: string[];
  cta_examples: string[];
  target_audience: string;
  brand_personality: string;
  visual_style: string;
}

export interface AnalyzeRequest {
  brand: BrandName;
  platform: Platform;
  post_type: PostType;
  campaign_goal: CampaignGoal;
  caption: string;
  audience: string;
  hashtags: string;
  competitor_caption: string;
  agency_mode: boolean;
  client_details: ClientDetails;
  custom_brand?: CustomBrandInput | null;
}

export interface HookAnalysis {
  hook_score: number;
  hook_strength: string;
  first_line: string;
  comment: string;
  suggestions: string[];
}

export interface ToneAnalysis {
  detected_tone: string[];
  tone_score: number;
  comment: string;
}

export interface CTAAnalysis {
  cta_found: boolean;
  cta_strength: number;
  detected_cta: string;
  recommended_ctas: string[];
  comment: string;
}

export interface KeywordAnalysis {
  keyword_score: number;
  matched_keywords: string[];
  missing_keywords: string[];
}

export interface HashtagAnalysis {
  hashtag_score: number;
  hashtag_count: number;
  relevant_hashtags: string[];
  keyword_hashtags: string[];
  generic_hashtags: string[];
  suggestions: string[];
  comment: string;
}

export interface CaptionQuality {
  clarity_score: number;
  length_status: string;
  word_count: number;
  character_count: number;
  emoji_count: number;
  has_excessive_punctuation: boolean;
  comment: string;
}

export interface PlatformSuggestions {
  platform: string;
  suggestions: string[];
}

export interface CampaignGoalRelevance {
  score: number;
  comment: string;
}

export interface ScoreBreakdownItem {
  score: number;
  max_score: number;
}

export interface ReadabilityAnalysis {
  word_count: number;
  sentence_count: number;
  average_words_per_sentence: number;
  readability_score: number;
  reading_level: string;
  comment: string;
}

export interface PlatformFit {
  score: number;
  recommended_length: string;
  comment: string;
  tips: string[];
}

export interface RiskAnalysis {
  risk_level: string;
  risky_terms: string[];
  comment: string;
}

export interface BeforeAfter {
  original: string;
  improved: string;
  key_improvements: string[];
}

export interface CampaignBrief {
  campaign_goal: string;
  target_audience: string;
  recommended_post_type: string;
  content_angle: string;
  caption_tone: string;
  recommended_cta: string;
  key_message: string;
  suggested_follow_up_content: string;
}

export interface DesignDirection {
  visual_style: string;
  colors: string[];
  typography: string;
  layout_suggestion: string;
  imagery_suggestion: string;
}

export interface CalendarSuggestion {
  suggested_day: string;
  content_role: string;
  follow_up_posts: string[];
  weekly_sequence: string[];
}

export interface CompetitorComparison {
  available: boolean;
  summary: string;
  your_strengths: string[];
  competitor_strengths: string[];
  recommendation: string;
}

export interface AnalysisResult {
  overall_score: number;
  score_label: string;
  publish_readiness: string;
  brand_voice_score: number;
  hook_analysis: HookAnalysis;
  tone_analysis: ToneAnalysis;
  cta_analysis: CTAAnalysis;
  keyword_analysis: KeywordAnalysis;
  hashtag_analysis: HashtagAnalysis;
  caption_quality: CaptionQuality;
  platform_suggestions: PlatformSuggestions;
  content_type: string;
  content_pillar: string;
  campaign_goal_relevance: CampaignGoalRelevance;
  score_breakdown: Record<string, ScoreBreakdownItem>;
  readability_analysis: ReadabilityAnalysis;
  platform_fit: PlatformFit;
  risk_analysis: RiskAnalysis;
  problems: string[];
  suggestions: string[];
  improved_caption: string;
  before_after: BeforeAfter;
  campaign_brief: CampaignBrief;
  design_direction: DesignDirection;
  calendar_suggestion: CalendarSuggestion;
  competitor_comparison: CompetitorComparison;
  final_recommendation: string;
}
