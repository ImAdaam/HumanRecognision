import requests
from requests.auth import HTTPBasicAuth

def post(url, data, auth):
    # Define your URL
    url = "https://example.com/api/endpoint"

    # Your data to send in the POST request
    data = {
        "key1": "value1",
        "key2": "value2"
    }

    # Your Basic Auth credentials
    username = "your_username"
    password = "your_password"

    # Make the POST request with Basic Authentication
    response = requests.post(url, data=data, auth=HTTPBasicAuth(username, password))

    # Check the response status
    if response.status_code == 200:
        print("Request successful!")
        print(response.json())  # or response.text to print raw response
    else:
        print("Request failed with status code:", response.status_code)