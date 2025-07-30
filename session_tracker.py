import os
import csv
import uuid
from datetime import datetime
import requests
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import streamlit as st
import pandas as pd

SHEET_ID = "1-h6G1QKP9gIa7V9T9Ked_V3pusBYOQLgC922Wy7_Pvg"
SESSION_LOG_FILE = "session_log.csv"
SESSION_COUNT_FILE = "total_sessions.txt"

def track_session():
    if "session_tracked" not in st.session_state:
        st.session_state.session_tracked = True

        # Google Sheets setup
        scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
        creds_dict = st.secrets["gcp_service_account"]
        creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
        client = gspread.authorize(creds)
        sheet = client.open_by_key(SHEET_ID).sheet1

        # Generate session info
        session_id = str(uuid.uuid4())
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        try:
            res = requests.get("https://ipapi.co/json/")
            data = res.json()
            ip_address = data.get("ip", "Unknown")
            country = data.get("country_name", "Unknown")
        except Exception:
            ip_address = "Error"
            country = "Error"

        user_agent = "Streamlit App"

        # Log locally
        if not os.path.exists(SESSION_LOG_FILE):
            with open(SESSION_LOG_FILE, "w", newline='') as f:
                writer = csv.writer(f)
                writer.writerow(["SessionID", "Timestamp", "IP", "Country", "UserAgent"])
        with open(SESSION_LOG_FILE, "a", newline='') as f:
            writer = csv.writer(f)
            writer.writerow([session_id, timestamp, ip_address, country, user_agent])

        # Log to Google Sheet
        try:
            sheet.append_row([session_id, timestamp, ip_address, country, user_agent])
        except Exception as e:
            st.warning("Could not log to Google Sheet.")
            st.exception(e)

        # Update session count
        if not os.path.exists(SESSION_COUNT_FILE):
            with open(SESSION_COUNT_FILE, "w") as f:
                f.write("1")
        else:
            with open(SESSION_COUNT_FILE, "r+") as f:
                count = int(f.read().strip())
                f.seek(0)
                f.write(str(count + 1))
    # Calculate session count
    try:
        df = pd.read_csv('session_log.csv')
        session_count = len(df)
    except FileNotFoundError:
        session_count = 0
        
    return session_count


        
