import streamlit as st

from components.notifications import send_alert, send_push

st.title("Streamlit Push Notifications 📢")
st.divider()

title = st.text_input(
    "Title:",
    placeholder="Input your title for the notification"
)
body = st.text_input(
    "Body:", placeholder="Input your value (body) for the notification"
)
icon = st.checkbox("Icon:", help="You can add your icons as well")
sound = st.checkbox("Sound:", help="You can add your audio as well")


def get_asset_path(enabled: bool, path: str) -> str:
    return path if enabled else ""


icon_path = get_asset_path(
    icon, "https://cdn-icons-png.flaticon.com/512/1040/1040237.png"
)
sound_path = get_asset_path(
    sound, "https://cdn.pixabay.com/audio/2024/02/19/audio_e4043ea6be.mp3"
)

if st.button("Push"):
    if not title or not body:
        st.error("Title and body must not be empty.")
    else:
        send_push(
            title=title,
            body=body,
            icon_path=icon_path,
            sound_path=sound_path
        )
        st.success("Push notification sent!")

if st.button("Alert"):
    if not body:
        st.error("Body must not be empty.")
    else:
        send_alert(body)
        st.success("Alert sent!")
