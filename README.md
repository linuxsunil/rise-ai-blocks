# rise-ai-blocks

AI-powered Rise 360 code block templates — live branching, roleplay coach, scenario judge.  
Proxy backend for Claude API integration via Streamlit Cloud.

## Structure

```
rise-ai-blocks/
├── api.py              # FastAPI judge endpoint (port 8000)
├── app.py              # Streamlit status dashboard (port 8501)
├── startup.sh          # Boots both services on Streamlit Cloud
├── requirements.txt    # Python dependencies
└── templates/
    └── live-branching.html   # Rise code block — AI-judged compliance scenarios
```

## Deploy to Streamlit Cloud

1. Go to [share.streamlit.io](https://share.streamlit.io) → New app
2. Pick this repo, branch `main`, file `app.py`
3. Expand **Advanced settings**:
   - Custom startup command: `bash startup.sh`
   - Secrets:
     ```toml
     ANTHROPIC_API_KEY = "sk-ant-..."
     APP_URL = "https://your-app-name.streamlit.app"
     ```
4. Deploy

Your judge endpoint: `https://your-app-name.streamlit.app/proxy/judge`

## Use in Rise

1. Open `templates/live-branching.html`
2. Set `PROXY_URL` to your deployed endpoint
3. Insert → Code Block in Rise → paste the HTML

## Templates

| Template | File | Status |
|---|---|---|
| Live Branching | `templates/live-branching.html` | ✅ Ready |
| Roleplay Coach | coming soon | 🔜 |
| Confidence MCQ | coming soon | 🔜 |
