from flask import Flask, request, jsonify
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os
import logging

app = Flask(__name__)

# Setup logging
logging.basicConfig(level=logging.DEBUG)

# Send email function
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
        logging.info("Connecting to Gmail SMTP server...")
        server = smtplib.SMTP(smtp_server, smtp_port)
        logging.debug(f"Connected to SMTP server: {smtp_server}:{smtp_port}")

        logging.info("Starting TLS encryption...")
        server.starttls()
        logging.debug("TLS session started.")

        logging.info("Logging into Gmail SMTP...")
        server.login(from_email, app_password)
        logging.debug(f"Logged in as: {from_email}")

        text = msg.as_string()
        logging.info("Sending email...")
        server.sendmail(from_email, to_email, text)
        server.quit()
        logging.info("Email sent successfully and SMTP connection closed.")

    except Exception as e:
        logging.error(f"Failed to send email: {e}")
        raise e

# Route to handle contact form submission
@app.route('/contact', methods=['POST'])
def contact():
    # Retrieve form data
    name = request.form['name']
    phone = request.form['phone']
    email = request.form['email']
    message = request.form['message']

    # Create the email subject and body
    subject = "New Contact Form Submission"
    body = f"Name: {name}\nPhone: {phone}\nEmail: {email}\nMessage: {message}"

    # Send email directly
    try:
        logging.info("Preparing to send contact form email...")
        send_email(subject, body, "your_email@gmail.com")  # Change this to your desired recipient email
        logging.info("Contact form email sent.")
        return jsonify({"message": "Message received! We will reach out to you soon.", "status": "success"})
    except Exception as e:
        logging.error(f"Error sending email from contact form: {e}")
        return jsonify({"message": f"Error: {e}", "status": "error"})

# Start the Flask app
if __name__ == '__main__':
    # Ensure the correct port for Render is used
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
