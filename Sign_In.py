import streamlit as st
import requests
import uuid

from utils.config import BACKEND_URL, FRONTEND_URL, TG_BOT_USERNAME

st.title("Авторизация через Telegram")

token = str(uuid.uuid4())

st.write(f"Сгенерированный ID: `{token}`")

if st.button("Войти через Telegram"):
    try:
        response = requests.post(
            f"{BACKEND_URL}/user/login",
            params={"token": token,
                    "callback_url": f"{FRONTEND_URL}/login_success"})
        if response.status_code == 200:
            st.success("Перейдите в Telegram "
                       "бота для продолжения авторизации.")

            tg_url = f"https://t.me/{TG_BOT_USERNAME}?start={token}"

            st.markdown(
                f'[Открыть Telegram-бота](https://t.me'
                f'/{TG_BOT_USERNAME}?start={token})',
                unsafe_allow_html=True
            )
        else:
            st.error(f"Ошибка при отправке: "
                     f"{response.status_code} — {response.text}")
    except Exception as e:
        st.error(f"Ошибка подключения к бэкенду: {e}")
