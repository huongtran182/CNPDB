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



# --- Section 2: resources for neuropeptide research ---
st.markdown("## RESOURCES FOR NEUROPEPTIDE RESEARCH")

# --- inject custom CSS for TOC images ---
st.markdown("""
<style>
/* White background block for TOC images */
.resource-item .toc-container {
    background-color: white;
    padding: 10px;
    display: flex;
    justify-content: center;
    align-items: center;
    height: 230px; /* Fixed height for TOC container */
    margin-bottom: 15px;
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
        "img": os.path.join("Assets", "Publication_TOC", "MotifQuest TOC.jpeg"),
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
          <div class="resource-item">
            <div class="toc-container">
              <img src="data:image/png;base64,{b64}"
                   style="max-height:100%; width:auto; object-fit:contain; border-radius:5px;" />
            </div>
          </div>

          <!-- title -->
          <div style="
              height: 50px;
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
              overflow: auto;
              text-align: left;
          ">
            {p["summary"]}
          </div>

          <!-- buttons -->
          <div style="display:flex; gap:10px; justify-content:center;">
            <a href="{p["read_link"]}" target="_blank" style="
                background-color:#29004c;
                color:white;
                padding:8px 16px;
                border-radius:5px;
                text-decoration:none;
                font-size:0.9em;
            ">Read More</a>
            <a href="{p["explore_link"]}" target="_blank" style="
                background-color:#29004c;
                color:white;
                padding:8px 16px;
                border-radius:5px;
                text-decoration:none;
                font-size:0.9em;
            ">Explore</a>
          </div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("""
<div style="text-align: center; font-size:14px; color:#2a2541;">
  <em>Last update: Jul 2025</em>
</div>
""", unsafe_allow_html=True)

