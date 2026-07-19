import geocoder
import requests
import math
import os
from dotenv import load_dotenv
from tenacity import retry, stop_after_attempt, wait_fixed
from exceptions import IpLocationFailed, AQITooLow


load_dotenv()
aqi_api = os.getenv("AQI_API")

retry_config = retry(
stop=stop_after_attempt(3),
wait=wait_fixed(5),
reraise=True
)
    
@retry_config
def guess_city_with_ip():
    """Locates the IP of the machine the program is ran from"""
    g = geocoder.ip("me")
    city_guess = g.city
    return city_guess

def ask_user_city(city_guess):
    """Fallback function in case the IP locator fails."""
    if city_guess and not city_guess == "None":
        city_confirmation = input(f"Is this your city(y/N): {city_guess} ")
        if city_confirmation.lower().startswith("y"):
            return city_guess
    while True:
        city = input(f"Please enter your city: ")
        if city == "" or city.isdigit():
                print("City field cannot be empty or numerical.")
        else:
            return city

#TODO: Add back if the AQI is too high, quit the program or just return "Unsafe"
@retry_config
def get_air_quality(confirmed_city):
    """Gets the air quality index from the API below."""
    try:
        air_quality_api = f"http://api.waqi.info/feed/{confirmed_city}/?token={aqi_api}"
        response = requests.get(air_quality_api)
        response.raise_for_status()
        data = response.json()

    except requests.exceptions.HTTPError:
        print("Couldn't fetch air quality...")
        raise RuntimeError()
    
    if "data" in data and "aqi" in data["data"] and isinstance(data["data"]["aqi"], int) :
        air_quality_index = data["data"]["aqi"]
        if air_quality_index > 200:
            raise AQITooLow("Air quality is too low for safety, try again at a later date.")
        return air_quality_index
    else:
        print(f"Corrupted data...")
        raise RuntimeError()


@retry_config
def get_humidity(confirmed_city):
    """Gets the humidity from the API below."""
    general_weather_api = f"https://wttr.in/{confirmed_city}?format=j1"

    response = requests.get(general_weather_api)
    if response.ok:
        data = response.json()
        try:
            humidity = int(data["current_condition"][0]["humidity"])
            return humidity
        except ValueError:
            print("Something went wrong when getting humidity information, please try again later.")
            raise RuntimeError()
    else:
        print(f"Connection failed. Status code: {response.status_code}")
        raise RuntimeError()

def distance_from_coast():
    """Calculates the distance from a coast for the given city."""
    raise NotImplementedError("Will be added on a later date: Low priority")

@retry_config
def get_altitude(confirmed_city):
    """Gets the altitude of the given city."""
    altitude_limit = 5000 # meters
    max_allowed_altitude = altitude_limit - 1
    g = geocoder.osm(confirmed_city, headers={"User-Agent": "rainwater-quality-checker"})

    try:
        lat, lon = g.latlng
    except TypeError:
        raise TypeError("Could not get latitude or longitude values.") 

    altitude_api = f"https://api.open-meteo.com/v1/elevation?latitude={lat}&longitude={lon}"
    response = requests.get(altitude_api)
    if response.ok:
        data = response.json()
        elevation = data["elevation"][0]
        if elevation > altitude_limit:
            elevation = max_allowed_altitude
        return elevation
    else:
        raise RuntimeError("Connection problem, try again later")
        

def calculate_rainwater_quality(air_quality_index, humidity, elevation):
    """Calculates rainwater quality based on AQI, humidity and elevation."""  
    aqi_score = (150 - air_quality_index) / 150
    humidity_score = (100 - humidity) / 100
    altitude_score = math.log(elevation + 1) / math.log(5001)  # + 1, log 0 means infinity
    rainwater_quality = (aqi_score * 0.65) + (humidity_score * 0.25) + (altitude_score * 0.10)
    if rainwater_quality >= 0.75:
        return "Safe"
    elif rainwater_quality >= 0.50:
        return "Reasonable"
    elif rainwater_quality >= 0.25:
        return "Danger Zone"
    elif rainwater_quality >= 0.0:
        return "Unsafe"

def main():
    """Main function."""
    try:
        city_guess = guess_city_with_ip()
    except IpLocationFailed:
        city_guess = None
        
    confirmed_city = ask_user_city(city_guess)
    air_quality_index = get_air_quality(confirmed_city)

    humidity = get_humidity(confirmed_city)
    elevation = get_altitude(confirmed_city)

    rainwater_quality = calculate_rainwater_quality(air_quality_index, humidity, elevation)
    print(f"{rainwater_quality:.3f}")
    
    result = calculate_rainwater_quality(air_quality_index, humidity, elevation)
    print(result)

    with open("logs.txt", "a") as f: # needs its own function
        f.write(f"City: {confirmed_city} | {rainwater_quality:.3f}\n")

if __name__ == "__main__":
    main()