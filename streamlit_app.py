import streamlit as st
from PIL import Image
import os

# Set page config
st.set_page_config(
    page_title="CNPD - Crustacean Neuropeptide Database",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Get current page name to highlight active link
current_page = os.path.basename(__file__)

# Custom CSS for the sidebar
st.markdown("""
<style>
    /* Main sidebar styling */
    [data-testid="stSidebar"] {
        background-color: #2a2541 !important;
        padding: 0rem !important;
    }
    
    /* Sidebar navigation links */
    .sidebar-link {
        color: white !important;
        font-family: 'Muli', sans-serif;
        font-size: 16px;
        padding: 0.5rem 1rem;
        margin: 0.1rem 0;
        border-radius: 0.25rem;
        display: block;
        text-decoration: none;
    }
    
    .sidebar-link:hover {
        background-color: #3f2d5a !important;
        color: white !important;
    }
    
    .sidebar-link.active {
        background-color: #4a3666 !important;
        font-weight: bold;
    }
    
    /* Logo styling */
    .logo-container {
        display: flex;
        justify-content: center;
        padding: 1.5rem 1rem 1rem 1rem;
    }
    
    .logo-img {
        border-radius: 50%;
        object-fit: cover;
        width: 120px;
        height: 120px;
        border: 3px solid white;
    }
    
    /* Title styling */
    .sidebar-title {
        color: white;
        text-align: center;
        font-family: 'Saira Extra Condensed', sans-serif;
        margin-bottom: 1.5rem;
        font-weight: 700;
        font-size: 1.8rem;
        text-transform: uppercase;
        padding: 0 1rem;
    }
    
    /* Navigation container */
    .nav-container {
        padding: 0 1rem 1.5rem 1rem;
    }
</style>
""", unsafe_allow_html=True)

# Sidebar with logo and navigation
with st.sidebar:
    # Logo in a circle
    st.markdown('<div class="logo-container">', unsafe_allow_html=True)
    try:
        logo = Image.open("Assets/Img/Website_Logo_2.png")
        st.image(logo, width=120, use_column_width=False)
    except:
        st.error("Logo image not found at: Assets/Img/Website_Logo_2.png")
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Title
    st.markdown('<div class="sidebar-title">CNPD</div>', unsafe_allow_html=True)
    
    # Navigation links
    st.markdown('<div class="nav-container">', unsafe_allow_html=True)
    
    # Create links with active state
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
    
    for page in pages:
        is_active = current_page == os.path.basename(page["file"])
        active_class = "active" if is_active else ""
        st.markdown(
            f'<a href="{page["file"]}" class="sidebar-link {active_class}">{page["label"]}</a>',
            unsafe_allow_html=True
        )
    
    st.markdown('</div>', unsafe_allow_html=True)

# Main content - Banner image
try:
    banner = Image.open("Assets/Img/CNPD_Banner.png")
    st.image(banner, use_column_width=True)
except:
    st.error("Banner image not found at: Assets/Img/CNPD_Banner.png")

# Rest of your content
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
