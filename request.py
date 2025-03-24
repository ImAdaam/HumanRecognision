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
        data = {"video": await video_file.read()}  # Read file asynchronously

    async with httpx.AsyncClient() as client:
        response = await client.post(url, data=data, auth=(username, password))

    if response.status_code == 200:
        print("Request successful!")
        print(response.json())  # or response.text for raw response
    else:
        print("Request failed with status code:", response.status_code)