<div align="center">

```
██████╗ ██╗███████╗███████╗      █████╗ ██╗
██╔══██╗██║██╔════╝██╔════╝     ██╔══██╗██║
██████╔╝██║███████╗█████╗       ███████║██║
██╔══██╗██║╚════██║██╔══╝       ██╔══██║██║
██║  ██║██║███████║███████╗     ██║  ██║██║
╚═╝  ╚═╝╚═╝╚══════╝╚══════╝     ╚═╝  ╚═╝╚═╝
```

**AI-powered interactive templates for Rise 360**  
_Learners type. Claude judges. Course branches._

[![Streamlit](https://img.shields.io/badge/Backend-Streamlit_Cloud-FF4B4B?style=flat-square&logo=streamlit&logoColor=white)](https://streamlit.io/cloud)
[![FastAPI](https://img.shields.io/badge/API-FastAPI-009688?style=flat-square&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![Claude](https://img.shields.io/badge/AI-Claude_Haiku-D4A574?style=flat-square)](https://anthropic.com)
[![Rise 360](https://img.shields.io/badge/Platform-Rise_360-FF6B35?style=flat-square)](https://articulate.com/360/rise)

</div>

---

## ✨ How it works

```
┌─────────────────────────────────────────────────────────────────┐
│                        RISE 360 COURSE                          │
│                                                                 │
│   📋 Scenario                                                   │
│      │                                                          │
│      ▼                                                          │
│   ✍️  Learner types free-text response                          │
│      │                                                          │
│      ▼                                                          │
│   🌐 fetch() → Streamlit proxy → Claude Haiku                  │
│                        │                                        │
│          ┌─────────────┴─────────────┐                         │
│          ▼             ▼             ▼             ▼            │
│        🟢 A          🟡 B          🔴 C          🚨 D           │
│      Correct        Partial      Incorrect     Violation        │
│     (+15–20)        (+5–10)      (-5–10)      (-15–20)          │
│          │                                                      │
│          ▼                                                      │
│   📊 Consequence view → Debrief → LMS score via postMessage    │
└─────────────────────────────────────────────────────────────────┘
```

---

## 📁 Structure

```
rise-ai-blocks/
├── api.py                      # FastAPI judge endpoint  (port 8000)
├── app.py                      # Streamlit dashboard     (port 8501)
├── startup.sh                  # Boots both on Streamlit Cloud
├── requirements.txt
└── templates/
    └── live-branching.html     # Drop straight into a Rise Code Block
```

---

## 🚀 Deploy to Streamlit Cloud

> **One-time setup — ~5 minutes**

**1 · Push this repo** (already done if you're reading this on GitHub)

**2 · New app on [share.streamlit.io](https://share.streamlit.io)**
- Repo: `linuxsunil/rise-ai-blocks` · Branch: `main` · File: `app.py`

**3 · Advanced settings**

| Field | Value |
|---|---|
| Custom startup command | `bash startup.sh` |

Secrets (paste as-is, fill in your values):
```toml
ANTHROPIC_API_KEY = "sk-ant-..."
APP_URL            = "https://your-app-name.streamlit.app"
```

**4 · Deploy** — your judge endpoint:

```
https://your-app-name.streamlit.app/proxy/judge
```

---

## 🎓 Use in Rise

```
1. Open  templates/live-branching.html
2. Set   const PROXY_URL = "https://your-app-name.streamlit.app/proxy/judge";
3. Rise  → Insert → Code Block → paste the HTML → Preview
```

That's it. Learners see a compliance scenario, type their answer, and the course routes itself.

---

## 🗂️ Templates

| Template | File | Status |
|---|---|:---:|
| **Live Branching** | `templates/live-branching.html` | ✅ Ready |
| Roleplay Coach | `templates/roleplay-coach.html` | 🔜 Soon |
| Confidence MCQ | `templates/confidence-mcq.html` | 🔜 Soon |

---

## 🔒 Security

- API key lives in **Streamlit Secrets only** — never in the repo
- Repo is **private** on GitHub
- CORS allowlist restricts calls to Rise / LMS domains
- Course **never breaks**: if the proxy is unreachable, falls back to Branch C gracefully

---

---

## 👤 Created by

<div align="center">

```
 ____  _   _ _   _ ___ _     
/ ___|| | | | \ | |_ _| |    
\___ \| | | |  \| || || |    
 ___) | |_| | |\  || || |___ 
|____/ \___/|_| \_|___|_____|
```

**Sunil**  
*Senior Instructional Designer*

[![Fractal Analytics](https://img.shields.io/badge/Company-Fractal_Analytics-1E3A8A?style=flat-square)](https://fractal.ai)
[![Location](https://img.shields.io/badge/📍-Bengaluru,_India-orange?style=flat-square)]()
[![GitHub](https://img.shields.io/badge/GitHub-linuxsunil-181717?style=flat-square&logo=github)](https://github.com/linuxsunil)
[![Experience](https://img.shields.io/badge/Experience-10+_years_ID-green?style=flat-square)]()

</div>

> 10+ years designing learning experiences across AI/ML, compliance, and enterprise training.  
> Previously at **Thomson Reuters** and **NIIT Limited**.  
> Builds AI-native eLearning tools at the intersection of instructional science and LLMs —  
> grounded in ADDIE, SAM, Bloom's Taxonomy, and evidence-based design (Ruth Colvin Clark).

**Expertise:** Rise 360 · Storyline 360 · SCORM/xAPI · Claude API · Streamlit · Python  
**Courses on:** Coursera · Udemy

---

<div align="center">

*Built for [Articulate Rise 360](https://articulate.com/360/rise) · Powered by [Claude](https://anthropic.com)*  
*A personal project — not affiliated with Fractal Analytics*

</div>
