"""
Final aggregate diagnostic report page.
"""

import streamlit as st
import pandas as pd
import random
import time
from PIL import Image

from modules.common import *


def render_final_report():
    progress_bar(17)
    main_col, side_col = st.columns([2.5, 1], gap="large")

    with main_col:
        user_banner()

        mri    = st.session_state.mri_score or 0
        speech = st.session_state.speech_score or 0
        facial = st.session_state.facial_score or 0
        mem    = st.session_state.memory_score or 0
        cog    = st.session_state.cognitive_score or 0

        risk, r_badge = risk_level(speech, facial, mem, cog)

        report_date = pd.Timestamp.now().strftime("%d %B %Y")
        report_time = pd.Timestamp.now().strftime("%I:%M %p")

        # ── Report Header ─────────────────────────────────────────────
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #0E7490 0%, #155E75 100%);
                    border-radius: 16px; padding: 32px 36px; margin-bottom: 24px;
                    box-shadow: 0 10px 15px -3px rgba(14,116,144,0.15);">
          <div style="display:flex; align-items:center; justify-content:space-between; flex-wrap:wrap; gap:12px;">
            <div>
              <div style="font-size:12px; font-weight:600; letter-spacing:1.5px; color:#CFFAFE;
                          text-transform:uppercase; margin-bottom:6px;">AlzAware Clinical Portal</div>
              <div style="font-size:26px; font-weight:800; color:#FFFFFF; letter-spacing:-0.5px;">
                Neurological Diagnostic Report
              </div>
              <div style="font-size:14px; color:#A5F3FC; margin-top:4px;">
                Integrated Multi-Modal Alzheimer's Risk Assessment
              </div>
            </div>
            <div style="text-align:right;">
              <div style="background:rgba(255,255,255,0.12); border-radius:10px; padding:12px 18px;">
                <div style="font-size:11px; color:#CFFAFE; font-weight:600; letter-spacing:1px;
                            text-transform:uppercase;">Date of Assessment</div>
                <div style="font-size:16px; font-weight:700; color:#FFFFFF; margin-top:2px;">{report_date}</div>
                <div style="font-size:12px; color:#A5F3FC;">{report_time}</div>
              </div>
            </div>
          </div>
        </div>
        """, unsafe_allow_html=True)

        # ── Patient Information Card ───────────────────────────────────
        st.markdown(f"""
        <div style="background:#FFFFFF; border-radius:14px; border:1px solid #E2E8F0;
                    padding:24px 28px; margin-bottom:20px;
                    box-shadow:0 4px 6px -1px rgba(0,0,0,0.03);">
          <div style="font-size:11px; font-weight:700; color:#0E7490; text-transform:uppercase;
                      letter-spacing:1.2px; margin-bottom:14px; border-bottom:2px solid #E0F2FE;
                      padding-bottom:10px;">
            🧑‍⚕️ Patient Information
          </div>
          <div style="display:grid; grid-template-columns: repeat(3, 1fr); gap:16px;">
            <div>
              <div style="font-size:11px; color:#94A3B8; font-weight:600; text-transform:uppercase;
                          letter-spacing:0.8px;">Full Name</div>
              <div style="font-size:15px; font-weight:700; color:#0F172A; margin-top:3px;">
                {st.session_state.user_name or "—"}
              </div>
            </div>
            <div>
              <div style="font-size:11px; color:#94A3B8; font-weight:600; text-transform:uppercase;
                          letter-spacing:0.8px;">Age</div>
              <div style="font-size:15px; font-weight:700; color:#0F172A; margin-top:3px;">
                {st.session_state.user_age} Years
              </div>
            </div>
            <div>
              <div style="font-size:11px; color:#94A3B8; font-weight:600; text-transform:uppercase;
                          letter-spacing:0.8px;">Gender</div>
              <div style="font-size:15px; font-weight:700; color:#0F172A; margin-top:3px;">
                {st.session_state.user_gender or "—"}
              </div>
            </div>
            <div>
              <div style="font-size:11px; color:#94A3B8; font-weight:600; text-transform:uppercase;
                          letter-spacing:0.8px;">Email</div>
              <div style="font-size:15px; font-weight:700; color:#0F172A; margin-top:3px;">
                {st.session_state.user_email or "—"}
              </div>
            </div>
            <div>
              <div style="font-size:11px; color:#94A3B8; font-weight:600; text-transform:uppercase;
                          letter-spacing:0.8px;">Contact</div>
              <div style="font-size:15px; font-weight:700; color:#0F172A; margin-top:3px;">
                {st.session_state.user_contact or "—"}
              </div>
            </div>
            <div>
              <div style="font-size:11px; color:#94A3B8; font-weight:600; text-transform:uppercase;
                          letter-spacing:0.8px;">Report ID</div>
              <div style="font-size:15px; font-weight:700; color:#0F172A; margin-top:3px;">
                ALZ-{pd.Timestamp.now().strftime("%Y%m%d%H%M")}
              </div>
            </div>
          </div>
        </div>
        """, unsafe_allow_html=True)

        # ── Overall Risk Banner ────────────────────────────────────────
        risk_bg  = {"badge-low":"#F0FDF4","badge-moderate":"#FFFBEB","badge-high":"#FEF2F2"}.get(r_badge, "#F8FAFC")
        risk_bdr = {"badge-low":"#86EFAC","badge-moderate":"#FDE68A","badge-high":"#FECACA"}.get(r_badge, "#E2E8F0")
        risk_clr = {"badge-low":"#15803D","badge-moderate":"#B45309","badge-high":"#B91C1C"}.get(r_badge, "#475569")
        risk_ico = {"badge-low":"🟢","badge-moderate":"🟡","badge-high":"🔴"}.get(r_badge, "⚪")

        st.markdown(f"""
        <div style="background:{risk_bg}; border:2px solid {risk_bdr}; border-radius:14px;
                    padding:22px 28px; margin-bottom:20px;
                    box-shadow:0 4px 6px -1px rgba(0,0,0,0.03);">
          <div style="display:flex; align-items:center; justify-content:space-between; flex-wrap:wrap; gap:12px;">
            <div>
              <div style="font-size:11px; font-weight:700; color:{risk_clr}; text-transform:uppercase;
                          letter-spacing:1.2px; margin-bottom:4px;">Overall Alzheimer's Risk Classification</div>
              <div style="font-size:22px; font-weight:800; color:{risk_clr};">
                {risk_ico} &nbsp;{risk}
              </div>
            </div>
            <div style="text-align:right;">
              <div style="font-size:11px; color:#94A3B8; font-weight:600; text-transform:uppercase;
                          letter-spacing:0.8px; margin-bottom:4px;">MRI Pathology</div>
              <div style="font-size:15px; font-weight:700; color:#0F172A;">
                {st.session_state.mri_label or "Unverified Baseline"}
              </div>
            </div>
          </div>
        </div>
        """, unsafe_allow_html=True)

        # ── Module Score Cards (2×3 grid) ──────────────────────────────
        st.markdown("""
        <div style="font-size:11px; font-weight:700; color:#0E7490; text-transform:uppercase;
                    letter-spacing:1.2px; margin-bottom:12px; margin-top:4px;">
          📋 Module-Wise Diagnostic Scores
        </div>
        """, unsafe_allow_html=True)

        mc1, mc2, mc3 = st.columns(3)
        score_cards = [
            (mc1, "🧲 MRI Structural Scan",    round(mri),    st.session_state.mri_label or "—",              "#0E7490", "#E0F2FE", "#0C4A6E"),
            (mc2, "🎙️ Speech Emotion",         round(speech), st.session_state.speech_emotion or "—",         "#D97706", "#FEF3C7", "#78350F"),
            (mc3, "😐 Facial Expression",      round(facial), st.session_state.facial_emotion or "—",         "#7C3AED", "#EDE9FE", "#4C1D95"),
        ]
        for col, title, score, label, accent, bg, txt in score_cards:
            with col:
                st.markdown(f"""
                <div style="background:{bg}; border-radius:14px; padding:20px; text-align:center;
                            border:1px solid {accent}33; box-shadow:0 2px 8px {accent}18;">
                  <div style="font-size:13px; font-weight:700; color:{txt}; margin-bottom:8px;">{title}</div>
                  <div style="font-size:38px; font-weight:800; color:{accent}; line-height:1;">
                    {score}<span style="font-size:16px; font-weight:500; color:{txt}; opacity:0.6;">/100</span>
                  </div>
                  <div style="font-size:12px; color:{txt}; margin-top:8px; font-weight:600;
                              background:white; border-radius:20px; padding:4px 12px; display:inline-block;">
                    {label}
                  </div>
                </div>
                """, unsafe_allow_html=True)

        st.write("")
        mc4, mc5 = st.columns(2)
        score_cards2 = [
            (mc4, "🧩 Memory Assessment",    round(mem), "Recall & Retention Score",  "#15803D", "#DCFCE7", "#14532D"),
            (mc5, "🧠 Cognitive Evaluation", round(cog), "Executive Function Score",  "#0369A1", "#DBEAFE", "#1E3A5F"),
        ]
        for col, title, score, label, accent, bg, txt in score_cards2:
            with col:
                st.markdown(f"""
                <div style="background:{bg}; border-radius:14px; padding:20px; text-align:center;
                            border:1px solid {accent}33; box-shadow:0 2px 8px {accent}18;">
                  <div style="font-size:13px; font-weight:700; color:{txt}; margin-bottom:8px;">{title}</div>
                  <div style="font-size:38px; font-weight:800; color:{accent}; line-height:1;">
                    {score}<span style="font-size:16px; font-weight:500; color:{txt}; opacity:0.6;">%</span>
                  </div>
                  <div style="font-size:12px; color:{txt}; margin-top:8px; font-weight:600;
                              background:white; border-radius:20px; padding:4px 12px; display:inline-block;">
                    {label}
                  </div>
                </div>
                """, unsafe_allow_html=True)

        # ── Clinical Recommendations ───────────────────────────────────
        st.write("")
        if r_badge == "badge-high":
            rec_items = [
                "Immediate referral to a certified neurologist or geriatric psychiatrist is advised.",
                "Consider scheduling a follow-up structural MRI and PET scan within 4–6 weeks.",
                "Initiate caregiver support planning and document advance care preferences.",
                "Review current medications for any that may exacerbate cognitive symptoms.",
            ]
            rec_color = "#B91C1C"; rec_bg = "#FEF2F2"; rec_bdr = "#FECACA"
        elif r_badge == "badge-moderate":
            rec_items = [
                "Schedule a consultation with a neurologist within the next 1–3 months.",
                "Begin cognitive stimulation activities and structured daily routines.",
                "Monitor sleep quality, blood pressure, and blood glucose regularly.",
                "Reassess using this platform in 3 months to track progression.",
            ]
            rec_color = "#B45309"; rec_bg = "#FFFBEB"; rec_bdr = "#FDE68A"
        else:
            rec_items = [
                "Continue regular physical exercise and a balanced, brain-healthy diet.",
                "Engage in mentally stimulating activities (reading, puzzles, social interaction).",
                "Schedule routine health check-ups and annual cognitive screenings.",
                "Reassess using this platform in 6 months as a preventive measure.",
            ]
            rec_color = "#15803D"; rec_bg = "#F0FDF4"; rec_bdr = "#86EFAC"

        rec_html = "".join(
            f'<li style="margin-bottom:8px; color:#374151; font-size:14px; line-height:1.6;">{r}</li>'
            for r in rec_items
        )
        st.markdown(f"""
        <div style="background:{rec_bg}; border:1px solid {rec_bdr}; border-left:5px solid {rec_color};
                    border-radius:14px; padding:22px 28px; margin-bottom:20px;">
          <div style="font-size:11px; font-weight:700; color:{rec_color}; text-transform:uppercase;
                      letter-spacing:1.2px; margin-bottom:12px;">
            📌 Clinical Recommendations
          </div>
          <ul style="margin:0; padding-left:20px;">{rec_html}</ul>
        </div>
        """, unsafe_allow_html=True)

        # ── Disclaimer ─────────────────────────────────────────────────
        st.markdown("""
        <div style="background:#F8FAFC; border:1px solid #E2E8F0; border-radius:12px;
                    padding:16px 20px; margin-bottom:20px;">
          <div style="font-size:11px; font-weight:700; color:#64748B; text-transform:uppercase;
                      letter-spacing:1px; margin-bottom:6px;">⚠️ Medical Disclaimer</div>
          <p style="font-size:12px; color:#94A3B8; margin:0; line-height:1.7;">
            This report is generated by an AI-assisted screening tool and is intended for
            informational purposes only. It does not constitute a medical diagnosis. All findings
            must be reviewed and validated by a licensed neurologist or qualified healthcare
            professional before any clinical decisions are made.
          </p>
        </div>
        """, unsafe_allow_html=True)

        save_result(dict(st.session_state))
        st.toast("✅ Diagnostic session log successfully saved to the database.")

        st.write("")
        c1, c2 = st.columns(2)
        with c1:
            if st.button("💬 Consult Assistant Regarding Records"):
                st.session_state.page = "chatbot"
                st.rerun()
        with c2:
            if st.button("🔄 Launch New Diagnostics Loop"):
                saved = {k: st.session_state[k] for k in ["user_name", "user_age", "user_gender", "user_email", "user_contact"]}
                for k in list(defaults.keys()):
                    if k in st.session_state: del st.session_state[k]
                for k, v in saved.items(): st.session_state[k] = v
                st.session_state.page = "mri_scan"
                st.rerun()

    with side_col:
        render_right_side_layout(
            "Report Breakdown",
            [
                "The MRI structural score reflects physical neurodegenerative findings only.",
                "Behavioral risk (speech, facial, memory, cognitive) is assessed via secondary modules and contributes to the overall risk classification.",
                "This report is auto-saved to your patient profile in the database.",
                "Forward this report to a certified neurologist for clinical validation and follow-up care planning."
            ], icon="📋"
        )

# ---------------------------------------------------------------------
# CONVERSATIONAL AI ASSISTANT SIDEBAR LOCKOUT
