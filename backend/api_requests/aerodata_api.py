"""API Aero Data, Provides Flight Schedules and Routes
1. routes from airport:- Cannot find the flights for a specific future date, also it won't show
the departure time and arrival time. it gives more departure data of all the airports served and
which all airlines provide the service
2. get airport schedules : - Provide more realtime of flights departing/arriving at an airport
with dep time and arrival time for any date in future
"""
import requests
import os
from dotenv import load_dotenv
from pydantic import TypeAdapter

from backend.business_logic.pydantic_models import AirportModel
from backend.utilities.time_travel import (get_current_date, is_valid_date_string,
                                           get_current_datetime, add_minutes_to_datetime,
                                           is_dates_in_order, parse_time)


# For API Key
load_dotenv()
RAPID_API_HEADERS =   {
        "x-rapidapi-key": os.getenv("RAPID_API_KEY"),
        "x-rapidapi-host": "aerodatabox.p.rapidapi.com"
    }
BASE_URL = "https://aerodatabox.p.rapidapi.com/"


def call_api(url,params=None):

    if params:
        response = requests.get(url, headers=RAPID_API_HEADERS, params=params)
    else:
        response = requests.get(url, headers=RAPID_API_HEADERS)
    if response.status_code != requests.codes.ok:
        return None
    return response.json()


def get_airport_by_code(code):
    """Airport API: airport by code"""
    url = BASE_URL + "airports/iata/{code}"

    airport_json = call_api(url)
    print(airport_json)


def search_airports_by_location(latitude,longitude,radius=100):
    """Airport API: To get the nearby airports"""
    url = BASE_URL + "airports/search/location"

    querystring = {"lat": str(latitude), "lon": str(longitude), "radiusKm": str(radius), "limit": "10",
                   "withFlightInfoOnly": "true"}

    response_json = call_api(url, querystring)

    print(response_json)

    if response_json:
        airports_json = response_json.get("items")
        if airports_json:
            # Take the key from json and use DB to fetch the additional airport details
            airports_list = [airport.get("iata") for airport in airports_json]
            # Below TypeAdapter No more needed as the logic is changed
            #airports = TypeAdapter(list[AirportModel]).validate_python(airports_json)
            return airports_list #(List of airports iata codes )
    return None


def search_airport_by_ip(ip_address, radius=50):
    url = BASE_URL + "airports/search/ip"

    querystring = {"q": str(ip_address), "radiusKm": str(radius), "limit": "10", "withFlightInfoOnly": "true"}

    response_json = call_api(url, querystring)

    print(response_json())


def search_airport_by_text(text):
    url = BASE_URL + "airports/search/term"

    querystring = {"q": str(text), "limit": "10"}

    response_json = call_api(url, querystring)

    print(response_json)

#####################################################################################
def routes_from_airport(airport_code, date_str=None):
    """ Statistical API
    Finds the most important or daily routes from an airport. If provided a date, daily routes
    are determined based on the 7 days prior data otherwise based on today's date (API will handle this)
    So cannot be used for future dated search, but helpful for a generic read only search
    :param airport_code: IATA code
    :param date_str: YYYY-MM-DD string
    :return: JSON
    """
    if date_str:
        # Date in YYYY-MM-DD format
        if is_valid_date_string(date_str):
            url = BASE_URL + f"airports/iata/{airport_code}/stats/routes/daily/{date_str}"
        else:
            raise Exception("Invalid Date String")
    else:
        url = BASE_URL + f"airports/iata/{airport_code}/stats/routes/daily/"

    response_json = call_api(url)

    #print(response_json)
    routes_json = response_json.get("routes")
    # API provide the destination airports served by the airport along with all airlines that serve the route
    routes_list = [
        {
            "orig_airport": airport_code,
            "dest_airport": route.get("destination").get("iata"),
            "status": "active",
            "airline": [
                airline.get("icao") # Because for airline ICAO is the key field in airline table
                for airline in route.get("operators")
                if airline.get("icao")
            ]
        }
        for route in routes_json
        if route.get("number")
    ]
    return routes_list

#####################################API needed for later requirements
def get_airport_schedules(
        airport_id,
        direction="Departure",
        from_time = None,
        time_period = 720):
    """ Flight API: airport departures and arrivals
    To get the scheduled departures/arrivals from an airport with in a local time range
    :param airport_id:
    :param direction:
    :param from_time:
    :param time_period: time duration in minutes
    :return:
    """
    if from_time is None:
        from_time = get_current_datetime()
    else:
        if not is_valid_date_string(from_time, "%Y-%m-%dT%H:%M"):
            raise Exception("Invalid Date string")
    to_time = add_minutes_to_datetime(
        from_time, time_period, "%Y-%m-%dT%H:%M")

    url = BASE_URL + f"flights/airports/iata/{airport_id}/{from_time}/{to_time}"

    querystring = {"withLeg": "true", "direction": direction, "withCancelled": "false", "withCargo": "false",
                   "withPrivate": "false", "withLocation": "false", }

    response_json = call_api(url, querystring)
    if direction == "Departure":
        schedules_json = response_json.get("departures")
    else:
        schedules_json = response_json.get("arrivals")

    routes_list = [
        {
            "flight_id": route.get("number").replace(" ", ""),
            "orig_airport": airport_id,
            "dest_airport": route.get("arrival").get("airport").get("iata"),
            "status": "active",
            "dep_time": parse_time(route.get("departure").get("scheduledTime").get("local")),
            "arr_time": parse_time(route.get("arrival").get("scheduledTime").get("local")),
            "airline": route.get("airline").get("iata"),
        }
        for route in schedules_json
        if route.get("number")
    ]
    return routes_list

def get_flight_duration(source, destination):
    """Misc API Distance and flight time between airports
    To get the approximate travel time between 2 airports
    :param source: IATA code of source airport
    :param destination: IATA code of destination airport
    :return: Duration minutes(Integer)
    """
    url = BASE_URL + f"airports/iata/{source}/distance-time/{destination}"
    querystring = {"flightTimeModel": "ML01"}

    response_json = call_api(url, querystring)
    duration_str = response_json.get("approxFlightTime")
    parts = duration_str.split(":")

    hours = parts[0]
    minutes = parts[1]
    duration = int(hours) * 60 + int(minutes)
    return duration


def get_flight_schedules(flight_id, from_date = None, to_date = None):
    """Flight API: Flight Departure Dates
    Once a flight is selected from airport schedules, the api will respond with list
    of days on which the flight is operational
    Gives the information about the rooster details of a particular flight
    :param flight_id: (IATA Code of the flight eg: LH003)
    :param from_date: format YYYY-MM-DD
    :param to_date:
    :return:
    """
    if flight_id is None:
        raise Exception("Flight ID is required")

    if from_date is None and to_date is None:
        # This is for flight rooster like functionality but provides operational dates
        # from last one year up to next 8 months(future dates may vary)
        url = BASE_URL + f"flights/number/{flight_id}/dates"
    else:
        if from_date is not None and to_date is None:
            if is_valid_date_string(from_date):
                to_date = from_date
            else:
                raise Exception("Invalid Date String")
        elif from_date is None and to_date is not None:
            if is_valid_date_string(to_date):
                from_date = get_current_date()
            else:
                raise Exception("Invalid Date String")
        else: # Both start and end dates has values
            if not is_dates_in_order(from_date, to_date):
                raise Exception("To date should be later than from date")
        url = BASE_URL + f"flights/number/{flight_id}/dates/{from_date}/{to_date}"
    dates_list = call_api(url)
    print(dates_list)


def get_flight_info(flight_id: str, date_str: str = get_current_date()):
    """Flight API: Flight Status(single day)
    This API provides more technical details about the flights travel. Not relevant for now"""
    url = BASE_URL + f"flights/number/{flight_id}/{date_str}"
    querystring = {"withAircraftImage": "false", "withLocation": "false", "dateLocalRole": "Departure"}
    response = requests.get(url,headers=RAPID_API_HEADERS, params= querystring)
    print(response.json())

if __name__ == "__main__":
    #get_airport_by_code("BLR")
    #search_airports_by_location(12.95,77.46, radius=500)
    #get_flight_schedules("LH003", to_date="2025-12-25")
    get_airport_schedules("BLR", "Departure", "2026-01-25T00:00")