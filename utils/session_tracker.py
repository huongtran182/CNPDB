import os
import csv
import uuid
from datetime import datetime, timedelta
import requests
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import streamlit as st
import streamlit.components.v1 as components

SHEET_ID = "1-h6G1QKP9gIa7V9T9Ked_V3pusBYOQLgC922Wy7_Pvg"
SESSION_EXPIRY_HOURS = 24
COOKIE_NAME = "visitor_id"


def get_visitor_id():
    # This component runs JS to get or set a visitor_id cookie, then returns it to Streamlit.
    js = f"""
    <script>
    (function() {{
        function getCookie(name) {{
            let value = "; " + document.cookie;
            let parts = value.split("; " + name + "=");
            if (parts.length === 2) return parts.pop().split(";").shift();
        }}
        function setCookie(name, value, days) {{
            let expires = "";
            if (days) {{
                let date = new Date();
                date.setTime(date.getTime() + (days*24*60*60*1000));
                expires = "; expires=" + date.toUTCString();
            }}
            document.cookie = name + "=" + value + expires + "; path=/";
        }}

        let visitor = getCookie("{COOKIE_NAME}");
        if (!visitor) {{
            visitor = "{str(uuid.uuid4())}";
            setCookie("{COOKIE_NAME}", visitor, 365);
        }}
        const streamlitEl = window.parent.document.querySelector('iframe[title^="streamlit-app"]');
        if(streamlitEl) {{
            // Send visitor ID to Streamlit by setting innerText on a div
            const el = document.getElementById('visitor_id_container');
            if (el) {{
                el.innerText = visitor;
            }}
        }}
    }})();
    </script>
    <div id="visitor_id_container" style="display:none">unknown</div>
    """
    components.html(js, height=0)
    # We return visitor id stored in session_state by another function below (see main app)
    return None


def get_or_create_visitor_id():
    # Return the visitor_id stored in st.session_state, or None if not yet set
    return st.session_state.get("visitor_id", None)


def track_session():
    now = datetime.now()

    # Run JS to get/set visitor cookie once (it will update the hidden div)
    get_visitor_id()

    # Grab visitor_id from session_state or from hidden div after rerun
    visitor_id = get_or_create_visitor_id()

    # If visitor_id is not yet set in session_state, try to grab it from component output
    # We can add a workaround by reading the value from st.query_params or other ways,
    # but here we require the app to rerun after the cookie is set, so on second run visitor_id is available.

    if visitor_id is None:
        # First run, visitor_id not ready, wait for next rerun
        st.rerun()
        return

    # Save visitor_id to session_state for reuse
    st.session_state["visitor_id"] = visitor_id

    # Check if this visitor already logged recently (within expiry)
    last_logged_time = st.session_state.get(f"last_logged_{visitor_id}", None)
    if last_logged_time and (now - last_logged_time) < timedelta(hours=SESSION_EXPIRY_HOURS):
        # Already logged recently, skip logging
        return get_logged_session_count()

    # Update last logged time
    st.session_state[f"last_logged_{visitor_id}"] = now

    # Google Sheets setup
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds_dict = st.secrets["gcp_service_account"]
    creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
    client = gspread.authorize(creds)
    sheet = client.open_by_key(SHEET_ID).sheet1

    timestamp = now.strftime("%Y-%m-%d %H:%M:%S")

    # Get IP and country from external API
    try:
        res = requests.get("https://ipapi.co/json/")
        data = res.json()
        ip_address = data.get("ip", "Unknown")
        country = data.get("country_name", "Unknown")
    except Exception:
        ip_address = "Error"
        country = "Error"

    user_agent = "Streamlit App"

    # Append row to Google Sheet
    try:
        sheet.append_row([visitor_id, timestamp, ip_address, country, user_agent])
    except Exception as e:
        st.warning("Could not log to Google Sheet.")
        st.exception(e)

    return get_logged_session_count()


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
