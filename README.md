# EverVFX AI Brand Content Analyzer

Premium SaaS-style AI tool built for EverVFX client demos, agency pitching, portfolio screenshots, and internship interviews.

The app analyzes social media captions before publishing and returns brand fit, hook strength, tone, CTA quality, keyword match, hashtag quality, platform suggestions, campaign brief, design direction, calendar suggestions, competitor comparison, improved captions, and a professional PDF report.

No OpenAI, Gemini, paid APIs, or external AI APIs are used. The analysis runs locally through modular Python rule-based NLP logic.

## EverVFX Positioning

EverVFX AI Brand Content Analyzer feels like an internal agency intelligence tool for brands, social media managers, designers, marketers, and creative teams. It helps turn rough captions into client-ready campaign direction.

## Features

- Premium dark EverVFX dashboard UI
- EverVFX logo branding
- Brand selector and custom brand profiles
- Platform, post type, campaign goal, audience, caption, hashtag, and competitor caption inputs
- Agency Mode with client/report details
- Brand Match Score and Brand Voice Score
- Hook strength analysis
- Tone, CTA, keyword, hashtag, caption quality, and campaign relevance scoring
- Platform-specific suggestions
- Problems and practical improvements
- Improved caption generator
- Before vs after comparison
- Campaign brief generator
- Design direction generator
- Content calendar suggestions
- Competitor comparison mode
- JSON export
- Professional PDF client report export
- Optional Streamlit dashboard
- One-click Windows launcher

## Tech Stack

- Frontend: Next.js, TypeScript, Tailwind CSS, lucide-react, @react-pdf/renderer
- Backend: FastAPI, Python, Pydantic
- AI/ML Logic: Local Python rule-based NLP, modular for future ML models
- Demo: Streamlit

## Architecture

```text
frontend/             Next.js SaaS dashboard
backend/app/          FastAPI API and reusable Python analyzer modules
streamlit_dashboard/  Optional Python demo UI
```

The frontend sends requests to FastAPI `POST /analyze`. FastAPI validates the request, calls the reusable Python analyzer, and returns a detailed report JSON.

## Scoring Logic

Total score is calculated out of 100:

- Brand keyword match: 20 points
- Tone match: 15 points
- CTA strength: 15 points
- Caption clarity and quality: 15 points
- Campaign goal relevance: 10 points
- Hook strength: 10 points
- Hashtag quality: 5 points
- Avoided bad words and risky language: 10 points

Publish readiness:

- 80-100: Ready to Publish
- 60-79: Good, Minor Improvements
- 40-59: Needs Revision
- Below 40: Not Ready

## Easiest Local Run On Windows

From the project root:

```powershell
.\run_app.bat
```

The launcher creates/uses the backend virtual environment, installs missing dependencies, starts FastAPI, starts Next.js, and opens the app.

## Manual Backend Run

```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

API docs: `http://localhost:8000/docs`

## Manual Frontend Run

```powershell
cd frontend
npm install
npm run dev
```

Frontend: `http://localhost:3000`

Local frontend API setting:

```env
NEXT_PUBLIC_API_URL=http://127.0.0.1:8000
```

## Fix: Unable To Connect To Analysis API

If the frontend shows an API connection error on another PC:

1. Use the launcher from the project root:

```powershell
.\run_app.bat
```

2. Keep both PowerShell windows open.

3. Open the backend health URL shown by the launcher. It should return:

```json
{"message":"EverVFX AI Brand Content Analyzer API is running."}
```

4. If running manually, start backend first:

```powershell
cd backend
.\.venv\Scripts\activate
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

5. Then start frontend with the matching API URL:

```powershell
cd frontend
$env:NEXT_PUBLIC_API_URL="http://127.0.0.1:8000"
npm run dev
```

If the frontend runs on `3001` or another port, the backend now allows local development ports automatically.

## Vercel Deployment

This repo is prepared for Vercel frontend deployment with root-level `vercel.json`.

In Vercel:

1. Import `Uzwal999/AI-Content-Analyzer`.
2. Keep the repository root as the project root.
3. Vercel will run:
   - Install: `npm --prefix frontend ci`
   - Build: `npm --prefix frontend run build`
   - Output: `frontend/.next`
4. Add environment variable:

```env
NEXT_PUBLIC_API_URL=https://your-hosted-fastapi-backend-url
```

Important: Vercel deploys the Next.js frontend. The FastAPI backend should be hosted separately on Render, Railway, Fly.io, VPS, or another Python API host. For local use, keep `NEXT_PUBLIC_API_URL=http://localhost:8000`.

## Streamlit Dashboard

```powershell
pip install -r backend/requirements.txt streamlit
streamlit run streamlit_dashboard/app.py
```

## PDF Report Feature

The frontend uses `@react-pdf/renderer` to export a client-ready agency report with:

- EverVFX branding
- Client and campaign details
- Original caption
- Score summary
- Hook, tone, CTA, keyword, hashtag, and quality analysis
- Problems and suggestions
- Improved caption
- Campaign brief
- Design direction
- Calendar suggestion
- Competitor comparison
- Final recommendation

## Future Improvements

- Real AI API integration
- Image/design analysis
- Brand guideline upload
- Database for saving reports
- Login system
- Team workspace
- Historical analytics
- ML model trained on social media performance data
- PDF design improvements
- Client portal
- Canva/Figma integration

## Portfolio And Client Pitching Use

This project demonstrates full-stack development, API design, modular Python analysis, TypeScript UI architecture, SaaS-style design, PDF generation, and a practical marketing/agency use case.
