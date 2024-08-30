import pandas as pd
import pickle
import os
import streamlit as st
from sendmail import send_mail
from PIL import Image
def run_compiler():
    logo=Image.open('Tap-Smart Logo-1.png').resize((150,100))
    st.image(logo)
    st.title('Compile Now')
    df=pd.DataFrame()
    if st.button('Compile Now',key='Compile'):
        if 'data.pkl' in os.listdir('dataframe/'):
            with open('dataframe/data.pkl','rb') as f:
                data=pickle.load(f)
                df=pd.DataFrame(data,columns=['Surname','Firstname','Job_title','Company','Address','PhoneNo','Email'])
                st.dataframe(df)
                csv=df.to_csv('export.csv')




        