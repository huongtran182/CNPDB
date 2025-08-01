import os
import csv
import uuid
from datetime import datetime, timedelta
import requests
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import streamlit as st
import streamlit.components.v1 as components
import pandas as pd

SESSION_LOG_FILE = "session_log.csv"
SESSION_EXPIRY_HOURS = 24
SHEET_ID = "1-h6G1QKP9gIa7V9T9Ked_V3pusBYOQLgC922Wy7_Pvg"

# -------------------
# JS Cookie Helper
# -------------------
def set_and_get_cookie(cookie_name, cookie_value=None, days_expire=30):
    js_code = f"""
    <script>
        function setCookie(name, value, days) {{
            const d = new Date();
            d.setTime(d.getTime() + (days*24*60*60*1000));
            let expires = "expires=" + d.toUTCString();
            document.cookie = name + "=" + value + ";" + expires + ";path=/";
        }}

        function getCookie(name) {{
            let nameEQ = name + "=";
            let ca = document.cookie.split(';');
            for (let i = 0; i < ca.length; i++) {{
                let c = ca[i];
                while (c.charAt(0) === ' ') c = c.substring(1);
                if (c.indexOf(nameEQ) === 0) return c.substring(nameEQ.length, c.length);
            }}
            return "";
        }}

        let cookieVal = getCookie("{cookie_name}");
        if (!cookieVal && "{cookie_value}" !== "") {{
            setCookie("{cookie_name}", "{cookie_value}", {days_expire});
            document.body.innerText = "{cookie_value}";
        }} else {{
            document.body.innerText = cookieVal;
        }}
    </script>
    """
    return components.html(js_code, height=0)

# -------------------
# Track User Session
# -------------------
def track_session():
    now = datetime.now()

    # Use cookie to persist visitor ID
    session_id = str(uuid.uuid4())
    visitor_id = set_and_get_cookie("visitor_id", session_id)

    if "visitor_id" not in st.session_state:
        st.session_state["visitor_id"] = visitor_id
    else:
        visitor_id = st.session_state["visitor_id"]

    if "session_tracked" in st.session_state:
        return get_logged_session_count()

    st.session_state["session_tracked"] = True

    # Log user IP
    try:
        res = requests.get("https://ipapi.co/json/")
        data = res.json()
        ip_address = data.get("ip", "Unknown")
        country = data.get("country_name", "Unknown")
    except Exception:
        ip_address = "Error"
        country = "Error"

    user_agent = "Streamlit App"
    timestamp = now.strftime("%Y-%m-%d %H:%M:%S")

    # Log to CSV
    if not os.path.exists(SESSION_LOG_FILE):
        with open(SESSION_LOG_FILE, "w", newline='') as f:
            writer = csv.writer(f)
            writer.writerow(["SessionID", "Timestamp", "IP", "Country", "UserAgent"])
    with open(SESSION_LOG_FILE, "a", newline='') as f:
        writer = csv.writer(f)
        writer.writerow([visitor_id, timestamp, ip_address, country, user_agent])

    # Log to Google Sheets
    try:
        scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
        creds_dict = st.secrets["gcp_service_account"]
        creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
        client = gspread.authorize(creds)
        sheet = client.open_by_key(SHEET_ID).sheet1
        sheet.append_row([visitor_id, timestamp, ip_address, country, user_agent])
    except Exception as e:
        st.warning("⚠️ Could not log to Google Sheet.")
        st.exception(e)

    return get_logged_session_count()

def get_logged_session_count():
    try:
        df = pd.read_csv(SESSION_LOG_FILE, on_bad_lines='skip')  # 👈 skip malformed lines)
        return len(df)
    except FileNotFoundError:
        return 0

