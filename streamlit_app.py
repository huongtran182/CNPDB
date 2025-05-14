import streamlit as st
from PIL import Image
import os

# Set page config
st.set_page_config(
    page_title="CNPD - Crustacean Neuropeptide Database",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Get current page to highlight active link
current_page = os.path.basename(__file__)

# Hide the auto-generated Streamlit sidebar nav
st.markdown("""
<style>
    /* Hide the default sidebar nav */
    [data-testid="stSidebarNav"] {
        display: none;
    }
    
    /* Your existing custom sidebar styles */
    [data-testid="stSidebar"] {
        background-color: #2a2541 !important;
        padding: 0 !important;
    }
    
    .nav-item {
        color: #ffffff !important;
        font-family: 'Arial', sans-serif;
        font-size: 14px;
        font-weight: 500;
        letter-spacing: 0.5px;
        text-transform: uppercase;
        text-align: center;
        padding: 12px 0 !important;
        margin: 0 !important;
        width: 100%;
        display: block;
        text-decoration: none !important;
    }
    
    
    .nav-item:hover {
        background-color: #3a2d5a !important;
    }
    
    .nav-item.active {
        background-color: #4a3666 !important;
        font-weight: 600;
    }
    
    /* Logo container */
    .logo-container {
        display: flex;
        justify-content: center;
        padding: 2rem 1rem 1.5rem 1rem;
    }
    
    .logo-img {
        border-radius: 50%;
        width: 120px;
        height: 120px;
        object-fit: cover;
        border: 3px solid #ffffff;
    }
    
    /* Navigation container */
    .nav-container {
        padding: 0.5rem 0 2rem 0;
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: 0;
    }
    
    /* Remove Streamlit's default sidebar spacing */
    .st-emotion-cache-6qob1r {
        padding-top: 0 !important;
    }
</style>
""", unsafe_allow_html=True)

# Your custom sidebar implementation
with st.sidebar:
    # Circular logo
    st.markdown('<div class="logo-container">', unsafe_allow_html=True)
    logo = Image.open("Assets/Img/Website_Logo_2.png")
    st.image(logo, width=120, use_column_width=False)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Custom navigation
    st.markdown('<div class="nav-container">', unsafe_allow_html=True)
    pages = [
        {"file": "streamlit_app.py", "label": "Home"},
        {"file": "pages/1_About.py", "label": "About"},
        {"file": "pages/2_NP_Database_Search.py", "label": "NP Database Search"},
        {"file": "pages/3_Tools.py", "label": "Tools"},
        {"file": "pages/4_Related_Databases.py", "label": "Related Databases"},
        {"file": "pages/5_Tutorials.py", "label": "Tutorials"},
        {"file": "pages/6_Statistics.py", "label": "Statistics"},
        {"file": "pages/7_Glossary.py", "label": "Glossary"},
        {"file": "pages/8_FAQ.py", "label": "FAQ"},
        {"file": "pages/9_Contact_Us.py", "label": "Contact Us"}
    ]
    
   current_page = os.path.basename(__file__)
    for page in pages:
        is_active = current_page == os.path.basename(page["file"])
        active_class = "active" if is_active else ""
        st.markdown(
            f'<a href="{page["file"]}" class="nav-item {active_class}" target="_self">{page["label"].upper()}</a>',
            unsafe_allow_html=True
        )
    
    st.markdown('</div>', unsafe_allow_html=True)

# Main content - Banner image spanning full width
col1, col2 = st.columns([1, 20])  # Adjust ratio to control sidebar offset
with col2:
    banner = Image.open("Assets/Img/CNPD_Banner.png")
    st.image(banner, use_container_width=True)
st.markdown("""
## WELCOME TO CNPD: THE CRUSTACEAN NEUROPEPTIDE DATABASE

Neuropeptides are critical signaling molecules involved in numerous physiological processes, including metabolism, reproduction, development, and behavior. In crustaceans, neuropeptides regulate key biological functions such as molting, feeding, and immune responses. Despite their significance, crustacean neuropeptides remain underrepresented in existing neuropeptide databases.

To address this gap, we introduce **The Crustacean Neuropeptide Database (CNPD)** – A comprehensive resource for neuropeptide research in crustacean species. CNPD systematically curates experimentally confirmed and predicted neuropeptides from various crustacean species using peer-reviewed literature, mass spectrometry-based peptidomics, and public protein databases.

This database provides detailed annotations to support **Comparative neurobiology**, **Functional studies**, and **Computational peptide discovery**.
""")

st.markdown("""
### GET INVOLVED & CONTRIBUTE

CNPD is a community-driven initiative! We welcome contributions from researchers in peptidomics, neurobiology, and comparative physiology.

To collaborate, submit data, or provide feedback, please contact Dr. Lingjun Li at **lingjun.li@wise.edu**
""")

st.markdown("""
### HOW TO CITE
If you use CNPD in your research, please cite:
Crustacean Neuropeptide Database (CNPD): A curated resource for neuropeptide research in crustacean species. [Authors]. [Journal Name], [Year]. DOI: [XXXX].
""")

st.markdown("""
### FUNDING
This work is supported by [Funding Agencies]

For other tools developed by the Li Lab, visit **www.lilabs.org/resources**
""")

st.markdown("""
<i>Last update: Jul 2025</i>
""", unsafe_allow_html=True)
