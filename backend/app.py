import requests
import uvicorn
from fastapi import FastAPI
from backend.routes.user_endpoints import router

app = FastAPI()
app.include_router(router)


def checking_aviation_stack():
    params = {
    'access_key': '406a10e437a689315b4e6b436096e78b'
    }

    api_result = requests.get('https://api.aviationstack.com/v1/flights', params)

    api_response = api_result.json()

    for flight in api_response['database']:
        print(u'%s flight %s from %s (%s) to %s (%s) is in the air.' % (
            flight['airline']['name'],
            flight['flight']['iata'],
            flight['departure']['airport'],
            flight['departure']['iata'],
            flight['arrival']['airport'],
            flight['arrival']['iata']))


def main():
    print(app.routes)
    print("Welcome to Wanderlust: Backend App")
if __name__ == "__main__":
    main()