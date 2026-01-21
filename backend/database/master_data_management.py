"""To add data to the database tables"""

from backend.api_requests import aviation_stack_api, airlabs_api
import orm_models
#from models import Session, Country

def add_countries():
    countries = airlabs_api.get_countries()
    with orm_models.SessionLocal() as session:
        for values in countries:
            country = orm_models.Country(**values)
            session.add(country)
        session.commit()

def add_cities():
    #cities = airlabs_api.get_cities()
    cities = aviation_stack_api.get_cities()
    with orm_models.SessionLocal() as session:
        for values in cities:
            city = orm_models.City(**values)
            session.add(city)
        session.commit()

def add_airports():
    airports = aviation_stack_api.get_airports()
    with orm_models.SessionLocal() as session:
        for values in airports:
            airport = orm_models.Airport(**values)
            session.add(airport)
            session.commit()

def add_airlines():
    package = 1
    offset = 0
    with orm_models.SessionLocal() as session:
        #last_airline = session.query(models.Airline).order_by(models.Airline.id.desc()).first()
        # if last_airline:
        #     offset = last_airline.id
        # if package > 100:
        #     number_of_calls = (package // 100)
        #     package = 100
        # else:
        #     number_of_calls = 1
        offset = 13159
        package = 1
        number_of_calls = 1
        for i in range(number_of_calls):
            airlines = aviation_stack_api.get_airlines(offset, package)
            offset = offset + package
            for values in airlines:
                airline = orm_models.Airline(**values)
                session.add(airline)
                session.commit()


def add_routes():
    from_airport = input("Enter the airport code: ")
    package = 1000
    offset = 0
    with orm_models.SessionLocal() as session:
        while True:
            routes, new_offset = aviation_stack_api.get_routes(from_airport,package=package, offset=offset)
            for route in routes:
                route = orm_models.Schedules(**route)
                session.add(route)
                session.commit()
            if new_offset == 0:
                break
            else:
                offset = new_offset
            if package < 1000: #For testing
                break


def clear_cities_table():
    with orm_models.SessionLocal() as session:
        try:
            session.query(orm_models.City).delete(synchronize_session="fetch")
            session.commit()
            print(f"Successfully deleted all data from table '{orm_models.City.__tablename__}'.")
        except Exception as e:
            session.rollback()
            print("Error during deletion", e)


if __name__ == "__main__":
    #add_cities()
    #add_airports()
    #add_airlines()

    add_routes()