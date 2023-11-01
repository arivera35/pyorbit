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

import numpy as np
from skyfield.api import load, EarthSatellite, Topos, wgs84
from datetime import datetime, timedelta
import pytz
from sgp4.io import fix_checksum

bluffton = wgs84.latlon(+31.7677, -106.4351)
ts = load.timescale()
tz = pytz.timezone('UTC')  # Use UTC timezone
bsp = load("de421.bsp")


def orbit_propagation(catalog_numbers):
    # Precompute values outside the loop
    start = datetime.now(tz=tz)
    end = start + timedelta(hours=12)
    delta = timedelta(seconds=60)

    time_series = {}
    for catalog_number in catalog_numbers:
        tle, satellite_name = get_tle_by_catalog(catalog_number)
        if tle:
            my_sat = EarthSatellite(tle[0], tle[1])
            now = start
            difference = my_sat - bluffton
            satellite_data = []

            while now <= end:
                astrometrics = my_sat.at(ts.utc(now))
                topocentric = difference.at(ts.utc(now))
                el, az, distance = topocentric.altaz()
                lat, lon = wgs84.latlon_of(astrometrics)
                velocity = astrometrics.velocity.km_per_s
                altitude = wgs84.height_of(astrometrics)
                sunlit = astrometrics.is_sunlit(bsp)
                satellite_data.append({'el': el.degrees, 'az': az.degrees, 'lat': lat.degrees, 'lon': lon.degrees, 'alt': altitude.km, 'speed': np.linalg.norm(velocity), 'sunlit': sunlit})
                now += delta

            time_series[satellite_name] = satellite_data

    return time_series

def get_tle_by_catalog(catalog_number):
    tle = []
    with open('active.txt', 'r') as file:
        lines = file.readlines()

    for i, line in enumerate(lines):
        if catalog_number in line:
            tle.append((lines[i-1]))
            tle.append((line))
            tle.append((lines[i + 1]))
            satellite_name = fix_checksum(tle[0])
            tle_fixed = (fix_checksum(tle[1]), fix_checksum(tle[2]))
            return tle_fixed, satellite_name

    return None, None

# Example usage:
catalog_numbers = ["25544", "57316"]
result = orbit_propagation(catalog_numbers)
print(result)