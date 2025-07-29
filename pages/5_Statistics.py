import streamlit as st
from sidebar import render_sidebar
from PIL import Image
import os
import base64
from datetime import datetime
import uuid
import csv
import requests
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Page settings
st.set_page_config(
    page_title="Statistics",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---- Constants ----
SESSION_LOG_FILE = "session_log.csv"
SESSION_COUNT_FILE = "total_sessions.txt"
SERVICE_ACCOUNT_FILE = "service_account.json"
SHEET_ID = "1-h6G1QKP9gIa7V9T9Ked_V3pusBYOQLgC922Wy7_Pvg"  # <-- Replace with your Google Sheet ID

# ---- Setup Google Sheets Client ----
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name(SERVICE_ACCOUNT_FILE, scope)
client = gspread.authorize(creds)
sheet = client.open_by_key(SHEET_ID).sheet1

# ---- Create local log file if not exists ----
if not os.path.exists(SESSION_LOG_FILE):
    with open(SESSION_LOG_FILE, "w", newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["SessionID", "Timestamp", "IP", "Country", "UserAgent"])

# ---- Track New Session ----
if "session_tracked" not in st.session_state:
    st.session_state.session_tracked = True

    # Generate session info
    session_id = str(uuid.uuid4())
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # IP and Country
    try:
        res = requests.get("https://ipapi.co/json/")
        data = res.json()
        ip_address = data.get("ip", "Unknown")
        country = data.get("country_name", "Unknown")
    except Exception:
        ip_address = "Error"
        country = "Error"

    user_agent = "Streamlit App"  # You can improve this if needed

    # Append to local CSV log
    with open(SESSION_LOG_FILE, "a", newline='') as f:
        writer = csv.writer(f)
        writer.writerow([session_id, timestamp, ip_address, country, user_agent])

    # Append to Google Sheet
    try:
        sheet.append_row([session_id, timestamp, ip_address, country, user_agent])
    except Exception as e:
        st.error("Failed to log to Google Sheet.")
        st.exception(e)

    # Increment session count
    if not os.path.exists(SESSION_COUNT_FILE):
        with open(SESSION_COUNT_FILE, "w") as f:
            f.write("1")
    else:
        with open(SESSION_COUNT_FILE, "r+") as f:
            count = int(f.read().strip())
            count += 1
            f.seek(0)
            f.write(str(count))

# ---- Read session count ----
with open(SESSION_COUNT_FILE, "r") as f:
    session_count = int(f.read().strip())

render_sidebar()

# ---- Horizontal Stats Bar ----
st.markdown("---")
st.markdown(f"""
<div style="display: flex; width: 100%;">
        <div style="flex: 1; background-color: #dadaeb; text-align: center; padding: 20px 0;">
            <h2 style="color:#4a3666; margin-left: 15px;">1379</h2>
            <p style="margin: 0; font-weight: bold; color:#4a3666;">Peptide Entries</p>
        </div>
        <div style="flex: 1; background-color: #eeeeee; text-align: center; padding: 20px 0;">
            <h2 style="color:#4a3666; margin-left: 15px;">30</h2>
            <p style="margin: 0; font-weight: bold; color:#4a3666;">Organisms</p>
        </div>
        <div style="flex: 1; background-color: #dadaeb; text-align: center; padding: 20px 0;">
            <h2 style="color:#4a3666; margin-left: 15px;">55</h2>
            <p style="margin: 0; font-weight: bold; color:#4a3666;">Neuropeptide Families</p>
        </div>
        <div style="flex: 1; background-color: #eeeeee; text-align: center; padding: 20px 0;">
            <h2 style="color:#4a3666; margin-left: 15px;">{session_count}</h2>
            <p style="margin: 0; font-weight: bold; color:#4a3666;">Page visits</p>
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

