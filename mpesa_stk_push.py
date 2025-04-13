import requests
from datetime import datetime
import base64
from mpesa_auth import get_access_token

# === M-PESA SANDBOX CONFIG ===
shortcode = "174379"  # Paybill for testing
passkey = "bfb279f9aa9bdbcf158e97dd71a467cd2e0c893059b10f78e6b72ada1ed2c919"  # From Daraja Portal
phone_number = "254743596344"  # A Safaricom test phone number
amount = 10  # Amount you want to charge (can be dynamic)

# === Generate password (base64 encoded) ===
timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
data_to_encode = shortcode + passkey + timestamp
encoded_password = base64.b64encode(data_to_encode.encode()).decode('utf-8')

# === Prepare headers ===
headers = {
    "Authorization": f"Bearer {get_access_token()}",
    "Content-Type": "application/json"
}

# === STK Push Payload ===
payload = {
    "BusinessShortCode": shortcode,
    "Password": encoded_password,
    "Timestamp": timestamp,
    "TransactionType": "CustomerPayBillOnline",
    "Amount": amount,
    "PartyA": phone_number,  # The number paying
    "PartyB": shortcode,
    "PhoneNumber": phone_number,  # The number receiving the push
    "CallBackURL": "https://ngrok.com/r/iep  ",  # Replace with your own or mock
    "AccountReference": "Redeemed Gospel Church",
    "TransactionDesc": "Offering"
}

# === Make the request ===
stk_push_url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
response = requests.post(stk_push_url, json=payload, headers=headers)

# === Print response ===
print("Status:", response.status_code)
print("Response:", response.json())
