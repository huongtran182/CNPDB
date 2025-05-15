import streamlit as st
from PIL import Image
import os
import base64
from sidebar import render_sidebar

st.set_page_config(
    page_title="Contact Us",
    layout="wide",
    initial_sidebar_state="expanded"
)

render_sidebar()

col1, col2 = st.columns([1, 3], gap="medium")
with col1:
    headshot = os.path.join("Assets", "Img", "PIHeadshot.jpg")
    if os.path.exists(headshot):
        st.image(headshot, use_container_width=True)
    else:
        st.error(f"Profile image not found at:\n{headshot}")

with col2:
    st.markdown("""
    <div style="line-height:1.2;">
      <h2 style="margin:0 0 0.25rem 0;">Lingjun Li, Ph.D.</h2>
      <p style="margin:0 0 1rem 0;"><strong>Professor</strong></p>
      <p style="margin:0 0 1rem 0;">Department of Pharmaceutical Sciences and Chemistry</p>
      <p style="margin:0 0 1rem 0;">University of Wisconsin – Madison</p>
      <p style="margin:0 0 1rem 0;">Madison, WI 53705, USA</p>
      <p style="margin:0 0 1rem 0;"><strong>Phone:</strong> +1 (608) 265-8491</p>
      <p style="margin:0;"><strong>Email:</strong> <a href="mailto:lingjun.li@wisc.edu">lingjun.li@wisc.edu</a></p>
    </div>
    """, unsafe_allow_html=True)


# ─── Opportunities ────────────────────────────────────────────────────────
st.markdown("### OPPORTUNITIES")
st.markdown("""
<div style="text-align: justify; text-justify: inter-word;">
  <p style="margin-bottom: 0.8em;">
    Join our research efforts! We are continuously expanding this database and welcome contributions from students and postdoctoral fellows with fellowships or scholarships.
  </p>
  <p style="margin-bottom: 0.8em;">
    If you’re interested in advancing neuropeptide research, please reach out to Dr. Li at <a href="mailto:lingjun.li@wisc.edu">lingjun.li@wisc.edu</a>.
  </p>
  <p style="margin-bottom: 0.8em;">
    If you want to initiate collaborations, support the development of the CNPD, or have any trouble accessing this database, please email graduate student Huong (Jacey) Tran at <a href="mailto:vtran23@wisc.edu">vtran23@wisc.edu</a>.
  </p>
</div>
""", unsafe_allow_html=True)


# ─── Publications Grid ───────────────────────────────────────────────────

# --- helper to load an image as base64 ---
def img_b64(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()

# --- your paper data ---
papers = [
    {
        "img": "Assets/Publication_TOC/Gaoyuan AmericanLobster TOC.jpeg",
        "title": "Neuropeptidomics of the American Lobster",
        "summary": (
            "Leveraging the recently sequenced high-quality draft genome of the American lobster, "
            "our study sought to profile the neuropeptidome of this model organism. "
            "We identified 24 neuropeptide precursors and 101 unique mature neuropeptides."
        ),
        "link": "https://pubs.acs.org/doi/10.1021/jasms.4c00192"
    },
    {
        "img": "Assets/Publication_TOC/Endogenius TOC.png",
        "title": "EndoGenius: Optimized Neuropeptide Identification from Mass Spectrometry Datasets",
        "summary": (
            "EndoGenius leverages optimized peptide–spectrum matching, an expansive motif database, "
            "and a novel scoring algorithm to broaden neuropeptidome coverage and minimize re-identification."
        ),
        "link": "https://pubs.acs.org/doi/full/10.1021/acs.jproteome.3c00758"
    }
]

st.markdown("### PI’s MAIN PUBLICATIONS ON NEUROPEPTIDES")

# create three equal columns
cols = st.columns(3, gap="medium")

for col, p in zip(cols, papers):
    b64 = img_b64(p["img"])
    with col:
        st.markdown(f"""
        <div style="
            background-color: #9e9ac8;
            border-radius: 10px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            padding: 20px;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            min-height: 510px;
        ">
          <!-- fixed-height image block -->
          <div style="height: 200px; flex-shrink: 0; display:flex; justify-content:center; align-items:center;">
            <img src="data:image/png;base64,{b64}"
                 style="max-height:100%; width:auto; object-fit:contain; border-radius:5px;" />
          </div>

          <!-- title -->
          <div style="
            height: 80px;             /* reserve exactly 80px for the title */
            overflow: hidden;         /* crop any extra if the text is very long */
            margin-bottom: 10px;      /* gap before the summary */
            display: flex;
            align-items: center;      /* vertical centering within that 60px */
            justify-content: center;  /* horizontal centering of the text */
        ">
          <h3 style="
              color: #29004c;
              margin: 0;
              text-align: center;
              font-size: 1.15em;
              line-height: 1.2;
          ">{p["title"]}</h3>
        </div>
          
          <!-- flexible summary block -->
          <div style="
             flex: 1;
              color: #555;
              font-size: 0.9em;
              line-height: 1.4;
              margin: 5px 0 0 0;
              overflow: auto; /* in case text is long */
              text-align: left;
          ">
            {p["summary"]}
          </div>

          <!-- fixed-height button block -->
          <div style="
              height: 45px;
              flex-shrink: 0;
              display: flex;
              justify-content: center;
              align-items: center;
          ">
            <a href="{p["link"]}" target="_blank" style="
                background-color: #29004c;
                color: white;
                text-decoration: none;
                padding: 8px 16px;
                border-radius: 5px;
                font-size: 0.9em;
            ">Read More</a>
          </div>
        </div>
        """, unsafe_allow_html=True)

# ─── Footer ───────────────────────────────────────────────────────────────
st.markdown("""
<div style="text-align: center; font-size: 14px; color: #2a2541;">
  <em>Last update: Jul 2025</em>
</div>
""", unsafe_allow_html=True)
