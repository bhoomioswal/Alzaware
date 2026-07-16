"""
Landing page and patient registration.
"""

import streamlit as st
import pandas as pd
import random
import time
from PIL import Image

from modules.common import *


def render_home():
    # Streamlined layout framework styles (No background-card overriding rules)
    st.markdown("""
    <style>
        /* Top Navigation Header Styling */
        .premium-nav-clean {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 10px 0px;
            margin-bottom: 40px;
            border-bottom: 1px solid #e2e8f0;
        }
        .nav-logo-clean {
            font-size: 22px;
            font-weight: 800;
            color: #0f172a;
            display: flex;
            align-items: center;
            gap: 8px;
        }
        .nav-links-clean {
            display: flex;
            gap: 32px;
            font-size: 15px;
            font-weight: 500;
            color: #475569;
        }
        
        /* Typography Elements */
        .hero-badge-clean {
            background-color: #e0f2fe;
            color: #0369a1;
            padding: 6px 16px;
            border-radius: 20px;
            font-size: 13px;
            font-weight: 600;
            display: inline-block;
            margin-bottom: 22px;
            border: 1px solid #bae6fd;
        }
        .hero-title-clean {
            font-size: 46px;
            color: #0f172a;
            line-height: 1.2;
            font-weight: 800;
            margin-bottom: 20px;
            letter-spacing: -1px;
        }
        .hero-title-clean span {
            color: #2563eb;
        }
        .hero-subtitle-clean {
            font-size: 16.5px;
            color: #475569;
            line-height: 1.65;
            margin-bottom: 35px;
        }
        
        /* Stats strip text items */
        .stat-num-text {
            font-size: 34px;
            font-weight: 800;
            color: #2563eb;
            margin-bottom: 2px;
            letter-spacing: -0.5px;
        }
        .stat-label-text {
            font-size: 14px;
            font-weight: 700;
            color: #0f172a;
            margin-bottom: 4px;
        }
        .stat-desc-text { font-size: 12.5px; color: #64748b; margin: 0; line-height: 1.4; }

        .section-grid-title {
            color: #0f172a; 
            margin-top: 50px; 
            margin-bottom: 25px;
            font-size: 22px;
            font-weight: 800;
            letter-spacing: -0.4px;
        }
        
        /* Dimension feature grid boxes */
        .clinical-dimension-box {
            background: #ffffff; 
            border-radius: 16px; 
            padding: 24px 20px; 
            text-align: left;
            border: 1px solid #e2e8f0; 
            transition: all 0.2s ease;
            height: 100%;
        }
        .clinical-dimension-box:hover { 
            transform: translateY(-2px); 
            border-color: #2563eb;
            box-shadow: 0 12px 20px -5px rgba(37, 99, 235, 0.08);
        }
        .card-icon-round {
            width: 44px;
            height: 44px;
            background: #eff6ff;
            border-radius: 10px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 22px;
            margin-bottom: 16px;
            border: 1px solid #dbeafe;
        }
    </style>
    """, unsafe_allow_html=True)

    # 1. Navbar Header Strip Configuration
    st.markdown("""
    <div class="premium-nav-clean">
        <div class="nav-logo-clean">AlzAware <span style="color:#2563eb; font-weight:400; font-size:15px; margin-left:-4px;"></span></div>
        <div class="nav-links-clean">
           
        
    </div>
    """, unsafe_allow_html=True)

    # 2. Main Text and Graphic Split Hero Section
    left_hero_col, right_hero_col = st.columns([1.25, 1.0], gap="large")
    
    with left_hero_col:
        st.markdown("""
            <div class="hero-badge-clean">🛡️ AI-Powered • Clinical Grade • Privacy-First</div>
            <div class="hero-title-clean">Predict Risk.<br>Protect <span>Memory.</span></div>
            <div class="hero-subtitle-clean">
                Leverage advanced multi-modal machine learning architectures and clinical risk analysis pipelines to evaluate 
                cognitive trajectories, structural biomarkers, and lifestyle profiles for early actionable insights.
            </div>
        """, unsafe_allow_html=True)
        
        # Dual Interactive Actions Button Row Layout
        btn_c1, btn_c2, _ = st.columns([1.3, 1.1, 0.8])
        with btn_c1:
            if st.button("Login page →", use_container_width=True, type="primary"):
                st.session_state.page = "register"
                st.rerun()
       
                
    with right_hero_col:
        # Native image presentation without custom layout cards wrapper tags
        st.image("assets/layout.png", use_container_width=True)
   
          

  
 
   
    
# ---------------------------------------------------------------------
# PAGE 2: RESTRUCTURED USER REGISTRATION


def render_register():
    progress_bar(1)
    main_col, side_col = st.columns([2.5, 1], gap="large")
    
    with main_col:
        st.markdown("""
        <div class="module-blue">
          <div style="position:absolute;right:-10px;top:-10px;font-size:120px;opacity:0.12;pointer-events:none;">📋</div>
          <span class="pill">Patient Configuration Intake</span>
          <h2 style="color:#0C4A6E; margin-top:8px; margin-bottom:6px; font-size:28px; font-weight:800;">Patient Registration</h2>
          <p style="color:#0369A1; font-size:14px; margin:0;">Complete all required fields to generate your intake file and begin the diagnostic pipeline.</p>
        </div>
        """, unsafe_allow_html=True)
        
        with st.form("professional_reg_form"):
            name = st.text_input("Full Name *", placeholder="Firstname Lastname")
            cc1, cc2 = st.columns(2)
            with cc1:
                age = st.number_input("Patient  Age *", min_value=1, max_value=120, value=65)
            with cc2:
                gender = st.selectbox("Biological Sex Demographics *", ["Select Layout Demographics", "Male", "Female", "Other", "Prefer not to disclose"])
            email = st.text_input("Verified Medical/Patient Email Address *", placeholder="patient@healthcare.com")
            contact = st.text_input("Emergency Contact Number *", placeholder="10-digit primary phone")
            
            st.write("")
            submit_reg = st.form_submit_button("Generate Intake File & Continue →")
            
        if submit_reg:
            if not name.strip() or gender.startswith("Select") or "@" not in email or len(contact.strip()) < 10:
                st.error("Validation Breakdown: Please ensure all field elements marked with an asterisk (*) are correctly filled out.")
            else:
                st.session_state.user_name = name.strip()
                st.session_state.user_age = age
                st.session_state.user_gender = gender
                st.session_state.user_email = email.strip()
                st.session_state.user_contact = contact.strip()
                save_registration(name.strip(), age, gender, email.strip(), contact.strip())
                st.toast("Patient File Successfully Instantiated.")
                st.success("Patient intake file created successfully!")
                st.session_state.page = "dashboard" # Set this to route to the new dashboard
                st.rerun()

    with side_col:
        render_right_side_layout(
            "Security & Compliance",
            [
                "All user metrics are stored within a secured, localized encryption ledger block system.",
                "Real identities and emails cross-reference past assessments to prevent data duplication.",
                "Age groups directly adjust contextual weighting loops within our validation algorithms."
            ], icon="🛡️"
        )
# ---------------------------------------------------------------------
# PAGE: CLINICAL PIPELINE DASHBOARD (SERENITY INSPIRED)
