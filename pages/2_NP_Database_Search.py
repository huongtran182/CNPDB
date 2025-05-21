import streamlit as st
from sidebar import render_sidebar
import pandas as pd
import os
from PIL import Image
import base64

st.set_page_config(
    page_title="NP Database search",
    layout="wide",
    initial_sidebar_state="expanded"
)

render_sidebar()

st.markdown(
    """
    <style>
      /* Make first column auto-size to its content */
      .peptide-details table {
        width: 100%;
        table-layout: auto;
        border-collapse: separate !important;
        border-spacing: 0 3px !important;
        margin-top:10px;
      }
      .peptide-details td:first-child {
        white-space: nowrap;
        width: 1%;
        color: white;
      }
      .peptide-details td:last-child {
        background-color: white;
      }
    </style>
    """,
    unsafe_allow_html=True,
)

def img_html(path):
    """Return a base64 <img> tag filling 100% width of its container."""   
    if not os.path.exists(path):
        return "<div style='color:#999; padding:20px;'>No image found</div>"
    ext = os.path.splitext(path)[1].lower().replace(".", "")
    mime = f"image/{'jpeg' if ext in ('jpg','jpeg') else ext}"
    data = base64.b64encode(open(path, "rb").read()).decode()
    return f"<img src='data:{mime};base64,{data}' style='width:100%; height:auto;'/>"

# Helper to blank out NaNs if there is no value in the cell of the column of excel file
def disp(val):
    """Return an empty string if val is NaN/None, else val itself."""
    if pd.isna(val) or val is None:
        return ""
    return val

def display_peptide_details(row: pd.Series):
    seq        = row["Seq"]
    cnpd_id    = row["CNPD ID"]

# Prepare all content as HTML strings first
    # 1) Metadata table
    gravy = row.get("GRAVY")
    gravy_str = f"{gravy:.2f}" if pd.notna(gravy) else ""

    metadata_html = f"""
    <div class="peptide-details">
        <table>
            <tr>
            <td style="background-color:#6a51a3; color:white; padding:4px 8px; line-height:1.2; border-radius: 10px 0 0 10px; ">CNPD ID</td>
            <td style="background-color:white; border:1px solid #6A0DAD; padding:4px 8px; line-height:1.2; border-radius: 0 10px 10px 0; ">{disp(row['CNPD ID'])}</td>
            </tr>
            <tr>
            <td style="background-color:#6a51a3; color:white; padding:4px 8px; line-height:1.2; border-radius: 10px 0 0 10px; ">Family</td>
            <td style="background-color:white; border:1px solid #6A0DAD; padding:4px 8px; line-height:1.2; border-radius: 0 10px 10px 0; ">{disp(row['Family'])}</td>
            </tr>
            <tr>
            <td style="background-color:#6a51a3; color:white; padding:4px 8px; line-height:1.2; border-radius: 10px 0 0 10px; ">Organisms</td>
            <td style="background-color:white; border:1px solid #6A0DAD; padding:4px 8px; line-height:1.2;; border-radius: 0 10px 10px 0; ">{disp(row['OS'])}</td>
            </tr>
            <tr>
            <td style="background-color:#6a51a3; color:white; padding:4px 8px; line-height:1.2; border-radius: 10px 0 0 10px; ">Tissue</td>
            <td style="background-color:white; border:1px solid #6A0DAD; padding:4px 8px; line-height:1.2; border-radius: 0 10px 10px 0; ">{disp(row['Tissue'])}</td>
            </tr>
            <tr>
            <td style="background-color:#6a51a3; color:white; padding:4px 8px; line-height:1.2; border-radius: 10px 0 0 10px; ">Existence</td>
            <td style="background-color:white; border:1px solid #6A0DAD; padding:4px 8px; line-height:1.2; border-radius: 0 10px 10px 0; ">{disp(row['Existence'])}</td>
            </tr>
            <tr>
            <td style="background-color:#6a51a3; color:white; padding:4px 8px; line-height:1.2; border-radius: 10px 0 0 10px; ">Monoisotopic Mass</td>
            <td style="background-color:white; border:1px solid #6A0DAD; padding:4px 8px; line-height:1.2; border-radius: 0 10px 10px 0; ">{disp(row['Monoisotopic Mass'])}</td>
            </tr>
            <tr>
            <td style="background-color:#6a51a3; color:white; padding:4px 8px; line-height:1.2; border-radius: 10px 0 0 10px; ">Length (a.a.)</td>
            <td style="background-color:white; border:1px solid #6A0DAD; padding:4px 8px; line-height:1.2; border-radius: 0 10px 10px 0; ">{disp(row['Length'])}</td>
            </tr>
            <tr>
            <td style="background-color:#6a51a3; color:white; padding:4px 8px; line-height:1.2; border-radius: 10px 0 0 10px; ">GRAVY Score</td>
            <td style="background-color:white; border:1px solid #6A0DAD; padding:4px 8px; line-height:1.2; border-radius: 0 10px 10px 0; ">{gravy_str}</td>
            </tr>
            <tr>
            <td style="background-color:#6a51a3; color:white; padding:4px 8px; line-height:1.2; border-radius: 10px 0 0 10px; ">% Hydrophobic Residues</td>
            <td style="background-color:white; border:1px solid #6A0DAD; padding:4px 8px; line-height:1.2; border-radius: 0 10px 10px 0; ">{disp(row['% Hydrophobic Residue (%)'])}</td>
            </tr>
            <tr>
            <td style="background-color:#6a51a3; color:white; padding:4px 8px; line-height:1.2; border-radius: 10px 0 0 10px; ">Half-life (Min)</td>
            <td style="background-color:white; border:1px solid #6A0DAD; padding:4px 8px; line-height:1.2; border-radius: 0 10px 10px 0; ">{disp(row['Predicted Half Life (Min)'])}</td>
            </tr>
            <tr>
            <td style="background-color:#6a51a3; color:white; padding:4px 8px; line-height:1.2; border-radius: 10px 0 0 10px; ">PTMs</td>
            <td style="background-color:white; border:1px solid #6A0DAD; padding:4px 8px; line-height:1.2; border-radius: 0 10px 10px 0; ">{disp(row['PTMs'])}</td>
            </tr>
        </table>
    </div>
    """

    # 2) 3D Structure
    structure_html = f"""
    <div style="
          color: #6a51a3;
          font-size: 16px;
          font-weight: bold;
          margin-top: 10px;
          text-align: center;
        ">
          3D Structure
        </div>
        <div style="
          border: 2px dashed #6a51a3;
          padding: 10px;
          text-align: center;
          margin-top:5px;
        ">
          {img_html(f"Assets/3D Structure/3D cNP{cnpd_id}.jpg")}
        </div>
    """
    
    # MSI Tissue 1
    tissue_1 = disp(row.get("MSI Tissue 1"))
    image_path_1 = f"Assets/MSImaging/MSI cNP{cnpd_id} 1.png"
    if os.path.exists(image_path_1):
        msi_html_1 = f"""
        <div style="
              color: #6a51a3;
              font-size: 16px;
              font-weight: bold;
              margin-top: 10px;
              text-align: center;
        ">
        MS Imaging – {tissue_1}
        </div>
        <div style="
            border: 2px dashed #6a51a3;
            padding: 10px;
            text-align: center;
            margin-top:5px;
        ">
        {img_html(image_path_1)}
        </div>
        """
    else:
        msi_html_1_unavailable = f"""
        <div style="
            color: #6a51a3;
            font-size: 16px;
            font-weight: bold;
            margin-top: 10px;
            text-align: center;
        ">
        MSImaging data is not available
        </div>
        """

    # MSI Tissue 2
    tissue_2 = disp(row.get("MSI Tissue 2"))
    image_path_2 = f"Assets/MSImaging/MSI cNP{cnpd_id} 2.png"
    if os.path.exists(image_path_2):
        msi_html_2 = f"""
        <div style="
              color: #6a51a3;
              font-size: 16px;
              font-weight: bold;
              margin-top: 10px;
              text-align: center;
            ">
            MS Imaging – {tissue_2}
            </div>
            <div style="
              border: 2px dashed #6a51a3;
              padding: 10px;
              text-align: center;
              margin-top:5px;
            ">
            {img_html(image_path_2)}
            </div>
        """
        
    # MSI Tissue 3
    tissue_3 = disp(row.get("MSI Tissue 3"))
    image_path_3 = f"Assets/MSImaging/MSI cNP{cnpd_id} 3.png"
    if os.path.exists(image_path_3):
        msi_html_3 = f"""
        <div style="
              color: #6a51a3;
              font-size: 16px;
              font-weight: bold;
              margin-top: 10px;
              text-align: center;
            ">
            MS Imaging – {tissue_3}
            </div>
            <div style="
              border: 2px dashed #6a51a3;
              padding: 10px;
              text-align: center;
              margin-top:5px;
            ">
            {img_html(image_path_3)}
            </div>
        """

 # Build the COMPLETE box as one HTML block
    full_html = f"""
    <div style="
      position: relative;
      background-color: #efedf5;
      border-radius: 20px;
      padding: 60px 20px 20px;
      margin: 80px 0 30px;
      display: flex;  /* Use flexbox for layout */
      gap: 20px; /* Space between columns */
    ">
      <!-- Header -->
      <div style="
        position: absolute;
        top: 0; left: 50%;
        transform: translate(-50%, -50%);
        width: 66%;
        background-color: #54278f;
        color: white;
        padding: 10px;
        border-radius: 5px;
        text-align: center;
        font-weight: bold;
      ">
        {seq}
      </div>
      
      <!-- Three-column content -->
      <div style="flex:4; padding:0 10px;">
        {metadata_html}
      </div>
      <div style="flex:3; padding:0 10px;">
        {structure_html}
      </div>
      <div style="flex:3; padding:0 10px; display: flex; flex-direction: column; gap: 0px;">
        {msi_html_1}
        {msi_html_1_unavailable}
        {msi_html_2}
        {msi_html_3}
      </div>
    </div>
    """
 # Render everything at once
    st.markdown(full_html, unsafe_allow_html=True)    
    
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
   /* Style every Streamlit vertical block with your lavender‐gray background */
      div[data-testid="stVerticalBlock"]:nth-of-type(3) {
        background-color: #efedf5 !important;
        padding: 20px !important;
        border-radius: 10px !important;
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

  /* 1) Make slider & text-input labels purple & bold */
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
    mono_mass_range  = st.slider("Monoisotopic mass (m/z)", 300.0, 2000.0, (300.0, 2000.0))
    length_range     = st.slider("Length (aa)", 3, 100, (3, 100))
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

# 1) Inject opening container div
st.markdown(
    "<div class='results-container'>",
    unsafe_allow_html=True
)

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
                <div style='border:1px solid #6A0DAD; padding:10px; margin:0px 10px 20px 0; border-radius:10px;'>
                    <div style='font-weight:bold; background-color:#6a51a3; color:white; padding:10px;'>
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
       left_space, right_button = st.columns([3,1])
       with right_button:
           view_clicked = st.button("View details", type="primary")
    with b2:
        fasta_str = ""
        for idx in selected_indices:
            r = df_filtered.loc[idx]
            fasta_str += f">{r['ID']}\n{r['Seq']}\n"
        st.download_button(
            "Download FASTA File",
            data=fasta_str,
            file_name="peptides.fasta",
            mime="text/plain",
            type="primary"
        )
else:
    st.info("No peptides matched the search criteria.")

# —— NOW at the top level, outside of any columns ——  
if 'view_clicked' in locals() and view_clicked:
    for idx in selected_indices:
        display_peptide_details(df_filtered.loc[idx])
    
# 5) Close container div
st.markdown(
    "</div>",
    unsafe_allow_html=True
)




# Footer
st.markdown("""
<div style="text-align: center; font-size:14px; color:#2a2541;">
  <em>Last update: Jul 2025</em>
</div>
""", unsafe_allow_html=True)
