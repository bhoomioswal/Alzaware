"""
Cognitive Assessment Module (Prototype)
==========================================
A short multiple-choice quiz used as a proxy exercise for general
cognitive engagement (attention, orientation, simple reasoning).

TODO:
- Replace with a validated instrument (e.g., adapted MMSE-style items)
  if extending beyond prototype stage — requires appropriate licensing
  and clinical oversight
- Randomize / expand the question bank
"""

import streamlit as st

QUESTIONS = [
    {
        "q": "What day of the week is it today?",
        "options": ["Cannot recall", "I know it"],
        "correct": "I know it",
    },
    {
        "q": "Count backwards from 20 to 15. Did you complete it correctly?",
        "options": ["No", "Yes"],
        "correct": "Yes",
    },
    {
        "q": "Which of these is the odd one out: Apple, Banana, Carrot, Mango?",
        "options": ["Apple", "Banana", "Carrot", "Mango"],
        "correct": "Carrot",
    },
]


def render():
    st.title("Cognitive Assessment (Prototype)")
    st.write("Answer the following short questions.")

    answers = {}
    for i, item in enumerate(QUESTIONS):
        answers[i] = st.radio(item["q"], item["options"], key=f"cog_{i}")

    if st.button("Submit Assessment"):
        score = sum(1 for i, item in enumerate(QUESTIONS) if answers[i] == item["correct"])
        total = len(QUESTIONS)

        st.session_state.setdefault("scores", {})["cognitive"] = score / total

        st.subheader("Result")
        st.write(f"**Score:** {score}/{total}")
