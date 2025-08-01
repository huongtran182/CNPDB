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
    """Retrieves the total session count from the Google Sheet."""
    try:
        sheet = get_google_sheet_client()
        all_records = sheet.get_all_records()
        
        # You can add logic here to deduplicate visits based on IP/Session ID and timestamp
        # if you want a "unique visitor" count rather than a "page visit" count.
        # However, for a simple count, len(all_records) is fine.
        
        session_count = len(all_records)
        return session_count
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
