from datetime import datetime, time
from pydantic import BaseModel, Field, AliasPath
from enum import Enum


class AirportModel(BaseModel):
    airport_key: str = Field(validation_alias="iata")
    name: str
    city_key: str = Field(validation_alias="municipalityName")
    latitude: float = Field(
        validation_alias=AliasPath("location","lat")
    )
    longitude: float = Field(
        validation_alias=AliasPath("location", "lon")
    )
    model_config = {
        "from_attributes": True,
        "extra": "ignore"
    }


class CityModel(BaseModel):
    city_key: str
    name: str
    country_key: str
    timezone: str
    latitude: float
    longitude: float
    airports: list[AirportModel]
    model_config = {
        "from_attributes": True
    }


class CountryModel(BaseModel):
    country_key: str
    name: str
    cities: list[CityModel]
    model_config = {
        "from_attributes": True
    }


class AirlineModel(BaseModel):
    airline_id: str  # ICAO code (International Civil Aviation Organization)
    name: str
    airline_code: str  # IATA code (International Air Transport Association)
    hub_airport: str
    hub: AirportModel
    model_config = {
        "from_attributes": True
    }


class RouteModel(BaseModel):
    # Master Table (Schedules)
    flight_id: str
    orig_airport: str
    dest_airport: str
    status: str | None
    dep_time: time
    arr_time: time
    airline: str
    planetype: str
    operates: str
    validity: str
    orig_airport_details: AirportModel
    dest_airport_details: AirportModel
    model_config = {
        "from_attributes": True
    }


class AirportRoutes(BaseModel):
    airport_key: str
    name: str
    city_key: str
    latitude: float
    longitude: float
    departures: RouteModel
    arrivals: RouteModel
    model_config = {
        "from_attributes": True
    }


class LegFlightOut(BaseModel):
    trip_id: int
    leg_no: int
    flight_id: str
    flight_data: RouteModel
    model_config = {
        "from_attributes": True
    }


class LegFlightIn(BaseModel):
    flight_id: str


class TripLegOut(BaseModel):
    trip_id: int
    leg_no: int
    mode: str | None = "flight"
    origin_city: str
    destination_city: str
    leg_start: datetime | None = None
    leg_stop: datetime | None = None
    saved_at: datetime
    flight_details: LegFlightOut | None = None
    model_config = {
        "from_attributes": True
    }


class TripLegIn(BaseModel):
    leg_no: int
    mode: str | None = "flight"
    origin_city: str
    destination_city: str
    leg_start: datetime | None = None
    leg_stop: datetime | None = None
    flight: LegFlightIn


class TripOut(BaseModel):
    trip_id: int
    user_id: int
    name: str | None
    created_at: datetime
    trip_details: list[TripLegOut]
    model_config = {
        "from_attributes": True
    }


class TripIn(BaseModel):
    user_id: int
    name: str | None
    trip_legs: list[TripLegIn]

"""
class TripUpdateType(str, Enum):
    trip = "trip"
    leg = "leg"
    flight = "flight"
"""

class UpdateMode(str, Enum):
    insert = "I"
    update = "U"
    delete = "D"


class TripHeaderUpdate(BaseModel):
    trip_id: int
    name: str | None


class TripLegUpdate(BaseModel):
    leg_no: int
    mode: str | None = "flight"
    origin_city: str
    destination_city: str
    leg_start: datetime | None = None
    leg_stop: datetime | None = None
    update_mode: UpdateMode


class LegFlightUpdate(BaseModel):
    leg_no: int
    flight_id: str
    update_mode: UpdateMode


class TripUpdate(BaseModel):
    #update_types: list[TripUpdateType]
    trip_header: TripHeaderUpdate
    trip_leg: list[TripLegUpdate] | None = None
    trip_flight: list[LegFlightUpdate] | None = None


class UserOut(BaseModel):
    id: int
    name: str
    email: str | None = None
    role: str = "normal"
    city: str | None = None
    country: str | None = None
    dark_mode: bool = False
    map_mode: bool = False
    date_tolerance: int | None = None
    created_at: datetime
    user_trips: list[TripOut] | None = None
    city_details: CityModel
    model_config = {
        "from_attributes": True
    }


class UserIn(BaseModel):
    name: str
    email: str | None = None
    role: str = "normal"
    city: str | None = None
    country: str | None = None
    dark_mode: bool = False
    map_mode: bool = False
    date_tolerance: int | None = None

class UserUpdate(BaseModel):
    id: int
    name: str | None = None
    email: str | None = None
    role: str = "normal"
    city: str | None = None
    country: str | None = None
    dark_mode: bool = False
    map_mode: bool = False
    date_tolerance: int | None = None