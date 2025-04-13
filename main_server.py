from flask import Flask, request, jsonify
from flask_cors import CORS  # Import this for CORS
import requests
import base64
from datetime import datetime
from requests.auth import HTTPBasicAuth
import json

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# MPESA Credentials (from Safaricom Developer Portal)
CONSUMER_KEY = 'bLzrDB5Ve1f1zoRuU1asA5UIzSACksuYxYwgPal4dWQ33FKQ'
CONSUMER_SECRET = 'DxLoR47VyUpLpvJF8zEYCZIQKOHczqKCgJX4n1AFzokYUhGtmbYnrNz5Hx90v9Ck'

# Function to get access token
def get_access_token():
    url = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"
    response = requests.get(url, auth=HTTPBasicAuth(CONSUMER_KEY, CONSUMER_SECRET))

    if response.status_code == 200:
        token = response.json()['access_token']
        return token
    else:
        raise Exception("Failed to obtain access token")

# STK Push Route (called from frontend)
@app.route('/api/stkpush', methods=['POST'])
def stk_push():
    data = request.get_json()
    phone = data.get('phone')
    amount = int(data.get('amount'))

    # M-Pesa credentials and settings
    shortcode = "174379"  # Sandbox shortcode
    passkey = "bfb279f9aa9bdbcf158e97dd71a467cd2e0c893059b10f78e6b72ada1ed2c919"  # Get this from the developer portal
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    password = base64.b64encode((shortcode + passkey + timestamp).encode()).decode()

    # M-Pesa request headers
    headers = {
        "Authorization": f"Bearer {get_access_token()}",
        "Content-Type": "application/json"
    }

    # Payload for M-Pesa STK Push request
    payload = {
        "BusinessShortCode": shortcode,
        "Password": password,
        "Timestamp": timestamp,
        "TransactionType": "CustomerPayBillOnline",
        "Amount": amount,
        "PartyA": phone,
        "PartyB": shortcode,
        "PhoneNumber": phone,
        "CallBackURL": "https://your-ngrok-url.ngrok.io/mpesa/callback",  # Use your ngrok URL here
        "AccountReference": "Redeemed Gospel Church",
        "TransactionDesc": "Offering"
    }

    # Send STK Push request to M-Pesa
    response = requests.post(
        "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest",
        json=payload,
        headers=headers
    )

    if response.status_code == 200:
        return jsonify({"message": "STK Push sent successfully!"})
    else:
        return jsonify({"error": "Failed to initiate payment"}), 500

# Callback route to receive response from M-Pesa
@app.route('/mpesa/callback', methods=['POST'])
def mpesa_callback():
    data = request.json
    print("✅ Callback received:")
    print(json.dumps(data, indent=4))

    # Optional: save to a file
    with open('mpesa_payments_log.json', 'a') as f:
        f.write(json.dumps(data) + "\n")

    # Return a success response
    return jsonify({"ResultCode": 0, "ResultDesc": "Callback received successfully"})

if __name__ == '__main__':
    app.run(port=8000)
