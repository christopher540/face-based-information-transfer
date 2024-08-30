import streamlit as st
import mysql.connector
import os
from PIL import Image

def login_page():
    logo=Image.open('Tap-Smart Logo-1.png').resize((150,100))
    st.image(logo)
    with st.form (key="Profile Setup"):
        username = st.text_input("username").strip()
        password=st.text_input("Password",type='password')
        submit_1=st.form_submit_button(label='Log in')
        if submit_1:
            if os.path.exists('dataframe/data.pkl'):
                os.remove('dataframe/data.pkl')
            st.success("Login Successful")
