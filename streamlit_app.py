import streamlit as st
from PIL import Image, ImageDraw
import os
import base64
from io import BytesIO
from sidebar import render_sidebar

# Set page config
st.set_page_config(layout="wide", initial_sidebar_state="expanded")

render_sidebar()

# Main content area
st.markdown("""<div style="padding:0;margin:0;">""", unsafe_allow_html=True)

try:
    banner = Image.open("Assets/Img/CNPD_Banner.png")
    st.image(banner, use_container_width=True)
except:
    st.error("Banner image not found")

st.markdown("""
## WELCOME TO cNPD: THE CRUSTACEAN NEUROPEPTIDE DATABASE

Neuropeptides are cell-to-cell signaling molecules involved in numerous physiological processes, including metabolism, development, reproduction, and behavior. They are highly conserved both structurally and functionally across the animal kingdom, making the neuropeptide study in simple invertebrate models advantageous for gaining insights into basic neurobiology principles, drug discoveries, and functional investigations that are translatable to mammalian systems.  Crustaceans are profound model organisms for neuropeptide studies and have long been used to investigate the robustness of rhythmic central pattern generator, feeding behavior, and neural responses to external stimuli.

Despite their significance, crustacean neuropeptides remain underrepresented in existing neuropeptide databases. To address this gap, we introduce the **Crustacean Neuropeptide Database (cNPD)** – A comprehensive resource for neuropeptide research in crustacean species. cNPD systematically curates experimentally confirmed and predicted neuropeptides from various crustacean species using genome-derived in silico mining, peer-reviewed literature, mass spectrometry-based peptidomics, and public protein databases. This database provides detailed annotations and sequences to support a range of endeavors, including comparative neurobiology, functional studies, education, and computational peptide discovery.

""")

st.markdown("""
### TOOLS & FEATURES
The current release of cNPD (Version 1.0, 2025) contains 2000 curated neuropeptide entries from 26 crustacean species, organized into 40 neuropeptide families. Some representative species include *Homarus americanus*  (American Lobster), *Callinectes sapidus*  (Blue Crab), *Cancer borealis*  (Jonah Crab), *Carcinus maenas*  (European green crab), and *Panulirus interruptus*  (California spiny lobster). cNPD offers various tools that facilitate functional investigation, evolutionary analysis, and synthetic peptide design:
- **Custom Search Engine** – Find neuropeptides by sequence, species, families, tissues, post-translational modifications (PTMs), and desired peptide physiological properties, with an option to download the resulted FASTA file.
- **Sequence Alignment & Homology Search** – Identify conserved motifs and sequence similarities.
- **Peptide Property Calculator** – Compute GRAVY scores, hydrophobicity, half-life, 3D structures, and other physiological properties.

Each cNPD search entry provides:
- Neuropeptide sequence (downloadable FASTA format)
- cNPD ID
- Neuropeptide Family
- Species taxonomy 
- Existence (MS/MS, *Denovo* Sequencing, Predicted)
- Physicochemical properties (monoisotopic mass, length, hydrophobicity, predicted Half-life)
- Post-translational modifications (PTMs)
- Predicted 3D Structure 
- Experimental Mass Spectrometry Imaging data of the peptide showing their spatial  distribution in tissues

For detailed instructions on how to navigate cNPD, please refer to the “Tutorials” page from the left sidebar. 
""")

st.markdown("""
### DATABASE SOURCES AND CURATION
cNPD integrates data from peer-reviewed studies and public proteomics repositories:
- Experimental Data – Mass spectrometry and other bioassays
- Literature Mining – Curated from PubMed and primary research papers
- Public Databases – Cross-linked with UniProt, NCBI, and NeuroPep
- Computational Predictions – *In silico* prediction from genomics data

Every neuropeptide entry undergoes manual examination to ensure accuracy and reliability.
""")

st.markdown("""
### GET INVOLVED & CONTRIBUTE

cNPD is a community-driven initiative! We welcome contributions from researchers in the field of peptidomics, neurobiology, and comparative physiology. Here are some ways to contribute:
- Submit new neuropeptide sequences
- Report missing or updated annotations
- Share mass spectrometry datasets
- Suggest additional features or improvements
""")

st.markdown("""
### FUTURE UPDATES
As genomic and experimental data become available for more crustacean species, new entries will be added to our database. Additional bioinformatics tools will be developed for tailored mass spectrometric data analysis to support the discovery and identification of neuropeptides. Experimental data provided by the community will be uploaded promptly upon receipt.

Stay updated on the latest cNPD developments by following us on our social media:
- [X](https://x.com/LiResearch) and [Bluesky](https://bsky.app/profile/liresearch.bsky.social): @LiResearch  
- [Facebook](https://www.facebook.com/profile.php?id=100057624782828) and [LinkedIn](https://www.linkedin.com/company/lingjun-li-lab): Lingjun Li Lab
""")

st.markdown("""
### CITATION AND FUNDING
If you use cNPD in your research, please cite: 

<div style="margin-left: 5cm;">
    cNPD: A Comprehensive Empirical Neuropeptide Database Extended by <i>In Silico</i> Predictions from <i>Callinectes sapidus</i> and <i>Cancer borealis</i> Genomes. Duong, T.U.; Fields, L.; Tran, V.N.H.; Beaver, M.; Tourlouskis, K.; and Li, L. <b>Nucleic Acids Research</b>. 2025.
</div>

**Funding:** This work is supported by [Funding Agencies]

For other tools developed by the Li Lab, please visit **[www.lilabs.org/resources](http://www.lilabs.org/resources)**
""", unsafe_allow_html=True)

st.markdown("""
### COPYRIGHTS
Copyright 2025 Department of Pharmaceutical Sciences, University of Wisconsin-Madison, **All Rights Reserved**

""")

st.markdown("""
<div style="text-align: center; font-size: 14px; color: #2a2541;">
  <em>Last update: Jul 2025</em>
</div>
""", unsafe_allow_html=True)
