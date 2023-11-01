# import skyfield.api as sf
# import numpy as np
# import time
# import csv

# # Orbit propagation parameters, for 24 hours of orbit positions
# SIM_TIME = 24 * 60 * 60  # in seconds


# # Load TLE
# ts = sf.load.timescale()
# stations_url = "http://celestrak.com/NORAD/elements/stations.txt"
# satellites = sf.load.tle(stations_url, reload=False)
# cubesat = satellites["ISS (ZARYA)"]

# # Build time array
# cubesat_tle_epoch = cubesat.epoch.utc_datetime()
# seconds = cubesat_tle_epoch.second + np.arange(0, SIM_TIME, 1.0)
# time_array = ts.utc(
#     year=cubesat_tle_epoch.year,
#     month=cubesat_tle_epoch.month,
#     day=cubesat_tle_epoch.day,
#     hour=cubesat_tle_epoch.hour,
#     minute=cubesat_tle_epoch.minute,
#     second=seconds,
# )

# # Perform EarthSatellite.at() orbit propagation
# cubesat_propagated = cubesat.at(time_array)

# # Save the results as a time series
# with open("cubesat_position_time_series.csv", "w") as f:
#     writer = csv.writer(f)
#     for time, position in zip(time_array, cubesat_propagated.position.km):
#         writer.writerow([time.utc_datetime, position[0], position[1], position[2]])







# from numpy import arange
# from skyfield.api import load, EarthSatellite, wgs84
# from datetime import timezone, timedelta, datetime
# import numpy as np
# iss_tle0 = """\
# 1 25544U 98067A   23303.48176097  .00029409  00000+0  52365-3 0  9990
# 2 25544  51.6456  18.3943 0000749  70.6008  47.8301 15.49875676422771
# """
# time_series = {}

# observer = wgs84.latlon(+31.7677, -106.4351)

# my_earthsat = EarthSatellite(*iss_tle0.splitlines())

# difference = my_earthsat - observer

# ts = load.timescale()  # create skyfield timescale object
# tz = timezone(timedelta(hours=0))  # whatever your timezone offset from UTC is
# start = datetime.now(tz=tz)  # timezone-aware start time
# end = start + timedelta(hours=24)  # one day's worth of times
# delta = timedelta(seconds=10)  # your interval over which you evaluate

# observer = wgs84.latlon(+31.7677, -106.4351)
# difference = my_earthsat - observer

# times = [start]
# now = start
# i =0
# while now <= end:
#     # print("TIME: ", now)
#     observer = wgs84.latlon(+31.7677, -106.4351)
#     difference = my_earthsat - observer
#     astrometrics = my_earthsat.at(ts.utc(now))
#     topocentric = difference.at(ts.utc(now))
#     el, az, distance = topocentric.altaz()
#     lat, lon = wgs84.latlon_of(astrometrics)
#     velocity = astrometrics.velocity.km_per_s
#     altitude = wgs84.height_of(astrometrics)
#     sunlit = astrometrics.is_sunlit(load("de421.bsp"))
#     time_series[now] = [{'el':el.degrees, 'az':az.degrees, 'lat': lat.degrees, 'lon': lon.degrees, 'alt': altitude.km, 'speed': np.linalg.norm(velocity), 'sunlit': sunlit}]
#     # times.append(now)
#     now += delta
#     # print(now)
#     i = i+1
# print(time_series)
# for element in time_series:
#     cur_day = datetime.now(tz=timezone(timedelta(hours=0))).day
#     curr_hour = datetime.now(tz=timezone(timedelta(hours=0))).hour
#     curr_min = datetime.now(tz=timezone(timedelta(hours=0))).min
#     curr_sec = datetime.now(tz=timezone(timedelta(hours=0))).second
#     if element.day == cur_day and element.hour == curr_hour and element.min == curr_min:
#         for i in range (curr_sec - 8, curr_sec+8):
#             if element.second == i:
#                 print(time_series[element])
#     # print(element)
# # print(times)













# astrometrics = my_earthsat.at(ts.utc(times))
# topocentric = difference.at(ts.utc(times))
# alt_az = []
# for index in topocentric:
#     alt_az.append(index.altaz())
# # print(alt_az)
# lat_lon = []
# for i in astrometrics:
#     lat_lon.append(wgs84.latlon_of(i))

# i = 0
# while i < 6:
#     print("EL: ", alt_az[i][0].degrees, " AZ: ", alt_az[i][1].degrees)
#     print("LAT: ", lat_lon[i][0].degrees, " LON: ", lat_lon[i][1].degrees)
#     i = i + 1


# iss_tle0 = """\
# 1 25544U 98067A   18184.80969102  .00001614  00000-0  31745-4 0  9993
# 2 25544  51.6414 295.8524 0003435 262.6267 204.2868 15.54005638121106
# """

# observer = wgs84.latlon(+31.7677, -106.4351)

# my_earthsat = EarthSatellite(*iss_tle0.splitlines())

# tz_offset = -6
# difference = my_earthsat - observer

# ts = load.timescale()
# t = ts.utc(2023, 10, 27, tz_offset, 0, arange(24 * 60 * 60))
# print(t)
# astrometrics = my_earthsat.at(t)
# topocentric = difference.at(t)
# lat,lon = wgs84.latlon_of(astrometrics)
# height = wgs84.height_of(astrometrics)
# el, az, distance = topocentric.altaz()


###################################################33
# import numpy as np
# from skyfield.api import load, EarthSatellite, Topos, wgs84
# from datetime import datetime, timedelta
# import pytz
# from sgp4.io import fix_checksum

# bluffton = wgs84.latlon(+31.7677, -106.4351)
# ts = load.timescale()
# tz = pytz.timezone('UTC')  # Use UTC timezone
# bsp = load("de421.bsp")

# def orbit_propagation(catalog_numbers):
#     # Precompute values outside the loop
#     start = datetime.now(tz=tz)
#     end = start + timedelta(hours=0.5)
#     delta = timedelta(seconds=60)

#     time_series = {}  # Modified to store position data
#     now = start
#     while now <= end:
#         time_series[now] = {}
#         for catalog_number in catalog_numbers:
#             tle, satellite_name = get_tle_by_catalog(catalog_number)
#             if tle:
#                 my_sat = EarthSatellite(tle[0], tle[1])
#                 difference = my_sat - bluffton
#                 satellite_data = []

#                 astrometrics = my_sat.at(ts.utc(now))
#                 topocentric = difference.at(ts.utc(now))
#                 el, az, distance = topocentric.altaz()
#                 lat, lon = wgs84.latlon_of(astrometrics)
#                 velocity = astrometrics.velocity.km_per_s
#                 altitude = wgs84.height_of(astrometrics)
#                 sunlit = astrometrics.is_sunlit(bsp)
                
#                 # Store position data in time_series
#                 satellite_data.append({'el': el.degrees, 'az': az.degrees, 'lat': lat.degrees, 'lon': lon.degrees, 'alt': altitude.km, 'speed': np.linalg.norm(velocity), 'sunlit': sunlit})
                
#                 time_series[now][satellite_name] = satellite_data

#         now += delta

#     return time_series

# def get_tle_by_catalog(catalog_number):
#     tle = []
#     with open('active.txt', 'r') as file:
#         lines = file.readlines()

#     for i, line in enumerate(lines):
#         if catalog_number in line:
#             tle.append((lines[i-1]))
#             tle.append((line))
#             tle.append((lines[i + 1]))
#             satellite_name = fix_checksum(tle[0])
#             tle_fixed = (fix_checksum(tle[1]), fix_checksum(tle[2]))
#             return tle_fixed, satellite_name

#     return None, None

# # Example usage:
# catalog_numbers = ["25544", "57316"]
# result = orbit_propagation(catalog_numbers)

# # Function to print the updated time_series
# def print_time_series(time_series):
#     for timestamp, satellite_data_dict in time_series.items():
#         print(f"Timestamp: {timestamp}")
#         for satellite_name, position_data in satellite_data_dict.items():
#             print(f"Satellite Name: {satellite_name}")
#             for data in position_data:
#                 print("Position Data:")
#                 for key, value in data.items():
#                     print(f"  {key}: {value}")
#             print()
#         print()

# print_time_series(result)

################################################################################

import numpy as np
from skyfield.api import load, EarthSatellite, Topos, wgs84
from datetime import datetime, timedelta
import pytz
from sgp4.io import fix_checksum
from concurrent.futures import ThreadPoolExecutor
# from flask import Flask, jsonify
import json

bluffton = wgs84.latlon(+31.7677, -106.4351)
ts = load.timescale()
tz = pytz.timezone('UTC')  # Use UTC timezone
bsp = load("de421.bsp")

def orbit_propagation(catalog_numbers):
    # Precompute values outside the loop
    start = datetime.now(tz=tz)
    end = start + timedelta(hours=12)
    delta = timedelta(seconds=60)

    time_series = {}  # Modified to store only the catalog_number as the identifier
    now = start
    while now <= end:
        time_series[now] = {}
        for catalog_number in catalog_numbers:
            tle, satellite_name = get_tle_by_catalog(catalog_number)
            if tle:
                my_sat = EarthSatellite(tle[0], tle[1])
                difference = my_sat - bluffton
                satellite_data = []

                astrometrics = my_sat.at(ts.utc(now))
                topocentric = difference.at(ts.utc(now))
                el, az, distance = topocentric.altaz()
                lat, lon = wgs84.latlon_of(astrometrics)
                velocity = astrometrics.velocity.km_per_s
                altitude = wgs84.height_of(astrometrics)
                sunlit = astrometrics.is_sunlit(bsp)
                
                # Store satellite_name as a field in the position data
                satellite_data.append({'el': el.degrees, 'az': az.degrees, 'lat': lat.degrees, 'lon': lon.degrees, 'alt': altitude.km, 'speed': np.linalg.norm(velocity), 'sunlit': sunlit, 'satellite_name': satellite_name})
                
                time_series[now][catalog_number] = satellite_data  # Use catalog_number as the identifier

        now += delta

    return time_series

# Rest of your code remains the same

def get_tle_by_catalog(catalog_number):
    tle = []
    with open('active.txt', 'r') as file:
        lines = file.readlines()

    for i, line in enumerate(lines):
        if catalog_number in line:
            tle.append((lines[i-1]))
            tle.append((line))
            tle.append((lines[i + 1]))
            tle_fixed = (fix_checksum(tle[1]), fix_checksum(tle[2]))
            return tle_fixed, fix_checksum(tle[0])  # Return satellite_name as well

    return None, None

# Example usage:
catalog_numbers = ["25544"]
result = orbit_propagation(catalog_numbers)

def jsonify_time_series(time_series):
    json_time_series = {}
    for timestamp, satellite_data_dict in time_series.items():
        json_time_series[str(timestamp)] = {}
        for catalog_number, position_data in satellite_data_dict.items():
            json_time_series[str(timestamp)][catalog_number] = position_data

    return json_time_series

json_result = jsonify_time_series(result)

# Serialize the JSON to a string
json_str = json.dumps(json_result, indent=4)
print(json_str)
