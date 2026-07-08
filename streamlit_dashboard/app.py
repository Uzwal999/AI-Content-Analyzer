"""Optional Streamlit dashboard for quick Python demo/testing."""

from __future__ import annotations

import sys
from pathlib import Path

import streamlit as st


ROOT_DIR = Path(__file__).resolve().parents[1]
BACKEND_DIR = ROOT_DIR / "backend"
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))

from app.analyzer import analyze_caption  # noqa: E402
from app.brand_profiles import get_brand_profiles  # noqa: E402


PLATFORMS = ["Instagram", "LinkedIn", "Facebook", "TikTok", "X/Twitter"]

POST_TYPES = [
    "Static Post",
    "Carousel",
    "Reel",
    "Story",
    "LinkedIn Post",
    "Product Post",
    "Hiring Post",
    "Event Post",
    "Service Promotion",
    "Testimonial Post",
]

CAMPAIGN_GOALS = [
    "Awareness",
    "Engagement",
    "Sales",
    "Hiring",
    "Website Traffic",
    "Lead Generation",
    "Brand Trust",
    "Community Building",
]


st.set_page_config(page_title="EverVFX AI Brand Content Analyzer", layout="wide")

st.title("EverVFX AI Brand Content Analyzer")
st.caption("Quick Python demo using the same reusable rule-based analyzer as FastAPI.")

profiles = get_brand_profiles()
brand = st.sidebar.selectbox("Brand", list(profiles.keys()) + ["Custom Brand"])
platform = st.sidebar.selectbox("Platform", PLATFORMS)
post_type = st.sidebar.selectbox("Post Type", POST_TYPES, index=5)
campaign_goal = st.sidebar.selectbox("Campaign Goal", CAMPAIGN_GOALS, index=2)
audience = st.sidebar.text_input("Audience", "UK skincare buyers")
hashtags = st.sidebar.text_input("Optional Hashtags", "#skincare #glow")

custom_brand = None
if brand == "Custom Brand":
    st.sidebar.subheader("Custom Brand Profile")
    custom_brand = {
        "brand_name": st.sidebar.text_input("Brand name"),
        "industry": st.sidebar.text_input("Industry"),
        "desired_tone": st.sidebar.text_input("Desired tone", "premium, helpful").split(","),
        "keywords": st.sidebar.text_input("Brand keywords", "quality, service, trusted").split(","),
        "avoid_words": st.sidebar.text_input("Words to avoid", "cheap, fake").split(","),
        "cta_examples": st.sidebar.text_input("CTA examples", "Learn more, Contact us").split(","),
        "visual_style": st.sidebar.text_input("Visual style", "Premium modern layout"),
    }

caption = st.text_area(
    "Caption",
    "A soft, clean glow starts with gentle skincare made for your daily self-care routine. Discover our natural clay and serum range for fresh, calm-looking skin. Shop now.",
    height=180,
)
competitor_caption = st.text_area("Competitor Caption Optional", "", height=100)

if st.button("Analyze Caption", type="primary"):
    result = analyze_caption(
        {
            "brand": brand,
            "platform": platform,
            "post_type": post_type,
            "campaign_goal": campaign_goal,
            "caption": caption,
            "audience": audience,
            "hashtags": hashtags,
            "competitor_caption": competitor_caption,
            "custom_brand": custom_brand,
        }
    )

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Overall Score", f"{result['overall_score']}/100", result["score_label"])
    col2.metric("Publish Readiness", result["publish_readiness"])
    col3.metric("Brand Voice", f"{result['brand_voice_score']}/100")
    col4.metric("Hook", f"{result['hook_analysis']['hook_score']}/10")

    st.progress(result["overall_score"] / 100)

    st.subheader("Advanced Scores")
    adv1, adv2, adv3, adv4 = st.columns(4)
    adv1.metric("Hashtags", f"{result['hashtag_analysis']['hashtag_score']}/5")
    adv2.metric("Readability", f"{result['readability_analysis']['readability_score']}/10")
    adv3.metric("Platform Fit", f"{result['platform_fit']['score']}/10")
    adv4.metric("Risk", result["risk_analysis"]["risk_level"])

    with st.expander("Detailed Analysis", expanded=True):
        st.write("Tone:", ", ".join(result["tone_analysis"]["detected_tone"]))
        st.write("Matched keywords:", ", ".join(result["keyword_analysis"]["matched_keywords"]) or "None")
        st.write("Content type:", result["content_type"])
        st.write("Content pillar:", result["content_pillar"])
        st.write("Campaign goal:", result["campaign_goal_relevance"]["comment"])
        st.write("Caption quality:", result["caption_quality"]["comment"])
        st.write("Hashtags:", result["hashtag_analysis"]["comment"])
        st.write("Readability:", result["readability_analysis"]["comment"])
        st.write("Platform fit:", result["platform_fit"]["comment"])
        st.write("Risk:", result["risk_analysis"]["comment"])

    with st.expander("Score Breakdown"):
        for label, item in result["score_breakdown"].items():
            st.write(f"{label}: {item['score']}/{item['max_score']}")

    col4, col5 = st.columns(2)
    with col4:
        st.subheader("Problems Found")
        if result["problems"]:
            for problem in result["problems"]:
                st.warning(problem)
        else:
            st.success("No major problems found.")

    with col5:
        st.subheader("Suggestions")
        for suggestion in result["suggestions"]:
            st.info(suggestion)

    st.subheader("Improved Caption")
    st.write(result["improved_caption"])
    st.subheader("Campaign Brief")
    st.json(result["campaign_brief"])
    st.subheader("Design Direction")
    st.json(result["design_direction"])
    st.subheader("Calendar Suggestion")
    st.json(result["calendar_suggestion"])
    if result["competitor_comparison"]["available"]:
        st.subheader("Competitor Comparison")
        st.write(result["competitor_comparison"]["summary"])
    st.subheader("Final Recommendation")
    st.success(result["final_recommendation"])
