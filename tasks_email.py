import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart



sender_email = "tasks.organizer.app@gmail.com"
sender_password = "evze pgjl olhi vtnr"
receiver_email = "ignatyuk.dariaa@gmail.com"

message = MIMEMultipart()
message["From"] = sender_email
message["To"] = receiver_email

def sent_email(table):
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = "Your to do list"

    # Plain text body
    body = table

    message.attach(MIMEText(body, "plain"))

    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, receiver_email, message.as_string()) 