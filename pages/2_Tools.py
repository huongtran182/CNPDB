import streamlit as st
from sidebar import render_sidebar
from Bio.SeqUtils.ProtParam import ProteinAnalysis
import pandas as pd
from Bio import pairwise2
from io import StringIO

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
col_calc1, col_calc2, col_calc3 = st.columns([1.6, 1, 1])
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
    return pd.read_excel("Assets/20250613_cNPDB.xlsx", sheet_name="Sheet 1")

df = load_data()

def clean_sequence(seq):
    lines = seq.strip().splitlines()
    # Remove any line that starts with '>'
    clean_lines = [line.strip() for line in lines if not line.startswith(">")]
    return ''.join(clean_lines).upper()
    
def parse_fasta_sequences(text):
    """Parses multiple FASTA-format sequences into a list of dicts"""
    sequences = []
    buffer = []
    header = None

    for line in text.strip().splitlines():
        if line.startswith(">"):
            if header and buffer:
                sequences.append({"header": header, "sequence": ''.join(buffer).upper()})
                buffer = []
            header = line[1:].strip()
        else:
            buffer.append(line.strip())

    # Add last sequence
    if header and buffer:
        sequences.append({"header": header, "sequence": ''.join(buffer).upper()})
    elif buffer:  # No headers, just raw sequence
        sequences.append({"header": None, "sequence": ''.join(buffer).upper()})
    return sequences

raw_input = st.text_area("Input one or more peptide sequences (FASTA or raw):", value="", height=150)
parsed_queries = parse_fasta_sequences(raw_input)

target_seq = st.text_area("Input target sequence (optional):", value="", height=68)
target_seq = clean_sequence(target_seq)

align_to_db = not target_seq.strip()
if align_to_db:
    st.info("You are aligning your input sequences against the cNPDB database.")
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

col1, col2, col3 = st.columns([1.5, 1, 1])
with col2:
    run_clicked = st.button("Run Alignment", type="primary")

# Run Alignment Button
if run_clicked:
    if not parsed_queries:
        st.error("❌ Please input at least one valid peptide sequence.")
    elif not target_seq.strip() and not align_to_db:
        st.error("❌ Please input a target sequence or choose to align against the database.")
    else:
        all_alignments = []

        for item in parsed_queries:
            seq_label = item["header"] or "Unnamed"
            seq = item["sequence"]

            st.markdown(f"<h4 style='color:#54278f;'>🔍 Query: {seq_label}</h4>", unsafe_allow_html=True)

            if target_seq.strip():
                # Align to provided sequence
                try:
                    aln = (
                        pairwise2.align.globalms(seq, target_seq, match_score, mismatch_score, gap_open, gap_extend)
                        if alignment_type == "global" else
                        pairwise2.align.localms(seq, target_seq, match_score, mismatch_score, gap_open, gap_extend)
                    )
                    if aln:
                        st.success(f"Top alignment result (score: {aln[0].score:.2f})")
                        st.code(custom_format_alignment(aln[0]))
                    else:
                        st.warning("No valid alignment.")
                except Exception as e:
                    st.error(f"❌ Alignment error: {e}")
            else:
                # Align to database
                results = []
                for db_seq in df["Sequence"]:
                    try:
                        aln = (
                            pairwise2.align.globalms(seq, db_seq, match_score, mismatch_score, gap_open, gap_extend, one_alignment_only=True)
                            if alignment_type == "global" else
                            pairwise2.align.localms(seq, db_seq, match_score, mismatch_score, gap_open, gap_extend, one_alignment_only=True)
                        )
                        score = aln[0].score if aln else 0
                        results.append((score, db_seq, aln[0] if aln else None))
                    except Exception:
                        continue

                top_hits = sorted(results, key=lambda x: -x[0])[:10]

                for i, (score, db_seq, aln) in enumerate(top_hits):
                    st.markdown(f"**Hit #{i+1} — Score: {score:.2f}**")
                    if aln:
                        st.code(custom_format_alignment(aln))
                    match_row = df[df["Sequence"] == db_seq].iloc[0] if not df[df["Sequence"] == db_seq].empty else None
                    if match_row is not None:
                        st.markdown(f"""
                            <div style='font-size:15px; margin-bottom:20px;'>
                                <strong>Family:</strong> {match_row.get("Family", "N/A")}<br>
                                <strong>Organism:</strong> {match_row.get("OS", "N/A")}<br>
                                <strong>Tissue:</strong> {match_row.get("Tissue", "N/A")}<br>
                                <strong>Active Sequence:</strong> {match_row.get("Active Sequence", "N/A")}
                            </div>
                        """, unsafe_allow_html=True)
                # Generate download content
                alignment_txt = generate_alignment_text(
                    seq, alignment_type, match_score, mismatch_score, gap_open, gap_extend, top_hits, df
                )
                st.download_button(
                    label=f"Download Results: {seq_label}",
                    data=alignment_txt,
                    file_name=f"alignment_{seq_label}.txt",
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

st.markdown("""
<div style="text-align: center; font-size:14px; color:#2a2541;">
  <em>Last update: Jul 2025</em>
</div>
""", unsafe_allow_html=True)
