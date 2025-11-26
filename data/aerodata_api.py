import requests
import os
from dotenv import load_dotenv

# For API Key
load_dotenv()
RAPID_API_HEADERS =   {
        "x-rapidapi-key": os.getenv("RAPID_API_KEY"),
        "x-rapidapi-host": "aerodatabox.p.rapidapi.com"
    }

def get_airport_by_code(code):

    url = f"https://aerodatabox.p.rapidapi.com/airports/iata/{code}"

    response = requests.get(url, headers=RAPID_API_HEADERS)

    print(response.json())

def search_airports_by_location(latitude,longitude,radius=50):

    url = "https://aerodatabox.p.rapidapi.com/airports/search/location"

    querystring = {"lat": str(latitude), "lon": str(longitude), "radiusKm": str(radius), "limit": "10",
                   "withFlightInfoOnly": "true"}

    response = requests.get(url, headers=RAPID_API_HEADERS, params=querystring)

    print(response.json())


def search_airport_by_ip(ip_address, radius=50):
    url = f"https://aerodatabox.p.rapidapi.com/airports/search/ip"

    querystring = {"q": str(ip_address), "radiusKm": str(radius), "limit": "10", "withFlightInfoOnly": "true"}

    response = requests.get(url, headers=RAPID_API_HEADERS, params=querystring)

    print(response.json())


def search_airport_by_text(text):
    url = "https://aerodatabox.p.rapidapi.com/airports/search/term"

    querystring = {"q": str(text), "limit": "10"}

    response = requests.get(url, headers=RAPID_API_HEADERS, params=querystring)

    print(response.json())

#####################################################################################
def routes_from_airport(airport_code, date=None):
    if date:
        # Date in YYYY-MM-DD format
        url = f"https://aerodatabox.p.rapidapi.com/airports/%7Biata%7D/{airport_code}/stats/routes/daily/{date}"
    else:
        url = f"https://aerodatabox.p.rapidapi.com/airports/%7Biata%7D/{airport_code}/stats/routes/daily/"

    response = requests.get(url, headers=RAPID_API_HEADERS)

    print(response.json())

#get_airport_by_code("BLR")
search_airports_by_location(12.95,77.46, radius=500)