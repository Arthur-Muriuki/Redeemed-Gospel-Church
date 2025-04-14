from flask import Flask, render_template, request, jsonify
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
import logging

app = Flask(__name__)
logging.basicConfig(level=logging.DEBUG)

def send_email(subject, body, to_email):
    from_email = os.getenv("EMAIL_USER")
    app_password = os.getenv("EMAIL_PASSWORD")

    if not from_email or not app_password:
        raise ValueError("EMAIL_USER or EMAIL_PASSWORD is not set.")

    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(from_email, app_password)
    server.sendmail(from_email, to_email, msg.as_string())
    server.quit()

@app.route('/')
def home():
    return render_template('Home.html')

@app.route('/about')
def aboutus():
    return render_template('aboutus.html')

@app.route('/give')
def giving():
    return render_template('giving.html')

@app.route('/contact', methods=['GET'])
def contactus_page():
    return render_template('contactus.html')

@app.route('/contact', methods=['POST'])
def contactus_submit():
    name = request.form['name']
    email = request.form['email']
    phone = request.form['phone']
    message = request.form['message']

    subject = "New Contact Form Submission"
    body = f"Name: {name}\nEmail: {email}\nPhone: {phone}\nMessage: {message}"
    to_email = os.getenv("RECIPIENT_EMAIL", "your_email@gmail.com")

    try:
        send_email(subject, body, to_email)
        return jsonify({'status': 'success', 'message': 'Message received! We will reach out to you soon.'})
    except Exception as e:
        logging.error(f"Error sending email: {e}")
        return jsonify({'status': 'error', 'message': f"Failed to send message: {e}"})

if __name__ == '__main__':
    app.run(debug=True)
