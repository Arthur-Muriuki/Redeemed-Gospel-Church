from flask import Flask, request, jsonify
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os

app = Flask(__name__)

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

    # Send email
    try:
        send_email(subject, body, "your_email@gmail.com")  # Change this to your desired recipient email
        return jsonify({"message": "Message received! We will reach out to you soon.", "status": "success"})
    except Exception as e:
        return jsonify({"message": f"Error: {e}", "status": "error"})

# Start the Flask app
if __name__ == '__main__':
    app.run(debug=True)
