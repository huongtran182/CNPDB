import streamlit as st
from sidebar import render_sidebar
import pandas as pd

st.set_page_config(
    page_title="NP Database search",
    layout="wide",
    initial_sidebar_state="expanded"
)

render_sidebar()

st.markdown("""
    <style>
    html, body, [class*="css"]  {
        font-family: 'Arial', sans-serif;
        font-size: 15px;
        color: #333;
    }
    h2.title {
        text-align: center;
        color: #4B0082;
    }
    .card {
        border: 1px solid #6A0DAD;
        border-radius: 10px;
        padding: 10px;
        margin-bottom: 10px;
        background-color: #f8f6fc;
    }
    .card-header {
        font-weight: bold;
        background-color: #4B0082;
        color: white;
        padding: 5px;
        border-radius: 6px;
    }
    </style>
""", unsafe_allow_html=True)

# --- Centered, spaced title ---
st.markdown(
    '<h2 class="custom-title">'
    'NEUROPEPTIDE SEARCH ENGINE'
    '</h2>',
    unsafe_allow_html=True
)

# --- Load Data ---
# --- Load Data ---
DF_PATH = "Assets/CNPD_Li.xlsx"
df = pd.read_excel(DF_PATH, sheet_name="Example")

# Coerce numeric
numeric_cols = ['Monoisotopic Mass', 'Length', 'GRAVY', '% Hydrophobic Residue (%)', 'Predicted Half Life (Min)']
for col in numeric_cols:
    df[col] = pd.to_numeric(df[col], errors='coerce')

# --- Sidebar Filters ---
st.sidebar.header("🔍 Filters")

peptide_input = st.sidebar.text_input("Peptide Sequence", placeholder="FDAFTTGFGHN NFDEIDRSGFGFN")

mono_mass_range = st.sidebar.slider("Monoisotopic Mass (m/z)", 300.0, 1600.0, (300.0, 1600.0))
length_range = st.sidebar.slider("Length (aa)", 3, 100, (3, 50))
gravy_range = st.sidebar.slider("GRAVY Score", -5.0, 5.0, (-5.0, 5.0))
hydro_range = st.sidebar.slider("% Hydrophobic Residue", 0, 100, (0, 100))
half_life_range = st.sidebar.slider("Predicted Half-life (min)", 0, 120, (0, 60))

family_selected = st.sidebar.multiselect("Family", sorted(df['Family'].dropna().unique()))
tissue_selected = st.sidebar.multiselect("Tissue", sorted(df['Tissue'].dropna().unique()))
existence_selected = st.sidebar.multiselect("Existence", sorted(df['Existence'].dropna().unique()))
organisms_selected = st.sidebar.multiselect("Organism", sorted(df['OS'].dropna().unique()))

# --- Filter Data ---
df_filtered = df.copy()

if peptide_input:
    for pep in peptide_input.split():
        df_filtered = df_filtered[df_filtered['Seq'].str.contains(pep, na=False)]

if family_selected:
    df_filtered = df_filtered[df_filtered['Family'].isin(family_selected)]
if tissue_selected:
    df_filtered = df_filtered[df_filtered['Tissue'].isin(tissue_selected)]
if existence_selected:
    df_filtered = df_filtered[df_filtered['Existence'].isin(existence_selected)]
if organisms_selected:
    df_filtered = df_filtered[df_filtered['OS'].isin(organisms_selected)]

# Numeric filters
df_filtered = df_filtered[df_filtered['Monoisotopic Mass'].between(*mono_mass_range)]
df_filtered = df_filtered[df_filtered['Length'].between(*length_range)]
df_filtered = df_filtered[df_filtered['GRAVY'].between(*gravy_range)]
df_filtered = df_filtered[df_filtered['% Hydrophobic Residue (%)'].between(*hydro_range)]
df_filtered = df_filtered[df_filtered['Predicted Half Life (Min)'].between(*half_life_range)]

# --- Results ---
st.subheader("🔬 Search Results")
st.write(f"{len(df_filtered)} hit(s)")

selected_indices = []

if len(df_filtered) > 0:
    for idx, row in df_filtered.iterrows():
        checked = st.checkbox(f"Select {row['Seq']}", key=f"chk_{idx}")
        if checked:
            selected_indices.append(idx)

        st.markdown(f"""
        <div class='card'>
            <div class='card-header'>{row['Seq']}</div>
            <div>
                <b>Family:</b> {row['Family']}<br>
                <b>Organism:</b> {row['OS']}<br>
                <b>Length:</b> {row['Length']}, <b>Mass:</b> {row['Monoisotopic Mass']:.2f}
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    col1, col2 = st.columns(2)

    with col1:
        if st.button("📋 View Selected"):
            st.dataframe(df_filtered.loc[selected_indices])

    with col2:
        if st.button("📥 Download FASTA"):
            fasta_str = ""
            for idx in selected_indices:
                row = df_filtered.loc[idx]
                fasta_str += f">{row['ID']}\n{row['Seq']}\n"
            st.download_button("Download .fasta", data=fasta_str, file_name="peptides.fasta", mime="text/plain")
else:
    st.info("No peptides matched the filters.")
# Footer
st.markdown("""
<div style="text-align: center; font-size:14px; color:#2a2541;">
  <em>Last update: Jul 2025</em>
</div>
""", unsafe_allow_html=True)
