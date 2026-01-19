"""
To handle the api requests to Airlabs(https://airlabs.co/)
But this api data is not good, junk data for cities with city code not adhering to IATA codes
"""
import requests
import os
from dotenv import load_dotenv

# For API Key
load_dotenv()
API_KEY = os.getenv("AIRLABS_API_KEY")
BASE_URL = "https://airlabs.co/api/v9/"

def get_countries():

    url = f"{BASE_URL}countries?api_key={API_KEY}"
    countries_json = call_api(url)
    countries = [
        {"country_key": country["code"], "name": country["name"]}
        for country in countries_json
    ]
    return countries

def get_cities():
    ### Not good as codes returned are in local language also
    url = f"{BASE_URL}cities?api_key={API_KEY}"
    cities_json = call_api(url)
    cities  = [
        {
            "city_key": city["city_code"],
            "name": city["name"],
            "country_key": city["country_code"],
            "timezone": city.get("time_zone"),
            "latitude": city["lat"],
            "longitude": city["lng"]
        }
        for city in cities_json
    ]
    return cities

def get_airports():
    """Not good as the city details to which the airport is assigned is not available in free tier"""
    url = f"{BASE_URL}airports?api_key={API_KEY}"
    airports_json = call_api(url)
    print(airports_json)


def get_nearby_airports(latitude, longitude, radius = 1):
    url = f"{BASE_URL}nearby?lat={latitude}&lng={longitude}&distance={radius}api_key={API_KEY}"
    airports_json = call_api(url)
    print(airports_json)


def auto_complete(freetext):
    """
    This endpoint returns countries, cities and airports matching the freetext.
    It will also return the cities by country, airports by country, respective
    cities by airports and airports by cities
    """
    url = f"{BASE_URL}suggest?q={freetext}&lang=EN&api_key={API_KEY}"
    suggestions = call_api(url)
    print(suggestions)


def get_routes(from_airport:str, to_airport:str|None =None, airline_id:str|None = None):
    """Generic routes database not uptodate or realtime"""
    url = f"{BASE_URL}routes?api_key={API_KEY}&dep_iata={from_airport}"
    if to_airport:
        url = url + f"&arr_iata={to_airport}"
    if airline_id:
        url = url + f"&airline_iata={airline_id}"

    routes_json = call_api(url)
    print(routes_json)


def get_airport_schedules(from_airport:str, to_airport:str|None =None, airline_id:str|None = None):
    """Upto date data and shows the flights available in the next 10 hours"""
    url = f"{BASE_URL}schedules?api_key={API_KEY}&dep_iata={from_airport}"
    if to_airport:
        url = url + f"&arr_iata={to_airport}"
    if airline_id:
        url = url + f"&airline_iata={airline_id}"
    schedules_json = call_api(url)
    print(schedules_json)

def get_timezones():
    url = f"{BASE_URL}timezones?api_key={API_KEY}"
    timezones_json = call_api(url)
    timezones = [
        {
            "timezone": timezone["timezone"],
            "gmt": timezone["gmt"],
            "dst": timezone["dst"],
            "country_code": timezone["country_code"]
        }
        for timezone in timezones_json
    ]
    print(timezones)


def call_api(url):
    response = requests.get(url)
    if response.status_code != requests.codes.ok:
        return None
    return response.json()["response"]