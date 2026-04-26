import geocoder
import sys
import requests


print("Welcome to the rainwater quality checker! IMPORTANT: THIS ADVICE SHOULDN'T BE TAKEN VERY SERIOUSLY, THEY ARE ONLY GUESSTIMATES, " \
"ALWAYS DO YOUR RESEARCH BEFORE USING RAINWATER FOR CLEANING OR CONSUMPTION! THIS PROGRAM ALSO ACCESSES YOUR DEVICE'S IP ADDRESS TO LOCATE YOUR CITY, BUT DOESN'T UPLOAD OR STORE THEM")

def locate_ip():
    g = geocoder.ip('me')
    city_guess = g.city.lower()
    return city_guess

def guess_city(city_guess):
    city_confirmation = input(f"Is this your city(y/N)): {city_guess} ")
    if city_confirmation.lower() in ("y","yes", "yeah"):
        confirmed_city = city_guess      
    elif city_confirmation.lower() in ("n", "no", "nosir", "nein"):
        confirmed_city = input("Please enter the city you're in(all lowercase): ")
    else:
        print("Something went wrong, please try running the program again.")
        sys.exit(1)
    return confirmed_city

def get_air_quality(confirmed_city):

    API = f"http://api.waqi.info/feed/{confirmed_city}/?token=be7d3d5731b7193927b8957960545285f4385a76"

    try:
        response = requests.get(API)
        data = response.json()
    except requests.exceptions.ConnectionError:
        print("A connection error has occured, please check your internet connection and try again")
        sys.exit(2)
    except requests.exceptions.ConnectTimeout:
        print("Connection timed out, please try again later.")
        sys.exit(3)
    if 'data' in data and 'aqi' in data['data'] and isinstance(data['data']['aqi'], int) :
        air_quality_index = data['data']['aqi']
        return air_quality_index
    else:
        print("Failed to fetch data due to a change in the incoming data stream, please wait for a patch from the author")
        sys.exit(4)

def guess_rainwater_quality(air_quality_index):
    if 0 <= air_quality_index <= 25:
        print("Safe, may be consumed after filtering and boiling.")
    elif 26 <= air_quality_index <= 50:
        print("Reasonable, not very safe to drink, you may filter it and water your plants.")
    elif air_quality_index > 50:
        print("Unsafe. Don't touch it with even a 2-meter stick.")
    else:
        print("Something went wrong, please try again later.")


def main():
    city_guess = locate_ip()
    confirmed_city = guess_city(city_guess)
    air_quality_index = get_air_quality(confirmed_city)
    print(air_quality_index)
    guess_rainwater_quality(air_quality_index)

main()