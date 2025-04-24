import streamlit as st

st.title("🔔 Notification Settings")

frequency = st.slider("Notification frequency (in minutes)", 5, 60, 15)

options = ["Pressure", "Temperature", "Humidity"]
selected_option = st.selectbox("Please choose a parameter:", options)

above_or_below = ["above", "below"]
selected_type = st.selectbox("Please choose a filter:", above_or_below)

temp_values = ["°C", 15, -70, 70]
press_values = ["hPa", 1013, 900, 1100]
hum_values = ["%", 50, 10, 100]

measurement_value = {
    "Temperature": temp_values,
    "Pressure": press_values,
    "Humidity": hum_values
}

temp_threshold = st.number_input(
    f"Notify if {selected_option} is {selected_type} \
    ({measurement_value[selected_option][0]})",
    value=measurement_value[selected_option][1],
    min_value=measurement_value[selected_option][2],
    max_value=measurement_value[selected_option][3]
    )

cities = ["Kazan", "Innopolis"]
selected_option = st.selectbox("Select a city (optional)", cities)

if st.button("Save settings"):
    st.success("Settings saved (mock)")
