from sklearn.neighbors import KNeighborsClassifier
import cv2
import numpy as np
import pickle
import os
from collections import Counter
import mysql.connector
import pandas as pd
import streamlit as st
from PIL import Image

def find_most_common(string_list):
    """
    Finds the most common element in a list of strings.
    
    Parameters:
    string_list (list): A list of strings.
    
    Returns:
    str: The most common element in the list.
    """
    # Use the Counter class from the collections module to count the occurrences of each element
    counts = Counter(string_list)
    
    # Find the element with the highest count
    most_common = counts.most_common(1)[0][0]
    
    return most_common

def run_search_face():
    logo=Image.open('Tap-Smart Logo-1.png').resize((150,100))
    st.image(logo)
    st.title("Let's Connect")
    if st.button('Click here to find person', key='add_person'):
        video=cv2.VideoCapture(0)
        face_detect=cv2.CascadeClassifier('data/haarcascade_frontalface_default.xml')

        with open('data/names.pkl','rb') as f:
            LABELS=pickle.load(f)

        with open('data/faces_data.pkl','rb') as f:
            FACES=pickle.load(f)

        knn=KNeighborsClassifier(n_neighbors=5)

        knn.fit(FACES,LABELS)

        names=[]
        placeholder=st.empty()
        while True:
            ret,frame=video.read()
            window_width = 800  # Set the desired window width
            window_height = 600  # Set the desired window height
            frame = cv2.resize(frame, (window_width, window_height))
            cvt_frame=cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
            placeholder.image(cvt_frame)
            gray=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
            faces=face_detect.detectMultiScale(gray,1.2,5)
            for (x,y,w,h) in faces:
                crop_img=frame[y:y+h,x:x+w,:]
                resized_img=cv2.resize(crop_img,(50,50)).flatten().reshape(1,-1)
                output=knn.predict(resized_img)
                names.append(str(output))
                cv2.putText(frame,str(output[0]),(x,y-15),cv2.FONT_HERSHEY_COMPLEX,1,(255,255,255),1)
                cv2.rectangle(frame,(x,y),(x+w,y+h),(50,50,255),2)

            cv2.imshow('Camera',frame)
            k=cv2.waitKey(1)
            if k==ord('q') or len(names)==20:
                break
        st.write('Name: '+output)

        video.release()
        cv2.destroyAllWindows()
        result=find_most_common(names)
        result=result[2:-2]

        mydb = mysql.connector.connect(
            host='localhost',
            user='root',
            passwd='lol123',
            database='user_files'
            )

        cursor = mydb.cursor()


        query = """
                SELECT *
                FROM business_cards AS U
                WHERE U.SURNAME = %s AND U.FIRST_NAME = %s
                """

        given_name,surname=result.split(' ')
        cursor.execute(query,(surname,given_name))
        results=cursor.fetchall()

        if 'data.pkl' not in os.listdir('dataframe/'):
            with open('dataframe\data.pkl','wb') as f:
                pickle.dump(results,f)
        else:
            with open('dataframe\data.pkl','rb') as f:
                temp=pickle.load(f)
                temp.append(results[0])
                with open('dataframe\data.pkl','wb') as f:
                    pickle.dump(temp,f)
                    st.success('Face found!')
    
   
                