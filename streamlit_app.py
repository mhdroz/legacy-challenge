# Streamlit front‑end for Safety‑First Triage POC
# Save this file as streamlit_app.py and run:  streamlit run streamlit_app.py

import os
import requests
import streamlit as st
from streamlit.components.v1 import html

# -----------------------------------------------------------------------------
# Config
# -----------------------------------------------------------------------------
API_URL = os.getenv("TRIAGE_API_URL", "http://localhost:8000")  # Point to FastAPI

# Simple mapping for risk bucket → color
RISK_COLORS = {
    0: "green",
    1: "orange",
    2: "red",
    3: "red",
    4: "red",
}

#USERNAME = st.secrets.get("auth", {}).get("username", "admin")
#PASSWORD = st.secrets.get("auth", {}).get("password", "changeme")

def _get_creds():
    """Retrieve creds from Streamlit secrets or env vars; fallback to defaults."""
    try:
        user = st.secrets["auth"]["username"]
        pwd = st.secrets["auth"]["password"]
    except Exception:
        user = os.getenv("TRIAGE_UI_USER", "admin")
        pwd = os.getenv("TRIAGE_UI_PWD", "changeme")
    return user, pwd

USERNAME, PASSWORD = _get_creds()


def login_gate():
    if "auth_ok" in st.session_state and st.session_state["auth_ok"]:
        return True

    st.title("🔒 Login")
    user = st.text_input("Username")
    pwd = st.text_input("Password", type="password")
    if st.button("Log in"):
        if user == USERNAME and pwd == PASSWORD:
            st.session_state["auth_ok"] = True
            st.rerun()
        else:
            st.error("Invalid credentials – try again.")
    st.stop()


# Run login check
login_gate()

st.set_page_config(page_title="Safety‑First Triage Assistant", page_icon="🩺", layout="centered")

st.title("🩺 Safety‑First Triage Assistant")

user_text = st.text_area("Paste the patient's statement or description", height=200)

if st.button("Assess & Advise", type="primary"):
    if not user_text.strip():
        st.warning("Please enter some text first.")
        st.stop()

    with st.spinner("Calling risk model & LLM…"):
        try:
            resp = requests.post(f"{API_URL}/advise", json={"text": user_text}, timeout=60)
            resp.raise_for_status()
            data = resp.json()
            #print(data)
        except Exception as e:
            st.error(f"Error contacting API: {e}")
            st.stop()

    # ------------------------------------------------------------------
    # Display results
    # ------------------------------------------------------------------
    bucket = data["risk"]["risk score"]
    conf = data["risk"]["confidence"] * 100
    color = RISK_COLORS.get(bucket, "gray")

    st.markdown(f"### Risk Level: <span style='color:{color}; font-weight:600'>{bucket} ({conf:.1f}% confidence)</span>", unsafe_allow_html=True)

    st.markdown("---")
    st.subheader("Suggested Next Steps")
    st.write(data["advice"])

    # Accordion for similar cases
    with st.expander(f"Similar Cases ({len(data['snippets'])})"):
        for snippet in data["snippets"]:
            st.markdown(
                f"<blockquote style='border-left: 4px solid #ddd; margin: 0 0 1rem; padding-left: .75rem; font-style: italic;'>{snippet}</blockquote>",
                unsafe_allow_html=True,
            )

if st.sidebar.button("Logout"):
    st.session_state.clear()
    st.rerun()