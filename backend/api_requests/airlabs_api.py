"""
To handle the api requests to Airlabs(https://airlabs.co/)
this api data is not good for cities, junk data for cities with city code not adhering to IATA codes
not suited for airports, as response won't show city details
Real time Flights only shows the flights which are available on flight radar
Airport Schedules/ Routes DB can be used for fetching routes data , but cannot be queried by time,
but response gives back time details
NameSuggestion and nearby airports can be used
"""
import requests
import os
from dotenv import load_dotenv
from backend.utilities.string_theory import weekdays_to_number
from backend.utilities.time_travel import parse_time

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


def get_nearby_airports(latitude, longitude, radius = 1):
    url = f"{BASE_URL}nearby?lat={latitude}&lng={longitude}&distance={radius}&api_key={API_KEY}"
    response = call_api(url)
    airports_json = response.get("airports")
    if airports_json:
        airports_list = [airport.get("iata_code") for airport in airports_json if airport.get("iata_code")]
        print(airports_list)
        return airports_list
    return None


def auto_complete(freetext):
    """
    This endpoint returns countries, cities and airports matching the freetext.
    It will also return the cities by country, airports by country, respective
    cities by airports and airports by cities
    """
    url = f"{BASE_URL}suggest?q={freetext}&lang=EN&api_key={API_KEY}"
    suggestions = call_api(url)
    print(suggestions)


def get_routes(
        from_airport:str|None=None,
        to_airport:str|None=None,
        airline_id:str|None = None
    ):
    """Generic routes database not uptodate or realtime"""
    if not from_airport and not to_airport:
        raise ValueError("From/To Required!!")

    url = f"{BASE_URL}routes?api_key={API_KEY}"
    if from_airport:
        url = url + f"&dep_iata={from_airport}"
    if to_airport:
        url = url + f"&arr_iata={to_airport}"
    if airline_id:
        url = url + f"&airline_iata={airline_id}"

    routes_json = call_api(url)
    routes_list = [
        {
            "flight_id": route.get("flight_iata"),
            "orig_airport" : route.get("dep_iata"),
            "dest_airport": route.get("arr_iata"),
            "status": "active",
            "dep_time": route.get("dep_time"),
            "arr_time": route.get("arr_time"),
            "airline": route.get("airline_iata"),
            "operates": weekdays_to_number(route.get("days"))
        }
        for route in routes_json
        if route.get("flight_iata")
    ]
    return routes_list


def get_airport_schedules(
        from_airport:str|None=None,
        to_airport:str|None=None,
        airline_id:str|None = None
    ):
    """Upto date data and shows the flights available in the next 10 hours"""

    url = f"{BASE_URL}schedules?api_key={API_KEY}"
    if from_airport:
        url = url + f"&dep_iata={from_airport}"
    if to_airport:
        url = url + f"&arr_iata={to_airport}"
    if airline_id:
        url = url + f"&airline_iata={airline_id}"
    schedules_json = call_api(url)
    routes_list = [
        {
            "flight_id": schedule.get("flight_iata"),
            "orig_airport": schedule.get("dep_iata"),
            "dest_airport": schedule.get("arr_iata"),
            "status": "active",
            "dep_time": parse_time(schedule.get("dep_time")),
            "arr_time": parse_time(schedule.get("arr_time")),
            "airline": schedule.get("airline_iata"),
        }
        for schedule in schedules_json
        if schedule.get("flight_iata")
    ]
    return routes_list


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


def get_cities():
    """Not good as codes returned are in local language also
    Use aviation stack"""
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
    """Not good as the city details to which the airport is assigned is not available in free tier.
    Use aviation stack"""
    url = f"{BASE_URL}airports?api_key={API_KEY}"
    airports_json = call_api(url)
    print(airports_json)

def call_api(url):
    response = requests.get(url)
    if response.status_code != requests.codes.ok:
        return None
    return response.json().get("response")

if __name__ == "__main__":
    get_nearby_airports(12.95,77.46, 300)