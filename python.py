import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os


def send_email(subject, body, to_email):
    from_email = os.getenv("EMAIL_USER")  # Fetch from environment variable
    app_password = os.getenv("EMAIL_PASSWORD")  # Fetch from environment variable
    smtp_server = "smtp.gmail.com"
    smtp_port = 587

    # Create the email message
    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    try:
        # Connect to the Gmail SMTP server and send the email
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()  # Secure the connection
        server.login(from_email, app_password)
        text = msg.as_string()
        server.sendmail(from_email, to_email, text)
        server.quit()  # Close the connection
        print("Email sent successfully!")
    except Exception as e:
        print(f"Failed to send email: {e}")


# Example usage:
subject = "New Contact Form Submission"
body = "Name: John Doe\nEmail: john.doe@example.com\nMessage: This is a test message!"
to_email = "your_email@gmail.com"

send_email(subject, body, to_email)
