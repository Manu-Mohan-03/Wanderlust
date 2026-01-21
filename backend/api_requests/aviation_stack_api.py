"""
To handle the api requests to AviationStack (https://aviationstack.com/)
It can only be used for master data , as their more transactional data API are paid services
Free APIs: -
/v1/airports, /v1/airlines, /v1/airplanes, /v1/aircraft_types,
/v1/cities, /v1/countries, /v1/taxes.
/v1/flights	(Real‑time or historical flights) is not productive as flight date parameter can only be used with
paid plan, and since the limit is 100/api request and flights also considers code shared airlines in the output, each
airport will have lot of entries in response and need to loop and call api for every 100 requests, which makes using
this API is complicated
"""
import requests
import os
from dotenv import load_dotenv
from backend.utilities.time_travel import convert_time

#For API KEY
load_dotenv()
API_KEY = "access_key=" + os.getenv("AVIATION_STACK_APIKEY")
BASE_URL = "https://api.aviationstack.com/v1/"
LIMIT = 1000


def get_countries():
    url = f"{BASE_URL}countries?api_key={API_KEY}&limit={LIMIT}"
    countries_json = call_api(url)[0]
    countries = [
        {"country_key": country["country_iso2"], "name": country["country_name"]}
        for country in countries_json
    ]
    return countries


def get_cities():
    url = f"{BASE_URL}cities?{API_KEY}&limit={LIMIT}"
    total_available_cities = 9374
    offset = 0
    cities = []

    while len(cities) < total_available_cities:
        url_with_offset = url + f"&offset={offset}"
        cities_json = call_api(url_with_offset)[0]
        offset += len(cities_json)
        print(cities_json)
        city_list = [
            {
                "city_key": city["iata_code"],
                "name": city["city_name"],
                "country_key": city["country_iso2"],
                "timezone": city.get("timezone"),
                "latitude": city["latitude"],
                "longitude": city["longitude"]
            }
            for city in cities_json
        ]
        cities.extend(city_list)
        print(len(cities))
    return cities


def get_airports():
    url = f"{BASE_URL}airports?{API_KEY}&limit={LIMIT}"
    total_available_airports = 6702
    offset = 6699
    airports = []

    while len(airports) < total_available_airports:
        url_with_offset = url + f"&offset={offset}"
        airports_json = call_api(url_with_offset)[0]
        offset += len(airports_json)
        print(airports_json)

        airports_list = [
            {
                "airport_key": airport["iata_code"],
                "name": airport["airport_name"],
                "city_key": airport["city_iata_code"],
                "latitude": airport["latitude"],
                "longitude": airport["longitude"]
            }
            for airport in airports_json
        ]
        airports.extend(airports_list)
        print(len(airports))
    return airports

def is_airline_valid(airline: dict):

    airline_types = ["charter", "historical", "cargo", "charter", "private" ]

    if not airline.get("icao_code"):
        return False
    if airline.get("status") != "active":
        return False
    if not airline.get("fleet_size"):
        return False
    if airline.get("type") in airline_types:
        return False
    if not airline.get("iata_code"):
        return False
    return True


def get_airlines(offset=0, package=1000):
    limit = package
    url = f"{BASE_URL}airlines?{API_KEY}&limit={limit}"
    #total_available_airlines = 13164
    airlines = []

    while len(airlines) < package:
        url_with_offset = url + f"&offset={offset}"
        airlines_json = call_api(url_with_offset)[0]
        offset += len(airlines_json)
        print(airlines_json)

        airlines_list = [
            {
                "airline_id": airline["icao_code"],
                "name": airline["airline_name"],
                "hub_airport": airline["hub_code"],
                "airline_code": airline["iata_code"],
                "id": airline["airline_id"]
            }
            for airline in airlines_json
            if is_airline_valid(airline)
        ]
        airlines.extend(airlines_list)
        print(len(airlines))
    return airlines


def get_flight_id(route: dict):
    flight_id = route["airline"]["iata"] + route["flight"]["number"]
    return flight_id

def is_route_valid(route):
    if not route.get("airline").get("iata"):
        return False
    if not route.get("departure").get("time"):
        return False
    if not route.get("arrival").get("time"):
        return False
    return True

def get_routes(
        from_airport,
        to_airport:str|None=None,
        airline_id:str|None=None,
        package=1000, offset=0
    ):
    """Paid plan required"""
    limit = package
    url = f"{BASE_URL}routes?{API_KEY}&limit={limit}&dep_iata={from_airport}"
    if to_airport:
        url = url + f"&arr_iata={to_airport}"
    if airline_id:
        url = url + f"&airline_iata={airline_id}"
    if offset:
        url = url + f"&offset={offset}"

    routes_json, offset = call_api(url)
    print(routes_json)
    routes_list = [
        {
            "flight_id" : get_flight_id(route),
            "orig_airport": route["departure"]["iata"],
            "dest_airport": route["arrival"]["iata"],
            "status": "active",
            "dep_time": route["departure"]["time"],
            "arr_time": route["arrival"]["time"],
            "airline": route["airline"]["iata"]
        }
        for route in routes_json
        if is_route_valid(route)
    ]
    return routes_list


def get_airport_schedules(
        from_airport, airline_id:str|None=None,travel_date: str|None = None, package=1000, offset=0,
):
    """Paid Plan required to use the API. This API cannot filter with arrival airport."""
    limit = package
    if travel_date: # YYYY-MM-DD
        url = f"{BASE_URL}flightsFuture?{API_KEY}&iataCode={from_airport}&date={travel_date}&type=departure"
    else: # two options either use same API with current date or use the real data API for the current data schedule
        url = f"{BASE_URL}timetable?{API_KEY}&iataCode={from_airport}&type=departure"

    if offset:
        url = url + f"&offset={offset}"
    if airline_id:
        url = url + f"&airline_iata={airline_id}"
    url = url + f"&limit={limit}"
    schedules_json = call_api(url)
    print(schedules_json[0])

def call_api(url):
    response = requests.get(url)
    if response.status_code != requests.codes.ok:
        return None
    pagination = response.json()["pagination"]
    offset = 0
    if pagination["total"] > pagination["limit"] + pagination["offset"]:
        offset = pagination["limit"] + pagination["offset"]
    return response.json()["data"], offset

