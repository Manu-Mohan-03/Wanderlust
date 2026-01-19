"""API Aero Data, Provides Flight Schedules and Routes"""
import requests
import os
from dotenv import load_dotenv
from pydantic import TypeAdapter

from backend.business_logic.pydantic_models import AirportModel
from backend.utilities.time_travel import (get_current_date, is_valid_date_string,
                                           get_current_datetime, add_duration_to_datetime,
                                           is_dates_in_order)


# For API Key
load_dotenv()
RAPID_API_HEADERS =   {
        "x-rapidapi-key": os.getenv("RAPID_API_KEY"),
        "x-rapidapi-host": "aerodatabox.p.rapidapi.com"
    }
BASE_URL = "https://aerodatabox.p.rapidapi.com/"
def get_airport_by_code(code):

    url = BASE_URL + "airports/iata/{code}"

    response = requests.get(url, headers=RAPID_API_HEADERS)

    print(response.json())

def search_airports_by_location(latitude,longitude,radius=100):

    url = BASE_URL + "airports/search/location"

    querystring = {"lat": str(latitude), "lon": str(longitude), "radiusKm": str(radius), "limit": "10",
                   "withFlightInfoOnly": "true"}

    response = requests.get(url, headers=RAPID_API_HEADERS, params=querystring)

    print(response.json())

    if response.json():
        airports_json = response.json().get("items")
        if airports_json:
            # Take the key from json and use DB to fill the rest of the details of airport
            airports_list = [airport.get("iata") for airport in airports_json]
            #airports = TypeAdapter(list[AirportModel]).validate_python(airports_json) No more needed
            return airports_list #(List of airports iata codes )
    return None


def search_airport_by_ip(ip_address, radius=50):
    url = BASE_URL + "airports/search/ip"

    querystring = {"q": str(ip_address), "radiusKm": str(radius), "limit": "10", "withFlightInfoOnly": "true"}

    response = requests.get(url, headers=RAPID_API_HEADERS, params=querystring)

    print(response.json())


def search_airport_by_text(text):
    url = BASE_URL + "airports/search/term"

    querystring = {"q": str(text), "limit": "10"}

    response = requests.get(url, headers=RAPID_API_HEADERS, params=querystring)

    print(response.json())

#####################################################################################
def routes_from_airport(airport_code, date_str=None):
    """
    Finds the most important or daily routes from an airport. If provided a date, daily routes
    are determined based on the 7 days prior data otherwise based on today's date (API will handle this)
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

    response = requests.get(url, headers=RAPID_API_HEADERS)

    print(response.json())

#####################################API needed for later requirements
def get_airport_schedules(airport_id, from_time = None, duration = 720):
    """
    To get the scheduled departures/arrivals from an airport with in a local time range
    :param airport_id:
    :param from_time:
    :param duration: time duration in minutes
    :return:
    """
    if from_time is None:
        from_time = get_current_datetime()
    else:
        if not is_valid_date_string(from_time):
            raise Exception("Invalid Date string")
    to_time = add_duration_to_datetime(from_time, duration)

    url = BASE_URL + f"flights/airports/iata/{airport_id}/{from_time}/{to_time}"

    querystring = {"withLeg": "true", "direction": "Departure", "withCancelled": "false", "withCargo": "false",
                   "withPrivate": "false", "withLocation": "false"}

    response = requests.get(url, headers=RAPID_API_HEADERS, params=querystring)
    print(response.json())


def get_flight_duration(source, destination):
    """
    To get the approximate travel time between 2 airports
    :param source: IATA code of source airport
    :param destination: IATA code of destination airport
    :return: Duration minutes(Integer)
    """
    url = BASE_URL + f"airports/iata/{source}/distance-time/{destination}"
    querystring = {"flightTimeModel": "ML01"}
    response = requests.get(url, headers=RAPID_API_HEADERS, params=querystring)
    duration_str = response.json().get("approxFlightTime")
    parts = duration_str.split(":")

    hours = parts[0]
    minutes = parts[1]
    duration = int(hours) * 60 + int(minutes)
    return duration


def get_flight_schedules(flight_id, from_date = None, to_date = None):
    """
    Gives the information about the rooster details of a particular flight
    :param flight_id: (IATA Code of the flight eg: LH003)
    :param from_date: format YYYY-MM-DD
    :param to_date:
    :return:
    """
    if flight_id is None:
        raise Exception("Flight ID is required")

    if from_date is None and to_date is None:
        # This is for flight rooster like functionality
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
    response = requests.get(url, headers=RAPID_API_HEADERS)
    print(response.json())


def get_flight_info(flight_id: str, date_str: str = get_current_date()):

    url = BASE_URL + f"flights/number/{flight_id}/{date_str}"
    querystring = {"withAircraftImage": "false", "withLocation": "false", "dateLocalRole": "Departure"}
    response = requests.get(url,headers=RAPID_API_HEADERS, params= querystring)
    print(response.json())

if __name__ == "__main__":
    #get_airport_by_code("BLR")
    search_airports_by_location(12.95,77.46, radius=500)
    #get_flight_schedules("LH003", to_date="2025-12-25")