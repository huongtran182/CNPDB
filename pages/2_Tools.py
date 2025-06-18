import streamlit as st
from sidebar import render_sidebar
from Bio.SeqUtils.ProtParam import ProteinAnalysis
import pandas as pd
from Bio import pairwise2
from Bio.pairwise2 import format_alignment

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

# --- Peptide property calculator ---
st.markdown(
    '<h2 class="custom-title">'
    'PEPTIDE PROPERTY CALCULATOR'
    '</h2>',
    unsafe_allow_html=True
)

st.markdown('<label style="font-size:20px; ">Enter your peptide sequence:</label>', unsafe_allow_html=True)
sequence_input = st.text_area("", height=68)

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

# --- Sequence alignment calculator ---
st.markdown(
    '<h2 class="custom-title">'
    'SEQUENCE ALIGNMENT'
    '</h2>',
    unsafe_allow_html=True
)

# Load your peptide sequence database
@st.cache_data
def load_data():
    return pd.read_csv("peptide_db.csv")  # Ensure there's a "Sequence" column

df = load_data()

# Page UI
st.title("🔬 Peptide Sequence Alignment Tool")

# User input sequence
query_seq = st.text_area("🧬 Input your peptide sequence:", "")
if not query_seq:
    st.warning("Please input your peptide sequence to continue.")
    st.stop()

# Optional direct second sequence input
use_database = st.checkbox("📚 Search against peptide database instead of comparing to a specific sequence")

if not use_database:
    target_seq = st.text_area("🎯 Input second sequence for alignment (optional):", "")
else:
    target_seq = None

# Alignment parameters
st.subheader("⚙️ Alignment Settings")
alignment_type = st.selectbox("Alignment Type", ["global", "local"])
match_score = st.number_input("Match Score", value=2)
mismatch_score = st.number_input("Mismatch Penalty", value=-1)
gap_open = st.number_input("Gap Open Penalty", value=-0.5)
gap_extend = st.number_input("Gap Extension Penalty", value=-0.1)

# Perform alignment
if st.button("🔍 Run Alignment"):
    if not use_database:
        if not target_seq:
            st.error("Please provide a second sequence.")
        else:
            if alignment_type == "global":
                alignments = pairwise2.align.globalms(query_seq, target_seq, match_score, mismatch_score, gap_open, gap_extend)
            else:
                alignments = pairwise2.align.localms(query_seq, target_seq, match_score, mismatch_score, gap_open, gap_extend)
            st.success(f"Top alignment result:")
            st.code(format_alignment(*alignments[0]))
    else:
        results = []
        for i, db_seq in enumerate(df["Sequence"]):
            try:
                if alignment_type == "global":
                    aln = pairwise2.align.globalms(query_seq, db_seq, match_score, mismatch_score, gap_open, gap_extend, one_alignment_only=True)
                else:
                    aln = pairwise2.align.localms(query_seq, db_seq, match_score, mismatch_score, gap_open, gap_extend, one_alignment_only=True)
                score = aln[0].score if aln else 0
                results.append((score, db_seq, aln[0] if aln else None))
            except Exception as e:
                continue  # skip bad sequences

        top_hits = sorted(results, key=lambda x: -x[0])[:20]
        st.success("Top 20 alignment hits from database:")

        for i, (score, db_seq, aln) in enumerate(top_hits):
            st.markdown(f"### 🔹 Hit #{i+1} - Score: `{score:.2f}`")
            if aln:
                st.code(format_alignment(*aln))
            else:
                st.text("⚠️ No valid alignment.")


st.markdown("""
<div style="text-align: center; font-size:14px; color:#2a2541;">
  <em>Last update: Jul 2025</em>
</div>
""", unsafe_allow_html=True)
