import streamlit as st
from PIL import Image, ImageDraw
import os
import base64
from io import BytesIO

# Set page config
st.set_page_config(layout="wide", initial_sidebar_state="expanded")

# Custom CSS for logo and nav
st.markdown("""
<style>
    html, body, .stApp {
        height: 100% !important;
        padding: 0 !important;
        margin: 0 !important;
    }
    header[data-testid="stHeader"] {
        height: 0 !important;
    }
    [data-testid="stSidebarNav"] {
        display: none;
    }
    
    /* Reset default Streamlit sidebar styles */
    section[data-testid="stSidebar"] {
    background-color: #2a2541 !important;
    padding: 0 !important;
    margin: 0 !important;
    height: 100vh !important;
    display: flex !important;
    flex-direction: column;
    align-items: center !important;
    justify-content: flex-start !important;
    }

    /* Fixes ghost search bar and mobile collapse weirdness */
    section[data-testid="stSidebar"] input,
    div[data-testid="collapsedControl"] {
    display: none !important;
    }
    
    .logo-container {
    width: 100%;
    display: flex;
    justify-content: center;
    align-items: center;
    height: 0px;
    }
    .logo-border {
    width: 160px;
    height: 160px;
    border: 7px solid #555167;
    border-radius: 100%;
    display: flex;
    justify-content: center;
    align-items: center;
    overflow: hidden;
    margin: 0 auto;
    }
    .circle-img {
    width: 150px;
    height: 150px;
    border-radius: 100%;
    }

    .nav-container {
        padding: 0 !important;
        margin: 0 !important;
        width: 100%;
    }
    
   /* New sidebar navigation styles */
    .stPageLink {
        display: block !important;
        text-align: center !important;
        padding: 4px 0 !important;
        margin: 0 !important;
        width: 100% !important;
    }
    
    .stPageLink a {
        color: #9592a0 !important;
        font-family: 'Arial', sans-serif !important;
        font-size: 30px !important;
        font-weight: bold !important;
        text-transform: uppercase !important;
        text-align: center !important;
        letter-spacing: 0.5px !important;
        padding: 0px 8px !important;
        margin: 0 !important;
        width: 100% !important;
        display: block !important;
        cursor: pointer !important;
        transition: all 0.3s ease !important;
        text-decoration: none !important;
    }
    
    .stPageLink a:hover {
        background-color: #3a2d5a !important;
        color: #ffcc00 !important;
        text-decoration: none !important;
    }

    .stPageLink a:active {
        background-color: #4a3666 !important;
    }

    /* Add separator between nav items */
    .nav-separator {
        height: 0.1px;
        background-color: #555167;
        width: 10%;
        margin: 0 auto;
    }
</style>
""", unsafe_allow_html=True)


def image_to_base64(image):
    buffered = BytesIO()
    image.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode()


# Sidebar content
with st.sidebar:
    st.markdown('<div class="logo-container">', unsafe_allow_html=True)

    logo_path = os.path.join("Assets", "Img", "Website_Logo_2.png")
    if os.path.exists(logo_path):
        logo = Image.open(logo_path).convert("RGBA").resize((160, 160))

        # Circular mask
        mask = Image.new("L", (160, 160), 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse((0, 0, 160, 160), fill=255)
        logo.putalpha(mask)

        # Base64 encoding
        buffered = BytesIO()
        logo.save(buffered, format="PNG")
        img_base64 = base64.b64encode(buffered.getvalue()).decode()

        st.markdown(f"""
            <div class="logo-border">
                <img src="data:image/png;base64,{img_base64}" class="circle-img" />
            </div>
        """, unsafe_allow_html=True)
    else:
        st.error(f"Logo image not found at: {logo_path}")
        st.text(f"Working directory: {os.getcwd()}")

    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="nav-container">', unsafe_allow_html=True)
    pages = [
    st.page_link("streamlit_app.py", label="Home"),
    st.page_link("pages/1_About.py", label="About"),
    st.page_link("pages/2_NP_Database_Search.py", label="Neuropeptide Database Search Engine"),
    st.page_link("pages/3_Tools.py", label="Tools"),
    st.page_link("pages/4_Related_Databases.py", label="Related Resources"),
    st.page_link("pages/5_Tutorials.py", label="Tutorials"),
    st.page_link("pages/6_Statistics.py", label="Statistics"),
    st.page_link("pages/7_Glossary.py", label="Glossary"),
    st.page_link("pages/8_FAQ.py", label="Frequently Asked Questions"),
    st.page_link("pages/9_Contact_Us.py", label="Contact Us"),
    ]
    
    st.markdown('</div>', unsafe_allow_html=True)


# Main content area
st.markdown("""<div style="padding:0;margin:0;">""", unsafe_allow_html=True)

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
