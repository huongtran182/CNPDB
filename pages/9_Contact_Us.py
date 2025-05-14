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
Join our research efforts! We are continuously expanding this database and welcome contributions from students and postdoctoral fellows with fellowships or scholarships.  
If you're interested in advancing neuropeptide research or initiating collaborations, please reach out to Prof. Li at [lingjun.li@wisc.edu](mailto:lingjun.li@wisc.edu).

If you want to support the development of the CNPD, or have any trouble accessing this database, please email our graduate student Huong (Jacey) Tran at [vtran23@wisc.edu](mailto:vtran23@wisc.edu).
""")


# ─── Publications Grid ────────────────────────────────────────────────────
st.markdown("### PI’s MAIN PUBLICATIONS ON NEUROPEPTIDES")

# 1) CSS for the grid + cards
st.markdown("""
<style>
.paper-grid {
  display: grid;
  grid-template-columns: repeat(2,1fr);
  gap: 20px;
  margin-top: 1rem;
}
.paper-card {
  background-color: #9e9ac8;
  border-radius: 10px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
  padding: 20px;
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
}
.paper-card img {
  max-width: 100%; height: auto;
  object-fit: contain;
  margin-bottom: 15px;
  border-radius: 5px;
}
.paper-card h3 {
  margin: 0 0 10px;
  color: #29004c;
  font-size: 1.2em;
  line-height: 1.2;
}
.paper-card p {
  flex: 1;
  color: #555;
  font-size: 0.9em;
  margin-bottom: 15px;
  overflow: hidden;
}
.paper-card a.btn {
  background-color: #29004c;
  color: #fff;
  text-decoration: none;
  padding: 8px 16px;
  border-radius: 5px;
  transition: background-color 0.2s ease;
}
.paper-card a.btn:hover {
  background-color: #7c78a8;
}
</style>
""", unsafe_allow_html=True)


# 2) Prepare your paper data
papers = [
    {
      "img": "Assets/Publication_TOC/Gaoyuan AmericanLobster TOC.jpeg",
      "title": "Neuropeptidomics of the American Lobster",
      "summary": "Leveraging the recently sequenced high-quality draft genome of the American lobster, we identified 24 neuropeptide precursors and 101 unique mature neuropeptides.",
      "link": "https://pubs.acs.org/doi/10.1021/jasms.4c00192"
    },
    {
      "img": "Assets/Publication_TOC/Endogenius TOC.png",
      "title": "EndoGenius: Optimized Neuropeptide Identification from Mass Spectrometry Datasets",
      "summary": "EndoGenius leverages optimized peptide–spectrum matching, an expansive motif database, and a novel algorithm to broaden neuropeptidome coverage.",
      "link": "https://pubs.acs.org/doi/full/10.1021/acs.jproteome.3c00758"
    }
]

# 3) Build the cards as one big HTML string
cards_html = []
for p in papers:
    # Read & base64-encode the TOC image
    with open(p["img"], "rb") as f:
        b64 = base64.b64encode(f.read()).decode()
    cards_html.append(f"""
    <div class="paper-card">
      <img src="data:image/png;base64,{b64}" />
      <h3>{p['title']}</h3>
      <p>{p['summary']}</p>
      <a class="btn" href="{p['link']}" target="_blank">Read More</a>
    </div>
    """)

grid_html = f'<div class="paper-grid">{"".join(cards_html)}</div>'

# 4) Finally render the grid, again with unsafe_allow_html:
st.markdown(grid_html, unsafe_allow_html=True)

# ─── Footer ───────────────────────────────────────────────────────────────
st.markdown("""
<div style="text-align: center; font-size: 14px; color: #2a2541;">
  <em>Last update: Jul 2025</em>
</div>
""", unsafe_allow_html=True)
