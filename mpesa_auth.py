import requests
from requests.auth import HTTPBasicAuth

# Sandbox credentials from developer portal
CONSUMER_KEY = 'bLzrDB5Ve1f1zoRuU1asA5UIzSACksuYxYwgPal4dWQ33FKQ'
CONSUMER_SECRET = 'DxLoR47VyUpLpvJF8zEYCZIQKOHczqKCgJX4n1AFzokYUhGtmbYnrNz5Hx90v9Ck'


def get_access_token():
    url = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"
    response = requests.get(url, auth=HTTPBasicAuth(CONSUMER_KEY, CONSUMER_SECRET))

    if response.status_code == 200:
        token = response.json()['access_token']
        return token
    else:
        raise Exception("Failed to obtain access token")


# Test it
if __name__ == "__main__":
    print("Access Token:", get_access_token())
