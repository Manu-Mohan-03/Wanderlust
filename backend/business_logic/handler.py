"""This program defines Pydantic models and works as the Command/Control Centre for the application"""
import re

from datetime import datetime
from sqlalchemy.orm import Session

from backend.database.orm_models import TripSchema, UserSchema
from .pydantic_models import UserIn, UserOut, UserUpdate, TripIn, TripOut,TripUpdate, AirportModel, CityModel

from backend.database.datamanager import UserRepository, TripRepository, AirportRepo
from backend.utilities.where_is_waldo import get_location_from_ip

import backend.api_requests.aerodata_api as aerodata
import backend.api_requests.airlabs_api as airlabs

class User:
    def __init__(self, user_obj: UserIn | UserOut, db_session):
        self.user = user_obj
        self.user_db = UserRepository(db_session)

    def create_user(self): # Save User

        if not isinstance(self.user, UserIn):
            raise TypeError("Wrong Object Type")

        try:
            check_before_save_user(self.user.role, self.user.email)
        except ValueError as error:
            raise ValueError from error

        created_user = self.user_db.create_user(self.user)
        return created_user


    def update_user(self, user_db: UserSchema, user_update: UserUpdate):

        try:
            check_before_save_user(self.user.role, self.user.email)
        except ValueError as error:
            raise ValueError from error

        updated_user = self.user_db.update_user(user_db, user_update)
        return updated_user

    def get_user(self, user_id: int| None = None):

        if not user_id and isinstance(self.user, UserOut):
            user_id = self.user.id
        else:
            raise Exception("User Details cannot be fetched")
        user = self.user_db.get_user(user_id)
        return UserOut.model_validate(user)

    def get_user_by_id(self, user_id):
        pass

    def delete_user(self):
        pass

class Trip:
    def __init__(self, trip_obj: TripIn | TripOut, db_session):
        self.trip = trip_obj
        self.trip_db = TripRepository(db_session)

    def create_trip(self):
        trip_saved = self.trip_db.create_trip(self.trip)
        #Need to create trip_legs
        trip_legs = []
        for leg in self.trip.trip_legs:
            trip_leg = self.trip_db.add_trip_leg(trip_saved,leg)
            trip_leg.flight_details = self.trip_db.add_flight_to_trip(trip_leg, leg.flight)
            trip_legs.append(trip_leg)
        try:
            created_trip = self.trip_db.commit_db(trip_saved)
            return created_trip
            # trip_saved = self.trip_db.commit_db()
            # trip_saved.trip_details = trip_legs
            # return trip_saved
        except:
            raise Exception("Database Operation Failed!")

    def change_trip(self, trip_update: TripUpdate, existing_trip_db: TripSchema):
        # First check if there is a header change
        changed_trip = self.trip
        existing_trip = TripOut.model_validate(existing_trip_db)

        if trip_update.trip_leg:
            for trip_leg in trip_update.trip_leg:
                key = (changed_trip.trip_id, trip_leg.leg_no)
                if trip_leg.update_mode == "I":
                    self.trip_db.add_trip_leg(existing_trip_db,trip_leg)
                else:
                    trip_leg_db = next(
                        (trip_leg for trip_leg in existing_trip_db.trip_details
                         if (trip_leg.trip_id, trip_leg.leg_no) == key), None
                    )
                    match trip_leg.update_mode:
                        case "U":
                            self.trip_db.modify_trip_leg(trip_leg_db,trip_leg)
                        case "D":
                            self.trip_db.delete_trip_leg(trip_leg_db)

        if trip_update.trip_flight:
            for flight in trip_update.trip_flight:
                key = (changed_trip.trip_id, flight.leg_no)
                if flight.update_mode == "I":
                    trip_leg_db = next(
                        (trip_leg for trip_leg in existing_trip_db.trip_details
                         if(trip_leg.trip_id, trip_leg.leg_no) == key), None
                    )
                    self.trip_db.add_flight_to_trip(trip_leg_db, flight)
                else:
                    flight_db = next(
                        (trip_leg.flight_details for trip_leg in existing_trip_db.trip_details
                        if (trip_leg.trip_id,trip_leg.leg_no) == key), None
                    )
                    match flight.update_mode:
                        case "U":
                            self.trip_db.change_flight_in_trip(flight_db, flight )
                        case "D":
                            self.trip_db.delete_flight_from_trip(flight_db)
        if trip_update.trip_header:
            self.trip_db.change_trip(existing_trip_db, trip_update.trip_header)

        try:
            changed_trip = self.trip_db.commit_db(existing_trip_db)
            return changed_trip
        except:
            raise Exception("Database Operation Failed!")


    def get_trip(self, trip_id):
        trip = self.trip_db.get_trip(trip_id)
        if not trip:
            raise ValueError("Trip Not found!")
        return trip

    def delete_trip(self, db_session):
        trip_db = TripRepository(db_session)
        trip_db.delete_trip(self.trip.trip_id, commit=True)


def check_before_save_user(role, email: str | None = None):

    if email and not is_email_valid(email):
        raise ValueError("Invalid Email ID!!")
    if not email and role == "standard":
        raise ValueError("Email ID is needed")

    return True

def is_email_valid(email_id):
    # Regular expression for validating an Email
    regex = r'^[a-z0-9]+[._]?[a-z0-9]+[@]\w+[.]\w+$'
    if re.match(regex, email_id):
        return True
    else:
        return False

def get_user_data(
        db_session,
        user_id: int | None = None,
        username: str | None = None
    ):

    if user_id is None and username is None:
        raise Exception("User Details cannot be retrieved!")

    user_db = UserRepository(db_session)
    if user_id:
        user = user_db.get_user(user_id)
        return user
    elif username:
        user = user_db.select_user_by_data(username)
        return user
    return None


def get_trip_data(
        db_session,
        trip_id: int,
    ):
    trip_db = TripRepository(db_session)
    trip = trip_db.get_trip(trip_id)
    if not trip:
        raise ValueError("Trip Not found!")
    return trip


def delete_trips_by_id(db_session, trips: list):
    trip_db = TripRepository(db_session)
    for trip in trips:
        try:
            trip_db.delete_trip(trip)
        except ValueError:
            raise
    try:
        trip_db.commit_db()
    except Exception:
        raise


def delete_user_by_id(db_session, user_id: int):
    user_db = UserRepository(db_session)
    try:
        user_db.delete_user(user_id)
    except ValueError:
        raise

def get_airports_by_location(db_object, latitude, longitude, radius=100):

    if isinstance(db_object, Session):
        airport_db = AirportRepo(db_object)
    elif isinstance(db_object, AirportRepo):
        airport_db = db_object
    else:
        raise ValueError("Cannot do a DB select to fetch the airports by location")
    # Using Aerodata API
    airport_keys = aerodata.search_airports_by_location(
        latitude, longitude, radius)
    if airport_keys:
        airports_list = airport_db.get_airports(airport_keys)
        return airports_list
    # Using Database
    airports_list = airport_db.get_airports_within_radius(latitude, longitude, radius)
    if airports_list:
        return airports_list
    return None

def find_nearby_airports(db_session, client_meta, radius=100):
    """To find the airports with in the radius of a specific location
    1. Use API
       a.
    2. Use Database Tables
    """
    airport_db = AirportRepo(db_session)
    if client_meta.get("location"):
        # Find airports based on location using API and DB
        latitude = client_meta["location"][0]
        longitude = client_meta["location"][1]
        airports_list = get_airports_by_location(airport_db, latitude, longitude, radius)
        return airports_list

    if client_meta.get("ip"):
        # Find airports based on ip using API directly , if not use function to get location based on IP and the DB to
        # to find airports
        client_ip = client_meta["ip"]
        # Use aerodata first if not use get_location_from_ip function and if not DB
        # Using Aerodata API
        airport_keys = aerodata.search_airport_by_ip(client_ip)
        if airport_keys:
            airports_list = airport_db.get_airports(airport_keys)
            return airports_list
        try:
            location = get_location_from_ip(client_ip)
        except KeyError:
            return None
        if location:
            latitude = location[0]
            longitude = location[1]
            airports_list = get_airports_by_location(airport_db, latitude, longitude, radius)
            return airports_list
    return None


def check_airport(db_session, airport):
    pass

def get_iata_code(db_session, iata_code, iata_type):
    """Check whether IATA code is a city/airport"""
    airport_db = AirportRepo(db_session)
    if iata_type == "airport":
        airport =  airport_db.get_airport(iata_code)
        if airport:
            return AirportModel.model_validate(airport)
    if iata_type == "city":
        city = airport_db.get_city(iata_code)
        if city:
            return CityModel.model_validate(city)
    return None

def get_flights(
        db_session,
        direction: str,
        from_airport: AirportModel | None = None,
        from_city: CityModel | None = None,
        to_airport: AirportModel | None = None,
        to_city: CityModel | None = None,
        timestamp: datetime | None = None,
    ):
    #print(f"{from_airport=},{from_city=},{to_airport=},{to_city=}")
    if not from_airport and not from_city and not to_airport and not to_city:
        raise Exception("Either origin or destination is required!")

    if direction == "Departure":
        dep_time = timestamp.time() if timestamp is not None else None
        arr_time = None
    else:    # (Arrival)
        arr_time = timestamp.time() if timestamp is not None else None
        dep_time = None

    airport_db = AirportRepo(db_session)
    from_airports = []
    to_airports = []

    if from_city:
        from_airports = [airport.airport_key for airport in from_city.airports]
    if from_airport:
        from_airports.append(from_airport.airport_key)
    if to_city:
        to_airports = [airport.airport_key for airport in to_city.airports]
    if to_airport:
        to_airports.append(to_airport.airport_key)

    routes = airport_db.get_airport_schedules(
        from_airports, to_airports, dep_time, arr_time
        )
    if routes:
        return routes

    if timestamp:
        timestamp = timestamp.strftime("%Y-%m-%dT%H:%M")

    # Using Aerodata API
    routes_list = []
    if from_airports is None:
        from_airports = [None]
    else:
        for from_airport in from_airports:
            schedules = aerodata.get_airport_schedules(
                from_airport,
                direction,
                timestamp
                )
            routes_list.extend(schedules)

    if to_airports is None:
        to_airports = [None]
    else:
        for to_airport in to_airports:
            schedules = aerodata.get_airport_schedules(
                to_airport,
                direction,
                timestamp
                )
            routes_list.extend(schedules)

    if routes_list:
        #Insert data to DB
        routes = airport_db.add_routes(routes_list)
        if from_airport and to_airport:
            routes = airport_db.get_airport_schedules(
                from_airports, to_airports, dep_time, arr_time
            )
        return routes
    return None
    #Using Airlabs API
    for from_airport in from_airports:
        for to_airport in to_airports:
            routes_list = airlabs.get_routes(from_airport, to_airport)
    if routes_list:
        routes = airport_db.add_routes(routes_list)
        if timestamp:
            routes = airport_db.get_airport_schedules(
                from_airports, to_airports, dep_time, arr_time
            )
        return routes
    return None






