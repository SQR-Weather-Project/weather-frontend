import streamlit as st
from streamlit_local_storage import LocalStorage

localS = LocalStorage()
st.set_page_config(page_title="Успешный вход")

st.title("✅ Вход прошёл успешно!")

params = st.query_params
token = params.get("token", [""])
telegram_id = params.get("telegram_id", [""])
auth_token = params.get("authorization_token", [""])

st.write("Вы успешно вошли в систему. Параметры сохранены в localStorage.")

localS.setItem("weather_token", token, key="set-token")
localS.setItem("weather_telegram_id", telegram_id, key="set-telegram_id")
localS.setItem("weather_auth_token", auth_token, key="set-auth_token")
