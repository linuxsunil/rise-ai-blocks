"""
Live Branching — FastAPI Judge Proxy
=====================================
Receives learner responses from Rise HTML,
calls Claude API, returns branch judgment as JSON.

Runs on port 8501 — Streamlit Cloud's public port.
"""

import os
import json
import httpx
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, HTMLResponse
from pydantic import BaseModel
from typing import Optional

# ─── App ─────────────────────────────────────────────────────────────────────

app = FastAPI(title="Live Branching Judge", docs_url=None, redoc_url=None)

# ─── CORS ─────────────────────────────────────────────────────────────────────
# Add your Rise / LMS domains here
ALLOWED_ORIGINS = [
    "https://rise.articulate.com",
    "https://rise360.articulate.com",
    "http://localhost",
    "http://127.0.0.1",
    "*",   # ← tighten this for production; fine for internal/piloting
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_methods=["POST", "OPTIONS"],
    allow_headers=["Content-Type"],
)

# ─── Prompt ──────────────────────────────────────────────────────────────────

SYSTEM_PROMPT = """You are a branching judge for a workplace compliance scenario exercise.

Your job: evaluate a learner's written response to a compliance scenario and return a structured judgment.

BRANCHES:
A = Correct. Policy-compliant, best practice followed, all key steps present.
B = Partially correct. Main intent is right but a minor procedural gap or missed step.
C = Incorrect. Wrong approach taken, misunderstands the policy, or key steps missing.
D = Serious violation. Action described would create legal/ethical/security risk.

SCORING:
A = +15 to +20 points (reward thoroughness)
B = +5 to +10 points
C = -5 to -10 points
D = -15 to -20 points

RULES:
- Judge the substance, not writing quality or length
- Reference the learner's specific words in feedback_text where possible
- feedback_text: 2-3 sentences. Constructive, not punitive for C/D
- reasoning: one concise sentence explaining the judgment
- Be consistent — apply the rubric strictly

OUTPUT: Return ONLY valid JSON. No prose, no markdown fences, nothing outside the JSON.

{
  "branch_id": "A" | "B" | "C" | "D",
  "feedback_text": "string",
  "score_delta": integer,
  "reasoning": "string"
}"""

# ─── Models ──────────────────────────────────────────────────────────────────

class PriorDecision(BaseModel):
    scenario_id: str
    branch_id: str

class JudgeRequest(BaseModel):
    scenario_context: str
    learner_response: str
    scenario_rubric: Optional[str] = None
    prior_decisions: Optional[list[PriorDecision]] = []

class JudgeResponse(BaseModel):
    branch_id: str
    feedback_text: str
    score_delta: int
    reasoning: str

# ─── Helpers ─────────────────────────────────────────────────────────────────

def make_fallback(reason: str = "Technical error") -> dict:
    return {
        "branch_id": "C",
        "feedback_text": "There was a technical issue evaluating your response. Your answer has been recorded for facilitator review.",
        "score_delta": 0,
        "reasoning": f"Technical fallback: {reason}"
    }

def parse_judgment(text: str) -> dict:
    """Try to extract valid JSON from Claude's response."""
    text = text.strip()

    # Direct parse
    try:
        return json.loads(text)
    except Exception:
        pass

    # Extract JSON block
    import re
    match = re.search(r'\{[\s\S]*\}', text)
    if match:
        try:
            return json.loads(match.group(0))
        except Exception:
            pass

    # Manual field extraction fallback
    branch_match  = re.search(r'"branch_id"\s*:\s*"([ABCD])"', text)
    feedback_match = re.search(r'"feedback_text"\s*:\s*"([^"]+)"', text)
    score_match   = re.search(r'"score_delta"\s*:\s*(-?\d+)', text)
    reason_match  = re.search(r'"reasoning"\s*:\s*"([^"]+)"', text)

    if branch_match:
        return {
            "branch_id":     branch_match.group(1),
            "feedback_text": feedback_match.group(1) if feedback_match else "Your response has been evaluated.",
            "score_delta":   int(score_match.group(1)) if score_match else 0,
            "reasoning":     reason_match.group(1) if reason_match else ""
        }

    return make_fallback("Could not parse Claude response")

def validate_judgment(j: dict) -> dict:
    """Ensure all fields are present and within bounds."""
    if j.get("branch_id") not in ["A", "B", "C", "D"]:
        j["branch_id"] = "C"
    j["score_delta"]   = max(-20, min(20, int(j.get("score_delta", 0))))
    j["feedback_text"] = str(j.get("feedback_text", ""))[:500]
    j["reasoning"]     = str(j.get("reasoning", ""))[:200]
    return j

# ─── Routes ──────────────────────────────────────────────────────────────────

@app.get("/")
async def health():
    api_key_set = bool(os.environ.get("ANTHROPIC_API_KEY", ""))
    return HTMLResponse(content=f"""
<!DOCTYPE html><html><head><title>Live Branching Judge</title>
<style>body{{font-family:sans-serif;max-width:600px;margin:60px auto;padding:0 20px;background:#f8f9fa}}
h1{{color:#1a1a2e}}code{{background:#e9ecef;padding:2px 8px;border-radius:4px;font-size:14px}}
.ok{{color:#198754}}.warn{{color:#dc3545}}.box{{background:#fff;border:1px solid #dee2e6;border-radius:8px;padding:24px;margin:16px 0}}</style>
</head><body>
<h1>⚡ Live Branching Judge</h1>
<p>Proxy service for Rise 360 — AI-powered compliance scenario branching.</p>
<div class="box">
  <p>API key: <strong class="{'ok'>✅ set' if api_key_set else 'warn'>❌ not set'}</strong></p>
  <p>Judge endpoint: <code>POST /judge</code></p>
</div>
<p style="color:#6c757d;font-size:13px">Built by Sunil · <a href="https://github.com/linuxsunil/rise-ai-blocks">GitHub</a></p>
</body></html>""")

@app.post("/judge")
async def judge(req: JudgeRequest):

    api_key = os.environ.get("ANTHROPIC_API_KEY", "")
    if not api_key:
        return JSONResponse(
            status_code=500,
            content={"error": "ANTHROPIC_API_KEY not set", "fallback": make_fallback("API key missing")}
        )

    # Validate input
    if not req.scenario_context or not req.learner_response:
        return JSONResponse(status_code=400, content={"error": "Missing required fields"})

    if len(req.learner_response) < 5 or len(req.learner_response) > 1000:
        return JSONResponse(status_code=400, content={"error": "Response must be 5–1000 characters"})

    # Build user message
    prior_ctx = "\n".join(
        f"  - Scenario {d.scenario_id}: Branch {d.branch_id}"
        for d in (req.prior_decisions or [])
    ) or "  None"

    user_message = f"""Scenario:
{req.scenario_context}

{f"Expected approach:{chr(10)}{req.scenario_rubric}{chr(10)}" if req.scenario_rubric else ""}
Prior decisions this session:
{prior_ctx}

Learner's response:
\"{req.learner_response}\""""

    # Call Anthropic
    try:
        async with httpx.AsyncClient(timeout=20.0) as client:
            resp = await client.post(
                "https://api.anthropic.com/v1/messages",
                headers={
                    "x-api-key":         api_key,
                    "anthropic-version": "2023-06-01",
                    "content-type":      "application/json",
                },
                json={
                    "model":      "claude-haiku-4-5",
                    "max_tokens": 400,
                    "system":     SYSTEM_PROMPT,
                    "messages":   [{"role": "user", "content": user_message}]
                }
            )

        if resp.status_code != 200:
            return JSONResponse(
                status_code=200,
                content={"error": "Upstream API error", "fallback": make_fallback(f"HTTP {resp.status_code}")}
            )

        data     = resp.json()
        raw_text = data["content"][0]["text"]
        judgment = validate_judgment(parse_judgment(raw_text))
        return JSONResponse(content=judgment)

    except httpx.TimeoutException:
        return JSONResponse(status_code=200, content=make_fallback("Request timed out"))
    except Exception as e:
        return JSONResponse(status_code=200, content=make_fallback(str(e)[:80]))
