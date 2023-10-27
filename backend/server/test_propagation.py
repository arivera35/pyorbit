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

from numpy import arange
from skyfield.api import load, EarthSatellite, wgs84
from datetime import timezone, timedelta, datetime

iss_tle0 = """\
1 25544U 98067A   18184.80969102  .00001614  00000-0  31745-4 0  9993
2 25544  51.6414 295.8524 0003435 262.6267 204.2868 15.54005638121106
"""

observer = wgs84.latlon(+31.7677, -106.4351)

my_earthsat = EarthSatellite(*iss_tle0.splitlines())

tz_offset = -6
difference = my_earthsat - observer

ts = load.timescale()  # create skyfield timescale object
tz = timezone(timedelta(hours=-6))  # whatever your timezone offset from UTC is
start = datetime.now(tz=tz)  # timezone-aware start time
end = start + timedelta(hours=24)  # one day's worth of times
delta = timedelta(minutes=1)  # your interval over which you evaluate
times = [start]
now = start
while now <= end:
    now += delta
    times.append(now)
# print(times)
observer = wgs84.latlon(+31.7677, -106.4351)
difference = my_earthsat - observer
astrometrics = my_earthsat.at(ts.utc(times))
topocentric = difference.at(ts.utc(times))
alt_az = []
for index in topocentric:
    alt_az.append(index.altaz())
# print(alt_az)
lat_lon = []
for i in astrometrics:
    lat_lon.append(wgs84.latlon_of(i))

i = 0
while i < 6:
    print("EL: ", alt_az[i][0].degrees, " AZ: ", alt_az[i][1].degrees)
    print("LAT: ", lat_lon[i][0].degrees, " LON: ", lat_lon[i][1].degrees)
    i = i + 1


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

