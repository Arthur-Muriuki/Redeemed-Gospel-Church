from flask import Flask, request, jsonify
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os
import logging

app = Flask(__name__)

# Setup logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s [%(levelname)s] - %(message)s')

# Send email function
def send_email(subject, body, to_email):
    from_email = os.getenv("EMAIL_USER")
    app_password = os.getenv("EMAIL_PASSWORD")

    # Validate environment variables
    if not from_email or not app_password:
        error_msg = "⚠️ EMAIL_USER or EMAIL_PASSWORD environment variable not set!"
        logging.error(error_msg)
        raise ValueError(error_msg)

    logging.debug(f"📨 EMAIL_USER: {from_email}")
    logging.debug(f"🔒 EMAIL_PASSWORD is set: {bool(app_password)}")
    logging.debug(f"🎯 Recipient Email: {to_email}")

    smtp_server = "smtp.gmail.com"
    smtp_port = 587

    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    try:
        logging.info("📡 Connecting to Gmail SMTP server...")
        server = smtplib.SMTP(smtp_server, smtp_port)
        logging.debug(f"✅ Connected to: {smtp_server}:{smtp_port}")

        logging.info("🔐 Starting TLS encryption...")
        server.starttls()
        logging.debug("🔒 TLS session started.")

        logging.info("🔑 Logging into Gmail SMTP...")
        server.login(from_email, app_password)
        logging.debug(f"✅ Logged in as: {from_email}")

        logging.info("📤 Sending email...")
        server.sendmail(from_email, to_email, msg.as_string())
        server.quit()
        logging.info("✅ Email sent successfully and connection closed.")

    except Exception as e:
        logging.error(f"❌ Failed to send email: {e}")
        raise e

# Route to handle contact form submission
@app.route('/contact', methods=['POST'])
def contact():
    try:
        name = request.form['name']
        phone = request.form['phone']
        email = request.form['email']
        message = request.form['message']

        subject = "New Contact Form Submission"
        body = f"Name: {name}\nPhone: {phone}\nEmail: {email}\nMessage: {message}"

        logging.info("📬 Preparing to send contact form email...")
        logging.debug(f"📝 Contact Data => Name: {name}, Phone: {phone}, Email: {email}, Message: {message}")

        # You can set a recipient email in env for more flexibility
        to_email = os.getenv("RECIPIENT_EMAIL", "your_email@gmail.com")

        send_email(subject, body, to_email)
        logging.info("✅ Contact form email sent.")
        return jsonify({"message": "Message received! We will reach out to you soon.", "status": "success"})

    except Exception as e:
        logging.error(f"🔥 Error sending email from contact form: {e}")
        return jsonify({"message": f"Error: {e}", "status": "error"})

# Start the Flask app
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
