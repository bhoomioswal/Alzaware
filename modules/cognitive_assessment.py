"""
Cognitive assessment suite: attention, orientation, language, executive function.
"""

import streamlit as st
import pandas as pd
import random
import time
from PIL import Image

from modules.common import *


def render_intro_cognitive():
    progress_bar(12)
    main_col, side_col = st.columns([2.5, 1], gap="large")
    with main_col:
        user_banner()
        st.markdown("""
        <div class="module-blue">
          <div style="position:absolute;right:-10px;top:-10px;font-size:120px;opacity:0.12;pointer-events:none;">🔬</div>
          <span class="pill">MODULE 05 · Cognitive Diagnostics</span>
          <h2 style="color:#0C4A6E; margin-top:8px; margin-bottom:6px; font-size:28px; font-weight:800;">🔬 System Cognitive Diagnostics Array</h2>
          <p style="color:#0369A1; font-size:14px; margin:0;">Profiles spatial orientation, semantic manipulation, attention, and executive reasoning across 20 points.</p>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("""
        <div style="background:white;border-radius:12px;padding:16px 20px;border:1px solid #BAE6FD;margin-bottom:16px;">
          <p style="color:#0369A1;margin:0;font-size:14px;">ℹ️ The next assessment stage profiles spatial orientation, semantic speech manipulation, structural attention, and executive reasoning matrices across 20 points.</p>
        </div>
        """, unsafe_allow_html=True)
        st.write("")
        if st.button("Initialize Cognitive Diagnostics Framework →"):
            st.session_state.page = "cog_attention"
            st.rerun()
    with side_col:
        render_right_side_layout("Diagnostic Targets", ["This configuration screens logical pathways to refine downstream composite risk estimations."], icon="🔬")


def render_cog_attention():
    progress_bar(12)
    main_col, side_col = st.columns([2.5, 1], gap="large")
    with main_col:
        user_banner()
        st.markdown("""
        <div class="module-blue">
          <div style="position:absolute;right:-10px;top:-10px;font-size:120px;opacity:0.12;pointer-events:none;">🔢</div>
          <span class="pill">SECTION 1 OF 4 · Attention</span>
          <h3 style="color:#0C4A6E; margin-top:8px; margin-bottom:4px; font-size:22px; font-weight:700;">Active Focus Processing</h3>
          <p style="color:#0369A1; font-size:14px; margin:0;">Arithmetic and time-based attention assessment.</p>
        </div>
        """, unsafe_allow_html=True)
        ans = st.session_state.cog_answers
        ans["a1"] = st.radio("1. Formulate: 27 + 15", ["40","42","44","46"], index=None)
        ans["a2"] = st.radio("2. Formulate: 84 − 29", ["55","54","53","52"], index=None)
        ans["a3"] = st.radio("3. Formulate: 12 × 4", ["42","48","50","52"], index=None)
        ans["a4"] = st.radio("4. Deduct 7 sequentially from 100 once:", ["91","92","93","94"], index=None)
        ans["a5"] = st.radio("5. A transit unit departs at 15:00 hours and arrives at 17:00 hours. Define runtime:", ["1 hour","2 hours","3 hours","4 hours"], index=None)
        
        st.write("")
        if st.button("Lock Section 1 Entries & Proceed →"):
            if None in [ans.get(f"a{i}") for i in range(1,6)]: st.error("Incomplete Evaluation: All matrix data elements must be answered.")
            else: st.session_state.page = "cog_orientation"; st.rerun()
    with side_col:
        render_right_side_layout("Focus Logic", ["Measures logical working performance limits securely."], icon="🔬")


def render_cog_orientation():
    progress_bar(13)
    main_col, side_col = st.columns([2.5, 1], gap="large")
    with main_col:
        user_banner()
        st.markdown("""
        <div class="module-amber">
          <div style="position:absolute;right:-10px;top:-10px;font-size:120px;opacity:0.12;pointer-events:none;">🌍</div>
          <span class="pill-amber">SECTION 2 OF 4 · Orientation</span>
          <h3 style="color:#78350F; margin-top:8px; margin-bottom:4px; font-size:22px; font-weight:700;">Environmental Orientation Framework</h3>
          <p style="color:#B45309; font-size:14px; margin:0;">Evaluates awareness of time, place, and general knowledge.</p>
        </div>
        """, unsafe_allow_html=True)
        ans = st.session_state.cog_answers
        ans["o1"] = st.radio("1. Which precise meteorologic phase patterns follow Summer?", ["Spring","Winter","Monsoon","Autumn"], index=None)
        ans["o2"] = st.radio("2. Identify the quantitative monthly counts inside a standard solar calendar year loop:", ["10","11","12","13"], index=None)
        ans["o3"] = st.radio("3. Identify the geopolitical territory housing New Delhi:", ["India","Nepal","Bangladesh","Sri Lanka"], index=None)
        ans["o4"] = st.radio("4. Quantify standard active operational days defined inside a single week structure:", ["5","6","7","8"], index=None)
        ans["o5"] = st.radio("5. Which standard epoch quadrant instantiates first within a solar calendar rotation day map?", ["Morning","Evening","Night","Afternoon"], index=None)
        
        st.write("")
        if st.button("Lock Section 2 Entries & Proceed →"):
            if None in [ans.get(f"o{i}") for i in range(1,6)]: st.error("Incomplete Evaluation: All matrix data elements must be answered.")
            else: st.session_state.page = "cog_language"; st.rerun()
    with side_col:
        render_right_side_layout("Orientation Engine", ["Tracks macro-situational database synchronization stability within immediate brain horizons."], icon="🔬")


def render_cog_language():
    progress_bar(13)
    main_col, side_col = st.columns([2.5, 1], gap="large")
    with main_col:
        user_banner()
        st.markdown("""
        <div class="module-green">
          <div style="position:absolute;right:-10px;top:-10px;font-size:120px;opacity:0.12;pointer-events:none;">💬</div>
          <span class="pill-green">SECTION 3 OF 4 · Language</span>
          <h3 style="color:#14532D; margin-top:8px; margin-bottom:4px; font-size:22px; font-weight:700;">Linguistic Logic Mapping</h3>
          <p style="color:#15803D; font-size:14px; margin:0;">Tests vocabulary, analogies, and semantic pattern recognition.</p>
        </div>
        """, unsafe_allow_html=True)
        ans = st.session_state.cog_answers
        ans["l1"] = st.radio("1. Complete the structural proverb: Actions speak louder than ____", ["Noise","Words","Thoughts","People"], index=None)
        ans["l2"] = st.radio("2. Isolate the direct semantic antonym for the tracking value 'Ancient':", ["Old","Historic","Modern","Traditional"], index=None)
        ans["l3"] = st.radio("3. Avian organisms execute flight protocols primarily due to integrated functional ____", ["Legs","Wings","Eyes","Beaks"], index=None)
        ans["l4"] = st.radio("4. Identify the semantic value outlier inside this array classification list: [Apple, Banana, Mango, Car]", ["Apple","Banana","Mango","Car"], index=None)
        ans["l5"] = st.radio("5. Identify the tool apparatus calibrated specifically to monitor temporal tracking parameters:", ["Chair","Watch","Bottle","Bag"], index=None)
        
        st.write("")
        if st.button("Lock Section 3 Entries & Proceed →"):
            if None in [ans.get(f"l{i}") for i in range(1,6)]: st.error("Incomplete Evaluation: All matrix data elements must be answered.")
            else: st.session_state.page = "cog_executive"; st.rerun()
    with side_col:
        render_right_side_layout("Linguistic Array", ["Calculates cognitive fluency thresholds effectively."], icon="🔬")


def render_cog_executive():
    progress_bar(14)
    main_col, side_col = st.columns([2.5, 1], gap="large")
    with main_col:
        user_banner()
        st.markdown("""
        <div class="module-purple">
          <div style="position:absolute;right:-10px;top:-10px;font-size:120px;opacity:0.12;pointer-events:none;">🧮</div>
          <span class="pill-purple">SECTION 4 OF 4 · Executive Function</span>
          <h3 style="color:#3B0764; margin-top:8px; margin-bottom:4px; font-size:22px; font-weight:700;">Executive Function Logic Array</h3>
          <p style="color:#6D28D9; font-size:14px; margin:0;">Evaluates abstract reasoning, logic sequencing, and problem solving.</p>
        </div>
        """, unsafe_allow_html=True)
        ans = st.session_state.cog_answers
        ans["e1"] = st.radio("1. If all conditional parameters state roses are classified as flora structures, are all roses flora?", ["Yes","No"], index=None)
        ans["e2"] = st.radio("2. Identify the logical progression sequence continuation entry: 2, 4, 8, 16, …", ["20","24","32","36"], index=None)
        ans["e3"] = st.radio("3. Compute the consolidated pricing architecture for two literature manuals valued flatly at ₹150 each unit:", ["250","300","350","400"], index=None)
        ans["e4"] = st.radio("4. Bicycles and Motorcycles share categorical class properties as functional operational ____", ["Animals","Vehicles","Foods","Buildings"], index=None)
        ans["e5"] = st.radio("5. If the current structural weekday calendar baseline points to Wednesday, evaluate the target point exactly 3 calendar days after tomorrow:", ["Thursday","Friday","Saturday","Sunday"], index=None)
        
        st.write("")
        if st.button("Submit Complete Cognitive Architecture Profile"):
            if None in [ans.get(f"e{i}") for i in range(1,6)]: st.error("Incomplete Evaluation: All matrix data elements must be answered.")
            else:
                truth = {
                    "a1":"42","a2":"55","a3":"48","a4":"93","a5":"2 hours",
                    "o1":"Monsoon","o2":"12","o3":"India","o4":"7","o5":"Morning",
                    "l1":"Words","l2":"Modern","l3":"Wings","l4":"Car","l5":"Watch",
                    "e1":"Yes","e2":"32","e3":"300","e4":"Vehicles","e5":"Saturday"
                }
                correct = sum(1 for k, v in truth.items() if ans.get(k) == v)
                st.session_state.cognitive_score = (correct / 20) * 100
                st.session_state.page = "cognitive_report"
                st.rerun()
    with side_col:
        render_right_side_layout("Executive Tracking", ["Evaluates abstract sorting and structural synthesis speeds directly."], icon="🔬")


def render_cognitive_report():
    progress_bar(15)
    main_col, side_col = st.columns([2.5, 1], gap="large")
    with main_col:
        user_banner()
        st.markdown("<h2 style='color:#0F172A; margin-top:0;'>📊 Cognitive Diagnostic Output</h2>", unsafe_allow_html=True)
        cog = st.session_state.cognitive_score
        badge, label = ("badge-low", "Exceptional Domain Matrix Performance") if cog >= 80 else (("badge-moderate", "Balanced Cognitive Architecture") if cog >= 60 else ("badge-high", "Analytical Degradation Risk Warning"))
        
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #0E7490 0%, #0891B2 100%); border-radius:16px; padding:32px; text-align:center; margin-bottom:24px; color:white; box-shadow:0 10px 15px -3px rgba(14, 116, 144, 0.2);">
            <div style="font-size:13px; text-transform:uppercase; letter-spacing:1px; font-weight:600;">Consolidated Cognitive Domain Profile</div>
            <div style="font-size:56px; font-weight:800; margin:8px 0;">{round(cog)}%</div>
            <div><span class="{badge}">{label}</span></div>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("Generate Consolidated Master Analytics Summary →"):
            st.session_state.page = "final_report"
            st.rerun()
    with side_col:
        render_right_side_layout("Performance Index", ["Scores scale evenly across attention, spatial orientation mapping, syntax matching, and processing efficiency metrics logs."], icon="📊")

# ---------------------------------------------------------------------
# FINAL COMBINED DIAGNOSTIC REPORT PAGE

