"""
Dashboard Module (Prototype)
==============================
Summarizes results collected across the session (memory and cognitive
assessment scores). MRI/facial/speech results are shown per-module and
are not yet aggregated here.

TODO:
- Add a combined, weighted "risk indicator" once methodology is finalized
  and validated — clearly label it as illustrative, not diagnostic
- Add exportable session summary (PDF/CSV)
"""

import streamlit as st


def render():
    st.title("Dashboard (Prototype)")

    user = st.session_state.get("user")
    if user:
        st.write(f"**Participant:** {user['name']} | Age: {user['age']} | Gender: {user['gender']}")
    else:
        st.info("No registration info found. Visit the Home / Registration page first.")

    scores = st.session_state.get("scores", {})
    if not scores:
        st.info("No assessment scores yet. Complete the Memory or Cognitive assessments.")
        return

    st.subheader("Session Summary")
    for name, value in scores.items():
        st.write(f"**{name.title()} score:** {value * 100:.1f}%")

    st.progress(sum(scores.values()) / len(scores))
    st.caption(
        "This summary is illustrative only and does not represent a clinical "
        "risk score."
    )
