## utils.py

# Outdated decorator, handled by tenacity lib

# import requests
# import sys

# def handle_network_issues(function): # TODO: add retry connection
#     def wrapper(*args, **kwargs):
#         try:
#             return function(*args, **kwargs)
#         except requests.exceptions.ConnectionError:
#             print("A connection error has occured, please check your internet connection and try again")
#             sys.exit(8)
#     return wrapper
