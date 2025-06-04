import streamlit as st
from sidebar import render_sidebar

st.set_page_config(
    page_title="Glossary",
    layout="wide",
    initial_sidebar_state="expanded"
)

render_sidebar()

# Inject custom CSS for the glossary layout
st.markdown("""
<style>
/* Section heading */
.section-heading {
  color: #29004c;
  font-size: 30px;
  font-weight: bold;
  margin-top: 2rem;
  margin-bottom: 0.25rem;
  position: relative;
  padding-bottom: 0.25rem;
  text-transform:uppercase;
}

/* Two‐column item: term on left, definition on right */
.glossary-item {
  display: grid;
  grid-template-columns: 20% 80%;
  margin-bottom: 10px;
  align-items: stretch;
}

/* Term cell */
.glossary-term {
  background-color: #9e9ac8;
  color: white;
  padding: 10px 20px;
  border-radius: 10px 0 0 10px;
  font-weight: bold;
  text-align: left;
}

/* Definition cell */
.glossary-def {
  background-color: white;
  color: #333;
  padding: 10px 10px;
  border: 3px solid #9e9ac8;
  border-radius: 0 10px 10px 0;
  display: flex;
  align-items: center;
}

/* Ensure definitions wrap and justify nicely */
.glossary-def p {
  margin: 0;
  text-align: justify;
}
</style>
""", unsafe_allow_html=True)

# Define your glossary content
species = [
    ("C. elegans", "Caenorhabditis elegans – a nematode used as a model organism in biological research."),
    ("D. melanogaster", "Drosophila melanogaster – the common fruit fly, widely used in genetic and neuropeptide research."),
    ("H. americanus", "Homarus americanus – the American lobster, a model organism for neuropeptide studies."),
]

families = [
    ("Allatostatin", "A family of neuropeptides that regulate juvenile hormone biosynthesis."),
    ("FMRFamide",      "A neuropeptide involved in muscle contraction and neurotransmission."),
    ("Tachykinin",     "A family of neuropeptides involved in pain perception and inflammation."),
]

tools = [
    ("BLAST",                 "Basic Local Alignment Search Tool for sequence similarity searches."),
    ("Mass Spectrometry",     "Techniques to measure mass-to-charge ratios of peptide ions."),
    ("Peptide Calculator",    "Computes GRAVY, hydrophobicity, charge, half-life, and more."),
]

# Helper to render one section
def render_section(title, entries):
    st.markdown(f'<div class="section-heading">{title}</div>', unsafe_allow_html=True)
    for term, definition in entries:
        st.markdown(f"""
        <div class="glossary-item">
          <div class="glossary-term">{term}</div>
          <div class="glossary-def"><p>{definition}</p></div>
        </div>
        """, unsafe_allow_html=True)

# Render each glossary section
render_section("Species", species)
render_section("Neuropeptide Family", families)
render_section("Tools", tools)


st.markdown("""
<div style="text-align: center; font-size:14px; color:#2a2541;">
  <em>Last update: Jul 2025</em>
</div>
""", unsafe_allow_html=True)

