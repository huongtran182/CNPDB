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
 /* 1) Centered title with10px top margin */
  h2.custom-title {
    text-align: center !important;
    margin-top: 10px !important;
    color: #29004c;
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

# Load data
df = pd.read_excel("Assets/CNPD_Li.xlsx", skiprows=1)

# Parse 'CNPD ID' for embedded info

def parse_metadata(row):
    metadata = row['id'] if pd.notna(row['id']) else ""
    def extract(pattern):
        match = re.search(pattern, metadata)
        return match.group(1) if match else None

    return pd.Series({
        'Family': extract(r'Family=([^\s]+)'),
        'OS': extract(r'OS=([^\s]+)'),
        'Existence': extract(r'Existence=([^\s]+)'),
        'Monoisotopic mass': float(extract(r'mz=([^\s]+)')) if extract(r'mz=([^\s]+)') else None,
        'Tissue': extract(r'Tissue=([^\s]+)'),
    })

parsed = df.apply(parse_metadata, axis=1)
df = pd.concat([df, parsed], axis=1)

# Search inputs
col1, col2 = st.columns(2)

with col1:
    peptide_input = st.text_input("Peptide Sequence", placeholder="Separate by space, e.g. FDAFTTGFGHN")
    family_selected = st.multiselect("Family", options=df['Family'].dropna().unique())
    tissue_selected = st.multiselect("Tissue", options=df['Tissue'].dropna().unique())
    existence_selected = st.multiselect("Existence", options=df['Existence'].dropna().unique())

with col2:
    pubmed_input = st.text_input("PubMED ID", placeholder="Separate by space, e.g. 19007832")
    organisms_selected = st.multiselect("Organisms", options=df['OS'].dropna().unique())
    mono_mass_range = st.slider("Monoisotopic mass (m/z)", 300.0, 1600.0, (300.0, 1600.0))

# Filtering
df_filtered = df.copy()

if peptide_input:
    for pep in peptide_input.split():
        df_filtered = df_filtered[df_filtered['Seq'].str.contains(pep, na=False)]

if pubmed_input:
    for pmid in pubmed_input.split():
        df_filtered = df_filtered[df_filtered['PubMed ID'].astype(str).str.contains(pmid, na=False)]

if family_selected:
    df_filtered = df_filtered[df_filtered['Family'].isin(family_selected)]

if organisms_selected:
    df_filtered = df_filtered[df_filtered['OS'].isin(organisms_selected)]

if tissue_selected:
    df_filtered = df_filtered[df_filtered['Tissue'].isin(tissue_selected)]

if existence_selected:
    df_filtered = df_filtered[df_filtered['Existence'].isin(existence_selected)]

# Apply numeric filters
df_filtered = df_filtered[df_filtered['Monoisotopic mass'].between(*mono_mass_range)]

# Display results
st.markdown("## Search Results")
st.write(f"Hit: {len(df_filtered)} peptides")

selected_indices = []

if len(df_filtered) > 0:
    check_all = st.checkbox("Check/Uncheck All")
    cols = st.columns(2)

    for i, (idx, row) in enumerate(df_filtered.iterrows()):
        with cols[i % 2]:
            checked = st.checkbox("", key=f"check_{idx}", value=check_all)
            if checked:
                selected_indices.append(idx)
            st.markdown(f"""
                <div style='border:1px solid #6A0DAD; padding:10px; margin:5px; border-radius:10px;'>
                    <div style='font-weight:bold; background-color:#4B0082; color:white; padding:5px;'>
                        {row['Seq']}
                    </div>
                    <div style='padding:5px;'>
                        Family: {row['Family']}<br>
                        OS: {row['OS']}
                    </div>
                </div>
            """, unsafe_allow_html=True)

    st.markdown("### Actions")
    col_a, col_b = st.columns(2)
    with col_a:
        if st.button("View details"):
            st.dataframe(df_filtered.loc[selected_indices])

    with col_b:
        if st.button("Download Fasta File"):
            fasta_str = ""
            for idx in selected_indices:
                row = df_filtered.loc[idx]
                fasta_str += f">{row['CNPD ID']}\n{row['Seq']}\n"
            st.download_button("Download FASTA", data=fasta_str, file_name="peptides.fasta", mime="text/plain")
else:
    st.info("No peptides matched the search criteria.")

st.markdown("""
<div style="text-align: center; font-size:14px; color:#2a2541;">
  <em>Last update: Jul 2025</em>
</div>
""", unsafe_allow_html=True)
