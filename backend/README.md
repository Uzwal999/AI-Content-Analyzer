# EverVFX Backend API

FastAPI backend for the EverVFX AI Brand Content Analyzer. It performs local rule-based NLP analysis without paid APIs or external AI services.

## Run With Full App

From the project root:

```powershell
.\run_app.bat
```

## Run Backend Only

```powershell
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

API docs: `http://localhost:8000/docs`

## Endpoints

- `GET /` health message
- `GET /brands` preset brand profiles
- `POST /analyze` full content analysis report

## Analyzer Modules

- `analyzer.py`: orchestration and scoring
- `tone_detector.py`: tone detection
- `cta_analyzer.py`: CTA detection and recommendations
- `hashtag_analyzer.py`: hashtag quality
- `hook_analyzer.py`: first-line hook analysis
- `campaign_brief.py`: campaign brief generation
- `design_direction.py`: visual direction generation
- `calendar_suggestions.py`: content calendar suggestions
- `competitor_analyzer.py`: competitor caption comparison

