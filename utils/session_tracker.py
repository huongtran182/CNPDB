from datetime import datetime, timedelta
import uuid
import pandas as pd
import os
import csv
import streamlit as st
from streamlit_extras.cookie_manager import CookieManager

SHEET_ID = "1-h6G1QKP9gIa7V9T9Ked_V3pusBYOQLgC922Wy7_Pvg"
SESSION_LOG_FILE = "session_log.csv"
COOKIE_EXPIRY_MINUTES = 30  # Only count again after 30 minutes

cookie_manager = CookieManager()
cookie_manager.get_all()  # Must call this first in app

def track_session(): #track_with_cookie
    now = datetime.now()
    session_cookie = cookie_manager.get("visitor_id")
    last_visit_cookie = cookie_manager.get("last_visit")

    should_log = False

    if session_cookie and last_visit_cookie:
        try:
            last_visit = datetime.fromisoformat(last_visit_cookie)
            if now - last_visit > timedelta(minutes=COOKIE_EXPIRY_MINUTES):
                should_log = True
        except Exception:
            should_log = True
    else:
        should_log = True

    if should_log:
        session_id = session_cookie or str(uuid.uuid4())
        cookie_manager.set("visitor_id", session_id, expires_at=None)
        cookie_manager.set("last_visit", now.isoformat(), expires_at=None)

        log_to_csv(session_id, now)

    return get_logged_session_count()

def log_to_csv(session_id, timestamp):
    if not os.path.exists(SESSION_LOG_FILE):
        with open(SESSION_LOG_FILE, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["SessionID", "Timestamp"])

    with open(SESSION_LOG_FILE, "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([session_id, timestamp.strftime("%Y-%m-%d %H:%M:%S")])

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
