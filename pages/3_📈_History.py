import json
from datetime import datetime
from pathlib import Path

import pandas as pd
import streamlit as st


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
        records.append(
            {
                "timestamp": timestamp,
                "date": date_str,
                "time": time_str,
                "city": city,
                "country": country,
                "temp": temp,
                "humidity": humidity,
            }
        )

    return pd.DataFrame(records)


st.set_page_config(page_title="Weather History",
                   page_icon="📈", layout="centered")
st.title("📈 Weather History")

try:
    data = get_mock_history()
except Exception as e:
    st.error(f"⚠️ Failed to load data: {e}")
    st.stop()

with st.expander("🔎 Filters", expanded=True):
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        countries = ["All"] + sorted(data["country"].unique())
        selected_country = st.selectbox("🌍 Country", countries)

    with col2:
        city_filter = (
            data
            if selected_country == "All"
            else data[data["country"] == selected_country]
        )
        city_options = ["All"] + sorted(city_filter["city"].unique())
        selected_city = st.selectbox("🌆 City", city_options)

    with col3:
        date_filter = (
            city_filter
            if selected_city == "All"
            else city_filter[city_filter["city"] == selected_city]
        )
        date_options = ["All"] + sorted(date_filter["date"].unique())
        selected_date = st.selectbox("📅 Date", date_options)

    with col4:
        time_filter = (
            date_filter
            if selected_date == "All"
            else date_filter[date_filter["date"] == selected_date]
        )
        time_options = ["All"] + sorted(time_filter["time"].unique())
        selected_time = st.selectbox("🕒 Time", time_options)

filtered = data.copy()
if selected_country != "All":
    filtered = filtered[filtered["country"] == selected_country]
if selected_city != "All":
    filtered = filtered[filtered["city"] == selected_city]
if selected_date != "All":
    filtered = filtered[filtered["date"] == selected_date]
if selected_time != "All":
    filtered = filtered[filtered["time"] == selected_time]

if not filtered.empty:
    st.markdown("### 📊 Weather Summary")
    st.caption(
        f"Showing data for "
        f"**{selected_city if selected_city != 'All' else 'all cities'}**, "
        f"**{(
            selected_country if selected_country != 'All'
            else 'all countries'
            )}** "
        f"on **{selected_date if selected_date != 'All' else 'all dates'}** "
        f"at **{selected_time if selected_time != 'All' else 'all times'}**."
    )
    chart_data = (
        filtered[["timestamp", "temp", "humidity"]]
        .set_index("timestamp")
        .rename(columns={"temp": "🌡️ Temp (°C)", "humidity": "💧 Humidity (%)"})
    )
    st.line_chart(chart_data, use_container_width=True)

    df_display = (
        filtered.drop(columns=["timestamp"])
        .sort_values(["date", "time"], ascending=[False, False])
        .rename(
            columns={
                "date": "📅 Date",
                "time": "🕒 Time",
                "city": "🌇 City",
                "country": "🌍 Country",
                "temp": "🌡️ Temp (°C)",
                "humidity": "💧 Humidity (%)",
            }
        )
    )
    st.dataframe(df_display, use_container_width=True)
else:
    st.warning("🚫 No data available for the selected filters.")
