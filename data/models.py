import psycopg2

from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from config import load_config


def get_db_url():
    # The format is: dialect+driver://user:password@host:port/database_name
    pgsql = load_config()
    if pgsql is dict:
        return (f"postgresql+psycopg2://{pgsql['user']}:"
                f"{pgsql['password']}@{pgsql['host']}:{pgsql['port']}/{pgsql['database']}")
    return None


# Define the data table class's parent class
class Base(DeclarativeBase):
    pass

class Users(Base):
    pass


class Trips(Base):
    pass


class TripLegs(Base):
    pass


class LegFlight(Base):
    pass


class Country(Base):
    __tablename__ = "country"

    country_key = Column(String, primary_key=True)
    name = Column(String)


class City(Base):
    pass


class Airport(Base):
    pass


class Airline(Base):
    pass


class Schedules(Base):
    pass



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


if __name__ == '__main__':
    engine = create_engine(get_db_url())
    Session = sessionmaker(bind=engine)
    session = Session()
    #connect(config)