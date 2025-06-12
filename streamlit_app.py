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
## WELCOME TO cNPD: THE CRUSTACEAN NEUROPEPTIDE DATABASE

Neuropeptides are cell-to-cell signaling molecules involved in numerous physiological processes, including metabolism, development, reproduction, and behavior. They are highly conserved both structurally and functionally across the animal kingdom, making the neuropeptide study in simple invertebrate models advantageous for gaining insights into basic neurobiology principles, drug discoveries, and functional investigations that are translatable to mammalian systems.  Crustaceans are profound model organisms for neuropeptide studies and have long been used to investigate the robustness of rhythmic central pattern generator, feeding behavior, and neural responses to external stimuli.

Despite their significance, crustacean neuropeptides remain underrepresented in existing neuropeptide databases. To address this gap, we introduce the **Crustacean Neuropeptide Database (cNPD)** – A comprehensive resource for neuropeptide research in crustacean species. cNPD systematically curates experimentally confirmed and predicted neuropeptides from various crustacean species using genome-derived in silico mining, peer-reviewed literature, mass spectrometry-based peptidomics, and public protein databases. This database provides detailed annotations and sequences to support a range of endeavors, including comparative neurobiology, functional studies, education, and computational peptide discovery.

""")

st.markdown("""
### DATABASE SOURCES AND CURATION
cNPD integrates data from peer-reviewed studies and public proteomics repositories:
•	Experimental Data – Mass spectrometry and other bioassays
•	Literature Mining – Curated from PubMed and primary research papers
•	Public Databases – Cross-linked with UniProt, NCBI, and NeuroPep
•	Computational Predictions – <i>In silico</i> prediction from genomics data
Every neuropeptide entry undergoes manual examination to ensure accuracy and reliability.

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
