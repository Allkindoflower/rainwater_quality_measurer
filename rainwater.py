import geocoder
import sys
import requests
import math
from tenacity import retry, stop_after_attempt, wait_fixed
from utils import handle_network_issues


@retry(
stop=stop_after_attempt(3)
wait=wait_fixed(5)
reraise=True
)

class CityNotFound(Exception):
    """Throws when user's city is not found."""
    pass

@handle_network_issues
def guess_city_with_ip():
    """Locates the IP of the machine the program is running from"""
    g = geocoder.ip("me")
    city_guess = g.city
    return city_guess

def ask_user_city(city_guess):
    """Asks the user for their city name, the IP method isn't foolproof, this function is the fallback."""
    city_confirmation = input(f"Is this your city(y/N): {city_guess} ")
    if city_confirmation.lower().startswith("y"):
        confirmed_city = city_guess      
    elif city_confirmation.lower().startswith("n"):
        confirmed_city = input("City: ")
    else:
        print("Something went wrong, please try running the program again.")
        sys.exit(1)
    return confirmed_city

@handle_network_issues
def get_air_quality(confirmed_city):
    """Gets the air quality index from the API below."""
    air_quality_api = f"http://api.waqi.info/feed/{confirmed_city}/?token=be7d3d5731b7193927b8957960545285f4385a76"
    response = requests.get(air_quality_api)
    if response.status_code == 200:
        data = response.json()
        if "data" in data and "aqi" in data["data"] and isinstance(data["data"]["aqi"], int) :
            air_quality_index = data["data"]["aqi"]
            return air_quality_index
        else:
            print("Cannot fetch air quality, try again later")
            sys.exit(2)
    else:
        print(f"Connection failed. Code: {response.status_code}")
        sys.exit(3)

@handle_network_issues
def get_humidity(confirmed_city):
    """Gets the humidity from the API below."""
    general_weather_api = f"https://wttr.in/{confirmed_city}?format=j1"

    response = requests.get(general_weather_api)
    if response.status_code == 200:
        data = response.json()
        try:
            humidity = int(data["current_condition"][0]["humidity"])
            return humidity
        except ValueError:
            print("Something went wrong when getting humidity information, please try again later.")
            sys.exit(4)
    else:
        print(f"Connection failed. Status code: {response.status_code}")
        sys.exit(5)

# another function to fetch how far away from a coast the city is, sea salt spray hurts quality of rainwater
def distance_from_coast():
    """Calculates the distance from a coast for the given city."""
    raise NotImplementedError("Will be added on a later date: Low priority")

@handle_network_issues
def get_altitude(confirmed_city):
    """Gets the altitude of the given city, higher up means cleaner air (up to a point)."""
    altitude_limit = 5000 # in meters
    max_allowed_altitude = altitude_limit - 1
    try:
        g = geocoder.osm(confirmed_city, headers={"User-Agent": "rainwater-quality-checker"})
        lat, lon = g.latlng
    except Exception as e:
        print(e)
        sys.exit(6)

    altitude_api = f"https://api.open-meteo.com/v1/elevation?latitude={lat}&longitude={lon}"
    response = requests.get(altitude_api)
    if response.status_code == 200:
        data = response.json()
        elevation = data["elevation"][0]
        if elevation > altitude_limit:
            elevation = max_allowed_altitude
        return elevation
    else:
        print(f"Connection failed. Status code: {response.status_code}")
        sys.exit(7)

def calculate_rainwater_quality(air_quality_index, humidity, elevation):
    """Calculates rainwater quality based on aqi, humidity and elevation. Each has their own weight. NOTE: The weights are guesstimates, will be improved upon on upcoming updates"""
    if air_quality_index >= 150:
        print(f"Air quality is too low: {air_quality_index}, please try again at a later time.")
        sys.exit(8)
    else:
        aqi_score = (150 - air_quality_index) / 150
    humidity_score = (100 - humidity) / 100
    altitude_score = math.log(elevation + 1) / math.log(5001)  # + 1, log 0 means infinity
    rainwater_quality = (aqi_score * 0.65) + (humidity_score * 0.25) + (altitude_score * 0.10)
    return rainwater_quality


def rainwater_advice(rainwater_quality):
    """Gives advice based on the rainwater quality."""
    if rainwater_quality >= 0.75:
        return "Safe"
    elif rainwater_quality >= 0.50:
        return "Reasonable"
    elif rainwater_quality >= 0.25:
        return "Danger zone"
    elif rainwater_quality >= 0.0:
        return "Unsafe"
    

def main():
    """Main function."""
    try:
        city_guess = guess_city_with_ip()
        confirmed_city = ask_user_city(city_guess)
    except CityNotFound:
        print("Your city was not found, retrying...")
        time.sleep(5)
        city_guess = guess_city_with_ip()
        confirmed_city = ask_user_city(city_guess)

    air_quality_index = get_air_quality(confirmed_city)
    humidity = get_humidity(confirmed_city)
    altitude = get_altitude(confirmed_city)
    rainwater_quality = calculate_rainwater_quality(air_quality_index, humidity, altitude)
    print(f"{rainwater_quality:.3f}")
    result = rainwater_advice(rainwater_quality)
    print(result)

    with open("logs.txt", "a") as f: # needs its own function
        f.write(f"City: {confirmed_city} | {rainwater_quality:.3f}\n")

if __name__ == "__main__":
    main()