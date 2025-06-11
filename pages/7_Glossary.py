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
  background-color: #7e7ba0;
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
  border: 3px solid #7e7ba0;
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
    ("C. elegans", "<i>Caenorhabditis elegans</i> – roundworm"),
    ("D. melanogaster", "<i>Drosophila melanogaster</i> – Fruit fly"),
    ("H. americanus", "<i>Homarus americanus</i> – American lobster"),
]

tissues = [
    ("Br",     "Brain - Modulates and initiates signalling communications and responses to external stimuli"),
    ("CG",     "Cardiac Ganglion - Embeds inside the heart muscle, regulates cardiac muscle contractions and heartbeat"),
    ("CNS",    "Central Nervous System - Controls and coordinates sensory input, motor functions, and behavior"),
    ("CoG",    "Commissural Ganglion - Coordinates signals between the brain and the stomatogastric ganglion for gut motility"),
    ("ES",     "Eyestalk Ganglia - Acts as a neurosecretory center, contains neurosecretory cells (also called X-organ) that synthesize neuropeptides and hormones"),
    ("IMN",    "Inhibitory Motorneuron"),
    ("OG",     "Oesophageal Ganglion - Integrates neural signals between the brain and lower ganglia"),
    ("PO",     "Pericardial Organ - Locates at two sides of the heart, secretes neuropeptides into the hemolymph to reach distant organs, affecting cardiac and downstream physiological processes"),
    ("SG",     "Sinus Gland - Locates in the eyestalks, stores and releases neurohormones that regulate molting, reproduction, and metabolism"),
    ("STG",    "Stomatogastric Ganglion - Locates in the foregut region, controls rhythmic muscle contractions for stomach and gut function"),
    ("TG",     "Thoracic Ganglion - Situates in the thorax, manages motor control of walking legs and other appendages"),
    ("VNC",    "Ventral Nerve cord - Locates along the ventral side of the crustacean's body, coordinates sensory input and motor output for the body segments"),
]

families = [
    ("CCAP",   "Crustacean Cardioactive Peptide"),
    ("CCAP_PRP",   "Crustacean Cardioactive Peptide Precursor Related Peptide"),
    ("CHH",    "Crustacean Hyperglycemic Hormone"),
    ("CP2",    "Cerebral peptide 2"),
    ("CPRP",   "Crustacean hyperglycemic hormone Precursor Related Peptide"),
    ("DH",     "Diuretic Hormone"),
    ("DH31",   "Diuretic Hormone 31"),
    ("DH44",   "Diuretic Hormone 44"),
    ("ETH",    "Ecdysis Triggering Hormone"),
    ("EH",     "Eclosion Hormone"),
    ("MIH",    "Molt Inhibiting Hormone"),
    ("MOIH",   "Mandibular Organ Inhibiting Hormone"),
    ("PDH",    "Pigment Dispersing Hormone"),
    ("RPCH",   "Red Pigment Concentrating Hormone"),
    ("sNPF",   "short Neuropeptide F"),
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
render_section("Tissues", tissues)
render_section("Neuropeptide Family", families)
render_section("Tools", tools)


st.markdown("""
<div style="text-align: center; font-size:14px; color:#2a2541;">
  <em>Last update: Jul 2025</em>
</div>
""", unsafe_allow_html=True)

