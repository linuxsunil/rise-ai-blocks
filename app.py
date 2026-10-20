"""
Live Branching — Streamlit Status Dashboard
============================================
Streamlit Cloud requires an app.py.
This shows the proxy status + instructions.
The real work is done by api.py on port 8000.
"""

import streamlit as st
import httpx
import os

st.set_page_config(
    page_title="Live Branching Proxy",
    page_icon="⚡",
    layout="centered"
)

st.title("⚡ Live Branching Judge")
st.caption("Proxy service for Rise eLearning — AI-powered compliance scenario branching")

st.divider()

# ─── Health check ─────────────────────────────────────────────────────────────
st.subheader("Service status")

col1, col2 = st.columns(2)

with col1:
    api_key_set = bool(os.environ.get("ANTHROPIC_API_KEY", ""))
    if api_key_set:
        st.success("✅ ANTHROPIC_API_KEY set")
    else:
        st.error("❌ ANTHROPIC_API_KEY not set")
        st.caption("Add it in App Settings → Secrets")

with col2:
    try:
        r = httpx.get("http://localhost:8000/", timeout=3)
        if r.status_code == 200:
            st.success("✅ Judge API running")
        else:
            st.warning(f"⚠️ API responded {r.status_code}")
    except Exception:
        st.warning("⏳ API starting up…")
        st.caption("Refresh in a few seconds")

st.divider()

# ─── Endpoint info ────────────────────────────────────────────────────────────
st.subheader("Your proxy endpoint")

app_url = st.secrets.get("APP_URL", "") if hasattr(st, "secrets") else ""

try:
    app_url = st.secrets.get("APP_URL", "")
except Exception:
    app_url = ""

if app_url:
    judge_url = f"{app_url.rstrip('/')}/judge"  # via nginx proxy path
    st.code(judge_url, language=None)
    st.caption("Paste this URL into PROXY_URL in rise-live-branching.html")
else:
    st.info("Add your app URL to Secrets as APP_URL to display the full endpoint here.")
    st.code("https://your-app-name.streamlit.app/proxy/judge", language=None)
    st.caption("Replace with your actual Streamlit Cloud URL + /proxy/judge")

st.divider()

# ─── Quick test ───────────────────────────────────────────────────────────────
st.subheader("Quick test")

with st.expander("Test the judge endpoint"):
    test_response = st.text_area(
        "Sample learner response",
        value="I would not share the data until I confirmed the vendor has a signed data processing agreement. I would email the data privacy officer to verify.",
        height=100
    )

    if st.button("Test judge", type="primary"):
        with st.spinner("Calling judge…"):
            try:
                r = httpx.post(
                    "http://localhost:8000/judge",
                    json={
                        "scenario_context": "A colleague asks you to share 500 customer records with an unverified vendor.",
                        "learner_response": test_response,
                        "scenario_rubric": "Correct: verify vendor approval, do not share until confirmed, escalate if uncertain."
                    },
                    timeout=20
                )
                result = r.json()
                branch = result.get("branch_id", "?")
                colors = {"A": "🟢", "B": "🟡", "C": "🔴", "D": "🔴"}
                st.write(f"{colors.get(branch, '⚪')} **Branch {branch}** — Score delta: {result.get('score_delta', 0):+d}")
                st.write(result.get("feedback_text", ""))
                st.caption(f"Reasoning: {result.get('reasoning', '')}")
            except Exception as e:
                st.error(f"Error: {e}")

st.divider()

# ─── Setup instructions ───────────────────────────────────────────────────────
with st.expander("Setup instructions"):
    st.markdown("""
**1. Add your API key**
In Streamlit Cloud → your app → Settings → Secrets, add:
```toml
ANTHROPIC_API_KEY = "sk-ant-..."
APP_URL = "https://your-app-name.streamlit.app"
```

**2. Update Rise HTML**
In `rise-live-branching.html`, set:
```js
const PROXY_URL = "https://your-app-name.streamlit.app/proxy/judge";
```

**3. Add your Rise domain to CORS**
In `api.py`, add your Rise/LMS URL to `ALLOWED_ORIGINS`.

**4. That's it.** Drop the HTML into a Rise code block.
""")
