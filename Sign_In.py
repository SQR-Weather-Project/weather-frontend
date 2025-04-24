import streamlit as st

st.set_page_config(page_title="Weather App", page_icon="🌤")

st.title("🌦 Welcome to Weather App!")

username = st.text_input("Username")
location = st.text_input("Location", placeholder="Enter your city")
password = st.text_input("Password", type="password")

st.markdown("---")

if st.button("Login"):
    st.success("Login successful (mock)!")
    st.info("Go to the '📊 Dashboard' section from the sidebar.")

st.page_link("pages/SignUp.py", label="Don't have an account? Sign Up")
