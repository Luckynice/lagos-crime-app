# utils/session_tracker.py
import datetime
import pandas as pd

def log_session(username, page):
    now = datetime.datetime.now()
    log_entry = pd.DataFrame([[username, page, now.strftime("%Y-%m-%d %H:%M:%S")]],
                             columns=["username", "page", "timestamp"])
    try:
        logs = pd.read_csv("data/session_logs.csv")
        logs = pd.concat([logs, log_entry], ignore_index=True)
    except FileNotFoundError:
        logs = log_entry
    logs.to_csv("data/session_logs.csv", index=False)
