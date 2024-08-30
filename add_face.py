import cv2
import numpy as np
import pickle
import os
import mysql.connector
import streamlit as st
from scan_card import scan_bus_card
from PIL import Image

def start_add_face():
    logo=Image.open('Tap-Smart Logo-1.png').resize((150,100))
    st.image(logo)
    
    video=cv2.VideoCapture(0)
    face_detect=cv2.CascadeClassifier('data/haarcascade_frontalface_default.xml')
    faces_data=[]

    place_holder=st.empty()
    counters=st.empty()

    with st.form (key="Registration Form"):
        name=st.text_input('Enter your name (Firstname [Space] Surname)')
        submit=st.form_submit_button(label='Submit')

    if submit:
        while True:
            ret,frame=video.read()
            cvt_frame=cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
            gray=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
            faces=face_detect.detectMultiScale(gray,1.2,5)
            for (x,y,w,h) in faces:
                crop_img=frame[y:y+h,x:x+w,:]
                resized_img=cv2.resize(crop_img,(50,50))

                if len(faces_data)<=100:
                    faces_data.append(resized_img)
                
                cv2.putText(frame,str(len(faces_data)),(50,50),cv2.FONT_HERSHEY_COMPLEX,1,(50,50,255),1)
                cv2.rectangle(frame,(x,y),(x+w,y+h),(50,50,255),2)
                place_holder.image(cvt_frame)
                counters.write(str(len(faces_data)))
            #cv2.imshow('Camera',frame)
            k=cv2.waitKey(1)
            if k==ord('q') or len(faces_data)==100:
                break

        video.release()
        cv2.destroyAllWindows()
        place_holder.image('Success.png')

        faces_data=np.array(faces_data)
        faces_data=faces_data.reshape(100,-1)

        if 'names.pkl' not in os.listdir('data/'):
            names=[name]*100
            with open('data/names.pkl','wb') as f:
                pickle.dump(names,f)
        else:
            with open('data/names.pkl','rb') as f:
                names=pickle.load(f)
            names=names+[name]*100
            with open('data/names.pkl','wb') as f:
                pickle.dump(names,f)

        if 'faces_data.pkl' not in os.listdir('data/'):
            with open('data/faces_data.pkl','wb') as f:
                pickle.dump(faces_data,f)
        else:
            with open('data/faces_data.pkl','rb') as f:
                faces=pickle.load(f)
            faces=np.append(faces,faces_data,axis=0)
            with open('data/faces_data.pkl','wb') as f:
                pickle.dump(faces,f)


