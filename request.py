import requests
from requests.auth import HTTPBasicAuth
import configparser

def post(path):

    config = configparser.ConfigParser()
    config.read("config.ini")

    # Open the video file in binary mode
    with open(path, "rb") as video_file:
        data = {"video": video_file}

        # Make the POST request with Basic Authentication
        response = requests.post(config["request"]["url"], data=data, auth=HTTPBasicAuth(config["request"]["username"], config["request"]["password"]))

    # Check the response status
    if response.status_code == 200:
        print("Request successful!")
        print(response.json())  # or response.text to print raw response
    else:
        print("Request failed with status code:", response.status_code)