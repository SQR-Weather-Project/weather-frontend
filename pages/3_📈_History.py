import streamlit as st
import json
from datetime import datetime
from pathlib import Path
import pandas as pd

def get_mock_history() -> pd.DataFrame:
    path = Path("utils/history.json")
    with path.open("r", encoding="utf-8") as f:
        raw = json.load(f)

    records = []
    for entry in raw:
        timestamp = datetime.strptime(entry["lastupdate"]["value"], "%Y-%m-%dT%H:%M:%S")
        city_data = entry["city"]
        city = city_data["name"]
        country = city_data["country"]
        temp = entry["temperature"]["value"]
        humidity = entry["humidity"]["value"]
        records.append({
            "timestamp": timestamp,
            "date": timestamp.date().isoformat(),
            "city": city,
            "country": country,
            "temp": round(temp - 273.15, 2),
            "humidity": humidity
        })

    return pd.DataFrame(records)

st.set_page_config(page_title="Weather History", page_icon="📈", layout="centered")
st.title("📈 Weather History")

try:
    data = get_mock_history()
except Exception as e:
    st.error(f"⚠️ Failed to load data: {e}")
    st.stop()

with st.expander("🔎 Filters", expanded=True):
    col1, col2, col3 = st.columns(3)

    with col1:
        countries = ["All"] + sorted(data["country"].unique())
        selected_country = st.selectbox("🌍 Country", countries)

    with col2:
        if selected_country == "All":
            cities = sorted(data["city"].unique())
        else:
            cities = sorted(data[data["country"] == selected_country]["city"].unique())
        city_options = ["All"] + cities
        selected_city = st.selectbox("🌆 City", city_options)

    with col3:
        if selected_city == "All":
            dates = sorted(data["date"].unique())
        else:
            dates = sorted(data[data["city"] == selected_city]["date"].unique())
        date_options = ["All"] + dates
        selected_date = st.selectbox("📅 Date", date_options)

filtered = data.copy()
if selected_country != "All":
    filtered = filtered[filtered["country"] == selected_country]
if selected_city != "All":
    filtered = filtered[filtered["city"] == selected_city]
if selected_date != "All":
    filtered = filtered[filtered["date"] == selected_date]

if not filtered.empty:
    st.markdown("### 📊 Weather Summary")
    st.caption(f"Showing data for **{selected_city if selected_city != 'All' else 'all cities'}**, **{selected_country if selected_country != 'All' else 'all countries'}** on **{selected_date if selected_date != 'All' else 'all dates'}**.")

    chart_data = filtered[["timestamp", "temp", "humidity"]].set_index("timestamp").rename(columns={
        "temp": "🌡️ Temp (°C)",
        "humidity": "💧 Humidity (%)"
    })
    st.line_chart(chart_data, use_container_width=True)

    st.dataframe(
        filtered.drop(columns=["timestamp"]).sort_values("date", ascending=False).rename(columns={
            "date": "📅 Date",
            "city": "🏙️ City",
            "country": "🌍 Country",
            "temp": "🌡️ Temp (°C)",
            "humidity": "💧 Humidity (%)"
        }),
        use_container_width=True
    )
else:
    st.warning("🚫 No data available for the selected filters.")
