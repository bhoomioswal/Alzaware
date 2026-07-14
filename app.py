"""
AlzAware — Prototype Entry Point
=================================
A Streamlit application that ties together the multimodal AlzAware
assessment modules: registration, MRI-based risk prediction, facial
emotion recognition, speech emotion recognition, memory assessment,
cognitive assessment, and a summary dashboard.

Run with:
    streamlit run app.py

NOTE: This is a prototype/research scaffold. Model files referenced in
`models/` are NOT included in this repository — see models/README.md.
"""

import streamlit as st

from modules import (
    registration,
    mri_prediction,
    facial_emotion,
    speech_emotion,
    memory_assessment,
    cognitive_assessment,
    chatbot,
    dashboard,
)

st.set_page_config(
    page_title="AlzAware (Prototype)",
    page_icon="🧠",
    layout="wide",
)

PAGES = {
    "Home / Registration": registration,
    "MRI Risk Prediction": mri_prediction,
    "Facial Emotion Recognition": facial_emotion,
    "Speech Emotion Recognition": speech_emotion,
    "Memory Assessment": memory_assessment,
    "Cognitive Assessment": cognitive_assessment,
    "AI Chatbot": chatbot,
    "Dashboard": dashboard,
}


def main():
    st.sidebar.title("🧠 AlzAware")
    st.sidebar.caption("Prototype — research & educational use only")

    choice = st.sidebar.radio("Navigate", list(PAGES.keys()))

    st.sidebar.markdown("---")
    st.sidebar.warning(
        "This tool is a non-clinical prototype. It does not provide "
        "medical diagnosis or advice."
    )

    page_module = PAGES[choice]
    page_module.render()


if __name__ == "__main__":
    main()
