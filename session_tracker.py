import os
import csv
import uuid
from datetime import datetime, timedelta
import requests
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import streamlit as st
import pandas as pd

SHEET_ID = "1-h6G1QKP9gIa7V9T9Ked_V3pusBYOQLgC922Wy7_Pvg"
SESSION_LOG_FILE = "session_log.csv"
SESSION_COUNT_FILE = "total_sessions.txt"

def get_or_create_user_session_id():
    # Use URL parameters as a workaround for browser-sticky session tracking
    query_params = st.query_params()
    
    if "sid" in query_params:
        session_id = query_params["sid"][0]
    else:
        session_id = str(uuid.uuid4())
        st.query_params(sid=session_id)
    
    return session_id


def track_session():
    now = datetime.now()
    session_id = get_or_create_user_session_id()

    # Avoid duplicate logging in same session
    if "session_tracked" in st.session_state:
        return get_logged_session_count()

    st.session_state.session_tracked = True

    # Google Sheets setup
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds_dict = st.secrets["gcp_service_account"]
    creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
    client = gspread.authorize(creds)
    sheet = client.open_by_key(SHEET_ID).sheet1

    timestamp = now.strftime("%Y-%m-%d %H:%M:%S")

    try:
        res = requests.get("https://ipapi.co/json/")
        data = res.json()
        ip_address = data.get("ip", "Unknown")
        country = data.get("country_name", "Unknown")
    except Exception:
        ip_address = "Error"
        country = "Error"

    user_agent = "Streamlit App"

    # Local log
    if not os.path.exists(SESSION_LOG_FILE):
        with open(SESSION_LOG_FILE, "w", newline='') as f:
            writer = csv.writer(f)
            writer.writerow(["SessionID", "Timestamp", "IP", "Country", "UserAgent"])
    with open(SESSION_LOG_FILE, "a", newline='') as f:
        writer = csv.writer(f)
        writer.writerow([session_id, timestamp, ip_address, country, user_agent])

    # Google Sheet log
    try:
        sheet.append_row([session_id, timestamp, ip_address, country, user_agent])
    except Exception as e:
        st.warning("Could not log to Google Sheet.")
        st.exception(e)

    # Session counter
    if not os.path.exists(SESSION_COUNT_FILE):
        with open(SESSION_COUNT_FILE, "w") as f:
            f.write("1")
    else:
        with open(SESSION_COUNT_FILE, "r+") as f:
            count = int(f.read().strip())
            f.seek(0)
            f.write(str(count + 1))

    return get_logged_session_count()

    # Return count from CSV
def get_logged_session_count():
    try:
        df = pd.read_csv(SESSION_LOG_FILE)
        session_count = len(df)
    except FileNotFoundError:
        session_count = 0

    return session_count
