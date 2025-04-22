import streamlit as st


def render_weather_card(data):
    weather = data["weather"][0]
    main = data["main"]
    wind = data["wind"]

    st.subheader(f"🌍 {data['name']}, {data['sys']['country']}")

    icon_url = f"https://openweathermap.org/img/wn/{weather['icon']}@2x.png"
    description = weather["description"].capitalize()

    st.markdown(
        f"""
        <div style='display: flex; align-items: center; gap: 1rem;'>
            <img src="{icon_url}" width="60">
            <div style="font-size: 1.5rem;">
                <strong>{description}</strong>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    col1, col2, col3, col4 = st.columns(4)
    col1.metric(
        "🌡 Temp",
        f"{main['temp']} °C",
        f"Feels like {main['feels_like']}",
        delta_color="off",
    )
    col2.metric("💧 Humidity", f"{main['humidity']}%")
    col3.metric("🌬 Wind", f"{wind['speed']} m/s")
    col4.metric("🧭 Pressure", f"{main['pressure']} hPa")
