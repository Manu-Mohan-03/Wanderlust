""" This API is ideal for airline routes, nearby airports and airport/city search.
It is not ideal for airport routes as it gives the city details served by from specific airports.
Only ideal for a view only purpose."""
import requests
import os
import time
from dotenv import load_dotenv

load_dotenv()
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
# Token endpoint URL
TOKEN_URL = "https://test.api.amadeus.com/v1/security/oauth2/token"

#Base url
BASE_URL = "https://test.api.amadeus.com/v1/"


def get_token():

    # Form database (URL-encoded)
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
        #print("Access Token:", token_data["access_token"])
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
        self._get_new_token()

    def _get_new_token(self):
        """Fetch a new access token from the authorization server."""
        data = {
            "grant_type": "client_credentials",
            "client_id": CLIENT_ID,
            "client_secret":CLIENT_SECRET
        }
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        response = self.session.post(TOKEN_URL, data=data, headers=headers)
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

    def get_request(self, endpoint, **kwargs):
        """Perform a GET request with automatic token handling."""
        self._ensure_token()
        url = f"{self.base_url.rstrip('/')}/{endpoint.lstrip('/')}"
        #response = self.session.get(url, **kwargs)
        response = self.session.get(url, params=kwargs)
        response.raise_for_status()
        return response.json()


    def get_relevant_nearby_airports(self, latitude, longitude):
        endpoint = "/reference-data/locations/airports"
        airports = self.get_request(endpoint, latitude=latitude, longitude=longitude, radius=500)
        print(airports)


    def get_location_by_freetext(self, freetext: str, country_code: str | None = None):
        """To get the city or airport details based on free text """
        endpoint = "/reference-data/locations"
        if country_code:
            locations = self.get_request(endpoint, subType="CITY,AIRPORT", keyword=freetext, countryCode=country_code)
        else:
            locations = self.get_request(endpoint, subType="CITY,AIRPORT", keyword=freetext)
        print(locations)

    def get_routes_from_airport(self, airport_id: str, to_country: str | None = None):
        """This api can provide the list of cities served by a particular airport"""
        endpoint = "airport/direct-destinations"
        if to_country:
            response = self.get_request(endpoint, departureAirportCode=airport_id, arrivalCountryCode=to_country)
        else:
            response = self.get_request(endpoint, departureAirportCode=airport_id)
        destinations = response.get("data")
        dest_city_list = [city.get("iataCode") for city in destinations if city.get("iataCode")]
        return dest_city_list


    def get_destinations_of_airline(self, airline_id: str, to_country: str | None = None):
        """This api can provide the list of cities served by a particular airline, but
        the problem is it won't show source city of the flight. Not all airlines operate in hub
        and spoc setup, in such scenario this endpoint does not meet its purpose. """
        endpoint = "/airline/destinations"
        if to_country:
            response = self.get_request(endpoint, airlineCode=airline_id, arrivalCountryCode=to_country)
        else:
            response = self.get_request(endpoint, airlineCode=airline_id)
        destinations = response.get("data")
        dest_city_list = [city.get("iataCode") for city in destinations if city.get("iataCode")]
        return dest_city_list

    def set_token_for_testing(self, token):
        self.token = token
        self.token_expiry = time.time() + 1800


if __name__ == "__main__":
    api = AmadeusAPIClient(
        base_url=BASE_URL
    )

    # token = input("Enter token for testing the API: ")
    # api.set_token_for_testing(token)
    api.get_routes_from_airport("DXB")