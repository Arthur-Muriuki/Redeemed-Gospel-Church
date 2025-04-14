from flask import Flask, render_template, request, jsonify
from twilio.rest import Client
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# Twilio config
TWILIO_ACCOUNT_SID = os.getenv('TWILIO_ACCOUNT_SID')
TWILIO_AUTH_TOKEN = os.getenv('TWILIO_AUTH_TOKEN')
TWILIO_WHATSAPP_FROM = 'whatsapp:+14155238886'  # Twilio Sandbox number
YOUR_WHATSAPP = os.getenv('YOUR_WHATSAPP')

client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

# Route to serve the home page
@app.route('/')
def home():
    return render_template('Home.html')

# About page
@app.route('/about')
def aboutus():
    return render_template('aboutus.html')

# Giving page
@app.route('/give')
def giving():
    return render_template('giving.html')

# Contact page (GET)
@app.route('/contact', methods=['GET'])
def contactus_page():
    return render_template('contactus.html')

# Contact form submission (POST)
@app.route('/contact', methods=['POST'])
def contactus_submit():  # Renamed this function to avoid conflict
    name = request.form['name']
    email = request.form['email']
    phone = request.form['phone']
    message = request.form['message']

    whatsapp_message = f"""📥 New Contact Message:

👤 Name: {name}
📧 Email: {email}
📱 Phone: {phone}
💬 Message:
{message}"""

    try:
        client.messages.create(
            body=whatsapp_message,
            from_=TWILIO_WHATSAPP_FROM,
            to=YOUR_WHATSAPP
        )
        return jsonify({'status': 'success', 'message': 'WhatsApp message sent!'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
