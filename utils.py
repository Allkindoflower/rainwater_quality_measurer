## utils.py

# importing in a dependency file, just be aware of it
import requests
import sys


def handle_network_issues(function): # TODO: add retry connection
    def wrapper(*args, **kwargs):
        try:
            return function(*args, **kwargs)
        except requests.exceptions.ConnectionError:
            print("A connection error has occured, please check your internet connection and try again")
            sys.exit(8)
        except requests.exceptions.ConnectTimeout:
            print("Connection timed out, please try again later.")
            sys.exit(9)
    return wrapper