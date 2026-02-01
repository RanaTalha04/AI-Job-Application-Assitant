import smtplib
from email.message import EmailMessage

def send_email(sender_email, sender_password, recipient_email, email_json):
    print("Function Send Email Called")
    print("From:", sender_email)
    print("To:", recipient_email)
    print("Subject:", email_json["subject"])

    msg = EmailMessage()
    msg["From"] = sender_email
    msg["To"] = recipient_email
    msg["Subject"] = email_json["subject"]
    msg.set_content(email_json["body"])

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(sender_email, sender_password)
        smtp.send_message(msg)

    print("EMAIL SENT")

