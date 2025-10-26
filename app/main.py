# app/main.py
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import streamlit as st
from llama.llama_runner import ask_go
from app.voice_assistant import speak, listen
from auth.session import current_user
from app.router import run_router

st.set_page_config(page_title="GO — Marathon Assistant", layout="centered")

# Header
st.markdown(
    "<h2 style='text-align: center; color: gray;'>Hi, I’m GO</h2>",
    unsafe_allow_html=True
)
st.markdown("<p style='text-align: center; color: gray;'>How can I assist you today?</p>", unsafe_allow_html=True)

# Speak welcome message (once)
if "welcomed" not in st.session_state:
    speak("Hi, I’m GO. How can I assist you today?")
    st.session_state.welcomed = True

# Public Q&A section
st.subheader("Ask GO (public Q&A)")
if st.button("🎙️ Ask a question by voice", key="public_voice"):
    q = listen()
    if not q:
        st.error("Couldn't capture your voice. Try again.")
    else:
        st.markdown(f"**You asked:** {q}")
        # Check if personal
        if any(word in q.lower() for word in ["my reminder", "my schedule", "my training", "my runs", "my goal"]):
            st.warning("You need to log in to access personal data.")
        else:
            ans = ask_go(q)
            st.success(ans)
            speak(ans)

typed_q = st.text_input("Or type your question")
if st.button("Ask GO", key="public_text"):
    if typed_q.strip():
        if any(word in typed_q.lower() for word in ["my reminder", "my schedule", "my training", "my runs", "my goal"]):
            st.warning("You need to log in to access personal data.")
        else:
            ans = ask_go(typed_q)
            st.success(ans)
    else:
        st.warning("Please type something.")

# Router (handles dashboard/login/register for logged users)
st.divider()
run_router()
