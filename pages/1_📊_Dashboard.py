import streamlit as st

from components.weather_card import render_weather_card
from utils.mock_data import get_mock_weather

st.title("🌤 Weather Dashboard")

weather_data = get_mock_weather()
render_weather_card(weather_data)
