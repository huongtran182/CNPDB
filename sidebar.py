# sidebar.py
import streamlit as st
from PIL import Image, ImageDraw
import os
import base64
from io import BytesIO

def render_sidebar():
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
        [data-testid="stSidebar"] {
            background-color: #2a2541 !important;
            padding: 0 !important;
            margin: 0 !important;
            height: 100vh !important;
            overflow-y: auto !important;
            display: flex !important;
            flex-direction: column;
            justify-content: flex-start;
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
        }
        .nav-item {
            color: #8a8695 !important;
            font-family: 'Arial', sans-serif;
            font-size: 16px !important;
            font-weight: bold !important;
            letter-spacing: 0.5px;
            text-transform: uppercase;
            text-align: center;
            padding: 0px 8px !important;
            margin: 0 !important;
            display: block;
            text-decoration: none !important;
            transition: all 0.3s ease;
        }
        .nav-item:hover { background-color: #3a2d5a !important; }
        .nav-item.active { background-color: #4a3666 !important; }
    </style>
    """, unsafe_allow_html=True)

    with st.sidebar:
        st.markdown('<div class="logo-container">', unsafe_allow_html=True)
        logo_path = os.path.join("Assets", "Img", "Website_Logo_2.png")

        if os.path.exists(logo_path):
            logo = Image.open(logo_path).convert("RGBA").resize((160, 160))
            mask = Image.new("L", (160, 160), 0)
            draw = ImageDraw.Draw(mask)
            draw.ellipse((0, 0, 160, 160), fill=255)
            logo.putalpha(mask)

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

        current_page = os.path.basename(__file__)
        for page in pages:
            is_active = current_page == os.path.basename(page["file"])
            active_class = "active" if is_active else ""
            st.markdown(
                f'<a href="{page["file"]}" class="nav-item {active_class}" target="_self">{page["label"].upper()}</a>',
                unsafe_allow_html=True
            )
        st.markdown('</div>', unsafe_allow_html=True)
