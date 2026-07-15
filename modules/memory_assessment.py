"""
Memory Assessment Module (Prototype)
=======================================
A simple sequence-recall game used as a proxy exercise for short-term
memory assessment. Score is stored in session_state for the dashboard.

TODO:
- Replace with a validated cognitive test format if moving beyond prototype
- Add difficulty scaling / multiple rounds
"""

import random
import streamlit as st


def render():
    st.title("Memory Assessment (Prototype)")
    st.write("Memorize the sequence of numbers shown, then enter it back in order.")

    if "memory_sequence" not in st.session_state:
        st.session_state["memory_sequence"] = [random.randint(0, 9) for _ in range(5)]
        st.session_state["memory_revealed"] = True

    if st.session_state.get("memory_revealed"):
        st.info(" ".join(str(n) for n in st.session_state["memory_sequence"]))
        if st.button("I've memorized it — hide and continue"):
            st.session_state["memory_revealed"] = False
            st.rerun()
        return

    user_input = st.text_input("Enter the sequence (space-separated numbers)")

    if st.button("Submit"):
        correct = st.session_state["memory_sequence"]
        try:
            attempt = [int(x) for x in user_input.split()]
        except ValueError:
            st.error("Please enter numbers separated by spaces.")
            return

        score = sum(1 for a, b in zip(attempt, correct) if a == b)
        total = len(correct)

        st.session_state.setdefault("scores", {})["memory"] = score / total

        st.subheader("Result")
        st.write(f"**Score:** {score}/{total}")

        if st.button("Try a new sequence"):
            del st.session_state["memory_sequence"]
            st.rerun()
