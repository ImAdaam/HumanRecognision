import requests
from requests.auth import HTTPBasicAuth

def post(url, data, auth):
    # Define your URL
    url = "https://example.com/api/endpoint"

    # Your data to send in the POST request
    data = {
        "video": "sightings/extracted_frames_0/video.mp4"
    }

    # Your Basic Auth credentials
    username = "rover_v1"
    password = "rover_v1_pw"

    # Make the POST request with Basic Authentication
    response = requests.post(url, data=data, auth=HTTPBasicAuth(username, password))

    # Check the response status
    if response.status_code == 200:
        print("Request successful!")
        print(response.json())  # or response.text to print raw response
    else:
        print("Request failed with status code:", response.status_code)