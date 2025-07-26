import streamlit as st
from sidebar import render_sidebar
from PIL import Image
import os
import base64
import json
import atexit
import collections.abc

from google.analytics.data_v1beta import BetaAnalyticsDataClient
from google.analytics.data_v1beta.types import RunRealtimeReportRequest
from google.oauth2 import service_account

# Page settings
st.set_page_config(
    page_title="Statistics",
    layout="wide",
    initial_sidebar_state="expanded"
)

render_sidebar()

# --- Load GA4 Credentials ---
service_account_info = dict(st.secrets["google_service_account"])  # convert from AttrDict
with open("tmp_service_account.json", "w") as f:
    json.dump(service_account_info, f)

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "tmp_service_account.json"

# Cleanup on exit
atexit.register(lambda: os.remove("tmp_service_account.json") if os.path.exists("tmp_service_account.json") else None)

# --- GA4 Property ID ---
PROPERTY_ID = "497897321"

# --- Function to fetch total pageviews ---
def get_active_users():
    client = BetaAnalyticsDataClient()

    request = RunRealtimeReportRequest(
        property=f"properties/{PROPERTY_ID}",
        dimensions=[],
        metrics=[{"name": "activeUsers"}],
    )

    response = client.run_realtime_report(request)
    return response.rows[0].metric_values[0].value if response.rows else "0"

# Fetch live pageviews
page_views = get_active_users()

# ---- Horizontal Stats Bar ----
st.markdown("---")
st.markdown(f"""
<div style="display: flex; width: 100%;">
        <div style="flex: 1; background-color: #dadaeb; text-align: center; padding: 20px 0;">
            <h2 style="color:#4a3666; margin-left: 15px;">1364</h2>
            <p style="margin: 0; font-weight: bold; color:#4a3666;">Peptide Entries</p>
        </div>
        <div style="flex: 1; background-color: #eeeeee; text-align: center; padding: 20px 0;">
            <h2 style="color:#4a3666; margin-left: 15px;">29</h2>
            <p style="margin: 0; font-weight: bold; color:#4a3666;">Organisms</p>
        </div>
        <div style="flex: 1; background-color: #dadaeb; text-align: center; padding: 20px 0;">
            <h2 style="color:#4a3666; margin-left: 15px;">55</h2>
            <p style="margin: 0; font-weight: bold; color:#4a3666;">Neuropeptide Families</p>
        </div>
        <div style="flex: 1; background-color: #eeeeee; text-align: center; padding: 20px 0;">
            <h2 style="color:#4a3666; margin-left: 15px;">{page_views}</h2>
            <p style="margin: 0; font-weight: bold; color:#4a3666;">Page Views</p>
        </div>
    </div>
""", unsafe_allow_html=True)
st.markdown("---")
# ---- Section: Composition Chart ----
st.markdown("""
<h4 style="margin-bottom: 10px;">1. Family Distribution of Neuropeptides in cNPDB</h4>
""", unsafe_allow_html=True)
image_path = os.path.join("Assets", "Statistics", "Pie Chart Family Distribution.png")
if os.path.exists(image_path):
    st.markdown(f"""
        <div style="margin: 0 auto; text-align: center;">
            <img src="data:image/png;base64,{base64.b64encode(open(image_path, "rb").read()).decode()}" style="width: auto; height: 400px;" />
        </div>
    """, unsafe_allow_html=True)
else:
    st.error(f"Image not found at {image_path}")

st.markdown("""
<h4 style="margin-top: 40px; margin-bottom: 10px;">2. Composition of Neuropeptides per Organism in cNPDB</h4>
""", unsafe_allow_html=True)
image_path = os.path.join("Assets", "Statistics", "Pie Chart Organism Distribution.png")
if os.path.exists(image_path):
    st.markdown(f"""
        <div style="margin: 0 auto; text-align: center;">
            <img src="data:image/png;base64,{base64.b64encode(open(image_path, "rb").read()).decode()}" style="width: auto; height: 400px;" />
        </div>
    """, unsafe_allow_html=True)
else:
    st.error(f"Image not found at {image_path}")

st.markdown("""
<h4 style="margin-top: 40px; margin-bottom: 10px;">3. Composition of Neuropeptides per Physiological and Biological Studies in cNPDB</h4>
""", unsafe_allow_html=True)
image_path = os.path.join("Assets", "Statistics", "Pie chart Biological Application.png")
if os.path.exists(image_path):
    st.markdown(f"""
        <div style="margin: 0 auto; text-align: center;">
            <img src="data:image/png;base64,{base64.b64encode(open(image_path, "rb").read()).decode()}" style="width: auto; height: 400px;" />
        </div>
    """, unsafe_allow_html=True)
else:
    st.error(f"Image not found at {image_path}")

st.markdown("""
<h4 style="margin-top: 40px; margin-bottom: 10px;">4. Composition of Neuropeptides per Investigation Techniques in cNPDB</h4>
""", unsafe_allow_html=True)
image_path = os.path.join("Assets", "Statistics", "Pie chart Technique.png")
if os.path.exists(image_path):
    st.markdown(f"""
        <div style="margin: 0 auto; text-align: center;">
            <img src="data:image/png;base64,{base64.b64encode(open(image_path, "rb").read()).decode()}" style="width: auto; height: 400px;" />
        </div>
    """, unsafe_allow_html=True)
else:
    st.error(f"Image not found at {image_path}")



st.markdown("""
<h4 style="margin-top: 40px; margin-bottom: 10px;">5. Properties of All Peptides in cNPDB</h4>
""", unsafe_allow_html=True)
image_path = os.path.join("Assets", "Statistics", "Peptide Property Violin.png")
if os.path.exists(image_path):
    st.markdown(f"""
        <div style="margin: 0 auto; text-align: center;">
            <img src="data:image/png;base64,{base64.b64encode(open(image_path, "rb").read()).decode()}" style="width: auto; height: 600px;" />
        </div>
    """, unsafe_allow_html=True)
else:
    st.error(f"Image not found at {image_path}")

st.markdown("""
<h4 style="margin-top: 40px; margin-bottom: 10px;">6. Distribution of Existence Evidence for All Peptides in cNPDB</h4>
""", unsafe_allow_html=True)
image_path = os.path.join("Assets", "Statistics", "Pie Chart Existence Distribution.png")
if os.path.exists(image_path):
    st.markdown(f"""
        <div style="margin: 0 auto; text-align: center;">
            <img src="data:image/png;base64,{base64.b64encode(open(image_path, "rb").read()).decode()}" style="width: auto; height: 400px;" />
        </div>
    """, unsafe_allow_html=True)
else:
    st.error(f"Image not found at {image_path}")

st.markdown("""
<h4 style="margin-top: 40px; margin-bottom: 10px;">7. Amino Acids Composition from All Peptides in cNPDB</h4>
""", unsafe_allow_html=True)
image_path = os.path.join("Assets", "Statistics", "Amino Acid Composition.png")
if os.path.exists(image_path):
    st.markdown(f"""
        <div style="margin: 0 auto; text-align: center;">
            <img src="data:image/png;base64,{base64.b64encode(open(image_path, "rb").read()).decode()}" style="width: auto; height: 400px;" />
        </div>
    """, unsafe_allow_html=True)
else:
    st.error(f"Image not found at {image_path}")


st.markdown("""
<div style="text-align: center; font-size:14px; color:#2a2541;">
  <em>Last update: Jul 2025</em>
</div>
""", unsafe_allow_html=True)

