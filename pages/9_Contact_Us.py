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
    If you’re interested in advancing neuropeptide research or initiating collaborations, please reach out to Prof. Li at <a href="mailto:lingjun.li@wisc.edu">lingjun.li@wisc.edu</a>.
  </p>
  <p style="margin-bottom: 0.8em;">
    If you want to support the development of the CNPD or have any trouble accessing this database, please email graduate student Huong (Jacey) Tran at <a href="mailto:vtran23@wisc.edu">vtran23@wisc.edu</a>.
  </p>
</div>
""", unsafe_allow_html=True)


# ─── Publications Grid ───────────────────────────────────────────────────
st.markdown("""
<style>
/* White background block for TOC images */
.resource-item .toc-container {
    background-color: white;
    padding: 10px;
    display: flex;
    justify-content: center;
    align-items: center;
    height: 190px; /* Fixed height for TOC container */
    margin-bottom: 0px;
}
</style>
""", unsafe_allow_html=True)

# --- helper to load an image as base64 ---
def img_b64(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()

# --- your paper data ---
papers = [
    {
        "img": "Assets/Publication_TOC/DecodingNeuropeptideComplexity.jpeg",
        "title": "Decoding Neuropeptide Complexity: Advancing Neurobiological Insights from Invertebrates to Vertebrates through Evolutionary Perspectives",
        "summary": (
            "The complex vertebrate neural networks poses significant challenges for neuropeptide functional studies. Invertebrate models "
            "offer simplified neural circuits for uncovering fundamental biological principles and their relevance to vertebrate systems."
        ),
        "link": "https://pubs.acs.org/doi/full/10.1021/acschemneuro.5c00053"
    },
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
        "img": "Assets/Publication_TOC/UpdatedGuideNeuropeptideProcess.jpeg",
        "title": "An Updated Guide to the Identification, Quantitation, and Imaging of the Crustacean Neuropeptidome",
        "summary": (
            "A general workflow and detailed multi-faceted approaches for MS-based neuropeptidomic analysis of crustacean tissue samples and circulating fluids."
        ),
        "link": "https://link.springer.com/protocol/10.1007/978-1-0716-3646-6_14"
    },
    {
        "img": "Assets/Publication_TOC/Endogenius TOC.png",
        "title": "EndoGenius: Optimized Neuropeptide Identification from Mass Spectrometry Datasets",
        "summary": (
            "EndoGenius leverages optimized peptide–spectrum matching, an expansive motif database, "
            "and a novel scoring algorithm to broaden neuropeptidome coverage and minimize re-identification."
        ),
        "link": "https://pubs.acs.org/doi/full/10.1021/acs.jproteome.3c00758"
    },
    {
        "img": "Assets/Publication_TOC/AcuteCocaine.jpeg",
        "title": "Cocaine-Induced Remodeling of the Rat Brain Peptidome: Quantitative MS Reveals Anatomically Specific Patterns of Cocaine-Regulated Peptide Changes",
        "summary": (
            "Mass spectrometry (MS) methods were employed to characterize acute cocaine-induced peptidomic changes in the rat brain, "
            "paving the way for developing new therapies to treat substance use disorders and related psychiatric conditions."
        ),
        "link": "https://pubs.acs.org/doi/full/10.1021/acschemneuro.4c00327"
    }
]

st.markdown("### PI’s MAIN PUBLICATIONS ON NEUROPEPTIDES")

# create three equal columns
from math import ceil

# display papers in rows of 3
num_columns = 3
num_rows = ceil(len(papers) / num_columns)

for row_index in range(num_rows):
    cols = st.columns(num_columns, gap="medium")
    for col_index in range(num_columns):
        paper_index = row_index * num_columns + col_index
        if paper_index < len(papers):
            p = papers[paper_index]
            b64 = img_b64(p["img"])
            with cols[col_index]:
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
                  <div class="resource-item">
                    <div class="toc-container">
                      <img src="data:image/png;base64,{b64}"
                           style="max-height:100%; width:auto; object-fit:contain; border-radius:5px;" />
                    </div>
                  </div>

                  <div style="
                    height: 100px;
                    overflow: hidden;
                    margin-bottom: 0px;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                  ">
                    <h3 style="
                        color: #29004c;
                        margin: 0;
                        text-align: center;
                        font-size: 1em;
                        line-height: 1.2;
                    ">{p["title"]}</h3>
                  </div>
                  
                  <div style="
                     flex: 1;
                      color: #555;
                      font-size: 0.9em;
                      line-height: 1.4;
                      margin: 5px 0 0 0;
                      overflow: auto;
                      text-align: left;
                  ">
                    {p["summary"]}
                  </div>

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
                
    st.markdown('<div style="height: 10px;"></div>', unsafe_allow_html=True)

# ─── Footer ───────────────────────────────────────────────────────────────
st.markdown("""
<div style="text-align: center; font-size: 14px; color: #2a2541;">
  <em>Last update: Jul 2025</em>
</div>
""", unsafe_allow_html=True)
