import requests
import time

# ### TESTING get_satellite_orbit

# app_url = "http://127.0.0.1:5000/get_satellite_orbit"

# # JSON data for the POST request
# data = {
#     "catalog_numbers": ["25544", "57316", "44393"]  # Replace with a valid catalog number
# }

# for i in range(1):
#     # Send a POST request
#     response = requests.post(app_url, json=data)
#     # Print the response
#     print(response.json())

#################################################

# ## TESTING get_satellite_position

# # TODO: Scale up to handle multiple satellites

# app_url = "http://127.0.0.1:5000/get_satellite_position"

# # JSON data for the POST request
# data = {
#     "catalog_number": "25544"  # Replace with a valid catalog number
# }

# for i in range(1):
#     # Send a POST request
#     response = requests.post(app_url, json=data)
#     # Print the response
#     print(response.json())


####################################################

### TESTING calculate_access_windows 

# app_url = "http://127.0.0.1:5000/get_access_windows"

# # JSON data for the POST request
# data = {
#     "catalog_number": "25544",  # Replace with a valid catalog number
#     "days": 3
# }

# for i in range(1):
#     # Send a POST request
#     response = requests.post(app_url, json=data)
#     # Print the response
#     print(response.json())

#######################################################

#### TESTING get_satellite_orbit
app_url = "http://127.0.0.1:5000/get_satellite_orbit"

# JSON data for the POST request
data = {
    "catalog_numbers": ["25544"],  # Replace with a valid catalog number
}

for i in range(1):
    # Send a POST request
    response = requests.post(app_url, json=data)
    # Print the response
    print(response.json())


######################################################

### TESTING orbit_data
# app_url = "http://127.0.0.1:5000/get_current_position_from_timeseries"

# # JSON data for the POST request
# data = {
#     "catalog_numbers": ["25544", "57316", "44393"],  # Replace with a valid catalog number
# }

# for i in range(1):
#     # Send a POST request
#     response = requests.post(app_url, json=data)
#     # Print the response
#     print(response.json())

########################################################

#### TESTING get_position_from_timeseries
app_url = "http://127.0.0.1:5000/get_position_from_timeseries"

# JSON data for the POST request
data = {
    "catalog_numbers": ["25544"],  # Replace with a valid catalog number
    "specific_time": "2023-11-03 19:57:18.672898+00:00"
}

for i in range(1):
    # Send a POST request
    response = requests.post(app_url, json=data)
    # Print the response
    print(response.json())