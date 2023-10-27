import requests
import time

#	mapboxgl.accessToken = 'pk.eyJ1IjoiYXJpdmVyYTM1IiwiYSI6ImNrbHVrenM2MDF6aXgybmx3bDN2ZjFtMm0ifQ.PnjnSxGKp1YMV7aik9cFjA';

# Define the URL of your Flask app
app_url = "http://127.0.0.1:5000/calculate_passes"

# Sample JSON data for the POST request
data = {
    "catalog_number": "02872",  # Replace with a valid catalog number
    "days" : "3"
}


for i in range(1):
    # Send a POST request to the app
    response = requests.post(app_url, json=data)
    # Print the response
    print(response.json())
    time.sleep(.7)

# app_url = "http://127.0.0.1:5000/get_pass_predictions"

# data = {
#     "catalog_number": "25544",
#     "min_elevation": 20.0,
#     "days": 1
# }
# resp_pass = requests.post(app_url, json=data)
# print(resp_pass.json())


# url = "http://127.0.0.1:5000/get_position_chunk"
# data = {
#     "catalog_number": "25544"
# }
# re = requests.post(url, json=data)
# print(re.json())