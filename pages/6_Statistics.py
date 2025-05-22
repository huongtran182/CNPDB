import streamlit as st
from sidebar import render_sidebar
from PIL import Image
import os
import base64

st.set_page_config(
    page_title="Statistics",
    layout="wide",
    initial_sidebar_state="expanded"
)

render_sidebar()

# ---- Horizontal Stats Bar ----
st.markdown("""
<div style="display: flex; width: 100%;">
        <div style="flex: 1; background-color: #dadaeb; text-align: center; padding: 20px 0;">
            <h2 style="color:#4a3666; margin-left: 15px;">12,354</h2>
            <p style="margin: 0; font-weight: bold; color:#4a3666;">Peptide Entries</p>
        </div>
        <div style="flex: 1; background-color: #eeeeee; text-align: center; padding: 20px 0;">
            <h2 style="color:#4a3666; margin-left: 15px;">47</h2>
            <p style="margin: 0; font-weight: bold; color:#4a3666;">Organisms</p>
        </div>
        <div style="flex: 1; background-color: #dadaeb; text-align: center; padding: 20px 0;">
            <h2 style="color:#4a3666; margin-left: 15px;">39</h2>
            <p style="margin: 0; font-weight: bold; color:#4a3666;">Neuropeptide Families</p>
        </div>
        <div style="flex: 1; background-color: #eeeeee; text-align: center; padding: 20px 0;">
            <h2 style="color:#4a3666; margin-left: 15px;">3,218</h2>
            <p style="margin: 0; font-weight: bold; color:#4a3666;">Page Views</p>
        </div>
    </div>
""", unsafe_allow_html=True)

# ---- Section: Composition Chart ----
st.markdown("""
<h4 style="margin-bottom: 10px;">1. Composition of Neuropeptides per Organism in cNPD</h4>
""", unsafe_allow_html=True)
image_path = os.path.join("Assets", "Statistics", "Composition.png")
if os.path.exists(image_path):
    st.markdown(f"""
        <div style="width: 70%; margin: 0 auto; text-align: center;">
            <img src="data:image/png;base64,{base64.b64encode(open(image_path, "rb").read()).decode()}" style="width: 100%; height: auto;" />
        </div>
    """, unsafe_allow_html=True)
else:
    st.error(f"Image not found at {image_path}")

st.markdown("""
<h4 style="margin-top: 20px; margin-bottom: 10px;">2. Proteolytic Cleavage Patterns from all Peptides in cNPD</h4>
""", unsafe_allow_html=True)
image_path2 = os.path.join("Assets", "Statistics", "Sequence Logo draft.png")
if os.path.exists(image_path):
    st.markdown(f"""
        <div style="width: 70%; margin: 0 auto; text-align: center;">
            <img src="data:image/png;base64,{base64.b64encode(open(image_path, "rb").read()).decode()}" style="width: 100%; height: auto;" />
        </div>
    """, unsafe_allow_html=True)
else:
    st.error(f"Image not found at {image_path}")

st.markdown("""
<h4 style="margin-top: 20px; margin-bottom: 10px;">3. Peptide Properties from all Peptides in cNPD</h4>
""", unsafe_allow_html=True)
image_path = os.path.join("Assets", "Statistics", "Peptide Properties draft.png")
if os.path.exists(image_path):
    st.markdown(f"""
        <div style="width: 70%; margin: 0 auto; text-align: center;">
            <img src="data:image/png;base64,{base64.b64encode(open(image_path, "rb").read()).decode()}" style="width: 100%; height: auto;" />
        </div>
    """, unsafe_allow_html=True)
else:
    st.error(f"Image not found at {image_path}")

st.markdown("""
<h4 style="margin-top: 20px; margin-bottom: 10px;">4. Distribution of Sequence Lengths from all Peptides in cNPD</h4>
""", unsafe_allow_html=True)
image_path = os.path.join("Assets", "Statistics", "Sequence Length Distribution.png")
if os.path.exists(image_path):
    st.markdown(f"""
        <div style="width: 70%; margin: 0 auto; text-align: center;">
            <img src="data:image/png;base64,{base64.b64encode(open(image_path, "rb").read()).decode()}" style="width: 100%; height: auto;" />
        </div>
    """, unsafe_allow_html=True)
else:
    st.error(f"Image not found at {image_path}")

st.markdown("""
<h4 style="margin-top: 20px; margin-bottom: 10px;">5. Amino Acids Composition from all Peptides in cNPD</h4>
""", unsafe_allow_html=True)
image_path = os.path.join("Assets", "Statistics", "Amino Acids Composition.png")
if os.path.exists(image_path):
    st.markdown(f"""
        <div style="width: 70%; margin: 0 auto; text-align: center;">
            <img src="data:image/png;base64,{base64.b64encode(open(image_path, "rb").read()).decode()}" style="width: 100%; height: auto;" />
        </div>
    """, unsafe_allow_html=True)
else:
    st.error(f"Image not found at {image_path}")


st.markdown("""
<div style="text-align: center; font-size:14px; color:#2a2541;">
  <em>Last update: Jul 2025</em>
</div>
""", unsafe_allow_html=True)

