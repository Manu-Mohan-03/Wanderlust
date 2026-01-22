from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import Literal
from datetime import datetime
#from pydantic import BaseModel
from backend.business_logic.pydantic_models import (
    UserIn, UserOut, AirportModel, CityModel, RouteModel, TripIn, TripOut, TripUpdate, UserUpdate)
from backend.business_logic.handler import (
    User, Trip, get_user_data, get_nearby_airports, get_flights, get_iata_code, delete_trips_by_id,
    get_trip_data, delete_user_by_id)
from backend.database.orm_models import SessionLocal

import backend.utilities.where_is_waldo as coordinates

router = APIRouter()

def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_from_sources(latitude: float, longitude: float):
    pass


@router.get("/", response_model=list[AirportModel])
async def home_page(
        location: tuple | None = Depends(coordinates.get_location),
        db: Session = Depends(get_db)
    ):
    # Get the nearby airports based IP address or location permission
    # Get the data from the header parameters. Use a custom header parameter
    # X-Latitude/X-Longitude if user is given location permission
    # If not check X-Forwarded-For and use first IP address. If it does not exist
    # use Remote Address (or Remote IP) header. Use a GeoIP Database to Resolve Location
    # The most common, reliable, and widely used tool for retrieving country and city from IP is MaxMind GeoLite2.

    airports_list = get_nearby_airports(db,location[0], location[1])
    return airports_list


@router.get("/{user_name}/", response_model=UserOut)
async def user_signed_in(
            user_name: str,
            db: Session = Depends(get_db)
    ):
    # Show user home screen with saved trip details
    # Determine whether user is normal or admin
    # Location can be based on user profile country or city
    user = get_user_data(db, username=user_name)
    return user


@router.get("/{user_id}/home/", response_model=AirportModel)
async def user_home_page(
        user_id: int,
        location: tuple | None = Depends(coordinates.get_location),
        db: Session = Depends(get_db)
    ):

    user_db = get_user_data(db,user_id)
    user_data = UserOut.model_validate(user_db)

    if user_data.city_details:
        location = (user_data.city_details.latitude, user_data.city_details.longitude)

    airports_list = get_nearby_airports(db,location[0], location[1])
    return airports_list


@router.get("/flights_of/{iata_code}/{iata_type}/", response_model=list[RouteModel])
async def get_flight_routes(
        iata_code: str,
        iata_type: Literal["city","airport"],
        mode: Literal["Departure","Arrival"] = "Departure",
        from_or_to: str | None = None,
        ft_type: Literal["city","airport"] | None = None,
        local_time: datetime | None = None,
        db: Session = Depends(get_db)
    ):
    """direction is either departure/arrival"""
    #1 First check whether code is city/airport
    from_object = to_object = from_airport = to_airport = from_city = to_city = None
    if mode == "dep":
        from_object = get_iata_code(db,iata_code, iata_type)
        if from_or_to:
            to_object = get_iata_code(db, from_or_to, ft_type)
    else:
        to_object = get_iata_code(db, iata_code, iata_type)
        if from_or_to:
            from_object = get_iata_code(db, from_or_to, ft_type)
    if isinstance(from_object, AirportModel):
        from_airport = from_object
    elif isinstance(from_object, CityModel):
        from_city = from_object
    if isinstance(to_object, AirportModel):
        to_airport = to_object
    elif isinstance(to_object, CityModel):
        to_city = to_object
    routes = get_flights(
        db,
        mode,
        from_airport,
        from_city,
        to_airport,
        to_city,
        local_time,
        )

    return routes


@router.post("/trip/", response_model=TripOut)
async def create_trips(
        trip_data: TripIn,
        db: Session = Depends(get_db)
    ):
    trip = Trip(trip_data, db)
    trip_out = trip.create_trip()
    return trip_out

@router.delete("/trip/")
async def delete_trips(
        trips: list[int],
        db: Session = Depends(get_db)
    ):

    delete_trips_by_id(db,trips)

@router.put("/trip", response_model=TripOut)
async def modify_trip(
        trip_data: TripUpdate,
        db: Session = Depends(get_db)
    ):

    trip_db = get_trip_data(db,trip_data.trip_header.trip_id)
    old_trip = TripOut.model_validate(trip_db)

    trip = Trip(old_trip, db)
    trip_out = trip.change_trip(trip_data, trip_db)
    return trip_out

@router.get("/user/{user_name}")
async def get_user(user_name:str):
    # This shows the account details
    pass

@router.post("/user/", response_model=UserOut)
async def create_user(
        user_data: UserIn,
        db: Session = Depends(get_db)
        ):
    # To create a user
    user = User(user_data, db)
    new_user = user.create_user()
    return new_user

@router.put("/user/", response_model=UserOut)
async def modify_user(
        user_data: UserUpdate,
        db: Session = Depends(get_db)
    ):
    user_db = get_user_data(db, user_data.id)
    existing_user = UserOut.model_validate(user_db)

    user = User(existing_user, db)
    modified_user = user.update_user(user_db, user_data)
    return modified_user

@router.delete("/user/{user_id}")
async def delete_user(
        user_id: int,
        db: Session = Depends(get_db)
    ):
    delete_user_by_id(db, user_id)



