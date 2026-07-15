"""
User Registration Module
=========================
Collects basic participant details before proceeding to the assessment
modules. In this prototype, data is kept in `st.session_state` only —
no persistent database is wired up yet.

TODO:
- Connect to a real backend (e.g., Firebase / SQLite) if persistence is needed
- Add input validation (age range, required fields, consent checkbox)
"""

import streamlit as st


def render():
    st.title("Welcome to AlzAware")
    st.write(
        "Please fill in your details to begin the prototype assessment. "
        "This information is used only within this session."
    )

    with st.form("registration_form"):
        name = st.text_input("Full Name")
        age = st.number_input("Age", min_value=18, max_value=110, step=1)
        gender = st.selectbox("Gender", ["Prefer not to say", "Male", "Female", "Other"])
        consent = st.checkbox(
            "I understand this is a research prototype and not a medical diagnostic tool."
        )
        submitted = st.form_submit_button("Continue")

    if submitted:
        if not name or not consent:
            st.error("Please enter your name and confirm the consent checkbox.")
            return

        st.session_state["user"] = {"name": name, "age": age, "gender": gender}
        st.success(f"Welcome, {name}! Use the sidebar to proceed to an assessment module.")
