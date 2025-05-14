# pages/1_About.py
import streamlit as st
from sidebar import render_sidebar

st.set_page_config(
    page_title="About CNPD",
    layout="wide",
    initial_sidebar_state="expanded"
)

render_sidebar()

# Page title
st.markdown("# About CNPD – Crustacean Neuropeptide Database")

# Overview section
st.markdown("""
## Overview

The current release of **CNPD (Version 1.0, 2025)** contains **[X]** curated neuropeptide entries from **[Y]** crustacean species, organized into **[Z]** neuropeptide families.

Data is manually curated from peer-reviewed literature, mass spectrometry-based peptidomics, and public protein databases such as **UniProt** and **NCBI**.
""")

# What CNPD Provides
st.markdown("""
## What CNPD Provides

- Neuropeptide sequence (FASTA format)  
- Species taxonomy & homology  
- Physicochemical properties (mass, charge, hydrophobicity, etc.)  
- Post-translational modifications (PTMs)  
- Experimental validation methods (LC-MS/MS, transcriptomic mining, etc.)  
- MS Imaging of the peptide showing their distribution in tissues  
- Predicted 3D structure  
- Predicted half-life  
- Predicted/validated biological functions  

CNPD also provides cross-links to **UniProt**, **NCBI**, and **PubMed**, along with search and analysis tools for neuropeptide research.
""")

# Database Features & Tools
st.markdown("""
## Database Features & Tools

- **Flexible Search Engine** – Find neuropeptides by name, sequence, family, or function.  
- **Comparative Peptide Analysis** – Compare neuropeptide sequences across crustacean species.  
- **Sequence Alignment & Homology Search** – Identify conserved motifs and sequence similarities.  
- **Mass Spectrometry Data Integration** – Explore MS-validated peptides and spectral evidence.  
- **Peptide Property Calculator** – Compute GRAVY scores, hydrophobicity, half-life, 3D structures, and more.  
""")

# Crustacean Species Covered
st.markdown("""
## Crustacean Species Covered

- *Homarus americanus* (American Lobster)  
- *Callinectes sapidus* (Blue Crab)  
- *Cancer borealis* (Jonah Crab)  
- *Litopenaeus vannamei* (Pacific White Shrimp)  
- *Pandalus borealis* (Northern Shrimp)  
""")

# Data Sources & Curation
st.markdown("""
## Data Sources & Curation

- **Experimental Data** – Mass spectrometry & neuropeptide bioassays  
- **Literature Mining** – Curated from PubMed & primary research papers  
- **Public Databases** – Cross-linked with UniProt, NCBI, and NeuroPep  
- **Computational Predictions** – Sequence-based neuropeptide identification  

Every neuropeptide entry undergoes **manual examination** to ensure accuracy and reliability.
""")

# Get Involved & Contribute
st.markdown("""
## Get Involved & Contribute

- Submit new neuropeptide sequences  
- Report missing or updated annotations  
- Share mass spectrometry datasets  
- Suggest additional features or improvements  

For collaborations, submissions, or feedback, please contact **Dr. Lingjun Li** at <lingjun.li@wisc.edu>.
""")

# Citation & Funding
st.markdown("""
## Citation & Funding

If you use CNPD in your research, please cite:

> **Crustacean Neuropeptide Database (CNPD):**  
> A curated resource for neuropeptide research in crustacean species. [Authors]. [Journal Name], [Year]. DOI: [XXXX].

**Funding:** This work is supported by [Funding Agencies].
""")

# Future Updates
st.markdown("""
## Future Updates

- Expansion to more crustacean species  
- Enhanced peptide discovery tools  
- Improved mass spectrometry integration  
- User-submitted experimental data uploads  
""")

# Centered “last update”
st.markdown("""
<div style="text-align: center; font-size:14px; color:#2a2541;">
  <em>Last update: Jul 2025</em>
</div>
""", unsafe_allow_html=True)
