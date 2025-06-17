import streamlit as st
from sidebar import render_sidebar
from Bio.SeqUtils.ProtParam import ProteinAnalysis

st.set_page_config(
    page_title="Tools",
    layout="wide",
    initial_sidebar_state="expanded"
)

render_sidebar()

# Hydrophobic residues
hydrophobic_residues = set("AILMFWYV")

def calculate_properties(sequence):
    sequence = sequence.upper().replace(" ", "").replace("\n", "")
    analysis = ProteinAnalysis(sequence)

    length = len(sequence)
    molecular_weight = analysis.molecular_weight()
    gravy = analysis.gravy()
    instability_val = analysis.instability_index()
    instability_status = "stable" if instability_val < 40 else "unstable"
    
    hydrophobic_count = sum(1 for aa in sequence if aa in hydrophobic_residues)
    hydrophobic_pct = (hydrophobic_count / length) * 100 if length > 0 else 0

    return {
        "Peptide Sequence": sequence,
        "Molecular Weight": round(molecular_weight, 3),
        "Length": length,
        "GRAVY Score": round(gravy, 3),
        "% Hydrophobic Residue": round(hydrophobic_pct, 2),
        "Instability Index": f"{round(instability_val, 3)} ({instability_status})",
    }

# Page layout
st.markdown("""
<style>
 /* 1) Centered title with10px top margin */
  h2.custom-title {
    text-align: center !important;
    margin-top: 0px !important;
    color: #29004c;
  }
</style>
""", unsafe_allow_html=True)

# --- Centered, spaced title ---
st.markdown(
    '<h2 class="custom-title">'
    'PEPTIDE PROPERTY CALCULATOR'
    '</h2>',
    unsafe_allow_html=True
)

st.markdown('<label style="font-size:20px; ">Enter your peptide sequence:</label>', unsafe_allow_html=True)
sequence_input = st.text_area("", height=68)

# Create a container for centering the button
col1, col2, col3 = st.columns([1, 1, 1])
with col2:
    if st.button("Calculate"):
        if not sequence_input.strip():
            st.error("Please enter a peptide sequence")
        else:
            try:
                props = calculate_properties(sequence_input)
                st.markdown("### Peptide Property Results")
                for key, value in props.items():
                    st.write(f"**{key}**: {value}")
            except Exception as e:
                st.error(f"Error: {e}")

st.markdown(
    '<h2 class="custom-title">'
    'OTHER TOOLS FOR NEUROPEPTIDE RESEARCH'
    '</h2>',
    unsafe_allow_html=True
)

st.markdown("""
<h4 style="margin-bottom: 10px;">
  1. <a href="https://academic.oup.com/bib/article/24/2/bbad077/7073964?login=false">NeuroPred-PLM</a>
</h4>
""", unsafe_allow_html=True)
st.markdown("""
NeuroPred‑PLM is a machine learning-based tool that predicts whether a peptide is a neuropeptide using protein language model 
embeddings and convolutional neural networks. It provides interpretable results through attention mechanisms that highlight 
important sequence regions. The tool is available as a Python package and through a web interface for easy use.
""")

st.markdown("""
<h4 style="margin-bottom: 10px;">
  2. <a href="https://services.healthtech.dtu.dk/services/SignalP-6.0/" target="_blank">SignalP - 6.0</a>
</h4>
""", unsafe_allow_html=True)
st.markdown("""
SignalP 6.0 is a deep learning-based tool that predicts the presence and cleavage sites of signal peptides in protein sequences. 
It helps identify peptides likely to be secreted, making it especially useful for discovering and filtering neuropeptide prohormone 
precursors from whole-proteome datasets.
""")

st.markdown("""
<h4 style="margin-bottom: 10px;">
  3. <a href="https://www.uniprot.org/blast" target="_blank">BLAST</a>
</h4>
""", unsafe_allow_html=True)
st.markdown("""
BLAST on UniProt allows researchers to compare a peptide sequence against a vast database of known proteins. This helps identify 
homologous or functionally similar sequences across species, providing insights into evolutionary conservation or potential functions 
of novel peptides. Simply paste your peptide sequence, choose the database, and run the search to explore matches.
""")

st.markdown("""
<h4 style="margin-bottom: 10px;">
  4. <a href="http://www.clustal.org/" target="_blank">Clustal Omega</a>
</h4>
""", unsafe_allow_html=True)
st.markdown("""
Clustal Omega is a tool for multiple sequence alignment, useful when comparing several neuropeptide sequences to identify conserved motifs, patterns, 
or evolutionary relationships. It helps align candidate peptides with known neuropeptides across species to find functional similarities or 
conserved cleavage regions.
""")

st.markdown("""
<h4 style="margin-bottom: 10px;">
  5. <a href="https://www.retentionprediction.org/hplc/retentionpredictor.php#launch">HPLC Retention Predictor</a>
</h4>
""", unsafe_allow_html=True)
st.markdown("""
The HPLC Retention Predictor is a web-based tool that estimates HPLC retention times for peptides based on their sequence. It helps predict 
how a peptide might behave during liquid chromatography, aiding in experimental design and peptide identification when comparing predicted 
retention times with observed LC-MS data.
""")

st.markdown("""
<h4 style="margin-bottom: 10px;">
6. <a href="https://alphafoldserver.com/welcome">AlphaFold3</a>
</h4>
""", unsafe_allow_html=True)
st.markdown("""
The AlphaFold Server provides structure predictions for proteins and peptides based on their amino acid sequence powered by Artificial Inteligence (AI).
AlphaFold can help visualize the 3D structure of neuropeptides or their prohormone precursors, offering insights into functional domains, receptor binding, 
or post-translational modification sites.
""")

st.markdown("""
<div style="text-align: center; font-size:14px; color:#2a2541;">
  <em>Last update: Jul 2025</em>
</div>
""", unsafe_allow_html=True)
