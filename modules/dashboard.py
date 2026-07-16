"""
Post-registration module-selection dashboard.
"""

import streamlit as st
import pandas as pd
import random
import time
from PIL import Image

from modules.common import *


def render_dashboard():
    
    # Header Section with Profile Overviews
    st.markdown("""
    <div style="background: linear-gradient(135deg, #F8FAFC 0%, #F1F5F9 100%); padding: 35px 25px; border-radius: 24px; border: 1px solid #E2E8F0; margin-bottom: 30px;">
        <span style="background: #E0F2FE; color: #0369A1; padding: 6px 12px; border-radius: 20px; font-size: 12px; font-weight: 700; text-transform: uppercase; letter-spacing: 0.5px;">Active Patient Intake</span>
        <h1 style="color: #0F172A; font-size: 32px; font-weight: 800; margin-top: 10px; margin-bottom: 6px;">Multi-Modal Diagnostic Matrix</h1>
        <p style="color: #64748B; font-size: 14px; max-width: 600px; margin: 0;">
            Follow the structured clinical pipeline below to generate an aggregate diagnostic risk profile. Complete modules sequentially for baseline profiling.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # 3-Column Image-Style Interactive Card Grid (Matches image_9ac7c6.jpg layouts)
    c1, c2, c3 = st.columns(3)
    
    with c1:
        # Card 1: Neuro-Imaging
        st.markdown("""
        <div style="background: linear-gradient(to bottom, #E0F2FE, #BAE6FD); border-radius: 24px; padding: 24px; height: 320px; display: flex; flex-direction: column; justify-content: space-between; box-shadow: 0 4px 15px rgba(0,0,0,0.02); position: relative; overflow: hidden;">
            <div style="position: absolute; right: -20px; top: -10px; font-size: 140px; opacity: 0.15; pointer-events: none;">🧬</div>
            <div>
                <span style="background: white; padding: 6px 14px; border-radius: 20px; font-size: 11px; font-weight: 600; color: #0369A1;">MODULE 01</span>
                <h3 style="color: #0C4A6E; font-size: 22px; font-weight: 700; margin-top: 16px; margin-bottom: 8px;">Neuro-Imaging<br/>Scanner</h3>
                <p style="color: #0369A1; font-size: 13px; line-height: 1.4; max-width: 90%;">Structural MRI density classifications using analytical random forests.</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
        # Clean button acting like the arrow link in the reference image
        if st.button("Begin Scan Integration ↗", key="btn_mri", use_container_width=True):
            st.session_state.page = "mri_scan"
            st.rerun()

    with c2:
        # Card 2: Speech Biomarkers
        st.markdown("""
        <div style="background: linear-gradient(to bottom, #FEF3C7, #FDE68A); border-radius: 24px; padding: 24px; height: 320px; display: flex; flex-direction: column; justify-content: space-between; box-shadow: 0 4px 15px rgba(0,0,0,0.02); position: relative; overflow: hidden;">
            <div style="position: absolute; right: -20px; top: -10px; font-size: 140px; opacity: 0.15; pointer-events: none;">🎙️</div>
            <div>
                <span style="background: white; padding: 6px 14px; border-radius: 20px; font-size: 11px; font-weight: 600; color: #B45309;">MODULE 02</span>
                <h3 style="color: #78350F; font-size: 22px; font-weight: 700; margin-top: 16px; margin-bottom: 8px;">Acoustic Speech<br/>Biomarkers</h3>
                <p style="color: #B45309; font-size: 13px; line-height: 1.4; max-width: 90%;">Vocal acoustic and response lag mapping via MFCC feature extractions.</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Analyze Audio Track ↗", key="btn_speech", use_container_width=True):
            st.session_state.page = "speech_analysis" # update to match your specific speech page key
            st.rerun()

    with c3:
        # Card 3: Facial Expression
        st.markdown("""
        <div style="background: linear-gradient(to bottom, #DCFCE7, #BBF7D0); border-radius: 24px; padding: 24px; height: 320px; display: flex; flex-direction: column; justify-content: space-between; box-shadow: 0 4px 15px rgba(0,0,0,0.02); position: relative; overflow: hidden;">
            <div style="position: absolute; right: -20px; top: -10px; font-size: 140px; opacity: 0.15; pointer-events: none;">😶</div>
            <div>
                <span style="background: white; padding: 6px 14px; border-radius: 20px; font-size: 11px; font-weight: 600; color: #15803D;">MODULE 03</span>
                <h3 style="color: #14532D; font-size: 22px; font-weight: 700; margin-top: 16px; margin-bottom: 8px;">Neuromuscular<br/>Expression Engine</h3>
                <p style="color: #15803D; font-size: 13px; line-height: 1.4; max-width: 90%;">Deep computer vision monitoring for tracking micro-expression indicators.</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Initialize Vision Stream ↗", key="btn_fer", use_container_width=True):
            st.session_state.page = "facial_expression" # update to match your specific facial page key
            st.rerun()

   
# ---------------------------------------------------------------------
# MODULE 1 — MRI SCAN
