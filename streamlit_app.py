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

# Custom CSS for the sidebar
st.markdown("""
<style>
    /* Hide the default sidebar nav */
    [data-testid="stSidebarNav"] {
        display: none;
    }
    
    /* Main sidebar styling */
    [data-testid="stSidebar"] {
        background-color: #2a2541 !important;
        padding: 0 !important;
    }
    
    /* Navigation links */
    .nav-item {
        color: #ffffff !important;
        font-family: 'Arial', sans-serif;
        font-size: 14px;
        font-weight: 500;
        letter-spacing: 0.5px;
        text-transform: uppercase;
        text-align: left;
        padding: 12px 20px !important;
        margin: 0 !important;
        width: 100%;
        display: block;
        text-decoration: none !important;
        transition: all 0.3s ease;
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
        padding: 2rem 1rem;
        border-bottom: 1px solid #4a3666;
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
        padding: 1rem 0;
        display: flex;
        flex-direction: column;
        gap: 0;
    }
    
    /* Remove Streamlit's default sidebar spacing */
    .st-emotion-cache-6qob1r {
        padding-top: 0 !important;
    }
</style>
""", unsafe_allow_html=True)

# Sidebar with logo and navigation
with st.sidebar:
    # Circular logo at top-center
    st.markdown('<div class="logo-container">', unsafe_allow_html=True)
    try:
        logo = Image.open("Assets/Img/Website_Logo_2.png")
        st.image(logo, width=120, use_container_width=False)
    except:
        st.error("Logo image not found")
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Navigation menu (left-aligned)
    st.markdown('<div class="nav-container">', unsafe_allow_html=True)
    
    pages = [
        {"file": "streamlit_app.py", "label": "Home"},
        {"file": "pages/1_About.py", "label": "About"},
        {"file": "pages/2_NP_Database_Search.py", "label": "Neuropeptide Database Search"},
        {"file": "pages/3_Tools.py", "label": "Tools"},
        {"file": "pages/4_Related_Databases.py", "label": "Related Databases and Resources"},
        {"file": "pages/5_Tutorials.py", "label": "Tutorials"},
        {"file": "pages/6_Statistics.py", "label": "Statistics"},
        {"file": "pages/7_Glossary.py", "label": "Glossary"},
        {"file": "pages/8_FAQ.py", "label": "Frequently Asked Questions"},
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

# Main content
col1, col2 = st.columns([1, 20])
with col2:
    try:
        banner = Image.open("Assets/Img/CNPD_Banner.png")
        st.image(banner, use_container_width=True)
    except:
        st.error("Banner image not found")

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
