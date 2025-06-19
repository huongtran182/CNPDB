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

st.markdown("""
<div style='font-size:15px; padding:10px 10px;'>
Peptide Alignment allows users to align two peptide sequences or align a query peptide against neuropeptide sequences in the cNPDB database. Default settings are suitable for most neuropeptide alignments, but users can modify the alignment parameters for custom analysis. For more guidance, please refer to the <i>Glossary</i> and <i>Tutorials</i> pages.
</div>
""", unsafe_allow_html=True)


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

st.markdown("""
<div style='font-size:15px; padding:10px 10px;'>
BLAST Search allows users to compare their peptide sequence against the cNPDB database and identify similar neuropeptides. Default parameters are optimized for typical neuropeptide BLAST searches, but users can customize settings to suit their needs. See <i>Glossary</i> and <i>Tutorials</i> pages for more details.
</div>
""", unsafe_allow_html=True)


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
    e_value_thresh = st.number_input("E-value Threshold", value=10.0, step=0.1)
with col_param[1]:
    matrix_options = ["BLOSUM62", "BLOSUM80", "BLOSUM45", "PAM30", "PAM70"]
    matrix_choice = st.selectbox("Matrix", matrix_options, index=matrix_options.index("BLOSUM80"), key="matrix_select")
with col_param[2]:
    gap_open = st.number_input("Gap Open", value=-10.0, step=0.5)
with col_param[3]:
    gap_extend = st.number_input("Gap Extend", value=-0.5, step=0.1)
with col_param[4]:
    word_size = st.slider("Word Size", 2, 5, 3)

col_opt = st.columns(2)
with col_opt[0]:
    top_n = st.selectbox("Number of Top Hits", [5, 10, 20], index=1)   
with col_opt[1]:
    seg_filter = st.checkbox("SEG Filtering", value=True)
    comp_bias = st.checkbox("Composition-based Stats", value=True)

# Load and convert substitution matrix to pairwise2-compatible format
mat = substitution_matrices.load(matrix_choice)
scoring_matrix = { (a, b): mat[a][b] for a in mat.alphabet for b in mat.alphabet }

# Format alignment manually
def format_alignment(aln):
    seqA, seqB = aln.seqA, aln.seqB
    midline = ''.join(['|' if a == b else ' ' for a, b in zip(seqA, seqB)])
    return f"{seqA}\n{midline}\n{seqB}"

# --- Generate report text ---
def generate_blast_text(query_seq, e_value_thresh, matrix_choice, gap_open, gap_extend, word_size, results, df):
    report = StringIO()
    report.write("cNPDB BLAST Report\n")
    report.write("="*40 + "\n")
    report.write(f"Query Sequence:\n{query_seq}\n\n")
    report.write("Settings:\n")
    report.write(f"E-value Threshold: {e_value_thresh}\n")
    report.write(f"Matrix: {matrix_choice}\n")
    report.write(f"Gap Open Penalty: {gap_open}\n")
    report.write(f"Gap Extend Penalty: {gap_extend}\n")
    report.write(f"Word Size: {word_size}\n\n")

    for i, (score, e_val, db_seq, aln) in enumerate(results):
        report.write(f"Hit #{i+1} - Score: {score:.2f} | E-value: {e_val:.2e}\n")
        if aln:
            seqA, seqB = aln.seqA, aln.seqB
            midline = ''.join(['|' if a == b else ' ' for a, b in zip(seqA, seqB)])
            identity = sum(a == b for a, b in zip(seqA, seqB))
            aln_len = len(seqA)
            identity_pct = (identity / aln_len) * 100 if aln_len > 0 else 0
            report.write(f"{seqA}\n{midline}\n{seqB}\n")
            report.write(f"Identity: {identity_pct:.1f}% | Alignment Length: {aln_len}\n")
        else:
            report.write("No valid alignment available.\n")

        row = df[df["Sequence"] == db_seq]
        if not row.empty:
            row = row.iloc[0]
            report.write(f"Family: {row.get('Family', 'N/A')}\n")
            report.write(f"Organism: {row.get('OS', 'N/A')}\n")
            report.write(f"Tissue: {row.get('Tissue', 'N/A')}\n")
            report.write(f"Active Sequence: {row.get('Active Sequence', 'N/A')}\n")
        report.write("\n")

    return report.getvalue()

col1, col2, col3 = st.columns([1.6, 1, 1])
with col2:
    run = st.button("Run BLAST", type="primary")

# Run BLAST
if run:
    # Clean sequence if seg_filter
        seq_for_search = query_seq
        if seg_filter:
            seq_for_search = re.sub(r'[^A-Z]', '', seq_for_search)
            seq_for_search = re.sub(r'(.)\1{3,}', '', seq_for_search)

        results = []
        for i, db_seq in enumerate(df["Sequence"]):
            db_seq_clean = db_seq
            if seg_filter:
                db_seq_clean = re.sub(r'[^A-Z]', '', db_seq_clean)
                db_seq_clean = re.sub(r'(.)\1{3,}', '', db_seq_clean)

            if len(seq_for_search) < word_size or len(db_seq_clean) < word_size:
                continue

            try:
                aln = pairwise2.align.localds(seq_for_search, db_seq_clean, scoring_matrix, gap_open, gap_extend, one_alignment_only=True)
                score = aln[0].score if aln else 0
                e_val = 1e-5 * (100 - score / len(seq_for_search)) * (i + 1)
                if comp_bias:
                    bias_penalty = abs(len(seq_for_search) - len(db_seq_clean)) * 0.01
                    e_val += bias_penalty

                if e_val <= e_value_thresh:
                    results.append((score, e_val, db_seq, aln[0] if aln else None))
            except Exception:
                continue

        results = sorted(results, key=lambda x: -x[0])[:top_n]

        if not results:
            st.warning(f"No hits found with E-value ≤ {e_value_thresh}.")
        else:
            st.success(f"{len(results)} hit(s) found with E-value ≤ {e_value_thresh}")

            # Generate downloadable report text
            blast_txt = generate_blast_text(query_seq, e_value_thresh, matrix_choice, gap_open, gap_extend, word_size, results, df)

            col_dl1, col_dl2, col_dl3 = st.columns([1.35, 1, 1])
            with col_dl2:
                st.download_button(
                    label="Download BLAST Results",
                    data=blast_txt,
                    file_name="cNPDB_BLAST_results.txt",
                    mime="text/plain"
                )

            # Show hits
            for i, (score, e_val, db_seq, aln) in enumerate(results):
                st.subheader(f"Hit #{i+1}")

                if aln:
                    identical = sum(a == b for a, b in zip(aln.seqA, aln.seqB))
                    aln_length = len(aln.seqA)
                    identity_pct = (identical / aln_length) * 100 if aln_length > 0 else 0
                    st.text(f"Score: {score:.2f} | E-value: {e_val:.2e} | Identity: {identity_pct:.1f}% | Length: {aln_length}")
                    st.code(format_alignment(aln))
                else:
                    st.text(f"Score: {score:.2f} | E-value: {e_val:.2e}")
                    st.warning("No alignment available")

                row = df[df["Sequence"] == db_seq]
                if not row.empty:
                    row = row.iloc[0]
                    st.markdown(f"""
                        **Family**: {row.get('Family', 'N/A')}  
                        **Organism**: {row.get('OS', 'N/A')}  
                        **Tissue**: {row.get('Tissue', 'N/A')}  
                        **Active Sequence**: {row.get('Active Sequence', 'N/A')}
                    """)

    
st.markdown("""
<div style="text-align: center; font-size:14px; color:#2a2541;">
  <em>Last update: Jul 2025</em>
</div>
""", unsafe_allow_html=True)
