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
        video_bytes = await video_file.read()

    async with httpx.AsyncClient(timeout=30.0) as client:
        files = {
            "video": (path, video_bytes, "video/mp4")  # Adjust MIME type if needed
        }
        response = await client.post(url, files=files, data={"username": username, "password": password})

    if response.status_code == 200:
        print("Request successful!")
        print(response.json())  # or response.text for raw response
    else:
        print("Request failed with status code:", response.status_code)
        print(response.headers)
        print(response.json())

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