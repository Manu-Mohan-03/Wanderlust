import requests
import os
import time
from dotenv import load_dotenv

load_dotenv()
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
# Token endpoint URL
TOKEN_URL = "https://test.api.amadeus.com/v1/security/oauth2/token"


def get_token():

    # Form data (URL-encoded)
    data = {
        "grant_type": "client_credentials",
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET
    }

    # Header specifying the encoding
    headers = {
     "Content-Type": "application/x-www-form-urlencoded"
    }

    # Make the POST request
    response = requests.post(TOKEN_URL, data=data, headers=headers)

    # Check for success
    if response.status_code == 200:
        token_data = response.json()
        print("Access Token:", token_data["access_token"])
        return token_data["access_token"]
    else:
        print("Error:", response.status_code, response.text)
        return None

def call_api(access_token):

    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    api_url = "https://test.api.amadeus.com/v1/airport/direct-destinations?departureAirportCode=DXB"
    api_response = requests.get(api_url, headers=headers)

    print(api_response.json())



class AmadeusAPIClient:
    def __init__(self, base_url):
        self.base_url = base_url

        self.session = requests.Session()     # Persistent connection
        self.token = None
        self.token_expiry = 0

    def _get_new_token(self):
        """Fetch a new access token from the authorization server."""
        data = {
            "grant_type": "client_credentials",
            "client_id": CLIENT_ID,
            "client_secret":CLIENT_SECRET
        }
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        response = self.session.post(self.token_url, data=data, headers=headers)
        response.raise_for_status()  # raise an error for non-2xx responses
        token_data = response.json()
        self.token = token_data["access_token"]
        self.token_expiry = time.time() + token_data.get("expires_in", 3600) - 60  # refresh 1 min early

        # Attach token to session headers
        self.session.headers.update({"Authorization": f"Bearer {self.token}"})

    def _ensure_token(self):
        """Check if token is expired or missing, and refresh if needed."""
        if not self.token or time.time() > self.token_expiry:
            self._get_new_token()

    def get(self, endpoint, **kwargs):
        """Perform a GET request with automatic token handling."""
        self._ensure_token()
        url = f"{self.base_url.rstrip('/')}/{endpoint.lstrip('/')}"
        response = self.session.get(url, **kwargs)
        response.raise_for_status()
        return response.json()

def call_amadues_object():
    api = AmadeusAPIClient(
        base_url="https://test.api.amadeus.com/v1/"
        )
    endpoint = "airport/direct-destinations"
    flight_info = api.get(endpoint, airport_code="DXB")