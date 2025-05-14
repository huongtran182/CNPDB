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
        padding: 0 !important;
        margin: 0 !important;
    }
    header[data-testid="stHeader"] {
        height: 0 !important;
    }
    [data-testid="stSidebarNav"] {
        display: none;
    }
    [data-testid="stSidebar"] {
        background-color: #2a2541 !important;
        padding: 0 !important;
        margin: 0 !important;
        min-width: 250px !important;
    }
    .logo-container {
    display: flex;
    justify-content: center;
    align-items: center;
    height: 200px;
    margin-top: 10px;
    }
    .logo-border {
    width: 160px;
    height: 160px;
    border: 5px solid #b9b0cc;
    border-radius: 100%;
    display: flex;
    justify-content: center;
    align-items: center;
    }
    .circle-img {
    width: 150px;
    height: 150px;
    border-radius: 100%;
    }

    .nav-container {
        padding: 0 !important;
        margin: 0 !important;
    }
    .nav-item {
        color: #8a8695 !important;
        font-family: 'Arial', sans-serif;
        font-size: 16px !important;
        font-weight: bold !important;
        letter-spacing: 0.5px;
        text-transform: uppercase;
        text-align: center;
        padding: 3px 16px !important;
        margin: 0 !important;
        display: block;
        text-decoration: none !important;
        transition: all 0.3s ease;
    }
    .nav-item:hover { background-color: #3a2d5a !important; }
    .nav-item.active { background-color: #4a3666 !important; }
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
        {"file": "streamlit_app.py", "label": "Home"},
        {"file": "pages/1_About.py", "label": "About"},
        {"file": "pages/2_NP_Database_Search.py", "label": "Neuropeptide Database Search Engine"},
        {"file": "pages/3_Tools.py", "label": "Tools"},
        {"file": "pages/4_Related_Databases.py", "label": "Related Resources"},
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
