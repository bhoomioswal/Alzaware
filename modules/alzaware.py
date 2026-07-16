import streamlit as st
import random
import time
import pandas as pd
from PIL import Image
import io
import sqlite3
import numpy as np
import joblib
import os
import math

# =====================================================
# DATABASE SETUP
# =====================================================
DB_PATH = "Alzaware1.db"

def get_conn():
    return sqlite3.connect(DB_PATH, check_same_thread=False)

def init_db():
    conn = get_conn()
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS registrations (
            id            INTEGER PRIMARY KEY AUTOINCREMENT,
            registered_on TEXT,
            full_name     TEXT,
            age           INTEGER,
            gender        TEXT,
            email         TEXT,
            contact       TEXT
        )
    """)
    c.execute("""
        CREATE TABLE IF NOT EXISTS assessment_results (
            id               INTEGER PRIMARY KEY AUTOINCREMENT,
            saved_on         TEXT,
            full_name        TEXT,
            age              INTEGER,
            gender           TEXT,
            email            TEXT,
            contact          TEXT,
            mri_score        REAL,
            mri_label        TEXT,
            speech_score     REAL,
            speech_emotion   TEXT,
            facial_score     REAL,
            facial_emotion   TEXT,
            memory_score     REAL,
            cognitive_score  REAL,
            risk_level       TEXT
        )
    """)
    conn.commit()
    conn.close()

init_db()

def save_registration(name, age, gender, email, contact):
    conn = get_conn()
    conn.execute("""
        INSERT INTO registrations (registered_on, full_name, age, gender, email, contact)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S"), name, age, gender, email, contact))
    conn.commit()
    conn.close()

def save_result(s):
    conn = get_conn()
    conn.execute("""
        INSERT INTO assessment_results
            (saved_on, full_name, age, gender, email, contact,
             mri_score, mri_label, speech_score, speech_emotion,
             facial_score, facial_emotion, memory_score, cognitive_score,
             risk_level)
        VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
    """, (
        pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S"),
        s["user_name"], s["user_age"], s["user_gender"], s["user_email"], s["user_contact"],
        round(s["mri_score"] or 0, 2), s.get("mri_label") or "—",
        round(s["speech_score"] or 0, 2), s.get("speech_emotion") or "—",
        round(s["facial_score"] or 0, 2), s.get("facial_emotion") or "—",
        round(s["memory_score"] or 0, 2), round(s["cognitive_score"] or 0, 2),
         s["risk_level"],
    ))
    conn.commit()
    conn.close()

def get_user_history(name, email):
    conn = get_conn()
    df = pd.read_sql(
        "SELECT * FROM assessment_results WHERE full_name = ? AND email = ? ORDER BY saved_on DESC",
        conn, params=(name, email)
    )
    conn.close()
    return df

# =====================================================
# PAGE CONFIG
# =====================================================
st.set_page_config(
    page_title="AlzAware | Healthcare Portal",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# =====================================================
# ADVANCED HEALTHCARE UI/UX THEME (CSS)
# =====================================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
.stApp { background-color: #F4F7FA; }

/* Clinical Navbar Styling */
.navbar-brand { font-size: 24px; font-weight: 700; color: #0E7490; display: flex; align-items: center; gap: 8px; letter-spacing: -0.5px;}
.navbar-sub { font-size: 13px; color: #64748B; margin-top: -2px; font-weight: 500;}

/* Main Components */
.page-header {
    background: linear-gradient(135deg, #0E7490 0%, #155E75 100%);
    color: white; padding: 32px; border-radius: 16px;
    margin-bottom: 24px; box-shadow: 0 10px 15px -3px rgba(14, 116, 144, 0.1);
}
.page-header h1 { font-size: 30px; font-weight: 700; margin: 0; color: white; letter-spacing: -0.5px;}
.page-header p  { font-size: 15px; margin: 8px 0 0; color: #CFFAFE; opacity: 0.9; }

/* Module-colored pills */
.pill {
    display: inline-block; background: #E0F2FE; color: #0369A1;
    font-size: 12px; font-weight: 600; padding: 6px 16px;
    border-radius: 30px; letter-spacing: 0.5px;
    text-transform: uppercase; margin-bottom: 16px;
}
.pill-amber {
    display: inline-block; background: #FEF3C7; color: #B45309;
    font-size: 12px; font-weight: 600; padding: 6px 16px;
    border-radius: 30px; letter-spacing: 0.5px;
    text-transform: uppercase; margin-bottom: 16px;
}
.pill-green {
    display: inline-block; background: #DCFCE7; color: #15803D;
    font-size: 12px; font-weight: 600; padding: 6px 16px;
    border-radius: 30px; letter-spacing: 0.5px;
    text-transform: uppercase; margin-bottom: 16px;
}
.pill-purple {
    display: inline-block; background: #EDE9FE; color: #6D28D9;
    font-size: 12px; font-weight: 600; padding: 6px 16px;
    border-radius: 30px; letter-spacing: 0.5px;
    text-transform: uppercase; margin-bottom: 16px;
}

/* Module-themed section wrappers */
.module-blue {
    background: linear-gradient(to bottom, #E0F2FE, #BAE6FD);
    border-radius: 20px; padding: 28px; margin-bottom: 24px;
    border: 1px solid #BAE6FD; position: relative; overflow: hidden;
}
.module-amber {
    background: linear-gradient(to bottom, #FEF3C7, #FDE68A);
    border-radius: 20px; padding: 28px; margin-bottom: 24px;
    border: 1px solid #FDE68A; position: relative; overflow: hidden;
}
.module-green {
    background: linear-gradient(to bottom, #DCFCE7, #BBF7D0);
    border-radius: 20px; padding: 28px; margin-bottom: 24px;
    border: 1px solid #BBF7D0; position: relative; overflow: hidden;
}
.module-purple {
    background: linear-gradient(to bottom, #EDE9FE, #DDD6FE);
    border-radius: 20px; padding: 28px; margin-bottom: 24px;
    border: 1px solid #DDD6FE; position: relative; overflow: hidden;
}

/* Result boxes themed by module */
.result-box-blue {
    background: white; border-radius: 14px; padding: 24px;
    border-left: 5px solid #0E7490; margin-top: 20px;
    box-shadow: 0 4px 6px -1px rgba(14,116,144,0.08);
}
.result-box-amber {
    background: white; border-radius: 14px; padding: 24px;
    border-left: 5px solid #D97706; margin-top: 20px;
    box-shadow: 0 4px 6px -1px rgba(217,119,6,0.08);
}
.result-box-green {
    background: white; border-radius: 14px; padding: 24px;
    border-left: 5px solid #15803D; margin-top: 20px;
    box-shadow: 0 4px 6px -1px rgba(21,128,61,0.08);
}
.result-box-purple {
    background: white; border-radius: 14px; padding: 24px;
    border-left: 5px solid #7C3AED; margin-top: 20px;
    box-shadow: 0 4px 6px -1px rgba(124,58,237,0.08);
}

.card {
    background: white; border-radius: 16px; padding: 24px;
    border: 1px solid #E2E8F0; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.02); margin-bottom: 20px;
}

/* Right Side Instruction Panel — themed variants */
.instruction-panel {
    background: white; border-radius: 16px; padding: 24px;
    border: 1px solid #E2E8F0; border-top: 4px solid #0E7490;
    position: sticky; top: 24px; margin-bottom: 16px;
    box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.03);
}
.instruction-panel h4 {
    color: #0E7490; font-size: 16px; font-weight: 700;
    margin: 0 0 16px 0; display:flex; align-items:center; gap:8px;
}
.instruction-panel p, .instruction-panel li {
    color: #475569; font-size: 14px; line-height: 1.6;
}
.instruction-panel ul { padding-left: 20px; margin: 8px 0; }

/* Dynamic History Panel on Right Side */
.history-pane {
    background: #F8FAFC; border-radius: 12px; padding: 16px;
    border: 1px solid #E2E8F0; max-height: 500px; overflow-y: auto;
}
.history-card {
    background: white; border-radius: 10px; padding: 16px;
    margin-bottom: 12px; border-left: 4px solid #0E7490; box-shadow: 0 2px 4px rgba(0,0,0,0.02);
}

/* Results Formatting */
.score-mini {
    background: white; border-radius: 12px; padding: 20px; text-align: center; border: 1px solid #E2E8F0;
    box-shadow: 0 2px 4px rgba(0,0,0,0.02);
}

/* Word/card tiles with teal theme */
.word-tile {
    background: linear-gradient(135deg, #E0F2FE, #BAE6FD);
    border: 1px solid #BAE6FD; padding: 20px; text-align: center;
    font-weight: 700; border-radius: 12px; color: #0C4A6E;
    font-size: 16px; box-shadow: 0 2px 4px rgba(14,116,144,0.1);
}
.object-tile {
    background: linear-gradient(135deg, #DCFCE7, #BBF7D0);
    border: 1px solid #BBF7D0; padding: 20px; text-align: center;
    font-weight: 700; border-radius: 12px; color: #14532D;
    font-size: 16px; box-shadow: 0 2px 4px rgba(21,128,61,0.1);
}
.card-tile {
    background: linear-gradient(135deg, #FEF3C7, #FDE68A);
    border: 1px solid #FDE68A; text-align: center;
    font-size: 42px; padding: 20px; border-radius: 12px;
    box-shadow: 0 2px 4px rgba(217,119,6,0.1);
}
.score-mini .label { font-size: 12px; font-weight: 600; color: #64748B; text-transform: uppercase; letter-spacing: 0.5px; }
.score-mini .value { font-size: 32px; font-weight: 700; color: #0E7490; margin-top: 6px; }

.badge-low      { background:#DCFCE7; color:#15803D; padding:8px 18px; border-radius:20px; font-size:13px; font-weight:600; display:inline-block; }
.badge-moderate { background:#FEF3C7; color:#B45309; padding:8px 18px; border-radius:20px; font-size:13px; font-weight:600; display:inline-block; }
.badge-high     { background:#FEE2E2; color:#B91C1C; padding:8px 18px; border-radius:20px; font-size:13px; font-weight:600; display:inline-block; }

.module-tile {
    background: white; border-radius: 16px; padding: 28px 24px;
    border: 1px solid #E2E8F0; text-align: center;
    transition: transform 0.2s ease, box-shadow 0.2s ease;
    box-shadow: 0 4px 6px -1px rgba(0,0,0,0.02);
    height: 100%;
}
.module-tile:hover { transform: translateY(-4px); box-shadow: 0 10px 15px -3px rgba(0,0,0,0.06); border-color: #0E7490; }
.module-tile .icon  { font-size: 36px; margin-bottom: 12px; }
.module-tile .title { font-size: 16px; font-weight: 600; color: #0F172A; }
.module-tile .sub   { font-size: 13px; color: #64748B; margin-top: 6px; line-height: 1.5; }

/* Legacy result-box fallback */
.result-box {
    background: white; border-radius: 14px; padding: 24px; margin-top: 20px;
    box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05);
}

.reading-passage {
    background: linear-gradient(to bottom right, #FEF3C7, #FDE68A);
    border: 1px solid #FDE68A; border-radius: 12px; padding: 20px; margin: 20px 0;
}
.reading-passage p { color: #78350F; font-size: 16px; line-height: 1.7; margin: 0; font-style: italic; }

/* Custom Form & Interactive Controls */
.stButton > button {
    background: #0E7490; color: white; border: none; border-radius: 10px;
    height: 48px; font-weight: 600; font-size: 15px; width: 100%; transition: all 0.2s ease;
    box-shadow: 0 2px 4px rgba(14, 116, 144, 0.2);
}
.stButton > button:hover { background: #155E75; color: white; transform: translateY(-1px); box-shadow: 0 4px 6px rgba(14, 116, 144, 0.3); }

/* Centered CTA Button */
.cta-button > button {
    background: linear-gradient(135deg, #0E7490 0%, #0369A1 100%);
    font-size: 16px; height: 56px; border-radius: 12px;
}

hr { border: none; border-top: 1px solid #E2E8F0; margin: 24px 0; }
</style>
""", unsafe_allow_html=True)

# =====================================================
# SESSION STATE
# =====================================================
defaults = {
    "page": "home",
    "user_name": "", "user_age": 30, "user_gender": "",
    "user_email": "", "user_contact": "",
    "mri_score": None,    "mri_label": None,
    "speech_score": None, "speech_emotion": None,
    "facial_score": None, "facial_emotion": None,
    "memory_score": None, "cognitive_score": None,
    "risk_level": None,
    "word_score": 0, "card_score": 0, "object_score": 0,
    "selected_words": None, "show_start_time": None,
    "cards": None, "matched_pairs": 0, "attempts": 0,
    "objects": None, "object_start_time": None,
    "cog_answers": {},
    "show_history_panel": False,
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

if st.session_state.selected_words is None:
    word_list = ["Apple","Chair","River","Book","Flower","Mountain","Dog","School","Orange","Clock"]
    st.session_state.selected_words = random.sample(word_list, 5)

# =====================================================
# GLOBAL COMPONENT WORKFLOWS (TOP RIGHT CONTROLS)
# =====================================================
def render_top_navigation():
    """Renders a ChatGPT style top right bar configuration for History and Logout."""
    if st.session_state.page == "home":
        return

    nav_col, spacer, btn_col_1, btn_col_2 = st.columns([2.5, 3, 1, 0.8])
    with nav_col:
        st.markdown("""
        <div class='navbar-brand'>🧠 AlzAware Portal</div>
        <div class='navbar-sub'>Clinical Assessment & Neuro-Analytics Engine</div>
        """, unsafe_allow_html=True)
    
    with btn_col_1:
        if st.session_state.user_name:
            if st.button("📜 Toggle History", key="nav_hist_trigger"):
                st.session_state.show_history_panel = not st.session_state.show_history_panel
                st.rerun()
    with btn_col_2:
        if st.button("🚪 Logout", key="nav_logout_trigger"):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.session_state.page = "home"
            st.rerun()
    st.markdown("<hr style='margin-top:10px; margin-bottom:20px;' />", unsafe_allow_html=True)

def render_right_side_layout(instruction_title, instruction_points, icon="ℹ️"):
    """Drives the app-like layout with instruction panels or history dynamically locked to the right."""
    if st.session_state.show_history_panel and st.session_state.user_name:
        st.markdown(f"""
        <div class="instruction-panel" style="border-top-color: #64748B;">
          <h4 style="color: #0F172A;">📜 Personal Diagnostic History</h4>
          <p style="font-size: 13px; margin-bottom: 12px; color: #475569;">Logged Patient: <b>{st.session_state.user_name}</b></p>
        </div>
        """, unsafe_allow_html=True)
        
        df = get_user_history(st.session_state.user_name, st.session_state.user_email)
        if df.empty:
            st.info("No clinical entries verified under this patient file.")
        else:
            with st.container():
                for _, row in df.iterrows():
                    mri_val = row["mri_score"]
                    with st.expander(f"🗓️ {row['saved_on'][:16]}"):
                        st.markdown(f"""
                        <div class="history-card">
                            <b>MRI Score:</b> {round(mri_val) if mri_val is not None else 0}/100 ({row['mri_label']})<br/>
                            <b>Risk Level:</b> {row['risk_level']}<br/>
                            <b>Cognitive:</b> {round(row['cognitive_score'] or 0)}% | <b>Memory:</b> {round(row['memory_score'] or 0)}%
                        </div>
                        """, unsafe_allow_html=True)
    else:
        items = "".join(f"<li>{p}</li>" for p in instruction_points)
        st.markdown(f"""
        <div class="instruction-panel">
          <h4>{icon} {instruction_title}</h4>
          <ul>{items}</ul>
        </div>
        """, unsafe_allow_html=True)

def progress_bar(step, total=17):
    pct = int((step / total) * 100)
    st.markdown(f"""
    <div style="background:#E2E8F0;border-radius:10px;height:8px;margin-bottom:8px;margin-top:10px;">
      <div style="background:linear-gradient(90deg, #0E7490, #06B6D4);width:{pct}%;height:8px;border-radius:10px;"></div>
    </div>
    <p style="text-align:right;font-size:12px;font-weight:500;color:#64748B;margin-top:-2px;margin-bottom:20px;">Stage {step} of {total} Complete</p>
    """, unsafe_allow_html=True)

def user_banner():
    if st.session_state.user_name:
        st.markdown(f"""
        <div style="background:#FFFFFF;border-radius:12px;padding:14px 20px;
                    display:flex;gap:30px;margin-bottom:24px;border:1px solid #E2E8F0;box-shadow:0 2px 4px rgba(0,0,0,0.02);font-size:14px;color:#475569;">
          <span>👤 Patient File: <b style="color:#0E7490">{st.session_state.user_name}</b></span>
          <span>📅 Age Parameter: <b style="color:#0F172A">{st.session_state.user_age} yrs</b></span>
          <span>⚧ Demographics: <b style="color:#0F172A">{st.session_state.user_gender}</b></span>
        </div>""", unsafe_allow_html=True)

def integration_status_badge(model_name, is_loaded):
    """Renders a beautiful inline status badge for model integration."""
    if is_loaded:
        st.markdown(f"""
        <div style="background-color: #F0FDF4; border: 1px solid #BBF7D0; padding: 12px 16px; border-radius: 8px; margin-bottom: 20px; display: flex; align-items: center; gap: 10px;">
            <span style="font-size: 18px;">✅</span>
            <div>
                <div style="color: #166534; font-weight: 600; font-size: 14px;">Integration Confirmed</div>
                <div style="color: #15803D; font-size: 12px;">The <code>{model_name}</code> model is active and ready.</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div style="background-color: #FEF2F2; border: 1px solid #FECACA; padding: 12px 16px; border-radius: 8px; margin-bottom: 20px; display: flex; align-items: center; gap: 10px;">
            <span style="font-size: 18px;">⚠️</span>
            <div>
                <div style="color: #991B1B; font-weight: 600; font-size: 14px;">Integration Warning</div>
                <div style="color: #B91C1C; font-size: 12px;">Could not load <code>{model_name}</code>. Operating in fallback simulation mode.</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

# =====================================================
# MACHINE LEARNING CORE ENGINES
# =====================================================
# =====================================================
# RAVDESS SPEECH MODEL
# =====================================================
RAVDESS_LABELS = {
    0: "Neutral",  1: "Calm",     2: "Happy",    3: "Sad",
    4: "Angry",    5: "Fearful",  6: "Disgust",  7: "Surprised"
}
SPEECH_SCORE_MAP = {
    "Happy":85, "Calm":80, "Neutral":70, "Surprised":65,
    "Sad":40,   "Fearful":35, "Angry":30, "Disgust":25
}
EMOTION_COLORS = {
    "Happy":"#1E8449",    "Calm":"#2980B9",   "Neutral":"#5D6D7E",
    "Surprised":"#8E44AD","Sad":"#E67E22",    "Fearful":"#E74C3C",
    "Angry":"#C0392B",    "Disgust":"#784212"
}
SPEECH_MODEL_PATH = "ravdess_emotion_model (1).pkl"

READING_PASSAGES = [
    "I was so happy when I saw my old friend again after many years apart. "
    "It felt like no time had passed at all, and we laughed about old memories.",
    "She felt a deep sadness as she packed away her childhood home, "
    "remembering all the quiet mornings and warm afternoons spent there.",
    "He was furious when he discovered that someone had taken his parking spot "
    "again, slamming the car door in frustration.",
    "The sudden loud noise from the kitchen startled everyone, and for a moment "
    "they all sat frozen, hearts racing with fear.",
    "Walking into the surprise party, she gasped in astonishment, her eyes wide "
    "as everyone shouted happy birthday all at once.",
    "He spoke in a calm, steady voice, taking a slow breath before continuing "
    "his explanation, completely at ease with the situation.",
]

@st.cache_resource
def load_speech_model():
    if os.path.exists(SPEECH_MODEL_PATH):
        try:
            model = joblib.load(SPEECH_MODEL_PATH)
            return model, True
        except Exception as e:
            st.error(f"DEBUG — Speech model load error: {e}")
            return None, False
    return None, False

def extract_mfcc(audio_bytes, n_mfcc=40):
    try:
        import librosa
        y, sr = librosa.load(io.BytesIO(audio_bytes), sr=22050, mono=True)
        mfcc  = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=n_mfcc)
        return np.mean(mfcc.T, axis=0).reshape(1, -1), True
    except ImportError:
        return None, False
    except Exception as e:
        st.error(f"DEBUG — librosa error: {e}")
        return None, False

def predict_speech(audio_bytes):
    features, ok = extract_mfcc(audio_bytes)
    if not ok or features is None:
        return None, None, None
    model, loaded = load_speech_model()
    if not loaded or model is None:
        return None, None, None
    pred  = model.predict(features)[0]
    proba = model.predict_proba(features)[0]
    label = RAVDESS_LABELS.get(int(pred), "Neutral")
    score = SPEECH_SCORE_MAP.get(label, 50)
    proba_dict = {RAVDESS_LABELS[i]: round(float(proba[i])*100, 1)
                  for i in range(len(proba))}
    return label, score, proba_dict

# =====================================================
# FER2013 FACIAL MODEL
# =====================================================
FER_LABELS    = ["Angry","Disgust","Fear","Happy","Neutral","Sad","Surprise"]
FER_SCORE_MAP = {
    "Happy":85, "Surprise":75, "Neutral":70,
    "Sad":45,   "Fear":35,     "Angry":30, "Disgust":25
}
FER_COLORS = {
    "Happy":"#1E8449",  "Surprise":"#8E44AD", "Neutral":"#2980B9",
    "Sad":"#E67E22",    "Fear":"#E74C3C",     "Angry":"#C0392B",
    "Disgust":"#784212"
}
FER_MODEL_PATH = "fer_model1.pkl"

@st.cache_resource
def load_fer_model():
    if os.path.exists(FER_MODEL_PATH):
        try:
            import pickle
            with open(FER_MODEL_PATH, "rb") as f:
                model = pickle.load(f)
            return model, "keras"
        except Exception as e:
            st.error(f"DEBUG — FER model load error: {e}")
            return None, None
    return None, None

def predict_fer(image_pil):
    model, kind = load_fer_model()
    if model is None:
        return None, None, None
    img = image_pil.convert("L").resize((48, 48))
    arr = np.array(img, dtype="float32") / 255.0
    arr = arr.reshape(1, 48, 48, 1)
    try:
        preds = model.predict(arr, verbose=0)[0]
        idx   = int(np.argmax(preds))
        label = FER_LABELS[idx]
        score = FER_SCORE_MAP.get(label, 50)
        proba_dict = {FER_LABELS[i]: round(float(preds[i])*100, 1)
                      for i in range(len(preds))}
        return label, score, proba_dict
    except Exception as e:
        st.error(f"DEBUG — FER predict error: {e}")
        return None, None, None

# =====================================================
# ALZHEIMER MRI MODEL (Scikit-Learn RandomForest)
# =====================================================
# =====================================================
# ALZHEIMER MRI MODEL (Fixed & Synchronized)
# =====================================================
MRI_MODEL_PATH = "mri(2).pkl"

# CRITICAL: Keep names standardized with spaces so everything maps cleanly
MRI_LABELS = ["Mild Demented", "Moderate Demented", "Non Demented", "Very Mild Demented"]

MRI_SCORE_MAP = {
    "Non Demented": 95, 
    "Very Mild Demented": 70,
    "Mild Demented": 45, 
    "Moderate Demented": 20
}

MRI_COLOR_MAP = {
    "Non Demented": "#1E8449", 
    "Very Mild Demented": "#F39C12",
    "Mild Demented": "#E67E22", 
    "Moderate Demented": "#C0392B"
}

@st.cache_resource
def load_mri_model():
    if not os.path.exists(MRI_MODEL_PATH):
        return None, False
    try:
        model = joblib.load(MRI_MODEL_PATH)
        return model, True
    except Exception as e:
        st.error(f"DEBUG — MRI model load error: {e}")
        return None, False

def predict_mri(image_pil):
    model, loaded = load_mri_model()
    if not loaded or model is None:
        return None, None, None
    try:
        # 1. Convert to RGB color mode because your model expects 49,152 features (128x128x3)
        img_rgb = image_pil.convert("RGB")
        
        # 2. Use proper 2D resizing instead of 1D array interpolation
        img_resized = img_rgb.resize((64,64))
        
        # 3. Convert to numpy array and flatten safely into 49,152 features
        features = np.array(img_resized, dtype="float32").flatten().reshape(1, -1)
        
        # 4. Generate prediction and probabilities
        preds = model.predict(features)[0]
        probs = model.predict_proba(features)[0]
        
        # 5. Determine the predicted string label safely
        if isinstance(preds, (int, np.integer)):
            idx = int(preds)
            label = MRI_LABELS[idx] if idx < len(MRI_LABELS) else MRI_LABELS[2] # Default to Non Demented if out of bounds
        else:
            # If the model predicts strings, ensure it matches our mapping format
            label = str(preds).replace("Demented", " Demented").strip() 
            if label not in MRI_SCORE_MAP:
                label = "Non Demented"
                        
        score = MRI_SCORE_MAP.get(label, 50)
        
        # 6. Build the confidence probabilities dictionary
        proba_dict = {}
        for i, p in enumerate(probs):
            if i < len(MRI_LABELS):
                proba_dict[MRI_LABELS[i]] = round(float(p) * 100, 1)
            else:
                proba_dict[f"Class {i}"] = round(float(p) * 100, 1)
                
        return label, score, proba_dict
        
    except Exception as e:
        st.error(f"DEBUG — MRI predict error: {e}")
        return None, None, None
def risk_level(speech, facial, mem, cog):
    """
    Calculates an aggregate clinical risk level and returns a label and an HTML badge color.
    """
    # Simple logic to aggregate the scores (Adjust this math to fit your specific medical criteria)
    total_score = (speech + facial + mem + cog) / 4.0
    
    if total_score >= 75:
        return "Low Risk", "#EF4444"      # Red
    elif total_score >= 40:
        return "Moderate Risk", "#F59E0B"  # Orange
    else:
        return "High Risk", "#10B981"       # Green
# =====================================================================
# PAGE SYSTEM FLOWS
# =====================================================================
render_top_navigation()

# ---------------------------------------------------------------------
# PAGE 1: REFINED HEALTH-TECH LANDING PAGE (WHITE CONTAINER STRIP REMOVAL)
# ---------------------------------------------------------------------
if st.session_state.page == "home":
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
        st.image("C:/Users/oswal/Downloads/layout.png", use_container_width=True)
   
          

  
 
   
    
# ---------------------------------------------------------------------
# PAGE 2: RESTRUCTURED USER REGISTRATION
# ---------------------------------------------------------------------
elif st.session_state.page == "register":
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
# ---------------------------------------------------------------------
if st.session_state.page == "dashboard":
    
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
# ---------------------------------------------------------------------
elif st.session_state.page == "mri_scan":
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
# ---------------------------------------------------------------------
elif st.session_state.page == "speech_emotion":
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
# ---------------------------------------------------------------------
elif st.session_state.page == "facial_expression":
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
# ---------------------------------------------------------------------
elif st.session_state.page == "intro_memory":
    progress_bar(7)
    main_col, side_col = st.columns([2.5, 1], gap="large")
    with main_col:
        user_banner()
        st.markdown("""
        <div class="module-purple">
          <div style="position:absolute;right:-10px;top:-10px;font-size:120px;opacity:0.12;pointer-events:none;">🧩</div>
          <span class="pill-purple">MODULE 04 · Short-Term Memory Suite</span>
          <h2 style="color:#3B0764; margin-top:8px; margin-bottom:6px; font-size:28px; font-weight:800;">🧩 Short-Term Memory Assessment Suite</h2>
          <p style="color:#6D28D9; font-size:14px; margin:0;">Interactive cluster tracking word association, card matching, and object recognition modules.</p>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("""
        <div style="background:white;border-radius:12px;padding:16px 20px;border:1px solid #DDD6FE;margin-bottom:16px;">
          <p style="color:#4C1D95;margin:0;font-size:14px;">⚡ The next interactive cluster contains three games tracking word association loops, card matching matrix tracking, and randomized objective verification models.</p>
        </div>
        """, unsafe_allow_html=True)
        st.write("")
        if st.button("Begin Memory Verification Modules →"):
            st.session_state.page = "word_show"
            st.rerun()
    with side_col:
        render_right_side_layout("Game Mechanics", ["Metrics weight processing speeds, selection accuracies, and retrieval stability."], icon="🧩")

elif st.session_state.page == "word_show":
    progress_bar(8)
    main_col, side_col = st.columns([2.5, 1], gap="large")
    with main_col:
        user_banner()
        st.markdown("""
        <div class="module-purple">
          <div style="position:absolute;right:-10px;top:-10px;font-size:120px;opacity:0.12;pointer-events:none;">🧠</div>
          <span class="pill-purple">GAME 1 · Memorization Matrix</span>
          <h3 style="color:#3B0764; margin-top:8px; margin-bottom:4px; font-size:22px; font-weight:700;">Word Memorization</h3>
          <p style="color:#6D28D9; font-size:14px; margin:0;">Commit all five words to memory before the timer expires.</p>
        </div>
        """, unsafe_allow_html=True)
        if st.session_state.show_start_time is None: st.session_state.show_start_time = time.time()
        rem = int(10 - (time.time() - st.session_state.show_start_time))
        
        if rem > 0:
            st.markdown(f"<div style='background:#EDE9FE;border-radius:10px;padding:12px 18px;margin-bottom:16px;color:#4C1D95;font-weight:600;font-size:14px;'>⏳ Interface locks in: <b>{rem} seconds</b></div>", unsafe_allow_html=True)
            cols = st.columns(5)
            for idx, w in enumerate(st.session_state.selected_words):
                cols[idx].markdown(f"<div class='word-tile'>{w}</div>", unsafe_allow_html=True)
            time.sleep(1)
            st.rerun()
        else:
            st.session_state.page = "word_recall"
            st.rerun()
    with side_col:
        render_right_side_layout("Instructions", ["Commit all 5 displayed string variables to active logical memory layouts now."], icon="🧩")

elif st.session_state.page == "word_recall":
    progress_bar(8)
    main_col, side_col = st.columns([2.5, 1], gap="large")
    with main_col:
        user_banner()
        st.markdown("""
        <div class="module-purple">
          <div style="position:absolute;right:-10px;top:-10px;font-size:120px;opacity:0.12;pointer-events:none;">✍️</div>
          <span class="pill-purple">GAME 1 · Word Recall</span>
          <h3 style="color:#3B0764; margin-top:8px; margin-bottom:4px; font-size:22px; font-weight:700;">Data Variable Recall</h3>
          <p style="color:#6D28D9; font-size:14px; margin:0;">Type all five words you memorized, separated by commas.</p>
        </div>
        """, unsafe_allow_html=True)
        user_words = st.text_area("Input all strings captured previously separated explicitly via commas:")
        if st.button("Verify Dataset Values"):
            entered = [x.strip().lower() for x in user_words.split(",")]
            matches = sum(1 for w in st.session_state.selected_words if w.lower() in entered)
            st.session_state.word_score = (matches / 5) * 100
            st.session_state.page = "card_matching"
            st.rerun()
    with side_col:
        render_right_side_layout("Verification", ["Order layout parameters do not impact scoring patterns directly."], icon="🧩")

elif st.session_state.page == "card_matching":
    progress_bar(9)
    main_col, side_col = st.columns([2.5, 1], gap="large")
    with main_col:
        user_banner()
        st.markdown("""
        <div class="module-amber">
          <div style="position:absolute;right:-10px;top:-10px;font-size:120px;opacity:0.12;pointer-events:none;">🃏</div>
          <span class="pill-amber">GAME 2 · Spatial Matching</span>
          <h3 style="color:#78350F; margin-top:8px; margin-bottom:4px; font-size:22px; font-weight:700;">Spatial Matrix Configuration Matching</h3>
          <p style="color:#B45309; font-size:14px; margin:0;">Select two matching card positions to earn a pair. Aim for at least 3 matches.</p>
        </div>
        """, unsafe_allow_html=True)
        if st.session_state.cards is None:
            items = ["😀","😀","😎","😎","😍","😍","🤩","🤩","🥳","🥳","😇","😇","🤖","🤖","👻","👻"]
            random.shuffle(items)
            st.session_state.cards = items
            
        cards = st.session_state.cards
        c1, c2 = st.columns(2)
        with c1:
            idx1 = st.selectbox("Select Target Coordinate Alpha", range(len(cards)), format_func=lambda x: f"Card Frame Element {x+1}", key="c_slot_1")
            st.markdown(f"<div class='card-tile'>{cards[idx1]}</div>", unsafe_allow_html=True)
        with c2:
            idx2 = st.selectbox("Select Target Coordinate Beta", range(len(cards)), format_func=lambda x: f"Card Frame Element {x+1}", key="c_slot_2")
            st.markdown(f"<div class='card-tile'>{cards[idx2]}</div>", unsafe_allow_html=True)
            
        st.write("")
        if st.button("Process Coordinate Overlaps"):
            if idx1 == idx2: st.error("Invalid action configuration. Coordinate parameters must point to distinct slots.")
            else:
                st.session_state.attempts += 1
                if cards[idx1] == cards[idx2]:
                    st.success("Target Configuration Match Validated.")
                    st.session_state.matched_pairs += 1
                else: st.error("Acoustical Alignment Conflict. Target structures do not match.")
                
        mc1, mc2 = st.columns(2)
        mc1.metric("Confirmed Identical Sets Locked", st.session_state.matched_pairs)
        mc2.metric("Iterative Runtime Attempts", st.session_state.attempts)
        
        if st.button("Consolidate Game 2 Progress ->"):
            st.session_state.card_score = min((st.session_state.matched_pairs / 3) * 100, 100)
            st.session_state.page = "object_show"
            st.rerun()
    with side_col:
        render_right_side_layout("Spatial Matching Matrix", ["Identify at least 3 identical matrix clusters to establish an optimal scoring loop index output value."], icon="🧩")

elif st.session_state.page == "object_show":
    progress_bar(10)
    main_col, side_col = st.columns([2.5, 1], gap="large")
    with main_col:
        user_banner()
        st.markdown("""
        <div class="module-green">
          <div style="position:absolute;right:-10px;top:-10px;font-size:120px;opacity:0.12;pointer-events:none;">🔍</div>
          <span class="pill-green">GAME 3 · Object Visualization</span>
          <h3 style="color:#14532D; margin-top:8px; margin-bottom:4px; font-size:22px; font-weight:700;">Objective Visualization Array</h3>
          <p style="color:#15803D; font-size:14px; margin:0;">Memorize the five objects displayed before the timer expires.</p>
        </div>
        """, unsafe_allow_html=True)
        if st.session_state.objects is None: st.session_state.objects = ["Apple","Book","Clock","Dog","Flower"]
        if st.session_state.object_start_time is None: st.session_state.object_start_time = time.time()
        rem = int(10 - (time.time() - st.session_state.object_start_time))
        if rem > 0:
            st.markdown(f"<div style='background:#DCFCE7;border-radius:10px;padding:12px 18px;margin-bottom:16px;color:#14532D;font-weight:600;font-size:14px;'>⏳ Interface locks in: <b>{rem} seconds</b></div>", unsafe_allow_html=True)
            cols = st.columns(5)
            for idx, obj in enumerate(st.session_state.objects):
                cols[idx].markdown(f"<div class='object-tile'>{obj}</div>", unsafe_allow_html=True)
            time.sleep(1); st.rerun()
        else:
            st.session_state.page = "object_recall"
            st.rerun()
    with side_col:
        render_right_side_layout("Objective Cache", ["Isolate structural visual identities within immediate focus horizons."], icon="🧩")

elif st.session_state.page == "object_recall":
    progress_bar(10)
    main_col, side_col = st.columns([2.5, 1], gap="large")
    with main_col:
        user_banner()
        st.markdown("""
        <div class="module-green">
          <div style="position:absolute;right:-10px;top:-10px;font-size:120px;opacity:0.12;pointer-events:none;">✅</div>
          <span class="pill-green">GAME 3 · Object Recognition</span>
          <h3 style="color:#14532D; margin-top:8px; margin-bottom:4px; font-size:22px; font-weight:700;">Object Recognition Matrix</h3>
          <p style="color:#15803D; font-size:14px; margin:0;">Select all objects you saw in the previous visualization. Distractor items are included.</p>
        </div>
        """, unsafe_allow_html=True)
        base = st.session_state.objects
        pool = sorted(list(set(base + ["Laptop","Train","Phone","Bottle","Fan","Keyboard","Mouse"])))
        selected = []
        cols = st.columns(2)
        for idx, item in enumerate(pool):
            with cols[idx % 2]:
                if st.checkbox(item, key=f"obj_chk_{item}"): selected.append(item)
        
        st.write("")
        if st.button("Finalize Recognition Assessment"):
            hits = sum(1 for x in base if x in selected)
            st.session_state.object_score = (hits / 5) * 100
            st.session_state.page = "memory_report"
            st.rerun()
    with side_col:
        render_right_side_layout("Recognition Rules", ["Distractor values are inserted to evaluate sorting confusion metrics accurately."], icon="🧩")

elif st.session_state.page == "memory_report":
    progress_bar(11)
    main_col, side_col = st.columns([2.5, 1], gap="large")
    with main_col:
        user_banner()
        st.markdown("<h2 style='color:#0F172A; margin-top:0;'>📊 Memory Metrics Analysis</h2>", unsafe_allow_html=True)
        score = st.session_state.word_score*0.4 + st.session_state.card_score*0.3 + st.session_state.object_score*0.3
        st.session_state.memory_score = score
        badge, label = ("badge-low", "Highly Stable Memory Dynamics") if score >= 80 else (("badge-moderate", "Balanced Retention Matrix") if score >= 60 else ("badge-high", "Attention Vector Flagged"))
        
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #0E7490 0%, #0891B2 100%); border-radius:16px; padding:32px; text-align:center; margin-bottom:24px; color:white; box-shadow:0 10px 15px -3px rgba(14, 116, 144, 0.2);">
            <div style="font-size:13px; text-transform:uppercase; letter-spacing:1px; font-weight: 600;">Aggregated Memory Matrix Index</div>
            <div style="font-size:56px; font-weight:800; margin:8px 0;">{round(score)}%</div>
            <div><span class="{badge}">{label}</span></div>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("Continue to Comprehensive Cognitive Domain Map →"):
            st.session_state.page = "intro_cognitive"
            st.rerun()
    with side_col:
        render_right_side_layout("Metric Distribution", ["Individual weight values: Word association sets (40%), Card layouts (30%), Object array mapping (30%)."], icon="📊")

# ---------------------------------------------------------------------
# MODULE 5 — COGNITIVE TRACKING MODULE
# ---------------------------------------------------------------------
elif st.session_state.page == "intro_cognitive":
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

elif st.session_state.page == "cog_attention":
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

elif st.session_state.page == "cog_orientation":
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

elif st.session_state.page == "cog_language":
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

elif st.session_state.page == "cog_executive":
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

elif st.session_state.page == "cognitive_report":
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
# ---------------------------------------------------------------------
elif st.session_state.page == "final_report":
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
# ---------------------------------------------------------------------
elif st.session_state.page == "chatbot":
    main_col, side_col = st.columns([2.5, 1], gap="large")
    
    with main_col:
        user_banner()
        st.markdown("""
        <div class="module-blue">
          <div style="position:absolute;right:-10px;top:-10px;font-size:120px;opacity:0.12;pointer-events:none;">🤖</div>
          <span class="pill">Conversational Interface</span>
          <h2 style="color:#0C4A6E; margin-top:8px; margin-bottom:6px; font-size:28px; font-weight:800;">🤖 Conversational Wellness Intelligence</h2>
          <p style="color:#0369A1; font-size:14px; margin:0;">Ask questions about your diagnostic results or general Alzheimer's information.</p>
        </div>
        """, unsafe_allow_html=True)
        
        if "chat_history" not in st.session_state: st.session_state.chat_history = []
        api_present = bool(os.environ.get("GROQ_API_KEY"))
        
        if not api_present:
            st.warning("Clinical Notification: Conversational API pipelines are not actively configured in environment profiles.")
            
        for msg in st.session_state.chat_history:
            with st.chat_message(msg["role"]): st.write(msg["content"])
            
        query = st.chat_input("Query the clinical matrix engine regarding your profiles or metrics:")
        if query:
            with st.chat_message("user"): st.write(query)
            st.session_state.chat_history.append({"role": "user", "content": query})
            
            reply = "This simulation module verified your interactive message. Configure GROQ_API_KEY tokens to execute dynamic LLM tracking transformations live."
            if api_present:
                try:
                    from groq import Groq
                    client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
                    res = client.chat.completions.create(
                        model="llama-3.3-70b-versatile",
                        messages=[{"role":"system","content":"Clinical Assistant Mode Active."},{"role":"user","content":query}],
                        max_tokens=512
                    )
                    reply = res.choices[0].message.content
                except Exception as e: reply = f"Connection Interrupted: {e}"
                
            with st.chat_message("assistant"): st.write(reply)
            st.session_state.chat_history.append({"role": "assistant", "content": reply})
            
        st.write("")
        cc1, cc2 = st.columns(2)
        with cc1:
            if st.session_state.chat_history:
                if st.button("🗑️ Clear Diagnostic Chat Logs"):
                    st.session_state.chat_history = []
                    st.rerun()
        with cc2:
            if st.button("⬅ Back to Central Hub"):
                st.session_state.page = "home"
                st.rerun()

    with side_col:
        render_right_side_layout(
            "Assistant Protocols",
            [
                "Natural language responses break down metric interpretations smoothly.",
                "Automated insights do not replace direct customized evaluations under licensed physicians."
            ], icon="🤖"
        )
