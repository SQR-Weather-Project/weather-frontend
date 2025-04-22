import streamlit as st

st.title("🔔 Notification Settings")

frequency = st.slider("Notification frequency (in minutes)", 5, 60, 15)
temp_threshold = st.number_input("Notify if temperature is above (°C)", value=30)

if st.button("Save settings"):
    st.success("Settings saved (mock)")
