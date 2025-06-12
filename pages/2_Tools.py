import streamlit as st
from sidebar import render_sidebar

st.set_page_config(
    page_title="Tools",
    layout="wide",
    initial_sidebar_state="expanded"
)

render_sidebar()

st.markdown("""
## OVERVIEW

The current release of **CNPD (Version 1.0, 2025)** contains **[X]** curated neuropeptide entries from **[Y]** crustacean species, organized into **[Z]** neuropeptide families.

Data is manually curated from peer-reviewed literature, mass spectrometry-based peptidomics, and public protein databases such as **UniProt** and **NCBI**.
""")


st.markdown("""
<div style="text-align: center; font-size:14px; color:#2a2541;">
  <em>Last update: Jul 2025</em>
</div>
""", unsafe_allow_html=True)

