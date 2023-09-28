# import requests
# from skyfield.api import load, wgs84

# # Add this code block to your app.py



# def fetch_and_store_tles():
#     tle_data = {}

#     celesTrak_tle_url = "https://www.celestrak.com/NORAD/elements/active.txt"
#     response = requests.get(celesTrak_tle_url)

#     if response.status_code == 200:
#         lines = response.text.strip().split('\n')
#         num_lines = len(lines)

#         for i in range(0, num_lines, 3):
#             name_line, tle_line1, tle_line2 = lines[i:i+3]
#             name = name_line.strip()
#             tle_lines = [tle_line1.strip(), tle_line2.strip()]

#             tle_data[name] = tle_lines
#     else:
#         print("Failed to fetch TLE data from CelesTrak")

#     return tle_data

# def get_tle_by_catalog_number(tle_data, catalog_number):
#     for satellite_name, tle_lines in tle_data.items():
#         tle_catalog_number = tle_lines[1][2:7]  # Extract catalog number from line 2
#         if tle_catalog_number == catalog_number:
#             return tle_lines

#     return None  # Catalog number not found in tle_data


# # Fetch TLEs and store them in a dictionary
# #tle_data = fetch_and_store_tles()

# catalog_number = '25544'  # Replace with a valid catalog number
# #tle_lines = get_tle_by_catalog_number(tle_data, catalog_number)
# #print(tle_lines)

# from skyfield.api import Topos, load
# from datetime import datetime

# # Load the satellite ephemeris data
# ts = load.timescale()
# planets = load('de421.bsp')
# earth, satellite = planets['earth'], planets['ISS (ZARYA)']

# # Create an observer for your location (latitude, longitude, elevation in meters)
# observer = earth + Topos(latitude_degrees=31.767600, longitude_degrees=-106.43502, elevation_m=255)

# # Calculate the satellite position at a specific time
# time = ts.utc(2023, 8, 23, 12, 0, 0)  # Replace with your desired time
# astrometric = (observer - satellite).at(time)
# alt, az, distance = astrometric.altaz()

# print("Altitude:", alt.degrees)
# print("Azimuth:", az.degrees)

# def calculate_pass_predictionss(catalog_number, observer_location, start_time, end_time, min_elevation_deg):
#     satellite = satellite_dict.get(catalog_number)
#     if not satellite:
#         return []

#     observer = wgs84.latlon(observer_location[0], observer_location[1])
#     t, events = satellite.find_events(observer, start_time, end_time, altitude_degrees=min_elevation_deg)

#     pass_predictions = []
#     event_names = 'rise above {}°'.format(min_elevation_deg), 'culminate', 'set below {}°'.format(min_elevation_deg)
#     for pass_number, (ti, event) in enumerate(zip(t, events), start=1):
#         if pass_number >= len(t) or pass_number >= len(events):
#             break  # Stop iterating if we've gone beyond available events
        
#         name = event_names[event]
        
#         if event == 1:  # Culminate event
#             topocentric = satellite - observer
#             alt, az, _ = topocentric.at(ti).altaz()
#             max_elevation = alt.degrees
#             max_azimuth = az.degrees
#         else:
#             max_elevation = 0.0
#             max_azimuth = 0.0
#         local_ti = ti.astimezone(pytz.timezone('America/Denver'))
        
#         pass_info = {
#             'pass_number': pass_number,
#             'start_time': local_ti.strftime('%Y-%m-%d %H:%M:%S %Z'),
#             'end_time': t[pass_number].utc_iso(),
#             'max_elevation': max_elevation,
#             'max_azimuth': max_azimuth,
#             'duration_seconds': (t[pass_number] - ti).item(),  # Corrected duration calculation
#             'event': name
#         }
#         pass_predictions.append(pass_info)

#     return pass_predictions

# def calculate_pass_predictions2(catalog_number, observer_location, start_time, end_time, min_elevation_deg):
#     satellite = satellite_dict.get(catalog_number)
#     if not satellite:
#         return []

#     observer = wgs84.latlon(observer_location[0], observer_location[1])
#     t, events = satellite.find_events(observer, start_time, end_time, altitude_degrees=min_elevation_deg)

#     pass_predictions = []
    
#     for ti, event in zip(t, events):
#         if event != 1:  # Only consider the culminate event
#             continue
        
#         topocentric = satellite - observer
#         alt, az, _ = topocentric.at(ti).altaz()
#         max_elevation = alt.degrees
#         max_azimuth = az.degrees

#         # Convert UTC time to El Paso local time
#         local_ti = ti.astimezone(pytz.timezone('America/Denver'))
#         local_end_time = end_time.astimezone(pytz.timezone('America/Denver'))    

#         pass_info = {
#             'start_time': local_ti.strftime('%Y-%m-%d %H:%M:%S %Z'),  # Convert to local time format
#             'max_elevation': max_elevation,
#             'max_azimuth': max_azimuth,
#         }
#         pass_predictions.append(pass_info)

#     return pass_predictions


import ephem
# import predict
import datetime as dt
from sgp4.earth_gravity import wgs84
from sgp4.io import twoline2rv, verify_checksum, fix_checksum, compute_checksum

# station = ephem.Observer()
# station.lat = '+31.7677'
# station.long = '-106.4351'
# station.elev = 0

# # TLE data for a satellite (without checksum)
# line1 = "1 25544U 98067A   23261.44473810  .00015356  00000+0  28244-3 0  9997"
# line2 = "2 25544  51.6419 226.5842 0005864  32.1953 116.9329 15.49383676416254"

 
# def passes(station, satellite, start=None, duration=7):
#     result = []
#     if start is not None:
#         station.date = ephem.date(start)
#     end = ephem.date(station.date + duration)
#     while station.date < end:
#         t_aos, azr, t_max, elt, t_los, azs = station.next_pass(satellite)
#         result.append({'aos': t_aos.datetime(), 'los': t_los.datetime()})
#         station.date = t_los + ephem.second
#     return result

# # Calculate and append checksum for each line
# checksum1 = str(compute_checksum(line1))
# checksum2 = str(compute_checksum(line2))

 

# # Append the checksum digits to the end of each line
# line1 = line1[:-1] + checksum1
# line2 = line2[:-1] + checksum2

 
# epoch = dt.datetime.utcnow()
# # Create a TLE object
# tle = ephem.readtle("ISS (ZARYA)", line1, line2)
# for i in passes(station, tle, epoch, 2):
#     print("AOS ", i['aos'], "LOS ", i['los'], "DURATION ", (i['los']-i['aos']))

def passes(station, satellite, start=None, duration=7):
    result = []
    if start is not None:
        station.date = ephem.date(start)
    end = ephem.date(station.date + duration)
    while station.date < end:
        t_aos, azr, t_max, elt, t_los, azs = station.next_pass(satellite)
        result.append({'aos': t_aos.datetime(), 'aos_az': azr, 'tmax':t_max.datetime(), 'los': t_los.datetime(), 'los_az': azs, 'max_el': elt})
        station.date = t_los + ephem.second
    return result

# tle = """ISS (ZARYA)             
# 1 25544U 98067A   23261.44473810  .00015356  00000+0  28244-3 0  9997
# 2 25544  51.6419 226.5842 0005864  32.1953 116.9329 15.49383676416254"""

station = ephem.Observer()
station.lat = '+31.7677'
station.long = '-106.4351'
station.elev = 0

epoch = dt.datetime.utcnow()

# for i in passes(station, ephem.readtle(*tle), epoch, 2):
#     print("AOS ", i['aos'], "LOS ", i['los'], "DURATION ", (i['los']-i['aos']))
print("===============")

def get_tle_by_catalog(catalog_number):
    tle = []
    with open('active.txt', 'r') as file:
        lines = file.readlines()

    for i, line in enumerate(lines):
        if catalog_number in line:
            tle.append((lines[i-1]))
            tle.append((line))
            tle.append((lines[i + 1]))
            break
    return tle

# Main program
catalog_number = input("Enter the catalog number: ")
tle = get_tle_by_catalog(catalog_number)
# print(type(tle))

print(fix_checksum(tle[1]))
print(fix_checksum(tle[2]))
tle1_fixed = (fix_checksum(tle[1]), fix_checksum(tle[2]))

for i in passes(station, ephem.readtle("ISS (ZARYA)", tle1_fixed[0], tle1_fixed[1]), epoch, 3):
    print("AOS ", i['aos'], "   LOS ", i['los'], "   DURATION ", (i['los']-i['aos']))

# for i in passes(station, ephem.readtle("ISS (ZARYA)", "1 25544U 98067A   23261.44473810  .00015356  00000+0  28244-3 0  9997", "2 25544  51.6419 226.5842 0005864  32.1953 116.9329 15.49383676416254"), epoch, 2):
#     print("AOS ", i['aos'], "LOS ", i['los'], "DURATION ", (i['los']-i['aos']))













######################################################################################
# p = predict.transits(tle, (station.lat, -station.long, station.elev), (epoch - dt.datetime(1970,1,1)).total_seconds())
# for i in range(1, 8):
#         transit = next(p)
#         print(dt.datetime.utcfromtimestamp(transit.start), dt.datetime.utcfromtimestamp(transit.end))


# def passes(station, satellite, start=None, duration=7):
#     result = []
#     if start is not None:
#         station.date = ephem.date(start)
#     end = ephem.date(station.date + duration)
#     while station.date < end:
#         t_aos, azr, t_max, elt, t_los, azs = station.next_pass(satellite)
#         result.append({'aos': t_aos.datetime(), 'los': t_los.datetime()})
#         station.date = t_los + ephem.second
#     return result

# tle = """ISS (ZARYA)          
# 1 25544U 98067A   23258.21279622  .00017394  00000+0  31980-3 0  9998
# 2 25544  51.6410 242.5802 0005771  19.7421  91.0046 15.49290350415756"""

# station = ephem.Observer()
# station.lat = '+31.7677'
# station.long = '-106.4351'
# station.elev = 0.0

# epoch = dt.datetime.utcnow()

# for i in passes(station, ephem.readtle(*tle.split("\n")), epoch, 1):
#     print(i['aos'], i['los'], (i['los'] - i['aos']))

# print("===============")
# p = predict.transits(tle, (station.lat, -station.long, station.elev), (epoch - dt.datetime(1970,1,1)).total_seconds())
# for i in range(1, 8):
#         transit = next(p)
#         print(dt.datetime.utcfromtimestamp(transit.start), dt.datetime.utcfromtimestamp(transit.end), (dt.datetime.utcfromtimestamp(transit.end) - dt.datetime.utcfromtimestamp(transit.start)))