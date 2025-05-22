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
st.markdown("""
<div style="display: flex; width: 100%;">
        <div style="flex: 1; background-color: #dadaeb; text-align: center; padding: 20px 0;align-items: center; justify-content: center;">
            <h2 style="color:#4a3666; margin: 0;">12,354</h2>
            <p style="margin: 0; font-weight: bold; color:#4a3666;">Peptide Entries</p>
        </div>
        <div style="flex: 1; background-color: #eeeeee; text-align: center; padding: 20px 0;align-items: center; justify-content: center;">
            <h2 style="color:#4a3666; margin: 0;">47</h2>
            <p style="margin: 0; font-weight: bold; color:#4a3666;">Organisms</p>
        </div>
        <div style="flex: 1; background-color: #dadaeb; text-align: center; padding: 20px 0;align-items: center; justify-content: center;">
            <h2 style="color:#4a3666; margin: 0;">39</h2>
            <p style="margin: 0; font-weight: bold; color:#4a3666;">Neuropeptide Families</p>
        </div>
        <div style="flex: 1; background-color: #eeeeee; text-align: center; padding: 20px 0;align-items: center; justify-content: center;">
            <h2 style="color:#4a3666; margin: 0;">3,218</h2>
            <p style="margin: 0; font-weight: bold; color:#4a3666;">Page Views</p>
        </div>
    </div>
""", unsafe_allow_html=True)

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

