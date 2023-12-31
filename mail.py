import smtplib
from email.message import EmailMessage
from key import email,passw


def send_verification_code(user_email,code):
    msg = EmailMessage()
    msg['Subject']  = 'Recuperar senha'
    msg['From'] = email
    msg['To'] = user_email
    msg.set_content(f"Seu código de verificação é: {code}")
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(email, passw)
        smtp.send_message(msg)