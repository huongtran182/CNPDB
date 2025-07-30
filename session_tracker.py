# session_tracker.py
import os
import csv
import uuid
from datetime import datetime
import requests
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import streamlit as st
import pandas as pd
from streamlit_javascript import st_javascript

SHEET_ID = "1-h6G1QKP9gIa7V9T9Ked_V3pusBYOQLgC922Wy7_Pvg"
SESSION_LOG_FILE = "session_log.csv"
SESSION_COUNT_FILE = "total_sessions.txt"

def track_session():
    if "session_tracked" in st.session_state:
        return
    st.session_state.session_tracked = True

    # JavaScript to get IP + Country + UserAgent
    result = st_javascript(
        """
        async () => {
            try {
                const res = await fetch("https://ipapi.co/json/");
                const data = await res.json();
                return {
                    ip: data.ip || "Unavailable",
                    userAgent: navigator.userAgent || "Unavailable",
                    country: data.country_name || "Unavailable"
                };
            } catch (e) {
                return {
                    ip: "Unavailable",
                    userAgent: navigator.userAgent || "Unavailable",
                    country: "Unavailable"
                };
            }
        }
        """
    )

    ip = result.get("ip", "Unavailable") if result else "Unavailable"
    user_agent = result.get("userAgent", "Unavailable") if result else "Unavailable"
    country = result.get("country", "Unavailable") if result else "Unavailable"

    session_id = str(uuid.uuid4())
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # 📝 Write to log
    if not os.path.exists(SESSION_LOG_FILE):
        with open(SESSION_LOG_FILE, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["SessionID", "Timestamp", "IP", "Country", "UserAgent"])

    with open(SESSION_LOG_FILE, "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([session_id, timestamp, ip, country, user_agent])
    # Calculate session count
    try:
        df = pd.read_csv('session_log.csv')
        session_count = len(df)
    except FileNotFoundError:
        session_count = 0
        
    return session_count


        
