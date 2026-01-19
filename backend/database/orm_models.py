"""This program defines all the DB ORM models used for the project"""
import psycopg2

from sqlalchemy import (create_engine, Column, Integer, String, Numeric, Boolean, ForeignKey, DateTime,
                        Time, func, text, ForeignKeyConstraint)
from sqlalchemy.orm import DeclarativeBase, sessionmaker, relationship, Mapped, mapped_column

from .config import load_config
from decimal import Decimal


def get_db_url():
    # The format is: dialect+driver://user:password@host:port/database_name
    pgsql = load_config()
    if type(pgsql) is dict:
        return (f"postgresql+psycopg2://{pgsql['user']}:"
                f"{pgsql['password']}@{pgsql['host']}:{pgsql['port']}/{pgsql['database']}")
    return None


# Define the database table class's parent class
class Base(DeclarativeBase):
    pass

class UserSchema(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String, nullable=False)
    email = Column(String, nullable=True)
    role = Column(String, nullable=False, server_default=text("standard"))
    city = Column(String(3), ForeignKey("city.city_key"), nullable=True)
    country = Column(String(2), ForeignKey("country.country_key"), nullable=True)
    dark_mode = Column(Boolean, server_default=text("false"), nullable=False)
    map_mode = Column(Boolean, server_default=text("false"), nullable=False)
    date_tolerance = Column(Integer, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    city_details = relationship("City", back_populates="users")
    country_details = relationship("Country", back_populates="users")
    user_trips = relationship(
        "TripSchema",
        back_populates="user_details",
        cascade="all, delete-orphan"
    )

class TripSchema(Base):
    __tablename__ = "trips"

    trip_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    name = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    user_details = relationship("UserSchema", back_populates="user_trips")
    trip_details = relationship(
        "TripLeg",
        back_populates="trip_header",
        cascade = "all, delete-orphan"
    )


class TripLeg(Base):
    __tablename__ = "trip_legs"

    trip_id = Column(Integer, ForeignKey("trips.trip_id"), primary_key=True)
    leg_no = Column(Integer, primary_key=True)
    mode = Column(String, server_default=text("flight"), nullable=False)
    origin_city = Column(String(3), ForeignKey("city.city_key"))
    destination_city = Column(String(3), ForeignKey("city.city_key"))
    leg_start = Column(DateTime, nullable=True)
    leg_stop = Column(DateTime, nullable=True)
    saved_at = Column(
        DateTime(timezone=True), nullable=False,
        server_default=func.now(), onupdate=func.now()
    )

    trip_header = relationship("TripSchema", back_populates="trip_details")
    orig_city_details = relationship("City", back_populates="city_from")
    dest_city_details = relationship("City", back_populates="city_to")
    flight_details = relationship(
        "LegFlight",
        back_populates="trip_details",
        cascade= "all, delete-orphan",
        uselist=False
    )

    @staticmethod
    def next_leg_number(session, trip_number, step=10):
        """To find the next leg number per trip_id.
        Do not need this logic if frontend is passing leg_no: (better)
        """
        last = (
            session.query(TripLeg.leg_no)
            .filter_by(trip_id=trip_number)
            .order_by(TripLeg.leg_no.desc())
            .first()
        )
        if last is None:
            return step
        else:
            return last[0] + step
        #return step if last is None else last[0] + step
    """
    Try using the same logic for naming individual trips in the Trips class/model
    session = Session(engine)
    for attempt in range(attempts): # Try up to 3 times
        try:
            new_item = Item(
                header_id=100,
                line_number=Item.next_line_number(session, header_id=100),
                description="New item"
            )
            session.add(new_item)
            session.commit()
            return new_item
        except IntegrityError:
            session.rollback()
            time.sleep(0.1) # Wait 100ms and try again
    raise Exception(f"Could not save after {attempts} attempts")            
    """

class LegFlight(Base):
    __tablename__ = "leg_flight"

    trip_id = Column(Integer, primary_key=True)
    leg_no = Column(Integer, primary_key=True)
    flight_id = Column(String, ForeignKey("schedules.flight_id"))

    __table_args__ = (
        ForeignKeyConstraint(
            ["trip_id", "leg_no"],
            ["trip_legs.trip_id", "trip_legs.leg_no"]
        ),
    )

    flight_data = relationship("Schedules", back_populates="trips")
    trip_details = relationship("TripLeg", back_populates="flight_details")

class Country(Base):
    __tablename__ = "country"

    country_key = Column(String(2), primary_key=True)
    name = Column(String)

    cities = relationship("City", back_populates="country")
    users = relationship("UserSchema", back_populates="country_details")

class City(Base):
    __tablename__ = "city"

    city_key = Column(String(3), primary_key=True)
    name = Column(String)
    country_key = Column(String(2), ForeignKey("country.country_key"))
    # State/province also needed, need to add later
    timezone = Column(String)
    latitude = Column(Numeric)
    longitude = Column(Numeric)

    country = relationship("Country", back_populates="cities")
    airports = relationship("Airport", back_populates="city")
    users = relationship("UserSchema", back_populates="city_details")

    city_from = relationship("TripLeg", back_populates="orig_city_details")
    city_to = relationship("TripLeg", back_populates="dest_city_details")

class Airport(Base):
    __tablename__ = "airport"

    airport_key = Column(String(3), primary_key=True)
    name = Column(String)
    city_key = Column(String(3), ForeignKey("city.city_key"))
    #latitude = Column(Numeric)
    latitude: Mapped[Decimal] = mapped_column(Numeric)
    #longitude = Column(Numeric)
    longitude: Mapped[Decimal] = mapped_column(Numeric)

    city = relationship("City", back_populates="airports")
    airlines = relationship("Airline", back_populates="hub")

    departures = relationship("Schedules", foreign_keys="Schedules.orig_airport",
                              back_populates="orig_airport_details")
    arrivals = relationship("Schedules", foreign_keys="Schedules.dest_airport",
                              back_populates="dest_airport_details")

class Airline(Base):
    __tablename__ = "airline"

    airline_id = Column(String(3), primary_key=True)
    name = Column(String)
    hub_airport = Column(String(3), ForeignKey("airport.airport_key"), nullable=True)
    airline_code = Column(String(2))
    is_defunct = Column(Boolean(), nullable=True )
    logo = Column(String, nullable=True)
    id = Column(Integer)

    hub = relationship("Airport", back_populates="airlines")

class Schedules(Base):
    __tablename__ = "schedules"

    flight_id = Column(String(5), primary_key=True)
    orig_airport = Column(String(3), ForeignKey("airport.airport_key"))
    dest_airport = Column(String(3), ForeignKey("airport.airport_key"))
    status = Column(String, nullable=True)
    dep_time = Column(Time, nullable=True) # HH:MM:SS
    arr_time = Column(Time, nullable=True) # HH:MM:SS(+1)
    airline = Column(String(2),ForeignKey("airport.airport_key"))
    planetype = Column(String, nullable=True)
    operates = Column(String(7), nullable=True)
    validity = Column(String(11), nullable=True)

    orig_airport_details = relationship("Airport", foreign_keys=[orig_airport],
                                        back_populates="departures")
    dest_airport_details = relationship("Airport", foreign_keys=[dest_airport],
                                        back_populates="arrivals")
    trips = relationship("LegFlight", back_populates="flight_data")

def connect(config):
    """ Connect to the PostgreSQL database server """
    # try:
    #     # connecting to the PostgreSQL server
    #     with psycopg2.connect(**config) as conn:
    #         #In psycopg2, the with statement doesn't automatically close the database connection,
    #         # but it does in psycopg3, only transaction is closed in psycopg2.
    #         print('Connected to the PostgreSQL server.')
    #         return conn
    # except (psycopg2.DatabaseError, Exception) as error:
    #     print(error)
    pass

engine = create_engine(get_db_url())
SessionLocal = sessionmaker(bind=engine)
#session = Session()
#connect(config)