from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

def get_from_sources(latitude: float, longitude: float):
    pass

def get_nearby_airports(location: str):
    pass


def get_location_from_ip(ip_address: str):

    city = "Cologne"
    country = "Germany"

    return city, country

@app.get("/")
async def data_for_home():
    # Get the nearby airports based IP address or location permission
    # Get the data from the header parameters. Use a custom header parameter
    # X-Latitude/X-Longitude if user is given location permission
    # If not check X-Forwarded-For and use first IP address. If do not exist
    # use Remote Address (or Remote IP) header. Use a GeoIP Database to Resolve Location
    # The most common, reliable, and widely used tool for retreving country and city from IP is MaxMind GeoLite2.
    pass

@app.get("/origin/")
async def set_point_of_origin(lat, lon):
    pass


@app.get("/{user_name}")
async def user_home_page(user_name: str):
    # Show user home screen with saved trip details
    # Determine whether user is normal or admin
    # Location can be based on user profile country or city
    pass


@app.get("/{city}/")
async def search_flights(city_code: str, limit: int | None = 10, offset: int | None = None):
    # on selecting a city show direct flights from that city
    pass


@app.post("/{user_name}")
async def create_trip(user_name:str, trip_data: list[Trip]):
    pass


@app.get("/user/{user_name}")
async def get_user(user_name:str):
    # This shows the account details
    pass

@app.post("/user/{user_name}")
async def create_user(user_name: str, user_data: dict[User]):
    # To create a user
    pass

@app.put("/user/{user_name}")
async def modify_user(user_name: str, user_data: dict[User]):
    pass

@app.delete("/user/{user_name}")
async def delete_user(user_name: str):
    pass


