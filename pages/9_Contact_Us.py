import streamlit as st
from PIL import Image
import os
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
        st.image(headshot, use_column_width=True)
    else:
        st.error(f"Profile image not found at:\n{headshot}")

with col2:
    st.markdown("## Lingjun Li, Ph.D.")
    st.markdown("**Professor**")
    st.markdown("Department of Pharmaceutical Sciences and Chemistry")  
    st.markdown("University of Wisconsin – Madison")  
    st.markdown("Madison, WI 53705, USA")  
    st.markdown("**Phone:** +1 (608) 265-8491")  
    st.markdown("**Email:** [lingjun.li@wisc.edu](mailto:lingjun.li@wisc.edu)")  


# ─── Opportunities ────────────────────────────────────────────────────────
st.markdown("### Opportunities")
st.markdown("""
Join our research efforts! We are continuously expanding this database and welcome contributions from students and postdoctoral fellows with fellowships or scholarships.  
If you're interested in advancing neuropeptide research, please reach out to Dr. Li at [lingjun.li@wisc.edu](mailto:lingjun.li@wisc.edu).

If you want to initiate collaborations, support the development of the CNPD, or have any trouble accessing this database, please email Dr. Li at [lingjun.li@wisc.edu](mailto:lingjun.li@wisc.edu).
""")


# ─── Publications Grid ────────────────────────────────────────────────────
st.markdown("### PI’s Main Publications on Neuropeptides")

papers = [
    {
        "img": os.path.join("Assets", "Publication - Resource TOC", "Gaoyuan AmericanLobster TOC.jpeg"),
        "title": "Neuropeptidomics of the American Lobster",
        "summary": (
            "Leveraging the recently sequenced high-quality draft genome of the American lobster, our study "
            "sought to profile the neuropeptidome of this model organism. Employing advanced mass spectrometry "
            "techniques, we identified 24 neuropeptide precursors and 101 unique mature neuropeptides."
        ),
        "link": "https://pubs.acs.org/doi/10.1021/jasms.4c00192"
    },
    {
        "img": os.path.join("Assets", "Publication - Resource TOC", "Endogenius TOC.png"),
        "title": "EndoGenius: Optimized Neuropeptide Identification from Mass Spectrometry Datasets",
        "summary": (
            "EndoGenius is a database-searching strategy designed specifically for elucidating neuropeptide "
            "identifications from mass spectra. It leverages optimized peptide–spectrum matching, an expansive motif "
            "database, and a novel scoring algorithm to broaden neuropeptidome coverage and minimize re-identification."
        ),
        "link": "https://pubs.acs.org/doi/full/10.1021/acs.jproteome.3c00758"
    }
]

cols = st.columns(3, gap="medium")
for idx, paper in enumerate(papers):
    with cols[idx]:
        if os.path.exists(paper["img"]):
            st.image(paper["img"], use_column_width=True)
        else:
            st.warning(f"Couldn’t find image:\n{paper['img']}")
        st.markdown(f"**{paper['title']}**")
        st.write(paper["summary"])
        st.markdown(f"[Read More]({paper['link']})")


# ─── Footer ───────────────────────────────────────────────────────────────
st.markdown("""
<div style="text-align: center; font-size: 14px; color: #2a2541;">
  <em>Last update: Jul 2025</em>
</div>
""", unsafe_allow_html=True)
