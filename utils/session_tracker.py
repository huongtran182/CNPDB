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
# Set a duration for what constitutes a "new" visit.
# This logic will be applied on the Google Sheet side, not the app side.
# Your app's job is just to log a single visit per session.

def get_google_sheet_client():
    """Returns an authorized gspread client and the target sheet."""
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds_dict = st.secrets["gcp_service_account"]
    creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
    client = gspread.authorize(creds)
    sheet = client.open_by_key(SHEET_ID).sheet1
    return sheet

def log_to_google_sheet(session_id, timestamp, ip_address, country, user_agent):
    """Appends a new session row to the Google Sheet."""
    try:
        sheet = get_google_sheet_client()
        row = [session_id, timestamp, ip_address, country, user_agent]
        sheet.append_row(row)
    except Exception as e:
        st.warning("Error logging session to Google Sheet.")
        st.exception(e)

def get_logged_session_count():
    """
    Counts timestamps that are not within 5 minutes of any other timestamp
    in the log (i.e., isolated sessions).
    """
    try:
        sheet = get_google_sheet_client()
        all_records = sheet.get_all_records()

        if not all_records:
            return 0

        df = pd.DataFrame(all_records)
        df['Timestamp'] = pd.to_datetime(df['Timestamp'])
        df = df.sort_values(by='Timestamp').reset_index(drop=True)

        timestamps = df['Timestamp'].tolist()
        DEDUPLICATION_WINDOW_MINUTES = 5

        unique_count = 0

        for i, current_time in enumerate(timestamps):
            is_unique = True
            for j, compare_time in enumerate(timestamps):
                if i == j:
                    continue
                time_diff = abs((current_time - compare_time).total_seconds())
                if time_diff < DEDUPLICATION_WINDOW_MINUTES * 60:
                    is_unique = False
                    break
            if is_unique:
                unique_count += 1

        return unique_count

    except Exception as e:
        st.warning("Could not retrieve session count from Google Sheet.")
        st.exception(e)
        return 0

def track_session():
    """
    Tracks a user session by generating a unique ID and logging it to Google Sheets
    only once per Streamlit session (browser tab).
    """
    # Use a session state variable as a flag to prevent re-logging in the same session
    if "session_logged" in st.session_state:
        # Session already logged, do nothing and return the current count
        return get_logged_session_count()

    # If it's a new session, get a unique ID for this session.
    # This ID will persist for as long as the user keeps the tab open.
    if "session_id" not in st.session_state:
        st.session_state.session_id = str(uuid.uuid4())
    
    # Get user info
    now = datetime.now()
    timestamp = now.strftime("%Y-%m-%d %H:%M:%S")
    
    try:
        res = requests.get("https://ipapi.co/json/")
        data = res.json()
        ip_address = data.get("ip", "Unknown")
        country = data.get("country_name", "Unknown")
    except Exception:
        ip_address = "Error"
        country = "Error"
    
    user_agent = "Streamlit App" # Streamlit doesn't expose the real user-agent easily
    
    # Log the session to the Google Sheet
    log_to_google_sheet(
        st.session_state.session_id, 
        timestamp, 
        ip_address, 
        country, 
        user_agent
    )
    
    # Set the flag to true so we don't log again in this session
    st.session_state.session_logged = True
    
    return get_logged_session_count()
