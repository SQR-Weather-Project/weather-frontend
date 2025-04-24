import streamlit as st

st.set_page_config(page_title="Weather App", page_icon="🌤")

st.title("Registration")

username = st.text_input("Username")
location = st.text_input("Location", placeholder="Enter your city")
password = st.text_input("Password", type="password")
password = st.text_input("Repeat password", type="password")

if st.button("Sign Up"):
    st.success("Registration successful (mock)!")
    st.info("Go to the 'Sign In' section from the sidebar.")