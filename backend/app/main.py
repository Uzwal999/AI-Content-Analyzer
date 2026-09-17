"""FastAPI entrypoint for the AI Brand Content Analyzer."""

from __future__ import annotations

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .analyzer import analyze_caption
from .brand_profiles import get_brand_profiles
from .models import AnalyzeRequest, AnalyzeResponse


app = FastAPI(
    title="EverVFX AI Brand Content Analyzer API",
    description="Local rule-based API for analyzing brand fit, captions, hooks, CTAs, and campaign readiness.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ],
    allow_origin_regex=r"^http://(localhost|127\.0\.0\.1):\d+$",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root() -> dict[str, str]:
    return {"message": "EverVFX AI Brand Content Analyzer API is running."}


@app.get("/brands")
def read_brands() -> dict[str, dict]:
    return get_brand_profiles()


@app.post("/analyze", response_model=AnalyzeResponse)
def analyze(request: AnalyzeRequest) -> dict:
    return analyze_caption(request.model_dump())
