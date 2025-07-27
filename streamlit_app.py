import streamlit as st
from PIL import Image, ImageDraw
import os
import base64
from io import BytesIO
from sidebar import render_sidebar
import streamlit.components.v1 as components

components.html("""
<!-- Google Analytics -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-VWK5FWH61R"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'G-VWK5FWH61R');
</script>
""", height=0)
# Set page config
st.set_page_config(layout="wide", initial_sidebar_state="expanded")

render_sidebar()

# Main content area
st.markdown("""<div style="padding:0;margin:0;">""", unsafe_allow_html=True)

try:
    banner = Image.open("Assets/Img/cNPDB_Banner.png")
    st.image(banner, use_container_width=True)
except:
    st.error("Banner image not found")

st.markdown("""
## WELCOME TO cNPDB: THE CRUSTACEAN NEUROPEPTIDE DATABASE

Neuropeptides are cell-to-cell signaling molecules involved in numerous physiological processes, including metabolism, development, reproduction, and behavior. They are highly conserved both structurally and functionally across the animal kingdom, making the neuropeptide study in simple invertebrate models advantageous for gaining insights into basic neurobiology principles, drug discoveries, and functional investigations that are translatable to mammalian systems.  Crustaceans are profound model organisms for neuropeptide studies and have long been used to investigate the robustness of rhythmic central pattern generator, feeding behavior, and neural responses to external stimuli.

Despite their significance, crustacean neuropeptides remain underrepresented in existing neuropeptide databases. To address this gap, we introduce the **Crustacean Neuropeptide Database (cNPDB)** – A comprehensive resource for neuropeptide research in crustacean species. cNPDB systematically curates experimentally confirmed and predicted neuropeptides from various crustacean species using genome-derived in silico mining, peer-reviewed literature, mass spectrometry-based peptidomics, and public protein databases. This database provides detailed annotations and sequences to support a range of endeavors, including comparative neurobiology, functional studies, education, and computational peptide discovery.

""")

# Load Home page image and convert to base64
image_path = os.path.join("Assets", "Img", "Home page.png")
if os.path.exists(image_path):
    with open(image_path, "rb") as img_file:
        img_bytes = img_file.read()
        img_b64 = base64.b64encode(img_bytes).decode()

    st.markdown(f"""
        <div style="margin: 0 auto; text-align: center;">
            <img src="data:image/png;base64,{img_b64}" style="width: auto; max-height: 500px;" />
        </div>
    """, unsafe_allow_html=True)
else:
    st.error(f"Image not found at {image_path}")
    
st.markdown("""
### TOOLS & FEATURES
The current release of cNPDB (Version 1.0, 2025) contains **1379** curated neuropeptide entries from **30** crustacean species, organized into **55** neuropeptide families. Some representative species include *Homarus americanus*  (American Lobster), *Callinectes sapidus*  (Blue Crab), *Cancer borealis*  (Jonah Crab), *Carcinus maenas*  (European green crab), and *Panulirus interruptus*  (California spiny lobster). cNPDB offers various tools that facilitate functional investigation, evolutionary analysis, and synthetic peptide design:
- **Custom Search Engine** – Find neuropeptides by sequence, species, families, tissues, post-translational modifications (PTMs), and desired peptide physiological properties, with an option to download the resulted FASTA file.
- **Sequence Alignment & Homology Search** – Identify conserved motifs and sequence similarities.
- **Peptide Property Calculator** – Compute GRAVY scores, hydrophobicity, instability index, and other physiological properties.

Each cNPDB search entry provides:
- Neuropeptide sequence (downloadable FASTA format)
- cNPDB ID
- Neuropeptide Family
- Species taxonomy 
- Existence (MS/MS, *De novo* Sequencing, Predicted)
- Physicochemical properties (monoisotopic mass, length, hydrophobicity, instability index, isoelectric point, net charge, *etc.*)
- Post-translational modifications (PTMs)
- Predicted 3D Structure 
- Experimental Mass Spectrometry Imaging data of the peptide showing their spatial  distribution in tissues

For detailed instructions on how to navigate cNPDB, please refer to the “Tutorials” page from the left sidebar. 
""")

st.markdown("""
### DATABASE SOURCES AND CURATION
cNPDB integrates data from peer-reviewed studies and public proteomics repositories:
- Experimental Data: Mass spectrometry and other bioassays
- Literature Mining: Curated from PubMed and primary research papers
- Public Databases: Cross-linked with UniProt, NCBI, and NeuroPep
- Computational Predictions: *In silico* prediction from genomics data

Every neuropeptide entry undergoes manual examination to ensure accuracy and reliability.
""")

st.markdown("""
### GET INVOLVED & CONTRIBUTE

cNPDB is a community-driven initiative! We welcome contributions from researchers in the field of peptidomics, neurobiology, and comparative physiology.
If you would like to contribute, please visit the *Contact Us* page and fill out the Feedback Form. Here are  a few ways you can get involved:
- Submit newly discovered neuropeptide sequences
- Report missing data or suggest data corrections
- Provide references or annotations
- Share mass spectrometry datasets
- Suggest additional features or improvements
""")

st.markdown("""
### FUTURE UPDATES
As genomic and experimental data become available for more crustacean species, new entries will be added to our database. Additional bioinformatics tools will be developed for tailored mass spectrometric data analysis to support the discovery and identification of neuropeptides. Experimental data provided by the community will be uploaded promptly upon receipt.

Stay updated on the latest cNPDB developments by following us on our social media:
- [X](https://x.com/LiResearch) and [Bluesky](https://bsky.app/profile/liresearch.bsky.social): @LiResearch  
- [Facebook](https://www.facebook.com/profile.php?id=100057624782828) and [LinkedIn](https://www.linkedin.com/company/lingjun-li-lab): Lingjun Li Lab
""")

#st.markdown("""
#CITATION AND FUNDING
#If you use cNPDB in your research, please cite: 

#<div style="margin-left: 1cm;">
#    cNPDB: A centralized platform for crustacean neuropeptides featuring empirical data and predicted 3D structural insights. Tran, V.N.H.; Duong, T.U.; Fields, L.; Tourlouskis, K.; Beaver, M.; and Li, L. <b>Nucleic Acids Research</b>. 2025.
#</div>

#<br>

#**Funding:** This work is supported by in part by National Institutes of Health (NIH) through grants R01DK071801 and the Research Forward grant by University of Wisconsin - Madison Office of the Vice Chancellor for Research with funding from the Wisconsin Alumni Research Foundation. LF was supported in part by the National Institute of General Medical Sciences of the National Institutes of Health under Award Number T32GM008505 (Chemistry–Biology Interface Training Program), the 2024 Eli Lilly and Company/ACS Analytical Graduate Fellowship, and a predoctoral fellowship supported by the NIH, under Ruth L. Kirschstein National Research Service Award (NRSA) from the National Institutes of Health-General Medical Sciences F31GM156104. LL would like to acknowledge NIH grants R01AG052324, S10OD028473, and S10OD025084, as well as funding support from a Vilas Distinguished Achievement Professorship and Charles Melbourne Johnson Professorship with funding provided by the Wisconsin Alumni Research Foundation and University of Wisconsin-Madison School of Pharmacy. 

#For other tools developed by the Li Lab, please visit **[www.lilabs.org/resources](http://www.lilabs.org/resources)**
#""", unsafe_allow_html=True)

st.markdown("""
### COPYRIGHTS
Copyright 2025 Department of Pharmaceutical Sciences, University of Wisconsin-Madison, **All Rights Reserved**

**Disclaimer:** While we strive to provide accurate and up-to-date information, this database may contain errors, omissions, or outdated data. Users are encouraged to independently verify any information and consult original sources when making decisions or drawing conclusions based on the content provided here.

""")

st.markdown("""
<div style="text-align: center; font-size: 14px; color: #2a2541;">
  <em>Last update: Jul 2025</em>
</div>
""", unsafe_allow_html=True)
