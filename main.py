import geocoder
import sys
import requests


print("Welcome to the rainwater quality checker! IMPORTANT: THIS ADVICE SHOULDN'T BE TAKEN VERY SERIOUSLY, THEY ARE ONLY GUESSTIMATES, " \
"ALWAYS DO YOUR RESEARCH BEFORE USING RAINWATER FOR CLEANING OR CONSUMPTION! THIS PROGRAM ALSO ACCESSES YOUR DEVICE'S IP ADDRESS TO LOCATE YOUR CITY, BUT DOESN'T UPLOAD OR STORE THEM")

def handle_network_issues(function):
    def wrapper(*args, **kwargs):
        try:
            return function(*args, **kwargs)
        except requests.exceptions.ConnectionError:
            print("A connection error has occured, please check your internet connection and try again")
            sys.exit(1)
        except requests.exceptions.ConnectTimeout:
            print("Connection timed out, please try again later.")
            sys.exit(2)
    return wrapper

@handle_network_issues
def locate_ip():
    g = geocoder.ip("me")
    city_guess = g.city.lower()
    return city_guess

def guess_city(city_guess):
    city_confirmation = input(f"Is this your city(y/N): {city_guess} ")
    if city_confirmation.lower() in ("y","yes", "yessir", "yeah"):
        confirmed_city = city_guess      
    elif city_confirmation.lower() in ("n", "no", "nosir", "nein"):
        confirmed_city = input("Please enter the city you're in(all lowercase): ")
    else:
        print("Something went wrong, please try running the program again.")
        sys.exit(3)
    return confirmed_city

@handle_network_issues
def get_air_quality(confirmed_city):

    air_quality_api = f"http://api.waqi.info/feed/{confirmed_city}/?token=be7d3d5731b7193927b8957960545285f4385a76"
    response = requests.get(air_quality_api)
    if response.status_code == 200:
        data = response.json()
        if "data" in data and "aqi" in data["data"] and isinstance(data["data"]["aqi"], int) :
            air_quality_index = data["data"]["aqi"]
            return air_quality_index
        else:
            print("Failed to fetch data due to a change in the incoming data stream, please wait for a patch from the author")
            sys.exit(4)
    else:
        print(f"Connection failed. Status code: {response.status_code}")
        sys.exit(5)

@handle_network_issues
def get_humidity(confirmed_city):

    general_weather_api = f"https://wttr.in/{confirmed_city}?format=j1"

    response = requests.get(general_weather_api)
    if response.status_code == 200:
        data = response.json()
        try:
            humidity = int(data["current_condition"][0]["humidity"])
            return humidity
        except ValueError:
            print("Something went wrong when getting humidity information, please try again later.")
            sys.exit(6)
    else:
        print(f"Connection failed. Status code: {response.status_code}")
        sys.exit(5)

    
# another function to fetch how far away from a coast the city is, sea salt spray hurts quality of rainwater
def distance_from_coast():
    pass

@handle_network_issues
def get_altitude(confirmed_city):
    try:
        g = geocoder.osm(confirmed_city)
        lat, lon = g.latlng
    except Exception as e:
        print(e)
        sys.exit(7)

    altitude_api = f"https://api.open-meteo.com/v1/elevation?latitude={lat}&longitude={lon}"
    response = requests.get(altitude_api)
    if response.status_code == 200:
        data = response.json()
        altitude = data["elevation"][0]
        return altitude
    else:
        print(f"Connection failed. Status code: {response.status_code}")
        sys.exit(5)


def guess_rainwater_quality(air_quality_index): # placeholder for a coherent scoring system
    # if 0 <= air_quality_index <= 25:
    #     print("Safe, may be consumed after filtering and boiling.")
    # elif 26 <= air_quality_index <= 50:
    #     print("Reasonable, not very safe to drink, you may filter it and water your plants.")
    # elif 50 <= air_quality_index <= 100:
    #     print("Danger zone, consuming it even with filtering is not recommended, after careful filtering you may use it to water your plants or flush your toilet.")
    # elif air_quality_index > 100:
    #     print("Unsafe. Don't touch it with even a 2-meter stick.")
    # else:
    #     print("Something went wrong, please try again later.")
    pass

def main():
    city_guess = locate_ip()
    confirmed_city = guess_city(city_guess)
    air_quality_index = get_air_quality(confirmed_city)
    humidity = get_humidity(confirmed_city)
    altitude = get_altitude(confirmed_city)
    guess_rainwater_quality(air_quality_index, humidity, altitude) # Incomplete, need precise scoring system

main()