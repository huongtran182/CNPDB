from datetime import datetime, timedelta
import uuid
import pandas as pd
import os
import csv
import streamlit as st
import streamlit.components.v1 as components

SESSION_LOG_FILE = "session_log.csv"
COOKIE_EXPIRY_MINUTES = 30  # Only count again after 30 minutes

# Custom JS Cookie Reader/Setter
def set_and_get_cookies_js(cookie_name, cookie_value=None, days_expire=30):
    js_code = f"""
    <script>
        function setCookie(name, value, days) {{
            const d = new Date();
            d.setTime(d.getTime() + (days*24*60*60*1000));
            let expires = "expires=" + d.toUTCString();
            document.cookie = name + "=" + value + ";" + expires + ";path=/";
        }}

        function getCookie(name) {{
            let decodedCookie = decodeURIComponent(document.cookie);
            let ca = decodedCookie.split(';');
            for(let i = 0; i < ca.length; i++) {{
                let c = ca[i];
                while (c.charAt(0) == ' ') {{
                    c = c.substring(1);
                }}
                if (c.indexOf(name + "=") == 0) {{
                    return c.substring((name + "=").length, c.length);
                }}
            }}
            return "";
        }}

        const cookieName = "{cookie_name}";
        const cookieVal = getCookie(cookieName);

        if (!cookieVal && "{cookie_value}" !== "") {{
            setCookie(cookieName, "{cookie_value}", {days_expire});
            document.body.innerText = "{cookie_value}";
        }} else {{
            document.body.innerText = cookieVal;
        }}
    </script>
    """
    result = components.html(js_code, height=0)
    return result

def track_session():
    now = datetime.now()

    # Use JS to set/get visitor_id and last_visit cookies
    session_id = str(uuid.uuid4())
    visitor_id = set_and_get_cookies_js("visitor_id", session_id)
    last_visit = set_and_get_cookies_js("last_visit", now.isoformat())

    # Store them in session_state for access
    if "visitor_id" not in st.session_state:
        st.session_state.visitor_id = visitor_id
    if "last_visit" not in st.session_state:
        st.session_state.last_visit = last_visit

    # Try parse last visit
    should_log = False
    try:
        parsed_last_visit = datetime.fromisoformat(last_visit)
        if now - parsed_last_visit > timedelta(minutes=COOKIE_EXPIRY_MINUTES):
            should_log = True
    except Exception:
        should_log = True

    if should_log:
        log_to_csv(visitor_id or session_id, now)
        # Update cookie
        _ = set_and_get_cookies_js("last_visit", now.isoformat())

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
        df = pd.read_csv(SESSION_LOG_FILE)
        return len(df)
    except FileNotFoundError:
        return 0
