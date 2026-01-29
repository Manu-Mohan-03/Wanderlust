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
    if response.status_code != requests.codes.ok:
        return None
    try:
        location = float(response.json()["location"]["latitude"]) , \
                   float(response.json()["location"]["longitude"])
        return location
    except KeyError:
        return None

def get_public_ip():
    # Use service https://api.ipify.org  to find the public ip
    try:
        # api4.ipify provides IPv4 address
        #response = requests.get('https://api4.ipify.org', timeout=5)
        response_text = "34.159.56.80"
    except Exception:
        raise ValueError("Unexpected behaviour while fetching public IP!")

    # if response.text:
    #     return response.text
    if response_text:
        return response_text
    else:
        # # Fallback to a known public IP if offline
        return "8.8.8.8"


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
        return {"location": (float(latitude), float(longitude))}

    ip_addresses = request.headers.get("X-Forwarded-For")
    if ip_addresses:
        # The first IP in the comma-separated list is the client's
        client_ip = ip_addresses.split(",")[0].strip()
    else:
        # Fallback to the direct connection's IP
        client_ip = request.client.host if request.client else "127.0.0.1"
    # Handle local development check
    if client_ip in ("127.0.0.1", "::1"):
        #If the IP is localhost, swap it for your REAL public IP or a sample one
        client_ip = get_public_ip()
        #return should be a dictionary with location or ip address as key
        return {"ip": client_ip}
    return None

