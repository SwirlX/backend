import random
import string
import smtplib 
import ssl



def generate_reset_code():
    '''
    This is a function that will be used to generate an alphanumeric code of
    8 characters long. 
    Characters will include numerics 0-9, alpabetics a-z and A-Z.
    '''
    code = ''.join(random.choices(string.ascii_letters + string.digits, k=16))
    
    return code 

def send_reset_code(email, reset_code):
    
    port = 465 
    smtp_server = "smtp.gmail.com"
    sender_email = "farhanzahin368@gmail.com"
    sender_password = "bduznhytpwevlwrj"
    receiver_email = email
    
    # Email body
    message = f"""\
    Subject: Personal password reset code

    Hi,

    Your personal password reset code is: {reset_code} . 

    This message is sent from the team at NameThisMovie."""
    
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, receiver_email, message)
