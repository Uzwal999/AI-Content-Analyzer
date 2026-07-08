# Streamlit Dashboard

Optional quick demo for testing the Python analyzer without the Next.js frontend.

## Run

From the project root:

```bash
pip install -r backend/requirements.txt streamlit
streamlit run streamlit_dashboard/app.py
```

The Streamlit app imports `backend/app/analyzer.py`, so the scoring logic stays shared with the FastAPI API.

