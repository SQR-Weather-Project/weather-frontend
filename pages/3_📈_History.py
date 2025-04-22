import streamlit as st

from utils.mock_data import get_mock_history

st.title("📈 Weather History")

data = get_mock_history()

st.line_chart(data.set_index("timestamp")[["temp", "humidity"]])
st.dataframe(data)
