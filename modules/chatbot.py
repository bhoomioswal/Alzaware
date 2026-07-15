"""
AI Chatbot Module (Prototype)
===============================
A lightweight FAQ-style chatbot to answer general, non-diagnostic
questions about the AlzAware prototype and Alzheimer's awareness.

TODO:
- Optionally swap the rule-based responder for an API-backed model
- Keep responses strictly educational — never diagnostic or prescriptive
"""

import streamlit as st

FAQ = {
    "what is alzaware": "AlzAware is a research prototype combining multiple AI modules "
    "(MRI, facial emotion, speech emotion, memory and cognitive assessments) "
    "to explore early, non-clinical indicators related to cognitive health.",
    "is this a diagnosis": "No. AlzAware is a prototype for research and educational purposes "
    "only. It does not provide medical diagnosis. Please consult a qualified "
    "healthcare professional for any medical concerns.",
    "what datasets are used": "The prototype's models were trained/explored using public "
    "datasets such as OASIS (MRI), FER-2013 (facial emotion), and RAVDESS (speech emotion). "
    "See datasets/dataset_links.md.",
}


def simple_responder(user_message: str) -> str:
    msg = user_message.lower().strip()
    for key, response in FAQ.items():
        if key in msg:
            return response
    return (
        "I'm a prototype FAQ assistant and can't answer that yet. "
        "Try asking about AlzAware, the datasets used, or whether this provides a diagnosis."
    )


def render():
    st.title("AI Chatbot (Prototype)")
    st.caption("Rule-based FAQ assistant — not a medical advisor.")

    if "chat_history" not in st.session_state:
        st.session_state["chat_history"] = []

    user_message = st.chat_input("Ask a question about AlzAware...")

    if user_message:
        response = simple_responder(user_message)
        st.session_state["chat_history"].append(("user", user_message))
        st.session_state["chat_history"].append(("assistant", response))

    for role, text in st.session_state["chat_history"]:
        with st.chat_message(role):
            st.write(text)
