from fastapi import Request, Header
from typing import Optional

import requests
import os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("IP_INTEL_KEY")
BASE_URL = "https://ip-intelligence.abstractapi.com/v1/?"

def get_location_from_ip(ip_address):

    url = f"{BASE_URL}api_key={API_KEY}&ip_address={ip_address}"
    response = requests.get(url)
    print(response.status_code)
    location = float(response.json().get("location").get("latitude")) , \
               float(response.json().get("location").get("longitude"))

    return location

async def get_location(
        request: Request,
        location: Optional[str] = Header(None, alias="X-Geo-Location"),
        latitude: Optional[float] = Header(None, alias="X-Latitude"),
        longitude: Optional[float] = Header(None, alias="X-Longitude")
        ):

    if location:
        try:
            latitude, longitude = location.split(",")
        except ValueError: # Malformed header
            pass
    if latitude and longitude:
        return float(latitude), float(longitude)

    ip_addresses = request.headers.get("X-Forwarded-For")
    if ip_addresses:
        # The first IP in the comma-separated list is the client's
        client_ip = ip_addresses.split(",")[0].strip()
    else:
        # Fallback to the direct connection's IP
        client_ip = request.client.host if request.client else "127.0.0.1"

    # Handle local development check
    if client_ip in ("127.0.0.1", "::1"):
       client_ip = "8.8.8.8"  # Hardcode for testing on localhost

    try:
        location = get_location_from_ip(client_ip)
    except Exception:
        return None
    return location

