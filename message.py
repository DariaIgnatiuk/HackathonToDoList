import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os



def send_email(email, table):
    sender_email = "tasks.organizer.app@gmail.com"
    sender_password = os.getenv('email_pass')
    receiver_email = f"{email}"

    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = "Your to do list"
        # Create the email body with monospace font
    body = f"""
    <html>
      <body>
        <pre style="font-family: monospace;">
          {table}
        </pre>
      </body>
    </html>
    """
    message.attach(MIMEText(body, "html"))

    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, receiver_email, message.as_string()) 
