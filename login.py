import streamlit as st
from time import sleep
from navigation import make_sidebar

make_sidebar()


st.title("Dades trasplantament pulmonar 2023 OCATT")

st.write("Inicia sessió per poder veure la informació.")

username = st.text_input("Username")
password = st.text_input("Password", type="password")

if st.button("Log in", type="primary"):
    if username == "pulmonar2023" and password == "d#4h5B":
        st.session_state.logged_in = True
        st.success("Logged in successfully!")
        sleep(0.5)
        st.switch_page("pages/01_Ofertes.py")
    else:
        st.error("Incorrect username or password")