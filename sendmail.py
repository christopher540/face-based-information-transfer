import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
import os
import streamlit as st
from PIL import Image

def send_mail(receiver_emails,csv):
    """
    Send an email with an attached CSV file to multiple recipients.

    :param csv: Path to the CSV file to be attached.
    :param receiver_emails: List of email addresses to send the email to.
    """
    # Set the email parameters
    sender_email = "christophereleazar4@gmail.com"
    subject = "Networking CSV File"
    body = "Please find the attached CSV file in this email."

    # Create the email message
    msg = MIMEMultipart()
    msg['Subject'] = subject
    msg['From'] = sender_email
    msg['To'] = ", ".join(receiver_emails)  # Join the list of emails into a single string
    msg.attach(MIMEText(body, 'plain'))

    # Attach the CSV file
    csv_file = csv
    with open(csv_file, 'rb') as f:
        attachment = MIMEApplication(f.read(), _subtype="csv")
        attachment.add_header('Content-Disposition', 'attachment', filename=os.path.basename(csv_file))
        msg.attach(attachment)

    # Send the email
    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
            smtp.starttls()
            smtp.login(sender_email, 'kkzj acgl zhkc evkv')
            smtp.send_message(msg)
            return True
    except:
        return False

def email_ui():
    logo=Image.open('Tap-Smart Logo-1.png').resize((150,100))
    st.image(logo)
    st.title("Get a copy")
    with st.form("email"):
        email=st.text_input('List of emails seperated with commas "(abc@mail.com,def@mail.com.... )"')
        submit=st.form_submit_button('Send')
        if submit:
            email=email.split(',')
            if send_mail(email,'export.csv'):
                st.success('Email Sent!')
            else:
                st.error('Send fail')
    


