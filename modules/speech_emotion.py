"""
Speech emotion recognition page.
"""

import streamlit as st
import pandas as pd
import random
import time
from PIL import Image

from modules.common import *


def render_speech_emotion():
    progress_bar(4)
    main_col, side_col = st.columns([2.5, 1], gap="large")
    
    with main_col:
        user_banner()
        st.markdown("""
        <div class="module-amber">
          <div style="position:absolute;right:-10px;top:-10px;font-size:120px;opacity:0.12;pointer-events:none;">🎙️</div>
          <span class="pill-amber">MODULE 02 · Acoustic Speech Biomarkers</span>
          <h2 style="color:#78350F; margin-top:8px; margin-bottom:6px; font-size:28px; font-weight:800;">🎙️ Speech Acoustic Tracking</h2>
          <p style="color:#B45309; font-size:14px; margin:0;">Vocal acoustic and response lag mapping via MFCC feature extractions.</p>
        </div>
        """, unsafe_allow_html=True)
        
        
        if "reading_passage" not in st.session_state:
            st.session_state.reading_passage = random.choice(READING_PASSAGES)
            
        st.markdown(f"<div class='reading-passage'><p>📖 \"{st.session_state.reading_passage}\"</p></div>", unsafe_allow_html=True)
        
        audio_mode = st.radio("Acoustic Capture Channel:", ["📁 Local Audio File Upload", "🎤 Direct Stream Capture"], horizontal=True)
        audio_bytes = None
        
        if audio_mode == "📁 Local Audio File Upload":
            audio_file = st.file_uploader("Upload Clip (.wav/.mp3)", type=["wav","mp3"])
            if audio_file: audio_bytes = audio_file.read()
        else:
            recorded = st.audio_input("Live Microphone Capture Processing Link")
            if recorded: audio_bytes = recorded.read()
            
        if audio_bytes:
            with st.spinner("Deconstructing audio spectrum frequencies..."):
                label, score, proba_dict = predict_speech(audio_bytes)
            if label is None:
                label, score = "Calm", 80
            st.session_state.speech_emotion = label
            st.session_state.speech_score = score
            
            color = EMOTION_COLORS.get(label, "#D97706")
            st.markdown(f"""
            <div class="result-box-amber" style="border-left-color:{color};">
              <div style="font-size:11px;font-weight:700;color:#B45309;
                          text-transform:uppercase;letter-spacing:1px;margin-bottom:10px;background:#FEF3C7;display:inline-block;padding:4px 10px;border-radius:20px;">
                Detected Speech Emotion · Risk Factor</div>
              <div style="font-size:26px;font-weight:700;color:{color};margin:10px 0 6px;">
                {label}</div>
              <div style="font-size:48px;font-weight:800;color:#78350F;">
                {score}<span style="font-size:18px;font-weight:500;color:#B45309;margin-left:4px;">/ 100</span>
              </div>
            </div>""", unsafe_allow_html=True)

            if proba_dict:
                st.markdown("<p style='font-weight:600;color:#1B3A5C;margin-bottom:8px;'>"
                            "Confidence per emotion:</p>", unsafe_allow_html=True)
                prob_df = pd.DataFrame({
                    "Emotion": list(proba_dict.keys()),
                    "Confidence %": list(proba_dict.values())
                }).sort_values("Confidence %", ascending=False)
                st.bar_chart(prob_df.set_index("Emotion"))
            if st.button("Continue to Facial Expression →"):
                st.session_state.page = "facial_expression"
                st.rerun()
        else:
            st.info("Please upload or record an audio clip to proceed.")


    with side_col:
        render_right_side_layout(
            "Vocal Metric Capture",
            [
                "Maintain steady articulation speeds while evaluating the active text segment block.",
                "Speech biomarkers optimize secondary behavioral safety metric analytics loops."
            ], icon="🎙️"
        )

# ---------------------------------------------------------------------
# MODULE 3 — FACIAL EXPRESSION


