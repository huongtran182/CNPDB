import streamlit as st
from sidebar import render_sidebar # Assuming sidebar.py exists and works
import pandas as pd
import os
from PIL import Image # PIL is imported but not directly used in img_html, keeping it for other potential uses
import base64

st.set_page_config(
    page_title="NP Database search",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Call render_sidebar function from sidebar.py
render_sidebar()

# Custom CSS for styling
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

    /* Centered title */
    h2.custom-title {
        text-align: center !important;
        margin-top: 10px !important;
        color: #29004c;
    }
    /* Container background for filters and main section */
    div[data-testid="stColumns"] > div[data-testid="stColumn"] {
        background-color: #efedf5 !important;
        padding: 20px !important;
        border-radius: 10px !important;
    }
    /* Style every Streamlit vertical block with your lavender-gray background */
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

    /* Make slider & text-input labels purple & bold */
    [data-testid="stTextInput"] label,
    .stSlider label { /* Added .stSlider label for slider labels */
        color: #6a51a3 !important;
        font-weight: bold !important;
    }

    /* Added styles for the full details box */
    .peptide-details-box {
        position: relative;
        background-color: #efedf5;
        border-radius: 20px;
        padding: 60px 20px 20px;
        margin: 80px 0 30px;
        display: flex;
        gap: 20px;
    }
    .peptide-details-box-header {
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
        box-shadow: 0 4px 8px rgba(0,0,0,0.2); /* Add some shadow */
    }

    </style>
    """,
    unsafe_allow_html=True,
)

def img_html(path):
    """Return a base64 <img> tag filling 100% width of its container."""    
    # --- IMPORTANT DEBUGGING LINES ---
    # Convert to absolute path to see the full, resolved path
    absolute_path = os.path.abspath(path)
    # st.write(f"DEBUG (img_html): Attempting to access: `{absolute_path}`") # Uncomment for verbose path checking
    # --- END IMPORTANT DEBUGGING LINES ---

    if not os.path.exists(path):
        # --- IMPORTANT DEBUGGING LINES ---
        st.error(f"DEBUG (img_html): File NOT FOUND for path: `{absolute_path}`")
        # --- END IMPORTANT DEBUGGING LINES ---
        return "<div style='color:#999; padding:20px;'>No image found</div>"
    
    ext = os.path.splitext(path)[1].lower().replace(".", "")
    mime = f"image/{'jpeg' if ext in ('jpg','jpeg') else ext}"
    
    try:
        with open(path, "rb") as f:
            data = base64.b64encode(f.read()).decode()
        return f"<img src='data:{mime};base64,{data}' style='width:100%; height:auto;'/>"
    except Exception as e:
        # --- IMPORTANT DEBUGGING LINES ---
        st.error(f"DEBUG (img_html): Error reading or encoding file `{absolute_path}`: {e}")
        # --- END IMPORTANT DEBUGGING LINES ---
        return "<div style='color:red; padding:20px;'>Error loading image</div>"

# Helper to blank out NaNs if there is no value in the cell of the column of excel file
def disp(val):
    """Return an empty string if val is NaN/None, else val itself."""
    if pd.isna(val) or val is None:
        return ""
    return val

# Helper function to encapsulate metadata HTML for clarity
def metadata_html_content(row: pd.Series):
    gravy = row.get("GRAVY")
    gravy_str = f"{gravy:.2f}" if pd.notna(gravy) else ""

    return f"""
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

def display_peptide_details(row: pd.Series):
    seq         = row["Seq"]
    cnpd_id     = row["CNPD ID"]

    # Open the main styled box for the details
    st.markdown(f"""
    <div class="peptide-details-box">
        <div class="peptide-details-box-header">
            {seq}
        </div>
    """, unsafe_allow_html=True) 

    # Create the Streamlit columns for the content
    col_meta, col_3d, col_msi = st.columns([4, 3, 3])

    # --- Column 1: Metadata ---
    with col_meta:
        st.markdown(f"""
        <div style="
            color: #6a51a3;
            font-size: 16px;
            font-weight: bold;
            margin-top: 10px;
            text-align: center;
        ">
            Metadata
        </div>
        {metadata_html_content(row)}
        """, unsafe_allow_html=True)

    # --- Column 2: 3D Structure ---
    with col_3d:
        st.markdown(f"""
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
        """, unsafe_allow_html=True)

    # --- Column 3: MS Imaging ---
    with col_msi:
        st.markdown(f"""
        <div style="
            color: #6a51a3;
            font-size: 16px;
            font-weight: bold;
            margin-top: 10px;
            text-align: center;
        ">
            MS Imaging
        </div>
        """, unsafe_allow_html=True)
        
        # Loop through MSI Tissue 1–3, rendering each image block directly within this column
        for i in range(1, 4):
            col_name = f"MSI Tissue {i}"
            tissue_name = disp(row.get(col_name))

            if not tissue_name:
                # st.info(f"DEBUG: No tissue data for MSI Tissue {i} for CNPD ID {cnpd_id}. Skipping.") # Uncomment for debug messages
                continue

            image_filename = f"MSI cNP{cnpd_id} {i}.png"
            msi_image_path = os.path.join("Assets", "MSImaging", image_filename)
            
            st.markdown(f"""
            <div style="
                color: #6a51a3;
                font-size: 14px;
                font-weight: bold;
                text-align: center;
                margin-top: {'15px' if i > 1 else '5px'};
            ">
                – {tissue_name} –
            </div>
            <div style="
                border: 2px dashed #6a51a3;
                padding: 10px;
                text-align: center;
                margin-top: 5px;
            ">
                {img_html(msi_image_path)}
            </div>
            """, unsafe_allow_html=True)
            
    # Close the main peptide-details-box div after all columns are rendered
    st.markdown("</div>", unsafe_allow_html=True)


# --- Main application logic ---
