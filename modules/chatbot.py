"""
Conversational AI assistant page.
"""

import streamlit as st
import pandas as pd
import random
import time
from PIL import Image

from modules.common import *


def render_chatbot():
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

