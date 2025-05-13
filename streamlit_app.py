import streamlit as st
from PIL import Image

st.set_page_config(
    page_title="Crustacean Neuropeptide Database",
    layout="wide",
)

# Sidebar
with st.sidebar:
    logo = Image.open("Assets/Img/Website_Logo_2.png")
    st.image(logo, caption="Crustacean Neuropeptide Database", use_column_width=True)
    st.page_link("Pages/1_About.py", label="About")
    st.page_link("Pages/2_NP_Database_Search.py", label="Neuropeptide Database Search")
    st.page_link("Pages/3_Tools.py", label="Tools")
    st.page_link("Pages/4_Related_Databases.py", label="Related Databases and Resources")
    st.page_link("Pages/5_Tutorials.py", label="Tutorials")
    st.page_link("Pages/6_Statistics.py", label="Statistics")
    st.page_link("Pages/7_Glossary.py", label="Glossary")
    st.page_link("Pages/8_FAQ.py", label="Frequently Asked Questions")
    st.page_link("Pages/9_Contact_Us.py", label="Contact Us")

# Main content
st.title("🧠 Crustacean Neuropeptide Database")
st.markdown("""
Welcome to the Crustacean Neuropeptide Database!  
This platform offers a curated collection of **FASTA peptide sequences**, **physicochemical properties**, and **biological functions** for crustacean neuropeptides.

Explore the database using the sidebar and download sequences based on your criteria.
""")
