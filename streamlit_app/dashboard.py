import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import os
from dotenv import load_dotenv
from datetime import datetime

# Load environment variables
load_dotenv()
firebase_url = os.getenv("FIREBASE_URL")

st.set_page_config(page_title="📊 FinGenie Admin Dashboard", layout="wide")

st.title("📊 FinGenie – Admin Dashboard")
st.markdown("Monitor user insights, risk profiles, and investment goals.")

# --- Fetch data ---
@st.cache_data(ttl=300)
def fetch_user_logs():
    try:
        res = requests.get(f"{firebase_url}/user_logs.json")
        res.raise_for_status()
        data = res.json()
        st.write("📦 Raw Firebase Data:", data)  # 🧪 DEBUG LINE

        if not data:
            return pd.DataFrame()
        
        # Normalize Firebase dict into DataFrame
        df = pd.json_normalize(data).T.reset_index()
        df.columns = ['firebase_id', 'data']
        df = pd.json_normalize(df['data'])
        if 'timestamp' in df.columns:
            df['timestamp'] = pd.to_datetime(df['timestamp'], errors='coerce')
        else:
            df['timestamp'] = None
        return df
    except Exception as e:
        st.error(f"Error fetching data: {e}")
        return pd.DataFrame()

df = fetch_user_logs()

# --- If no data ---
if df.empty:
    st.info("No user logs found.")
    st.stop()


