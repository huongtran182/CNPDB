import streamlit as st
from sidebar import render_sidebar
import base64
import os

st.set_page_config(
    page_title="Related Databases",
    layout="wide",
    initial_sidebar_state="expanded"
)

render_sidebar()

# --- Section 1: Table of External Databases ---
st.markdown("## ACCESSIBLE NEUROPEPTIDE DATABASES")

# --- helper to load an image as base64 ---
def img_b64(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()

# --- your paper data ---
papers = [
     {
        "img": os.path.join("Assets", "Publication_TOC", "Endogenius TOC.png"),
        "title": "Endogenius",
        "summary": (
            "EndoGenius, a database searching strategy designed specifically for elucidating "
            "neuropeptide identifications from mass spectra by leveraging optimized peptide–spectrum "
            "matching approaches, an expansive motif database, and a novel scoring algorithm to "
            "achieve broader representation of the neuropeptidome and minimize reidentification."
        ),
        "read_link": "https://pubs.acs.org/doi/full/10.1021/acs.jproteome.3c00758",
        "explore_link": "https://yourdatabase.com/tools/endoGenius"
    },
    {
        "img": os.path.join("Assets", "Publication_TOC", "MotifQuest TOC.png"),
        "title": "MotifQuest",
        "summary": (
            "MotifQuest, our novel motif database generation algorithm, is designed to work in partnership "
            "with EndoGenius – a program optimized for database searching of endogenous peptides – and is "
            "powered by a motif database to capitalize on biological context for confident identifications."
        ),
        "read_link": "https://yourdatabase.com/publications/motifquest",
        "explore_link": "https://yourdatabase.com/tools/motifquest"
    },
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

st.markdown("""
<div style="text-align: center; font-size:14px; color:#2a2541;">
  <em>Last update: Jul 2025</em>
</div>
""", unsafe_allow_html=True)

