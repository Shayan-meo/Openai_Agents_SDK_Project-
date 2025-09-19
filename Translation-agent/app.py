import streamlit as st
import asyncio
from agents import Runner
from index import main_agent   # 👈 ye tumhara agent import karega jo index.py me banaya hai

st.set_page_config(page_title="Translation Agent", page_icon="🌍")
st.title("🌍 Translation Agent")
st.write("Translate English text into **Spanish, French, or Italian**.")

# User input box
user_input = st.text_area("Enter your text:", "")

# Button click
if st.button("Translate"):
    if user_input.strip():
        with st.spinner("Translating..."):
            result = asyncio.run(Runner.run(main_agent, user_input))
            st.subheader("Final Response:")
            st.success(result.final_output)
    else:
        st.warning("⚠️ Please enter some text first.")
