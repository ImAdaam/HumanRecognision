import asyncio
import httpx
import aiofiles
import configparser

async def post(path):
    config = configparser.ConfigParser()
    config.read("config.ini")

    url = config["request"]["url"].strip("'")
    username = config["request"]["username"]
    password = config["request"]["password"]

    async with aiofiles.open(path, "rb") as video_file:
        data = {
            "video": await video_file.read(),
            "username": username,
            "password": password
        }  # Read file asynchronously

    async with httpx.AsyncClient() as client:
        # response = await client.post(url, data=data, auth=(username, password))
        response = await client.post(url, data=data)

    if response.status_code == 200:
        print("Request successful!")
        print(response.json())  # or response.text for raw response
    else:
        print("Request failed with status code:", response.status_code)

# import requests
# from requests.auth import HTTPBasicAuth
# import configparser
#
# def post(path):
#
#     config = configparser.ConfigParser()
#     config.read("config.ini")
#
#     username = config["request"]["username"]
#     password = config["request"]["password"]
#     # Open the video file in binary mode
#     with open(path, "rb") as video_file:
#         data = {
#             "video": video_file,
#             "username": username,
#             "password": password
#         }
#
#         # Make the POST request with Basic Authentication
#         response = requests.post(config["request"]["url"], data=data)
#
#     # Check the response status
#     if response.status_code == 200:
#         print("Request successful!")
#         print(response.json())  # or response.text to print raw response
#     else:
#         print("Request failed with status code:", response.status_code)