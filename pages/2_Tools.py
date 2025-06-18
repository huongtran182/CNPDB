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
    'PEPTIDE SEQUENCE ALIGNMENT'
    '</h2>',
    unsafe_allow_html=True
)

# Load your peptide sequence database
@st.cache_data
def load_data():
    return pd.read_excel("Assets/20250613_cNPDB.xlsx", sheet_name="Sheet 1")

df = load_data()

# User input sequence
query_seq = st.text_area("Input your peptide sequence:", "")

# Option to align against another sequence or the database
target_seq = st.text_area("Input second sequence (optional):", "")
if not target_seq:
    use_database = st.checkbox("Align against the cNPDB database", value=False)
else:
    use_database = None

# Alignment parameters in compact column layout
st.markdown("### Alignment Settings")
col_param = st.columns(5)
with col_param[0]:
    alignment_type = st.selectbox("Type", ["global", "local"])
with col_param[1]:
    match_score = st.number_input("Match", value=2)
with col_param[2]:
    mismatch_score = st.number_input("Mismatch", value=-1)
with col_param[3]:
    gap_open = st.number_input("Gap Open", value=-0.5)
with col_param[4]:
    gap_extend = st.number_input("Gap Extend", value=-0.1)

# Run Alignment Button
button_disabled = not query_seq or (not use_database and not target_seq)

if st.button("🔍 Run Alignment", type="primary"):
    if not query_seq.strip():
        st.error("❌ Please input your peptide sequence.")
    elif not use_database and not target_seq.strip():
        st.error("❌ Please input the second sequence or choose to align against the cNPDB database.")
    else:
        if not use_database:
            try:
                alignments = (
                    pairwise2.align.globalms(query_seq, target_seq, match_score, mismatch_score, gap_open, gap_extend)
                    if alignment_type == "global" else
                    pairwise2.align.localms(query_seq, target_seq, match_score, mismatch_score, gap_open, gap_extend)
                )
                st.success("Top alignment result:")
                st.code(format_alignment(*alignments[0]))
            except Exception as e:
                st.error(f"Alignment failed: {e}")
        else:
            results = []
            for i, db_seq in enumerate(df["Sequence"]):
                try:
                    aln = (
                        pairwise2.align.globalms(query_seq, db_seq, match_score, mismatch_score, gap_open, gap_extend, one_alignment_only=True)
                        if alignment_type == "global" else
                        pairwise2.align.localms(query_seq, db_seq, match_score, mismatch_score, gap_open, gap_extend, one_alignment_only=True)
                    )
                    score = aln[0].score if aln else 0
                    results.append((score, db_seq, aln[0] if aln else None))
                except Exception:
                    continue

        top_hits = sorted(results, key=lambda x: -x[0])[:10]
        st.success("Top 10 alignment hits from cNPDB database:")

        for i, (score, db_seq, aln) in enumerate(top_hits):
            # Find additional info
            match_row = df[df["Sequence"] == db_seq].iloc[0] if not df[df["Sequence"] == db_seq].empty else None
        
            st.markdown(f"""
                <div style='padding:10px 0;'>
                    <span style='font-size:16px; color:#54278f; font-weight:bold;'>Hit #{i+1}</span>
                    <br>
                    <span style='font-size:16px;'>Score: <span style='color:#238b45; font-weight:bold;'>{score:.2f}</span></span>
                </div>
            """, unsafe_allow_html=True)
        
            if aln:
                st.code(format_alignment(*aln))
            
            if match_row is not None:
                st.markdown(f"""
                <div style='font-size:15px; margin-bottom:20px;'>
                    <strong>Family:</strong> {match_row.get("Family", "N/A")}<br>
                    <strong>Organisms:</strong> {match_row.get("OS", "N/A")}<br>
                    <strong>Active Sequence:</strong> {match_row.get("Active Sequence", "N/A")}
                </div>
                """, unsafe_allow_html=True)
            else:
                st.warning("No additional info found for this hit.")

st.markdown("""
<div style="text-align: center; font-size:14px; color:#2a2541;">
  <em>Last update: Jul 2025</em>
</div>
""", unsafe_allow_html=True)
