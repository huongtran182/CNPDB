from datetime import datetime
import uuid
import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Your Google Sheet ID
SHEET_ID = "1-h6G1QKP9gIa7V9T9Ked_V3pusBYOQLgC922Wy7_Pvg"

def get_google_sheet_client():
    """Returns an authorized gspread client and the target sheet."""
    try:
        scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
        creds_dict = st.secrets["gcp_service_account"]
        creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
        client = gspread.authorize(creds)
        sheet = client.open_by_key(SHEET_ID).sheet1
        return sheet
    except Exception as e:
        st.error("Authentication failed. Check your 'gcp_service_account' secrets.")
        st.exception(e)
        return None

def track_session():
    """Appends a new row to the Google Sheet for every page view."""
    sheet = get_google_sheet_client()
    if sheet:
        try:
            timestamp = datetime.now()
            # Generate a new unique ID for each page view
            page_view_id = str(uuid.uuid4())
            row = [page_view_id, timestamp.strftime("%Y-%m-%d %H:%M:%S")]
            sheet.append_row(row)
        except Exception as e:
            st.error("Error logging page view to Google Sheet.")
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

