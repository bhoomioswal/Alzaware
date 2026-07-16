"""
Facial expression recognition page.
"""

import streamlit as st
import pandas as pd
import random
import time
from PIL import Image

from modules.common import *


def render_facial_expression():
    progress_bar(6)
    main_col, side_col = st.columns([2.5, 1], gap="large")
    
    with main_col:
        user_banner()
        st.markdown("""
        <div class="module-green">
          <div style="position:absolute;right:-10px;top:-10px;font-size:120px;opacity:0.12;pointer-events:none;">😶</div>
          <span class="pill-green">MODULE 03 · Neuromuscular Expression Engine</span>
          <h2 style="color:#14532D; margin-top:8px; margin-bottom:6px; font-size:28px; font-weight:800;">😶 Facial Expression Mapping</h2>
          <p style="color:#15803D; font-size:14px; margin:0;">Deep computer vision monitoring for tracking micro-expression indicators.</p>
        </div>
        """, unsafe_allow_html=True)
        
        
        
        camera_photo = st.camera_input("Capture Patient Frontal Layout Frame Matrix")
        if camera_photo:
            img = Image.open(camera_photo)
            with st.spinner("Deconstructing micro-muscular layouts..."):
                label, score, proba_dict = predict_fer(img)
            if label is None: label, score = "Neutral", 70
            
            st.session_state.facial_emotion = label
            st.session_state.facial_score = score
            color = FER_COLORS.get(label, "#15803D")
            st.markdown(f"""
            <div class="result-box-green" style="border-left-color:{color};">
              <div style="font-size:11px;font-weight:700;color:#15803D;
                          text-transform:uppercase;letter-spacing:1px;margin-bottom:10px;background:#DCFCE7;display:inline-block;padding:4px 10px;border-radius:20px;">
                Detected Expression · Risk Factor</div>
              <div style="font-size:26px;font-weight:700;color:{color};margin:10px 0 6px;">
                {label}</div>
              <div style="font-size:48px;font-weight:800;color:#14532D;">
                {score}<span style="font-size:18px;font-weight:500;color:#15803D;margin-left:4px;">/ 100</span>
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

            if st.button("Continue to Memory Assessment →"):
                st.session_state.page = "intro_memory"
                st.rerun()
        else:
            st.info("Please capture a photo with your webcam to proceed.")

# ---------------------------------------------------------------------
# MODULE 4 — MEMORY TRACKING MODULE


