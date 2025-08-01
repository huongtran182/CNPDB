from datetime import datetime, timedelta
import uuid
import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from streamlit_cookies_manager import EncryptedCookieManager
import os

SHEET_ID = "1-h6G1QKP9gIa7V9T9Ked_V3pusBYOQLgC922Wy7_Pvg"
COOKIE_EXPIRY_MINUTES = 30

# This should be at the very top of your script
cookies = EncryptedCookieManager(
    prefix="your_app_name/",  # Change this to a unique identifier for your app
    password=os.environ.get("COOKIES_PASSWORD", "default_secret")
)

# This is the critical part to prevent the race condition
if not cookies.ready():
    st.stop()

def get_google_sheet_client():
    # Your existing function
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds_dict = st.secrets["gcp_service_account"]
    creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
    client = gspread.authorize(creds)
    sheet = client.open_by_key(SHEET_ID).sheet1
    return sheet

def log_to_google_sheet(session_id, timestamp):
    # Your existing function
    try:
        sheet = get_google_sheet_client()
        row = [session_id, timestamp.strftime("%Y-%m-%d %H:%M:%S")]
        sheet.append_row(row)
    except Exception as e:
        st.error("Error logging session to Google Sheet.")
        st.exception(e)

def get_logged_session_count():
    # Your existing function
    try:
        sheet = get_google_sheet_client()
        all_records = sheet.get_all_records()
        session_count = len(all_records)

    except Exception as e:
        st.warning("Could not retrieve session count from Google Sheet.")
        st.exception(e)
        session_count = 0

    return session_count


def track_session_robust_with_manager():
    now = datetime.now()
    session_id_from_cookie = cookies.get("visitor_id")
    last_visit_from_cookie = cookies.get("last_visit")

    should_log = False

    if session_id_from_cookie and last_visit_from_cookie:
        try:
            last_visit = datetime.fromisoformat(last_visit_from_cookie)
            if now - last_visit > timedelta(minutes=COOKIE_EXPIRY_MINUTES):
                should_log = True
        except (ValueError, TypeError):
            should_log = True
    else:
        should_log = True

    if should_log:
        session_id = session_id_from_cookie or str(uuid.uuid4())

        # Set cookies using the manager's dictionary-like interface
        cookies["visitor_id"] = session_id
        cookies["last_visit"] = now.isoformat()
        
        # Log to the Google Sheet
        log_to_google_sheet(session_id, now)

    return get_logged_session_count()
