import json
from datetime import datetime
from pathlib import Path

import pandas as pd
import streamlit as st

from streamlit_local_storage import LocalStorage
import requests

from utils.config import BACKEND_URL


def get_mock_history() -> pd.DataFrame:
    path = Path("utils/history.json")
    with path.open("r", encoding="utf-8") as f:
        raw = json.load(f)

    records = []
    for entry in raw:
        dt_unix = entry.get("dt")
        timestamp = datetime.fromtimestamp(dt_unix)
        date_str = timestamp.date().isoformat()
        time_str = timestamp.strftime("%H:%M:%S")
        city = entry.get("name")
        country = entry.get("sys", {}).get("country")
        main = entry.get("main", {})
        temp = main.get("temp")
        humidity = main.get("humidity")
        records.append({
            "timestamp": timestamp,
            "date": date_str,
            "time": time_str,
            "city": city,
            "country": country,
            "temp": temp,
            "humidity": humidity
        })

    return pd.DataFrame(records)


st.set_page_config(
    page_title="Weather History",
    page_icon="📈",
    layout="centered")
st.title("📈 Weather History")

localS = LocalStorage()
token = localS.getItem("weather_token")
telegram_id = localS.getItem("weather_telegram_id")
auth_token = localS.getItem("weather_auth_token")

print(token, telegram_id, auth_token)

raw_list = []
try:
    city = ""
    limit = 10

    params = {
        "user_token": auth_token,
        "city": city,
        "limit": limit
    }

    resp = requests.get(f"{BACKEND_URL}/weather/history", params=params)
    resp.raise_for_status()
    raw_list = resp.json()["history"]
except Exception as e:
    st.error(f"⚠️ Failed to load data: {e}")
    st.stop()

records = []
print(raw_list)

for entry in raw_list:
    ts = datetime.fromtimestamp(entry["time"])
    records.append({
        "timestamp": ts,
        "date": ts.date().isoformat(),
        "time": ts.strftime("%H:%M:%S"),
        "temperature": entry["temperature"],
        "feels_like": entry["feels_like"],
        "pressure": entry["pressure"],
        "humidity": entry["humidity"],
    })
data = pd.DataFrame(records)

with st.expander("🔎 Filters", expanded=True):
    col1, col2 = st.columns(2)

    with col1:
        date_options = ["All"] + sorted(data["date"].unique())
        selected_date = st.selectbox("📅 Date", date_options)

    with col2:
        time_filter = (
            data if selected_date == "All"
            else data[data["date"] == selected_date]
        )
        time_options = ["All"] + sorted(time_filter["time"].unique())
        selected_time = st.selectbox("🕒 Time", time_options)

filtered = data.copy()
if selected_date != "All":
    filtered = filtered[filtered["date"] == selected_date]
if selected_time != "All":
    filtered = filtered[filtered["time"] == selected_time]

if not filtered.empty:
    st.markdown("### 📊 Weather Summary")
    st.caption(
        f"Showing data for "
        f"**{selected_date if selected_date != 'All' else 'all dates'}** "
        f"at **{selected_time if selected_time != 'All' else 'all times'}**."
    )
    chart_data = (
        filtered[["time", "temperature", "humidity"]]
        .set_index("time")
        .rename(columns={
            "temperature": "🌡️ Temp (°C)",
            "humidity": "💧 Humidity (%)"
        })
    )
    st.line_chart(chart_data, use_container_width=True)

    df_display = (
        filtered.drop(columns=["timestamp"])
        .sort_values(["date", "time"], ascending=[False, False])
        .rename(columns={
            "date": "📅 Date",
            "time": "🕒 Time",
            "temp": "🌡️ Temp (°C)",
            "humidity": "💧 Humidity (%)"
        })
    )
    st.dataframe(df_display, use_container_width=True)
else:
    st.warning("🚫 No data available for the selected filters.")
