#!/bin/bash
# startup.sh
# Streamlit Cloud runs this instead of `streamlit run app.py`
# if you set it as the custom command.
#
# It starts FastAPI (port 8000) in the background,
# then starts Streamlit (port 8501) in the foreground.

echo "Starting FastAPI judge on port 8501..."
uvicorn api:app --host 0.0.0.0 --port 8501
