from search_face import run_search_face
from compiler_dataframe import run_compiler
from login import login_page
from sendmail import email_ui
import streamlit as st

pages = {
    "Login Page":login_page,
    "Add to data": run_search_face,
    "Compile data": run_compiler,
    "Send a copy":email_ui
}


st.sidebar.title('Navigation')
selection = st.sidebar.radio("Go to", list(pages.keys()))

pages[selection]()