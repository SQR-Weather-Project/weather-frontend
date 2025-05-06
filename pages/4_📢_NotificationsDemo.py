import streamlit as st

from components.notifications import send_push

st.title("Streamlit Push Notifications 📢")
st.divider()

title = st.text_input(
    "Title:",
    placeholder="Input your title for the notification"
)
user_id = st.text_input(
    "user_id:", placeholder="Input your user_id for the notification"
)

if st.button("Push"):
    if not title or not user_id:
        st.error("Title and body must not be empty.")
    else:
        send_push(
            title=title,
            user_id=user_id
        )
        st.success("Push notification sent!")