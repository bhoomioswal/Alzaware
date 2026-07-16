"""
MRI structural scan upload and prediction page.
"""

import streamlit as st
import pandas as pd
import random
import time
from PIL import Image

from modules.common import *


def render_mri_scan():
    progress_bar(2)
    main_col, side_col = st.columns([2.5, 1], gap="large")
    
    with main_col:
        user_banner()
        st.markdown("""
        <div class="module-blue">
          <div style="position:absolute;right:-10px;top:-10px;font-size:120px;opacity:0.12;pointer-events:none;">🧬</div>
          <span class="pill">MODULE 01 · Neuro-Imaging Scanner</span>
          <h2 style="color:#0C4A6E; margin-top:8px; margin-bottom:6px; font-size:28px; font-weight:800;">🧬 Brain Structural MRI Processing</h2>
          <p style="color:#0369A1; font-size:14px; margin:0;">Structural MRI density classifications using analytical random forests.</p>
        </div>
        """, unsafe_allow_html=True)
        
       
        uploaded = st.file_uploader("Upload Structural Scan Matrix (.jpg / .png)", type=["jpg","jpeg","png"])
        if uploaded:
            img = Image.open(uploaded)
            st.image(img, caption="Loaded Neuroimaging Asset", width=350)
            
            with st.spinner("Executing RandomForest Model Matrix Evaluation..."):
                result, mri_score, proba_dict = predict_mri(img)
                
            if result is None:
                st.caption("System Warning: Live model missing or incompatible. Activating simulated baseline processing fallback.")
                result = random.choices(MRI_LABELS, weights=[0.6, 0.2, 0.1, 0.1], k=1)[0]
                mri_score = MRI_SCORE_MAP[result]
                proba_dict = {lbl: 25.0 for lbl in MRI_LABELS}
                
            st.session_state.mri_label = result
            st.session_state.mri_score = mri_score
            
            color = MRI_COLOR_MAP.get(result, "#0E7490")
            st.markdown(f"""
            <div class="result-box-blue" style="border-left-color:{color};">
              <div style="font-size:11px;font-weight:700;color:#0369A1;
                          text-transform:uppercase;letter-spacing:1px;margin-bottom:10px;background:#E0F2FE;display:inline-block;padding:4px 10px;border-radius:20px;">
                Alzheimer Score · MRI Analysis</div>
              <div style="font-size:26px;font-weight:700;color:{color};margin:10px 0 6px;">
                {result}</div>
              <div style="font-size:48px;font-weight:800;color:#0C4A6E;">
                {mri_score}<span style="font-size:18px;font-weight:500;color:#0369A1;margin-left:4px;">/ 100</span>
              </div>
            </div>""", unsafe_allow_html=True)

            if proba_dict:
                st.markdown("<p style='font-weight:600;color:#1B3A5C;margin-bottom:8px;'>"
                            "Confidence per class:</p>", unsafe_allow_html=True)
                prob_df = pd.DataFrame({
                    "Class": list(proba_dict.keys()),
                    "Confidence %": list(proba_dict.values())
                }).sort_values("Confidence %", ascending=False)
                st.bar_chart(prob_df.set_index("Class"))
            
            if st.button("Continue to Speech Emotion Analysis →"):
                st.session_state.page = "speech_emotion"
                st.rerun()

    with side_col:
        render_right_side_layout(
            "MRI Scanner Protocols",
            [
                "Ensure image captures display high-contrast gray/white matter differentiations.",
                "This module dictates the primary <b>Alzheimer Score</b> logic framework directly."
            ], icon="🧬"
        )

# ---------------------------------------------------------------------
# MODULE 2 — SPEECH EMOTION

