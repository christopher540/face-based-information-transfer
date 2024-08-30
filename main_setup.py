import streamlit as st
from add_card import start_add_card
from add_face import start_add_face

pages = {
    "Add Face": start_add_face,
    "Add card": start_add_card,
}


st.sidebar.title('Navigation')
selection = st.sidebar.radio("Go to", list(pages.keys()))

pages[selection]()
