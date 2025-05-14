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
    [data-testid="stSidebar"] {
        background-color: #2a2541 !important;
        padding: 0 !important;
        margin: 0 !important;
        height: 100vh !important;        /* Full screen height */
        overflow-y: auto !important;     /* Allow scroll only if needed */
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
<h1>About CNPD – Crustacean Neuropeptide Database</h1>
""", unsafe_allow_html=True)

st.markdown("""
<div class="section">
<h2>Overview</h2>
<p>The current release of <span class="highlight">CNPD (Version 1.0, 2025)</span> contains <span class="highlight">[X]</span> curated neuropeptide entries from <span class="highlight">[Y]</span> crustacean species, organized into <span class="highlight">[Z]</span> neuropeptide families.</p>
<p>Data is manually curated from peer-reviewed literature, mass spectrometry-based peptidomics, and public protein databases such as <b>UniProt</b> and <b>NCBI</b>.</p>
</div>

<div class="section">
<h2>What CNPD Provides</h2>
<ul>
<li>Neuropeptide sequence (FASTA format)</li>
<li>Species taxonomy & homology</li>
<li>Physicochemical properties (mass, charge, hydrophobicity, etc.)</li>
<li>Post-translational modifications (PTMs)</li>
<li>Experimental validation methods (LC-MS/MS, transcriptomic mining, etc.)</li>
<li>MS Imaging of the peptide showing their distribution in tissues</li>
<li>Predicted 3D Structure</li>
<li>Predicted Half-life</li>
<li>Predicted/validated biological functions</li>
</ul>
<p>CNPD also provides cross-links to <b>UniProt, NCBI, and PubMed</b>, along with search and analysis tools for neuropeptide research.</p>
</div>

<div class="section">
<h2>Database Features & Tools</h2>
<ul>
<li><b>Flexible Search Engine</b> – Find neuropeptides by name, sequence, family, or function.</li>
<li><b>Comparative Peptide Analysis</b> – Compare neuropeptide sequences across crustacean species.</li>
<li><b>Sequence Alignment & Homology Search</b> – Identify conserved motifs and sequence similarities.</li>
<li><b>Mass Spectrometry Data Integration</b> – Explore MS-validated peptides and spectral evidence.</li>
<li><b>Peptide Property Calculator</b> – Compute GRAVY scores, hydrophobicity, half-life, 3D structures, and more.</li>
</ul>
</div>

<div class="section">
<h2>Crustacean Species Covered</h2>
<ul>
<li><i>Homarus americanus</i> (American Lobster)</li>
<li><i>Callinectes sapidus</i> (Blue Crab)</li>
<li><i>Cancer borealis</i> (Jonah Crab)</li>
<li><i>Litopenaeus vannamei</i> (Pacific White Shrimp)</li>
<li><i>Pandalus borealis</i> (Northern Shrimp)</li>
</ul>
</div>

<div class="section">
<h2>Data Sources & Curation</h2>
<ul>
<li><b>Experimental Data</b> – Mass spectrometry & neuropeptide bioassays</li>
<li><b>Literature Mining</b> – Curated from PubMed & primary research papers</li>
<li><b>Public Databases</b> – Cross-linked with UniProt, NCBI, and NeuroPep</li>
<li><b>Computational Predictions</b> – Sequence-based neuropeptide identification</li>
</ul>
<p>Every neuropeptide entry undergoes <b>manual examination</b> to ensure accuracy and reliability.</p>
</div>

<div class="section">
<h2>Get Involved & Contribute</h2>
<ul>
<li>Submit new neuropeptide sequences</li>
<li>Report missing or updated annotations</li>
<li>Share mass spectrometry datasets</li>
<li>Suggest additional features or improvements</li>
</ul>
<p>For collaborations, submissions, or feedback, please contact <a href="mailto:lingjun.li@wisc.edu" class="email">Dr. Lingjun Li</a>.</p>
</div>

<div class="section">
<h2>Citation & Funding</h2>
<p>If you use CNPD in your research, please cite:</p>
<p><b>Crustacean Neuropeptide Database (CNPD): A curated resource for neuropeptide research in crustacean species.</b> [Authors]. [Journal Name], [Year]. DOI: [XXXX].</p>
<p><b>Funding:</b> This work is supported by [Funding Agencies].</p>
</div>

<div class="section">
<h2>Future Updates</h2>
<ul>
<li>Expansion to more crustacean species</li>
<li>Enhanced peptide discovery tools</li>
<li>Improved mass spectrometry integration</li>
<li>User-submitted experimental data uploads</li>
</ul>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<i>Last update: Jul 2025</i>
""", unsafe_allow_html=True)
