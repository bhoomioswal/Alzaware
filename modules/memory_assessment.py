"""
Memory assessment suite: word recall, card matching, object recognition.
"""

import streamlit as st
import pandas as pd
import random
import time
from PIL import Image

from modules.common import *


def render_intro_memory():
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


def render_word_show():
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


def render_word_recall():
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


def render_card_matching():
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


def render_object_show():
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


def render_object_recall():
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


def render_memory_report():
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


            
