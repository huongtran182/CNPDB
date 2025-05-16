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
/* Centered title */
 h2.custom-title {
    text-align: center !important;
    margin-top: 10px !important;
    color: #29004c;
 }
 /* Container background */
div[data-testid="stColumns"] > div[data-testid="stColumn"] {
    background-color: #efedf5 !important;
    padding: 20px !important;
    border-radius: 10px !important;
 }
  .results-container {
    background-color: #efedf5;
    padding: 20px;
    border-radius: 10px;
    margin-bottom: 20px;
      }
 /* Section titles */
  .section-title {
    color: #6a51a3;
    font-size: 16px;
    font-weight: bold;
    margin-top: 10px;
  }
  /* Checkbox accent color */
  input[type="checkbox"] { accent-color: #6a51a3; }

    /* —— SLIDER TRACK & THUMB —— */
  /* The BaseWeb slider bar */
  div[data-testid="stSlider"]
    [data-baseweb="slider"] .base-slider-bar {
      background-color: #6a51a3 !important;
  }
  /* The BaseWeb slider handle */
  div[data-testid="stSlider"]
    [data-baseweb="slider"] .base-slider-handle {
      background-color: #6a51a3 !important;
      border: none !important;
  }

  /* —— BUTTONS —— */
  div[data-testid="stButton"] > button {
    background-color: #6a51a3 !important;
    color: white !important;
  }

  /* 1) Make slider & text-input labels purple & bold */
  [data-testid="stSlider"] label,
  [data-testid="stTextInput"] label {
    color: #6a51a3 !important;
    font-weight: bold !important;
  }

  /* 2) Wrap both filter & main columns in a purple-background box */
  div[data-testid="stColumns"] > div[data-testid="stColumn"] {
    background-color: #efedf5 !important;
    padding: 20px !important;
    border-radius: 10px !important;
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

# Begin styled container
st.markdown('<div class="main-search-container">', unsafe_allow_html=True)

# Load data
DF_PATH = "Assets/CNPD_Li.xlsx"
df = pd.read_excel(DF_PATH, sheet_name="Example")

# Ensure numeric columns are numeric
numeric_cols = ['Monoisotopic Mass', 'Length', 'GRAVY', '% Hydrophobic Residue (%)', 'Predicted Half Life (Min)']
for col in numeric_cols:
    df[col] = pd.to_numeric(df[col], errors='coerce')

# Layout: filters (1/4) and inputs (3/4)
col_filter, col_main = st.columns([1, 3])

with col_filter:
    mono_mass_range  = st.slider("Monoisotopic mass (m/z)", 300.0, 1600.0, (300.0, 1600.0))
    length_range     = st.slider("Length (aa)", 3, 100, (3, 50))
    gravy_range      = st.slider("GRAVY Score", -5.0, 5.0, (-5.0, 5.0))
    hydro_range      = st.slider("% Hydrophobic Residue", 0, 100, (0, 100))
    half_life_range  = st.slider("Predicted Half-life (min)", 0, 120, (0, 60))

with col_main:
    peptide_input = st.text_input(
        "Peptide Sequence",
        placeholder="Separate by space, e.g. FDAFTTGFGHN NFDEIDRSGFGFN"
    )

    # Family
    st.markdown('<div class="section-title">Family</div>', unsafe_allow_html=True)
    family_opts     = sorted(df['Family'].dropna().unique())
    family_selected = [opt for opt in family_opts if st.checkbox(opt, key=f"fam_{opt}")]

    # Tissue
    st.markdown('<div class="section-title">Tissue</div>', unsafe_allow_html=True)
    tissue_opts     = sorted(df['Tissue'].dropna().unique())
    tissue_selected = [opt for opt in tissue_opts if st.checkbox(opt, key=f"tiss_{opt}")]

    # Existence
    st.markdown('<div class="section-title">Existence</div>', unsafe_allow_html=True)
    exist_opts      = sorted(df['Existence'].dropna().unique())
    existence_selected = [opt for opt in exist_opts if st.checkbox(opt, key=f"ex_{opt}")]

    # Organisms
    st.markdown('<div class="section-title">Organisms</div>', unsafe_allow_html=True)
    org_opts        = sorted(df['OS'].dropna().unique())
    organisms_selected = [opt for opt in org_opts if st.checkbox(opt, key=f"org_{opt}")]

# Filtering logic
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

# Numeric filtering
df_filtered = df_filtered[df_filtered['Monoisotopic Mass'].between(*mono_mass_range)]
df_filtered = df_filtered[df_filtered['Length'].between(*length_range)]
df_filtered = df_filtered[df_filtered['GRAVY'].between(*gravy_range)]
df_filtered = df_filtered[df_filtered['% Hydrophobic Residue (%)'].between(*hydro_range)]
df_filtered = df_filtered[df_filtered['Predicted Half Life (Min)'].between(*half_life_range)]

# Display results
st.markdown(
    '<h2 class="custom-title">'
    'SEARCH RESULTS'
    '</h2>',
    unsafe_allow_html=True
)

# 2) Open your container div
st.markdown("<div class='results-container'>", unsafe_allow_html=True)

# 3) Header row: left = checkbox, right = hit count
col1, col2 = st.columns([1,1])
with col1:
    check_all = st.checkbox("Check/Uncheck All")
with col2:
    # align right
    st.markdown(f"<div style='text-align: right;'>Hit: {len(df_filtered)} peptides</div>", unsafe_allow_html=True)

# 4) Peptide cards in three columns
if len(df_filtered) > 0:
    cols = st.columns(3)
    selected_indices = []
    for i, (idx, row) in enumerate(df_filtered.iterrows()):
        with cols[i % 3]:
            checked = st.checkbox("", key=f"check_{idx}", value=check_all)
            if checked:
                selected_indices.append(idx)
            st.markdown(f"""
                <div style='border:1px solid #6A0DAD; padding:10px; margin:10px; border-radius:10px;'>
                    <div style='font-weight:bold; background-color:#6A0DAD; color:white; padding:5px;'>
                        {row['Seq']}
                    </div>
                    <div style='padding:5px;'>
                        Family: {row['Family']}<br>
                        OS: {row['OS']}
                    </div>
                </div>
            """, unsafe_allow_html=True)

# 5) Centered buttons row
    b1, b2 = st.columns([1,1])
    with b1:
        if st.button("View details"):
            st.dataframe(df_filtered.loc[selected_indices])
    with b2:
        if st.button("Download Fasta File"):
            fasta_str = ""
            for idx in selected_indices:
                row = df_filtered.loc[idx]
                fasta_str += f">{row['ID']}\n{row['Seq']}\n"
            st.download_button("Download FASTA", data=fasta_str, file_name="peptides.fasta", mime="text/plain")

else:
    st.info("No peptides matched the search criteria.")
    
# End styled container
st.markdown("</div>", unsafe_allow_html=True)

# Footer
st.markdown("""
<div style="text-align: center; font-size:14px; color:#2a2541;">
  <em>Last update: Jul 2025</em>
</div>
""", unsafe_allow_html=True)
