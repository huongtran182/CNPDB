import streamlit as st
from sidebar import render_sidebar
from PIL import Image
import os

st.set_page_config(
    page_title="Statistics",
    layout="wide",
    initial_sidebar_state="expanded"
)

render_sidebar()

# ---- Horizontal Stats Bar ----
st.markdown("---")
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("""
    <div style="text-align: center; padding: 10px; background-color: #29004c;">
        <h2 style="color:#4a3666;">12,354</h2>
        <p style="margin: 0; font-weight: bold;">Peptide Entries</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div style="text-align: center; padding: 10px;">
        <h2 style="color:#4a3666;">47</h2>
        <p style="margin: 0; font-weight: bold;">Organisms</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div style="text-align: center; padding: 10px;">
        <h2 style="color:#4a3666;">39</h2>
        <p style="margin: 0; font-weight: bold;">Neuropeptide Families</p>
    </div>
    """, unsafe_allow_html=True)

with col4:
    # Replace this with a live counter if you implement it later
    st.markdown("""
    <div style="text-align: center; padding: 10px;">
        <h2 style="color:#4a3666;">3,218</h2>
        <p style="margin: 0; font-weight: bold;">Page Views</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# ---- Section: Composition Chart ----
st.markdown("## 1. Composition of Neuropeptides per Organism in cNPD")

# Load and display the image
image_path = os.path.join("Assets", "Statistics", "Composition.png")
if os.path.exists(image_path):
    image = Image.open(image_path)
    st.image(image, use_column_width=True)
else:
    st.error(f"Image not found at {image_path}")


st.markdown("""
<div style="text-align: center; font-size:14px; color:#2a2541;">
  <em>Last update: Jul 2025</em>
</div>
""", unsafe_allow_html=True)

