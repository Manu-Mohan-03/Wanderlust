"""Here contains classes and methods that directly uses the ORM models for CRUD operations"""
from sqlalchemy.orm import Session
from sqlalchemy import delete, func
from datetime import time

from orm_models import UserSchema, TripSchema, TripLeg, LegFlight, Airport, City, Schedules # SessionLocal
from backend.business_logic.pydantic_models import (
    UserIn, TripIn, TripOut, TripLegIn, LegFlightIn, LegFlightUpdate, TripLegUpdate, TripHeaderUpdate, UserUpdate)

import math

#db = Session()
"""

"""
class SingletonMeta(type):
    """
    Meta Class, This is a factory class which creates other classes.
    Technically normal classes are inherited from object by default, Meta classes are
    inherited from type.
    """
    _instances = {}
    def __call__(cls, *args, **kwargs):
        """
        Normal methods of metaclasses will have cls as first parameter, not self
        Don't confuse with normal classes' class methods which also have cls as first parameter
        """
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]


class SessionManager(metaclass=SingletonMeta):
    #Class Variable
    #_db = SessionLocal()
    def __init__(self, session: Session):
        self._session = session

    @property
    def session(self):
        """Read-only access for all subclasses."""
        return self._session

    def commit(self):
        """To save the Database Updates to underlying database"""
        try:
            self.session.commit()
        except Exception as error:
            self.session.rollback()
            msg = "Database operation Failed:"
            raise RuntimeError(f"{msg}{str(error)}") from error

class UserRepository:
    def __init__(self, session: Session):
        self._db = SessionManager(session)

    @property
    def db(self):
        """Read-only access for all subclasses."""
        return self._db.session

    def is_admin_user(self, user_name):
        # For admin users design is not to set same username
        user = (
            self.db.query(UserSchema)
               .filter(UserSchema.username == user_name, UserSchema.role == "admin").all()
        )
        if user:
            return True
        return False


    def select_user_by_data(self, user_name: str, email: str | None = None):

        if email:
            user = (
                self.db.query(UserSchema)
                .filter(UserSchema.username == user_name, UserSchema.email == email).one()
            )
        else:
            user = (
                self.db.query(UserSchema)
                .filter(UserSchema.username == user_name).one()
            )
        return user

    def create_user(self, user_in: UserIn):

        user = self.select_user_by_data(user_in.name, user_in.email)
        if user:
            raise ValueError("User Data already exists.")
        user = UserSchema(**user_in.model_dump())
        self.db.add(user)
        self._db.commit()
        #db_commit(self.db)
        self.db.refresh(user)

        return user #Return can be made separate pydantic model (UserOut) either here or in handler.py

    def update_user(self, user_db: UserSchema, user_update: UserUpdate):

        new_user = user_update.model_dump(exclude_unset=True)
        for field, value in new_user:
            if hasattr(user_db, field):
                setattr(user_db, field, value)

        self._db.commit()
        self.db.refresh(user_db)

        return user_db

    def delete_user(self, user_id:int):
        """
        In Future can implement "Marked for deletion" can be implemented, but for User ID, it
        doesn't make much sense, it is better to delete it
        """
        """
        Need to delete all the trips that belongs to the user
        But because of cascading settings the trips and all related transaction data should get deleted
        """
        # trips = user.user_trips
        # trips_object = TripRepository(self.db)
        # trips_object.delete_trips(trips)

        user = self.get_user(user_id)
        if not user:
            raise ValueError("User Not found!")

        self.db.delete(user)
        #statement = delete(UserSchema).where(UserSchema.id == user.id)
        #self.db.execute(statement)
        """ # Another way
        user_local = self.db.merge(user)
        self.db.delete(user_local)
        """
        self._db.commit()

    def get_user(self, user_id: int):

        user = self.db.get(UserSchema, user_id)
        return user

    def get_trips_of_user(self):
        pass

    def get_users(self):
        """Admin Method"""
        pass

    def delete_users(self):
        """Admin Method"""
        pass
    """  # If it is only TripSchema, it should be in Trip class not User class
    def delete_trips_of_user(self, trips: list[TripSchema]):
        pass
    """



class TripRepository:
    def __init__(self, session: Session):
        self._db = SessionManager(session)

    @property
    def db(self):
        """Read-only access for all subclasses."""
        return self._db.session

    #def create_trip(self, trip_in: TripModel, commit:bool=False):
    def create_trip(self, trip_in: TripIn, commit:bool=False):

        trip_dict = trip_in.model_dump()
        trip = TripSchema()
        for field, value in trip_dict.items():
            if hasattr(trip, field):
                setattr(trip, field, value)
        #trip = TripSchema(**trip_in.model_dump())
        self.db.add(trip)
        #self.db.flush() #Not needed as relationship is maintained and
                         #properly instantiated using relationship trip_id will get value

        if commit:
            self._db.commit()
            self.db.refresh(trip)
        return trip

    def change_trip(self,trip_db: TripSchema, changed_trip: TripHeaderUpdate, commit:bool=False):

        new_trip = changed_trip.model_dump(exclude_unset=True)
        for field, value in new_trip:
            if hasattr(trip_db, field):
                setattr(trip_db, field, value)

        if commit:
            self._db.commit()
            self.db.refresh(trip_db)
        return trip_db

    #def delete_trip(self, trip: TripOut, commit:bool=False):
    def delete_trip(self, trip_id: int, commit:bool=False):
        """
        Need to delete the corresponding entries from Legs tables
        """
        # statement = delete(TripSchema).where(TripSchema.trip_id == trip.trip_id)
        # self.db.execute(statement)

        trip = self.get_trip(trip_id)
        if not trip:
            raise ValueError("Trip Not found!")

        self.db.delete(trip)
        if commit:
            self._db.commit()


    def get_trip(self, trip_id: int):

        trip = self.db.get(TripSchema, trip_id)
        return trip

    def modify_trip_leg(self, trip_leg_db: TripLeg, new_leg: TripLegUpdate, commit:bool=False):

        new_leg_dict = new_leg.model_dump(exclude_unset=True)
        if new_leg_dict:
            for field, value in new_leg_dict.items():
                if hasattr(trip_leg_db, field):
                    setattr(trip_leg_db, field, value)
        if commit:
            self._db.commit()
        return trip_leg_db

    def change_flight_in_trip(self, flight_db: LegFlight, new_flight: LegFlightUpdate, commit:bool=False):

        new_flight_dict = new_flight.model_dump(exclude_unset=True)
        if new_flight_dict:
            for field, value in new_flight_dict.items():
                if hasattr(flight_db, field ):
                    setattr(flight_db, field, value)

        # merged_flight = self.db.merge(old_flight)
        if commit:
            self._db.commit()
        return flight_db

    def delete_trip_leg(self, trip_leg: TripLeg, commit: bool = False):

        # statement = (delete(TripLeg)
        #             .where(TripLeg.trip_id == trip_leg.trip_id)
        #             .where(TripLeg.leg_no == trip_leg.leg_no)
        # )
        # self.db.execute(statement)
        self.db.delete(trip_leg)
        if commit:
            self._db.commit()

    def delete_flight_from_trip(self, flight: LegFlight, commit: bool=False):

        statement = (delete(LegFlight)
                    .where(LegFlight.trip_id == flight.trip_id)
                    .where(LegFlight.leg_no == flight.leg_no)
        )
        self.db.execute(statement)
        # self.db.delete(flight)
        if commit:
            self._db.commit()

    def add_trip_leg(self, trip_db: TripSchema, leg_in: TripLegIn | TripLegUpdate, commit:bool=False):

        leg_dict = leg_in.model_dump()
        trip_leg = TripLeg(
            trip_id= trip_db.trip_id
        )
        for field, value in leg_dict.items():
            if hasattr(trip_leg, field):
                setattr(trip_leg, field, value)

        self.db.add(trip_leg)

        if commit:
            self._db.commit()
            self.db.refresh(trip_leg)

        return trip_leg

    def add_flight_to_trip(self, trip_leg_db: TripLeg, flight: LegFlightIn | LegFlightUpdate, commit:bool=False):

        leg_flight = LegFlight(
            trip_id= trip_leg_db.trip_id,
            leg_no= trip_leg_db.leg_no,
            flight_id= flight.flight_id
        )
        self.db.add(leg_flight)

        if commit:
            self._db.commit()
            self.db.refresh(leg_flight)
        return leg_flight

    def get_trip_leg(self, trip_id: int, leg_no: int):

        trip_leg = self.db.get(TripLeg, (trip_id, leg_no))
        return trip_leg

    def get_trip_legs(self):
        pass

    def get_flight_for_leg(self, trip_id: int, leg_no: int):

        leg_flight = self.db.get(LegFlight, (trip_id, leg_no))
        if leg_flight:
            #return leg_flight
            return leg_flight.flight_id
        return None

    def commit_db(self, db_object=None):
        self._db.commit()
        if db_object:
            self.db.refresh(db_object)
            return db_object
        return None

class AirportRepo:
    def __init__(self, session: Session):
        self._db = SessionManager(session)

    @property
    def db(self):
        """Read-only access for all subclasses."""
        return self._db.session

    def get_airports_within_radius(self, centre_lat: float, centre_long: float, radius: int = 100 ):
        # Rough bounding box (1 degree ≈ 111 km)
        earth_radius = 6371

        lat_delta = radius / 111
        long_delta = radius / (111 * math.cos(math.radians(centre_lat)))

        lat_rad = math.radians(centre_lat)
        lon_rad = math.radians(centre_long)

        distance = (
                earth_radius * func.acos(
                    func.cos(lat_rad)
                    * func.cos(func.radians(Airport.latitude))
                    * func.cos(func.radians(Airport.longitude) - lon_rad)
                    + func.sin(lat_rad)
                    * func.sin(func.radians(Airport.latitude))
                )
        )

        query = (
            self.db.query(Airport)
            .filter(Airport.latitude.between(centre_lat - lat_delta, centre_lat + lat_delta))
            .filter(Airport.longitude.between(centre_long - long_delta, centre_long + long_delta))
            .filter(distance <= radius)
        )

        return query.all()

    def get_airport(self, code):
        airport = self.db.get(Airport, code)
        if airport:
            return airport
        return False

    def get_city(self, code):
        city = self.db.get(City, code)
        if city:
            return city
        return None

    def get_airport_schedules(self,
                              from_airports: list[str] | None = None,
                              to_airports: list[str] | None = None,
                              dep_time: time | None = None,
                              arr_time: time | None = None
                              ):
        if not from_airports and not to_airports:
            raise Exception("Airports needed to find airport routes!")

        if from_airports:
            query = (
                self.db.query(Schedules)
                .filter(Schedules.orig_airport.in_(from_airports))
            )
            if to_airports:
                query = query.filter(Schedules.dest_airport.in_(to_airports))
        else:
            query = (
                self.db.query(Schedules)
                .filter(Schedules.dest_airport.in_(to_airports))
            )
        if dep_time:
            query = query.filter(Schedules.dep_time >= dep_time )
        if arr_time:
            query = query.filter(Schedules.arr_time <= arr_time)
        routes = query.all()

        return routes


"""
def db_commit(session):
    """"""To save the Database Updates to underlying database""""""
    try:
        session.commit()
    except Exception as error:
        session.rollback()
        msg = "Database operation Failed:"
        raise RuntimeError(f"{msg}{str(error)}") from error
"""