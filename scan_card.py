import pickle
from groq import Groq
from PIL import Image
import pytesseract
import mysql.connector

def scan_bus_card(card):
    
    mydb=mysql.connector.connect(
        host='localhost',
        user='root',
        passwd='lol123',
        database='user_files'
    )

    cursor=mydb.cursor()



    client = Groq(
            api_key='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'
        )

    #insert card
    im = Image.open(card)
    pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files/Tesseract-OCR/tesseract.exe'
    text = pytesseract.image_to_string(im, lang='eng+chi_tra')


    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": """
                From this text give me the persons surname, first name, job title, company, address, one phone number, email 
                and give the results separated by a semicolon, specify NULL if it doesn't exist in the card,just give me the results with no other introduction/words, 
                here is the exact example output: Chan; Kalena; Senior Officer, Human Resources and Organizational Development; Nova Credit Limited; Unit A3, 20/F, NCB Innovation Centre, 888 Lai Chi Kok Road, Kowloon, HK; 2120 0381; kalena.chan@nova-credit.com
                here is the text: 
                """
                +text,
            }
        ],
        model="llama3-8b-8192",
    )

    summary=chat_completion.choices[0].message.content
    summary=summary.split('\n')
    summary=summary[0].split(';')
    data=['Surname','First Name','Job Title','Company','Address','Phone No','Email']
    profile={}

    if len(summary)!=7:
        diff=7-len(summary)
        for i in range(diff):
            summary.append('NULL')

    return summary
