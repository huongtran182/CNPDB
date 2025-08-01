from datetime import datetime, timedelta
import uuid
import pandas as pd
import os
import csv
import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from streamlit_cookies_controller import CookieController

SHEET_ID = "1-h6G1QKP9gIa7V9T9Ked_V3pusBYOQLgC922Wy7_Pvg"
COOKIE_EXPIRY_MINUTES = 30  # Only count again after 30 minutes

# Initialize the CookieController
cookie_controller = CookieController()
# You might need to add a short delay to ensure the controller is ready
# st.write(cookie_controller.get_all()) # You can use this to debug if needed

def track_session():
    now = datetime.now()
    session_cookie = cookie_controller.get("visitor_id")
    last_visit_cookie = cookie_controller.get("last_visit")
    
    should_log = False

    if session_cookie and last_visit_cookie:
        try:
            last_visit = datetime.fromisoformat(last_visit_cookie)
            if now - last_visit > timedelta(minutes=COOKIE_EXPIRY_MINUTES):
                should_log = True
        except (ValueError, TypeError):
            should_log = True
    else:
        should_log = True

    if should_log:
        session_id = session_cookie or str(uuid.uuid4())
        cookie_controller.set("visitor_id", session_id, expires=None)
        cookie_controller.set("last_visit", now.isoformat(), expires=None)
        
        # Log to the Google Sheet, not the local CSV
        log_to_google_sheet(session_id, now)

    return get_logged_session_count()

def get_google_sheet_client():
    """Returns an authorized gspread client and the target sheet."""
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds_dict = st.secrets["gcp_service_account"]
    creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
    client = gspread.authorize(creds)
    sheet = client.open_by_key(SHEET_ID).sheet1
    return sheet

def log_to_google_sheet(session_id, timestamp):
    """Appends a new session row to the Google Sheet."""
    try:
        sheet = get_google_sheet_client()
        row = [session_id, timestamp.strftime("%Y-%m-%d %H:%M:%S")]
        sheet.append_row(row)
    except Exception as e:
        st.error("Error logging session to Google Sheet.")
        st.exception(e)

def get_logged_session_count():
    try:
        scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
        creds_dict = st.secrets["gcp_service_account"]
        creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
        client = gspread.authorize(creds)
        sheet = client.open_by_key(SHEET_ID).sheet1

        all_records = sheet.get_all_records()
        session_count = len(all_records)

    except Exception as e:
        st.warning("Could not retrieve session count from Google Sheet.")
        st.exception(e)
        session_count = 0

    return session_count
