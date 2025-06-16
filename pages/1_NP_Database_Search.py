import streamlit as st
from sidebar import render_sidebar
import pandas as pd
import os
from PIL import Image
import base64
import re
import py3Dmol
import streamlit.components.v1 as components
from io import StringIO

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

def show_3d_structure(cif_path):
    """Render interactive 3D structure from CIF file using py3Dmol"""
    try:
        with open(cif_path, 'r') as f:
            cif_data = f.read()
        
        view = py3Dmol.view(width=400, height=300)
        view.addModel(cif_data, 'cif')
        view.setStyle({'stick': {}})
        view.zoomTo()
        view.spin()
        
        html = view._make_html()
        components.html(html, height=350)
        
    except FileNotFoundError:
        st.markdown("<div style='color:#999; padding:20px;'>3D structure not available</div>", unsafe_allow_html=True)
    except Exception as e:
        st.error(f"Error loading 3D structure: {str(e)}")

def display_peptide_details(row: pd.Series):
    active_seq = row["Active Sequence"]
    cNPDB_id    = row["cNPDB ID"]

# Prepare all content as HTML strings first
    # 1) Metadata table
    gravy = row.get("GRAVY")
    gravy_str = f"{gravy:.2f}" if pd.notna(gravy) else ""

    metadata_html = f"""
    <div class="peptide-details">
        <table>
            <tr>
            <td style="background-color:#6a51a3; color:white; padding:4px 8px; line-height:1.2; border-radius: 10px 0 0 10px; ">cNPDB ID</td>
            <td style="background-color:white; border:1px solid #6A0DAD; padding:4px 8px; line-height:1.2; border-radius: 0 10px 10px 0; ">{disp(row['cNPDB ID'])}</td>
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
            <td style="background-color:#6a51a3; color:white; padding:4px 8px; line-height:1.2; border-radius: 10px 0 0 10px; ">Instability Index </td>
            <td style="background-color:white; border:1px solid #6A0DAD; padding:4px 8px; line-height:1.2; border-radius: 0 10px 10px 0; ">{disp(row['Instability Index'])}</td>
            </tr>
            <tr>
            <td style="background-color:#6a51a3; color:white; padding:4px 8px; line-height:1.2; border-radius: 10px 0 0 10px; ">PTM</td>
            <td style="background-color:white; border:1px solid #6A0DAD; padding:4px 8px; line-height:1.2; border-radius: 0 10px 10px 0; ">{disp(row['PTM'])}</td>
            </tr>
        </table>
    </div>
    """
    # 2) 3D Structure - Interactive Viewer
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
    """
    
    # Render the HTML container
    st.markdown(structure_html, unsafe_allow_html=True)
    
    # Add the interactive viewer
    cif_path = f"Assets/3D Structure/3D cNP{cNPDB_id}.cif"
    show_3d_structure(cif_path)
    
    # Close the div
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Prepare MSI HTML blocks
    tissue_1 = disp(row.get("MSI Tissue 1"))
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
          {img_html(f"Assets/MSImaging/MSI cNP{cNPDB_id}.png")}
        </div>
    """
    tissue_2 = disp(row.get("MSI Tissue 2"))
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
          {img_html(f"/MSImaging/MSI cNP{cNPDB_id} 2.png")}
        </div>
    """
    
    tissue_3 = disp(row.get("MSI Tissue 3"))
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
          {img_html(f"/MSImaging/MSI cNP{cNPDB_id} 3.png")}
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
        {active_seq}
      </div>
      
      <div style="flex:4; padding:0 10px;">
        {metadata_html}
      </div>
      <div style="flex:3; padding:0 10px;">
        {structure_html}
      </div>
      <div style="flex:3; padding:0 10px; display: flex; flex-direction: column; gap: 0px;">
        {msi_html_1}
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
 
 /* Section titles */
  .section-title {
    color: #6a51a3;
    font-size: 16px;
    font-weight: bold;
  }
  /* Checkbox accent color */
  input[type="checkbox"] { accent-color: #6a51a3; }
  
    /* Adjusting space for sliders in col_filter */
  .stSlider { 
      margin-top: 5px;
      margin-bottom: 12px;
   }
   
   /* Custom columns layout: 20px gap between filter and main */
    .custom-col-container {
        display: flex;
        gap: 20px;
    }
    
    /* Force equal height by filling both columns */
    .fill-height {
        flex: 1;
    }

    /* Reduce space between checkboxes */
div.stCheckbox {
    margin-top: -5px;  /* adjust to your preference */
    margin-bottom: 0px;
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
DF_PATH = "Assets/20250613_cNPDB.xlsx"
df = pd.read_excel(DF_PATH)

# Ensure numeric columns are numeric
numeric_cols = ['Monoisotopic Mass', 'Length', 'GRAVY', '% Hydrophobic Residue (%)', 'Instability Index Value']
for col in numeric_cols:
    df[col] = pd.to_numeric(df[col], errors='coerce')

# Helper function to extract unique clean items from multi-value cells
def extract_unique_values(series):
    return sorted(set(
        item.strip()
        for entry in series.dropna()
        for item in re.split(r'[;,]', str(entry))
        if item.strip()
    ))

# Create two columns with a 20px gap using Streamlit's built-in layout
col_filter, col_main = st.columns([1, 3], gap= "large")

# Custom container with manual gap
st.markdown('<div class="custom-col-container">', unsafe_allow_html=True)

# Filter column (1/4 width)
with col_filter:
    st.markdown('<div class="fill-height">', unsafe_allow_html=True)

    st.markdown('<div class="section-title">Monoisotopic mass (Da)</div>', unsafe_allow_html=True)
    mono_mass_range = st.slider("", 200.0, 14000.0, (200.0, 14000.0), label_visibility="collapsed")

    st.markdown('<div class="section-title">Length (amino acids)</div>', unsafe_allow_html=True)
    length_range = st.slider("", 3, 130, (3, 130), label_visibility="collapsed")

    st.markdown('<div class="section-title">GRAVY Score</div>', unsafe_allow_html=True)
    gravy_range = st.slider("", -5.0, 5.0, (-5.0, 5.0), label_visibility="collapsed")

    st.markdown('<div class="section-title">% Hydrophobic Residue</div>', unsafe_allow_html=True)
    hydro_range = st.slider("", 0, 100, (0, 100), label_visibility="collapsed")

    st.markdown('<div class="section-title">Instability Index</div>', unsafe_allow_html=True)
    instability_index_value = st.slider("", -100, 250, (-100, 250), label_visibility="collapsed")

    st.markdown('</div>', unsafe_allow_html=True)
        
# Main column (3/4 width)
with col_main:
    st.markdown('<div class="fill-height">', unsafe_allow_html=True)

    st.markdown("""
    <div style="margin-bottom: 0px;" class="section-title">Peptide Sequence</div>
    <div style="margin-top: -30px;margin-bottom: -15px;">
    """, unsafe_allow_html=True)

    peptide_input = st.text_input(
        label=" ",
        placeholder="Separate by space, No PTMs included e.g., FDAFTTGFGHN ARPRNFLRF"
    )

    st.markdown("</div>", unsafe_allow_html=True)

    # Family
    st.markdown('<div class="section-title" style="margin-top: -10px; margin-bottom: 8px;">Family</div>', unsafe_allow_html=True)
    family_opts = sorted(df['Family'].dropna().unique())
    family_selected = st.multiselect(label=" ", options=family_opts, key="fam", label_visibility="collapsed")

    # Organisms
    st.markdown('<div class="section-title" style="margin-top: 0px; margin-bottom: 8px">Organisms</div>', unsafe_allow_html=True)
    org_opts = extract_unique_values(df['OS'])
    organisms_selected = st.multiselect(label=" ", options=org_opts, key="org", label_visibility="collapsed")

    # Tissue
    st.markdown('<div class="section-title" style="margin-top: 0px; margin-bottom: 8px">Tissue</div>', unsafe_allow_html=True)
    tissue_opts = extract_unique_values(df['Tissue'])
    tissue_selected = st.multiselect(label=" ", options=tissue_opts, key="tissue", label_visibility="collapsed")

    # PTM
    st.markdown('<div class="section-title" style="margin-top: 0px; margin-bottom: 8px">Post-translational modifications (PTM)</div>', unsafe_allow_html=True)
    ptm_opts = extract_unique_values(df['PTM'])
    ptm_selected = st.multiselect(label=" ", options=ptm_opts, key="ptm", label_visibility="collapsed")

    # Existence
    st.markdown('<div class="section-title" style="margin-top: 0px; margin-bottom: 8px">Existence</div>', unsafe_allow_html=True)
    exist_opts      = extract_unique_values(df['Existence'])
    existence_selected = st.multiselect(label=" ", options=exist_opts, key="exist", label_visibility="collapsed")

    st.markdown('</div>', unsafe_allow_html=True)

# Close outer flex div
st.markdown('</div>', unsafe_allow_html=True)

# Filtering logic
df_filtered = df.copy()

# 1) Always apply peptide sequence search if provided
if peptide_input:
    for pep in peptide_input.split():
        df_filtered = df_filtered[df_filtered['Sequence'].str.contains(pep, na=False)]

# 2) Apply right-side filters (multiselects) if any are selected
# These are "primary" filters - when used, they must be matched
right_filters_active = False

# Family filter
if family_selected:
    df_filtered = df_filtered[df_filtered['Family'].isin(family_selected)]
    right_filters_active = True

# Existence filter
if existence_selected:
    df_filtered = df_filtered[df_filtered['Existence'].isin(existence_selected)]
    right_filters_active = True

# Tissue filter (multi-value)
if tissue_selected:
    df_filtered = df_filtered[df_filtered['Tissue'].apply(
        lambda x: any(t in re.split(r'[;,]', str(x)) for t in tissue_selected)
    )]
    right_filters_active = True

# Organism filter (multi-value)
if organisms_selected:
    df_filtered = df_filtered[df_filtered['OS'].apply(
        lambda x: any(o in re.split(r'[;,]', str(x)) for o in organisms_selected)
    )]
    right_filters_active = True

# PTM filter (multi-value)
if ptm_selected:
    df_filtered = df_filtered[df_filtered['PTM'].apply(
        lambda x: any(p in re.split(r'[;,]', str(x)) for p in ptm_selected)
    )]
    right_filters_active = True

# 3) Apply left-side sliders ONLY if:
#    - They're not at their default values, OR
#    - No right-side filters are active
default_ranges = {
    'Monoisotopic Mass': (300.0, 2000.0),
    'Length': (3, 100),
    'GRAVY': (-5.0, 5.0),
    '% Hydrophobic Residue (%)': (0, 100),
    'Instability Index Value': (0, 120)
}

# Only apply slider filters if they differ from defaults OR no right filters are active
apply_slider_filters = (
    (mono_mass_range != default_ranges['Monoisotopic Mass']) or
    (length_range != default_ranges['Length']) or
    (gravy_range != default_ranges['GRAVY']) or
    (hydro_range != default_ranges['% Hydrophobic Residue (%)']) or
    (instability_index_value != default_ranges['Instability Index Value']) or
    (not right_filters_active)
)

if apply_slider_filters:
    df_filtered = df_filtered[
        df_filtered['Monoisotopic Mass'].between(*mono_mass_range) &
        df_filtered['Length'].between(*length_range) &
        df_filtered['GRAVY'].between(*gravy_range) &
        df_filtered['% Hydrophobic Residue (%)'].between(*hydro_range) &
        df_filtered['Instability Index Value'].between(*instability_index_value)
    ]

# --- Separator Line ---
st.markdown("""
<hr style='border: none; border-top: 2px solid #6a51a3; margin: 0px 30px;'>
""", unsafe_allow_html=True)

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

            # Clean organism field to only show unique values
            org_raw = str(row['OS']) if pd.notna(row['OS']) else ""
            org_list = [item.strip() for item in org_raw.split(';') if item.strip()]
            org_unique = "; ".join(sorted(set(org_list), key=org_list.index))

            st.markdown(f"""
                <div style='border:1px solid #6A0DAD; padding:10px; margin:0px 10px 20px 0; border-radius:10px;'>
                    <div style='font-weight:bold; background-color:#6a51a3; color:white; padding:10px;'>
                        {row['Active Sequence']}
                    </div>
                    <div style='padding:5px;'>
                        Family: {row['Family']}<br>
                        Organism: {org_unique}
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
            fasta_str += f">{r['ID']}\n{r['Sequence']}\n"
        st.download_button(
            "Download FASTA File",
            data=fasta_str,
            file_name="cNPDB_SearchResult.fasta",
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
