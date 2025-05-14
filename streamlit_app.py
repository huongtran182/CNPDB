import streamlit as st
from PIL import Image
import base64

# Set page config
st.set_page_config(
    page_title="CNPD - Crustacean Neuropeptide Database",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for the sidebar
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Apply custom CSS
st.markdown("""
<style>
    /* Main sidebar styling */
    [data-testid="stSidebar"] {
        background-color: #6a0dad !important;
        padding-top: 0rem;
    }
    
    /* Sidebar navigation links */
    .stPageLink {
        color: white !important;
        font-family: 'Arial', sans-serif;
        font-size: 16px;
        padding: 0.5rem 1rem;
        margin: 0.2rem 0;
    }
    
    .stPageLink:hover {
        background-color: #7b1fa2 !important;
        color: white !important;
    }
    
    /* Logo styling */
    .logo-container {
        display: flex;
        justify-content: center;
        margin-bottom: 1.5rem;
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
        font-family: 'Arial', sans-serif;
        margin-bottom: 1.5rem;
        font-weight: bold;
        font-size: 1.5rem;
    }
</style>
""", unsafe_allow_html=True)

# Sidebar with logo and navigation
with st.sidebar:
    # Logo in a circle
    st.markdown('<div class="logo-container">', unsafe_allow_html=True)
    logo = Image.open("Assets/Img/Website_Logo_2.png")
    st.image(logo, width=120, output_format="PNG", use_container_width=False)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Title
    st.markdown('<div class="sidebar-title">CNPD</div>', unsafe_allow_html=True)
    
    # Navigation links
    st.page_link("streamlit_app.py", label="Home")
    st.page_link("pages/1_About.py", label="About")
    st.page_link("pages/2_NP_Database_Search.py", label="NP Database Search")
    st.page_link("pages/3_Tools.py", label="Tools")
    st.page_link("pages/4_Related_Databases.py", label="Related Databases")
    st.page_link("pages/5_Tutorials.py", label="Tutorials")
    st.page_link("pages/6_Statistics.py", label="Statistics")
    st.page_link("pages/7_Glossary.py", label="Glossary")
    st.page_link("pages/8_FAQ.py", label="FAQ")
    st.page_link("pages/9_Contact_Us.py", label="Contact Us")

# Main content
st.title("🧠 CNPD: Crustacean Neuropeptide Database")
st.markdown("""
### WELCOME TO CNPD: THE CRUSTACEAN NEUROPEPTIDE DATABASE

Neuropeptides are critical signaling molecules involved in numerous physiological processes, including metabolism, reproduction, development, and behavior. In crustaceans, neuropeptides regulate key biological functions such as molting, feeding, and immune responses. Despite their significance, crustacean neuropeptides remain underrepresented in existing neuropeptide databases.

To address this gap, we introduce **The Crustacean Neuropeptide Database (CNPD)** – A comprehensive resource for neuropeptide research in crustacean species. CNPD systematically curates experimentally confirmed and predicted neuropeptides from various crustacean species using Peer-reviewed literature, Mass spectrometry-based peptidomics, and Public protein databases.

This database provides detailed annotations to support **Comparative neurobiology**, **Functional studies**, and **Computational peptide discovery**.
""")

st.markdown("""
### GET INVOLVED & CONTRIBUTE

CNPD is a community-driven initiative! We welcome contributions from researchers in peptidomics, neurobiology, and comparative physiology.

To collaborate, submit data, or provide feedback, please contact Dr. Lingjun Li at **lingjun.li@wise.edu**
""")
