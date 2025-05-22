import streamlit as st
from sidebar import render_sidebar
import os

st.set_page_config(
    page_title="Tutorials",
    layout="wide",
    initial_sidebar_state="expanded"
)

render_sidebar()

st.markdown("""
<h3 style="margin-top: 10px; margin-bottom: 10px; text-align: center;">
1. How to navigate cNPD website
</h3>
""", unsafe_allow_html=True)
video_path = os.path.join("Assets", "Statistics", "example.mp4")
if os.path.exists(video_path):
    st.video(video_path)
else:
    st.error(f"Video not found at {video_path}")

st.markdown("""
<h3 style="margin-top: 10px; margin-bottom: 10px; text-align: center;">
2. How to use Database Search Engine to search for your desired peptides and download FASTA file
</h3>
""", unsafe_allow_html=True)
video_path = os.path.join("Assets", "Statistics", "search_tutorial.mp4")
if os.path.exists(video_path):
    st.video(video_path)
else:
    st.error(f"Video not found at {video_path}")

st.markdown("""
<div style="text-align: center; font-size:14px; color:#2a2541;">
  <em>Last update: Jul 2025</em>
</div>
""", unsafe_allow_html=True)

