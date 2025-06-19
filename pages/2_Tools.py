import streamlit as st
from sidebar import render_sidebar
from Bio.SeqUtils.ProtParam import ProteinAnalysis
import pandas as pd
from Bio import pairwise2
from io import StringIO
from Bio.Align import substitution_matrices
import re

st.set_page_config(
    page_title="Tools",
    layout="wide",
    initial_sidebar_state="expanded"
)

render_sidebar()

st.markdown("""
<style>
.stDownloadButton>button {
    background-color: #54278f !important;
    color: white !important;
    border: none;
    border-radius: 0.5rem;
    padding: 0.6rem 1.2rem;
    font-weight: 600;
    transition: background-color 0.2s ease;
}
.stDownloadButton>button:hover {
    background-color: #3f007d !important;
}
</style>
""", unsafe_allow_html=True)

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

sequence_input = st.text_area("Enter your peptide sequence:", height=68)

# Centered Calculate Button
col_calc1, col_calc2, col_calc3 = st.columns([1.7, 1, 1])
with col_calc2:
    calculate_clicked = st.button("Calculate", type="primary")

if calculate_clicked:
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

# --- Separator Line ---
st.markdown("""
<hr style='border: none; border-top: 2px solid #6a51a3; margin-top: 10px; margin-bottom: 0px; margin-left: 30px; margin-right: 30px;'>
""", unsafe_allow_html=True)

# --- Sequence alignment calculator ---
st.markdown(
    '<h2 class="custom-title">'
    'PEPTIDE SEQUENCE ALIGNMENT'
    '</h2>',
    unsafe_allow_html=True
)

# Custom function to format alignment manually (without score)
def custom_format_alignment(aln):
    seqA = aln.seqA
    seqB = aln.seqB
    midline = ""

    for a, b in zip(seqA, seqB):
        if a == b:
            midline += "|"
        else:
            midline += " "

    return f"{seqA}\n{midline}\n{seqB}"


# Function to generate downloadable text report
def generate_alignment_text(query_seq, alignment_type, match_score, mismatch_score, gap_open, gap_extend, top_hits, df):
    report = StringIO()
    report.write("Peptide Sequence Alignment Report\n")
    report.write("="*40 + "\n")
    report.write(f"Query Sequence: {query_seq}\n")
    report.write(f"Alignment Type: {alignment_type}\n")
    report.write(f"Match Score: {match_score}, Mismatch Penalty: {mismatch_score}\n")
    report.write(f"Gap Open: {gap_open}, Gap Extend: {gap_extend}\n\n")

    for i, (score, db_seq, aln) in enumerate(top_hits):
        report.write(f"Hit #{i+1} - Score: {score:.2f}\n")
        report.write("-"*30 + "\n")
        if aln:
            report.write(custom_format_alignment(aln) + "\n")
        else:
            report.write("⚠️ No valid alignment.\n")

        match_row = df[df["Sequence"] == db_seq].iloc[0] if not df[df["Sequence"] == db_seq].empty else None
        if match_row is not None:
            report.write(f"Family: {match_row.get('Family', 'N/A')}\n")
            report.write(f"Organism (OS): {match_row.get('OS', 'N/A')}\n")
            report.write(f"Tissue: {match_row.get('Tissue', 'N/A')}\n")
            report.write(f"Active Sequence: {match_row.get('Active Sequence', 'N/A')}\n")

        report.write("\n")
    return report.getvalue()

# Load your peptide sequence database
@st.cache_data
def load_data():
    return pd.read_excel("Assets/20250617_cNPDB.xlsx", sheet_name="Sheet 1")

df = load_data()

def clean_sequence(seq):
    lines = seq.strip().splitlines()
    # Remove any line that starts with '>'
    clean_lines = [line.strip() for line in lines if not line.startswith(">")]
    return ''.join(clean_lines).upper()

# User input sequence
query_seq = st.text_area("Enter your peptide sequence (Only one sequence at a time):", value="", height=68)

# Option to align against another sequence or the database
target_seq = st.text_area("Enter second sequence for alignment (optional):", value="", height=68)

query_seq = clean_sequence(query_seq)
target_seq = clean_sequence(target_seq)

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

col1, col2, col3 = st.columns([1.6, 1, 1])
with col2:
    run_clicked = st.button("Run Alignment", type="primary")

# Run Alignment Button
if run_clicked:
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
                st.code(custom_format_alignment(alignments[0]))
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

            alignment_txt = generate_alignment_text(
                query_seq, alignment_type, match_score, mismatch_score, gap_open, gap_extend, top_hits, df
            )

            # Centered download button
            col_dl1, col_dl2, col_dl3 = st.columns([1.3, 1, 1])
            with col_dl2:
                st.download_button(
                label="Download Alignment Results",
                data=alignment_txt,
                file_name="cNPDB_alignment_results.txt",
                mime="text/plain"
            )

            for i, (score, db_seq, aln) in enumerate(top_hits):
                match_row = df[df["Sequence"] == db_seq].iloc[0] if not df[df["Sequence"] == db_seq].empty else None

                st.markdown(f"""
                    <div style='padding:10px 0;'>
                        <span style='font-size:16px; color:#54278f; font-weight:bold;'>Hit #{i+1}</span><br>
                        <span style='font-size:16px;'>Score: <span style='color:#238b45; font-weight:bold;'>{score:.2f}</span></span>
                    </div>
                """, unsafe_allow_html=True)

                if aln:
                    st.code(custom_format_alignment(aln))

                if match_row is not None:
                    st.markdown(f"""
                    <div style='font-size:15px; margin-bottom:20px;'>
                        <strong>Family:</strong> {match_row.get("Family", "N/A")}<br>
                        <strong>Organisms:</strong> {match_row.get("OS", "N/A")}<br>
                        <strong>Tissue:</strong> {match_row.get("Tissue", "N/A")}<br>
                        <strong>Active Sequence:</strong> {match_row.get("Active Sequence", "N/A")}
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.warning("No additional info found for this hit.")

# --- Separator Line ---
st.markdown("""
<hr style='border: none; border-top: 3px solid #6a51a3;  margin-top: 10px; margin-bottom: 0px; margin-left: 30px; margin-right: 30px;'>
""", unsafe_allow_html=True)

# --- BLAST Search ---
st.markdown(
    '<h2 class="custom-title">'
    'BLAST SEARCH'
    '</h2>',
    unsafe_allow_html=True
)

@st.cache_data
def load_db():
    return pd.read_excel("Assets/20250617_cNPDB.xlsx", sheet_name="Sheet 1")

df = load_db()

# --- Input ---
query_input = st.text_area("Enter your peptide sequence (Only one sequence at a time):", value="", height=69)

def parse_sequence(text):
    lines = text.strip().splitlines()
    clean = [l.strip() for l in lines if not l.startswith(">")]
    sequence = ''.join(clean).upper()
    return sequence

query_seq = parse_sequence(query_input)

# --- Settings ---
st.sidebar.header("BLAST Settings")

st.markdown("### BLAST Settings")
col_param = st.columns(5)
with col_param[0]:
    word_size = st.slider("Word Size", 1, 5, 3)
with col_param[1]:
    e_value_thresh = st.number_input("E-value Threshold", value=10.0, step=0.1)
with col_param[2]:
    gap_open = st.number_input("Gap Open Penalty", value=10.0, step=0.5)
with col_param[3]:
    gap_extend = st.number_input("Gap Extend Penalty", value=0.5, step=0.1)
with col_param[4]:
    matrix_options = ["BLOSUM62", "BLOSUM80", "BLOSUM45", "PAM30", "PAM70"]
    matrix_choice = st.selectbox("Matrix", matrix_options, key="matrix_select")

col_opt = st.columns(3)
with col_opt[0]:
    top_n = st.selectbox("Number of Top Hits", [5, 10, 20], index=1)   
with col_opt[1]:
    seg_filter = st.checkbox("SEG Filtering", value=True)    
with col_opt[2]:
    comp_bias = st.checkbox("Composition-based Stats", value=True)

# Load and convert substitution matrix to pairwise2-compatible format
mat = substitution_matrices.load(matrix_choice)
scoring_matrix = { (a, b): mat[a][b] for a in mat.alphabet for b in mat.alphabet }

# Format alignment manually
def format_alignment(aln):
    seqA, seqB = aln.seqA, aln.seqB
    midline = ''.join(['|' if a == b else ' ' for a, b in zip(seqA, seqB)])
    return f"{seqA}\n{midline}\n{seqB}"

col1, col2, col3 = st.columns([1.6, 1, 1])
with col2:
    run = st.button("Run BLAST", type="primary")

# Run Alignment Button
if run:
    if not query_seq:
        st.error("Please input a valid sequence.")
    else:
        if seg_filter:
            query_seq = re.sub(r'[^A-Z]', '', query_seq)
            query_seq = re.sub(r'(.)\1{3,}', '', query_seq)
        
        results = []
        for i, db_seq in enumerate(df["Sequence"]):
                if seg_filter:
                    db_seq = re.sub(r'[^A-Z]', '', db_seq)
                    db_seq = re.sub(r'(.)\1{3,}', '', db_seq)

                if len(query_seq) < word_size or len(db_seq) < word_size:
                    continue

                try:
                    aln = pairwise2.align.localds(query_seq, db_seq, scoring_matrix, -gap_open, -gap_extend, one_alignment_only=True)
                    score = aln[0].score if aln else 0
                    e_val = 1e-5 * (100 - score/len(query_seq)) * (i+1)
                    if comp_bias:
                        bias_penalty = abs(len(query_seq) - len(db_seq)) * 0.01
                        e_val += bias_penalty

                    if e_val <= e_value_thresh:
                        results.append((score, e_val, db_seq, aln[0] if aln else None))
                except Exception:
                    continue

        results = sorted(results, key=lambda x: -x[0])[:top_n]

        if not results:
            st.warning("No hits below the selected E-value threshold.")
        else:
            st.success(f"{len(results)} hit(s) found with E-value ≤ {e_value_thresh}")

            report = StringIO()
            report.write(f"cNPDB BLAST Report\nQuery: {query_seq}\nMatrix: {matrix_choice}\n")
            report.write(f"Word Size: {word_size}\nSEG Filtering: {seg_filter}\nComposition-based stats: {comp_bias}\n")
            report.write(f"Gap Open Penalty: {gap_open}\nGap Extend Penalty: {gap_extend}\n\n")

            col_dl1, col_dl2, col_dl3 = st.columns([1.35, 1, 1])
            with col_dl2:
                st.download_button(
                    label="Download BLAST Results",
                    data=report.getvalue(),
                    file_name="cNPDB_BLAST_results.txt",
                    mime="text/plain"
                )

            for i, (score, e_val, db_seq, aln) in enumerate(results):
                st.subheader(f"Hit #{i+1}")
                identical = sum(a == b for a, b in zip(aln.seqA, aln.seqB))
                aln_length = len(aln.seqA)
                identity_pct = (identical / aln_length) * 100 if aln_length > 0 else 0
                st.text(f"Score: {score:.2f} | E-value: {e_val:.2e} | Identity: {identity_pct:.1f}% | Length: {aln_length}")
                st.code(format_alignment(aln) if aln else "No alignment.")

                row = df[df["Sequence"] == db_seq].iloc[0] if not df[df["Sequence"] == db_seq].empty else None
                if row is not None:
                    st.markdown(f"""
                    **Family**: {row.get('Family', 'N/A')}  
                    **Organism**: {row.get('OS', 'N/A')}  
                    **Tissue**: {row.get('Tissue', 'N/A')}  
                    **Active Sequence**: {row.get('Active Sequence', 'N/A')}
                    """)
                    report.write(f"Hit #{i+1}\n")
                    report.write(format_alignment(aln) + "\n")
                    report.write(f"""Score: {score:.2f} | E-value: {e_val:.2e} | Identity: {identity_pct:.1f}% | Length: {aln_length}""")
                    report.write(f"""Family: {row.get('Family', 'N/A')}\nOrganism: {row.get('OS', 'N/A')}\n\n""") 

    
st.markdown("""
<div style="text-align: center; font-size:14px; color:#2a2541;">
  <em>Last update: Jul 2025</em>
</div>
""", unsafe_allow_html=True)
