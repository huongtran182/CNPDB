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
SESSION_EXPIRY_HOURS = 24

def get_or_create_user_session_id():
    now = datetime.now()

    # Check if we already have a session ID and timestamp
    session_id = st.session_state.get("session_id", None)
    session_start = st.session_state.get("session_start", None)

    if session_id and session_start:
        elapsed = now - session_start
        if elapsed < timedelta(hours=SESSION_EXPIRY_HOURS):
            return session_id  # Still valid session

    # Otherwise, create new session
    new_id = str(uuid.uuid4())
    st.session_state["session_id"] = new_id
    st.session_state["session_start"] = now
    return new_id


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
        df = pd.read_csv(
            SESSION_LOG_FILE,
            names=["SessionID", "Timestamp", "IP", "Country", "UserAgent"],
            header=0,  # Skip the header row if already present
            on_bad_lines='skip'  # Skip corrupted lines
        )
        session_count = len(df)
    except FileNotFoundError:
        session_count = 0
    except Exception as e:
        st.warning(f"Failed to read session log: {e}")
        session_count = 0

    return session_count
