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

st.markdown('<label style="font-size:10px; font-weight:bold;">Enter your peptide sequence:</label>', unsafe_allow_html=True)
sequence_input = st.text_area("", height=50)

if st.button("Calculate", type="primary"):
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
  1. <a href="https://services.healthtech.dtu.dk/services/SignalP-6.0/" target="_blank">SignalP - 6.0</a>
</h4>
""", unsafe_allow_html=True)
st.markdown("""
SignalP 6.0 is a deep learning-based tool that predicts the presence and cleavage sites of signal peptides in protein sequences. 
It helps identify peptides likely to be secreted, making it especially useful for discovering and filtering neuropeptide prohormone 
precursors from whole-proteome datasets.
""")

st.markdown("""
<h4 style="margin-bottom: 10px;">
  1. <a href="https://services.healthtech.dtu.dk/services/SignalP-6.0/" target="_blank">SignalP - 6.0</a>
</h4>
""", unsafe_allow_html=True)
st.markdown("""
SignalP 6.0 is a deep learning-based tool that predicts the presence and cleavage sites of signal peptides in protein sequences. 
It helps identify peptides likely to be secreted, making it especially useful for discovering and filtering neuropeptide prohormone 
precursors from whole-proteome datasets.
""")

st.markdown("""
<div style="text-align: center; font-size:14px; color:#2a2541;">
  <em>Last update: Jul 2025</em>
</div>
""", unsafe_allow_html=True)
