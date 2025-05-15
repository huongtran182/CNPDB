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

# CSS for table styling
st.markdown("""
<style>
.related-table {
  background-color: #9e9ac8;
  border-radius: 10px;
  padding: 20px;
}
.related-table table {
  width: 100%;
  border-collapse: collapse;
}
.related-table th, .related-table td {
  padding: 12px;
}
.related-table th {
  text-align: left;
  font-weight: bold;
  border-bottom: 2px solid #29004c;
}
.related-table tr + tr td {
  border-top: 1px solid #29004c;
}
.related-table a {
  color: #29004c;
  text-decoration: none;
  font-weight: bold;
}
.related-table a:hover {
  text-decoration: underline;
}
</style>
""", unsafe_allow_html=True)

# Table HTML
st.markdown("""
<div class="related-table">
  <table>
    <thead>
      <tr>
        <th>Website</th>
        <th>Year Published</th>
        <th>Database Description</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td><a href="http://neuropeptides.nl" target="_blank">neuropeptides.nl</a></td>
        <td>20xx</td>
        <td>The Neuropeptide Database is the internet resource to data about all known neuropeptides, their genes, precursors and expression in the brain.</td>
      </tr>
      <tr>
        <td><a href="https://neuropep.org" target="_blank">NeuroPep</a></td>
        <td>2015</td>
        <td>NeuroPep holds 5949 non-redundant neuropeptide entries originating from 493 organisms belonging to 65 neuropeptide families.</td>
      </tr>
      <tr>
        <td><a href="http://neuropepdia.org" target="_blank">Neuropepdia</a></td>
        <td>20xx</td>
        <td>abcxyz</td>
      </tr>
    </tbody>
  </table>
</div>
""", unsafe_allow_html=True)

# --- Section 2: Card Grid for Internal Tools/Resources ---
st.markdown("## RESOURCES FOR NEUROPEPTIDE RESEARCH")

# CSS for the card grid
st.markdown("""
<style>
.resource-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 40px;
  margin-top: 20px;
}
.card {
  background-color: #9e9ac8;
  border-radius: 10px;
  padding: 20px;
  display: flex;
  flex-direction: column;
  min-height: 500px;
}
.card img {
  width: 100%;
  height: auto;
  object-fit: contain;
  border-radius: 5px;
  margin-bottom: 15px;
}
.card h3 {
  color: #29004c;
  margin: 0 0 10px 0;
  text-align: center;
  font-size: 1.25em;
}
.card p {
  flex: 1;
  color: #555;
  font-size: 0.9em;
  margin-bottom: 15px;
  line-height: 1.4;
  text-align: left;
  overflow: auto;
}
.card .buttons {
  display: flex;
  gap: 10px;
  justify-content: center;
}
.card .buttons a {
  background-color: #29004c;
  color: white;
  padding: 8px 16px;
  border-radius: 5px;
  text-decoration: none;
  font-size: 0.9em;
}
.card .buttons a:hover {
  background-color: #7c78a8;
}
</style>
""", unsafe_allow_html=True)

# Data for your two internal resources
resources = [
    {
        "img": os.path.join("Assets", "Publication - Resource TOC", "Endogenius TOC.png"),
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
        "img": os.path.join("Assets", "Publication - Resource TOC", "MotifQuest TOC.png"),
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

# Helper to encode an image as base64
def img_to_b64(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()

# Build and render the grid
cards_html = []
for r in resources:
    b64 = img_to_b64(r["img"])
    cards_html.append(f"""
    <div class="card">
      <img src="data:image/png;base64,{b64}" />
      <h3>{r['title']}</h3>
      <p>{r['summary']}</p>
      <div class="buttons">
        <a href="{r['read_link']}" target="_blank">Read More</a>
        <a href="{r['explore_link']}" target="_blank">Explore</a>
      </div>
    </div>
    """)

grid_html = f'<div class="resource-grid">{"".join(cards_html)}</div>'
st.markdown(grid_html, unsafe_allow_html=True)



st.markdown("""
<div style="text-align: center; font-size:14px; color:#2a2541;">
  <em>Last update: Jul 2025</em>
</div>
""", unsafe_allow_html=True)

