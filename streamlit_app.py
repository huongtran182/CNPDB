import streamlit as st
from PIL import Image, ImageDraw
import os
import base64
from io import BytesIO
from sidebar import render_sidebar

# Set page config
st.set_page_config(layout="wide", initial_sidebar_state="expanded")

render_sidebar()

# Main content area
st.markdown("""<div style="padding:0;margin:0;">""", unsafe_allow_html=True)

try:
    banner = Image.open("Assets/Img/CNPD_Banner.png")
    st.image(banner, use_container_width=True)
except:
    st.error("Banner image not found")

st.markdown("""
## WELCOME TO CNPD: THE CRUSTACEAN NEUROPEPTIDE DATABASE

Neuropeptides are critical signaling molecules involved in numerous physiological processes, including metabolism, reproduction, development, and behavior. In crustaceans, neuropeptides regulate key biological functions such as molting, feeding, and immune responses. Despite their significance, crustacean neuropeptides remain underrepresented in existing neuropeptide databases.

To address this gap, we introduce **The Crustacean Neuropeptide Database (CNPD)** – A comprehensive resource for neuropeptide research in crustacean species. CNPD systematically curates experimentally confirmed and predicted neuropeptides from various crustacean species using peer-reviewed literature, mass spectrometry-based peptidomics, and public protein databases.

This database provides detailed annotations to support **Comparative neurobiology**, **Functional studies**, and **Computational peptide discovery**.
""")

st.markdown("""
### GET INVOLVED & CONTRIBUTE

CNPD is a community-driven initiative! We welcome contributions from researchers in peptidomics, neurobiology, and comparative physiology.

To collaborate, submit data, or provide feedback, please contact Dr. Lingjun Li at **lingjun.li@wise.edu**
""")

st.markdown("""
### HOW TO CITE
If you use CNPD in your research, please cite:
Crustacean Neuropeptide Database (CNPD): A curated resource for neuropeptide research in crustacean species. [Authors]. [Journal Name], [Year]. DOI: [XXXX].
""")

st.markdown("""
### FUNDING
This work is supported by [Funding Agencies]

For other tools developed by the Li Lab, visit **www.lilabs.org/resources**
""")

st.markdown("""
<div style="text-align: center; font-size: 14px; color: #2a2541;">
  <em>Last update: Jul 2025</em>
</div>
""", unsafe_allow_html=True)
