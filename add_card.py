import streamlit as st
import os
from scan_card import scan_bus_card
import mysql.connector
from PIL import Image
import time
mydb=mysql.connector.connect(
        host='localhost',
        user='root',
        passwd='lol123',
        database='user_files'
    )

cursor=mydb.cursor()

def save_file(file):
    #add your own folder
    folder="C:/Users/chris/OneDrive/Documents/Python Projects/Face Networking/Cards"
    with open(os.path.join(folder,file.name),'wb') as f:
        f.write(file.getbuffer())
    
    return os.path.join(folder,file.name)

def addInfo(a,b,c,d,e,f,g):
            cursor.execute("INSERT INTO business_cards VALUES (%s,%s,%s,%s,%s,%s,%s)",(a,b,c,d,e,f,g))
            mydb.commit()

def start_add_card():

    logo=Image.open('Tap-Smart Logo-1.png').resize((150,100))
    st.image(logo)

    uploaded_file = st.file_uploader("Upload Business Card", accept_multiple_files=False)

    def cache():
        st.session_state.surname=st.session_state.a
        st.session_state.firstname=st.session_state.b
        st.session_state.job_title=st.session_state.c
        st.session_state.company=st.session_state.d
        st.session_state.address=st.session_state.e
        st.session_state.phoneno=st.session_state.f
        st.session_state.email=st.session_state.g

    if uploaded_file:
        path=save_file(uploaded_file)
        profile=scan_bus_card(path)
        st.session_state.surname=profile[0]
        st.session_state.firstname=profile[1]
        st.session_state.job_title=profile[2]
        st.session_state.company=profile[3]
        st.session_state.address=profile[4]
        st.session_state.phoneno=profile[5]
        st.session_state.email=profile[6]
        with st.form (key="Profile Setup"):
            Surname = st.text_input("Surname", value=st.session_state.surname,key='a').strip()
            Firstname = st.text_input("First Name", value=st.session_state.firstname,key='b').strip()
            Job_title = st.text_input("Job Title", value=st.session_state.job_title,key='c').strip()
            Company = st.text_input("Company", value=st.session_state.company,key='d').strip()
            Address = st.text_input("Address", value=st.session_state.address,key='e').strip()
            PhoneNo = st.text_input("Phone Number", value=st.session_state.phoneno,key='f').strip()
            Email = st.text_input("Email", value=st.session_state.email,key='g').strip()
            submit_1=st.form_submit_button(label='Submit Profile',on_click=cache)
            
        if submit_1:
            addInfo(Surname,Firstname,Job_title,Company,Address,PhoneNo,Email)
            st.success('Database Updated')
            time.sleep(2)
            for key in st.session_state.keys():
                del st.session_state[key]
            st.rerun()


