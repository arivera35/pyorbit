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


# import ephem
# # import predict
# import datetime as dt
# from sgp4.earth_gravity import wgs84
# from sgp4.io import twoline2rv, verify_checksum, fix_checksum, compute_checksum

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

# def passes(station, satellite, start=None, duration=7):
#     result = []
#     if start is not None:
#         station.date = ephem.date(start)
#     end = ephem.date(station.date + duration)
#     while station.date < end:
#         t_aos, azr, t_max, elt, t_los, azs = station.next_pass(satellite)
#         result.append({'aos': t_aos.datetime(), 'aos_az': azr, 'tmax':t_max.datetime(), 'los': t_los.datetime(), 'los_az': azs, 'max_el': elt})
#         station.date = t_los + ephem.second
#     return result

# # tle = """ISS (ZARYA)             
# # 1 25544U 98067A   23261.44473810  .00015356  00000+0  28244-3 0  9997
# # 2 25544  51.6419 226.5842 0005864  32.1953 116.9329 15.49383676416254"""

# station = ephem.Observer()
# station.lat = '+31.7677'
# station.long = '-106.4351'
# station.elev = 0

# epoch = dt.datetime.utcnow()

# # for i in passes(station, ephem.readtle(*tle), epoch, 2):
# #     print("AOS ", i['aos'], "LOS ", i['los'], "DURATION ", (i['los']-i['aos']))
# print("===============")

# def get_tle_by_catalog(catalog_number):
#     tle = []
#     with open('active.txt', 'r') as file:
#         lines = file.readlines()

#     for i, line in enumerate(lines):
#         if catalog_number in line:
#             tle.append((lines[i-1]))
#             tle.append((line))
#             tle.append((lines[i + 1]))
#             break
#     return tle

# # Main program
# catalog_number = input("Enter the catalog number: ")
# tle = get_tle_by_catalog(catalog_number)
# # print(type(tle))

# print(fix_checksum(tle[1]))
# print(fix_checksum(tle[2]))
# tle1_fixed = (fix_checksum(tle[1]), fix_checksum(tle[2]))

# for i in passes(station, ephem.readtle("MOONLIGHTER (GENERATED)", tle1_fixed[0], tle1_fixed[1]), epoch, 3):
#     print("AOS ", i['aos'], "   LOS ", i['los'], "   DURATION ", (i['los']-i['aos']))

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


##############################################################################################################

# WITH GNURADIO SOCKET!!!!!!!!!!!!!!!!!

# from flask import Flask, request, jsonify
# from flask_apscheduler import APScheduler
# from flask_cors import CORS
# from skyfield.api import load, wgs84
# from datetime import timedelta
# from more_itertools import chunked
# import numpy as np
# import ephem
# import time
# import datetime as dt
# from sgp4.io import fix_checksum
# import os
# import zmq
# import array
# import matplotlib.pyplot as plt

# HOST = '127.0.0.1'
# PORT = 4444
# TASK_SOCKET = zmq.Context().socket(zmq.PULL)
# TASK_SOCKET.connect('tcp://{}:{}'.format(HOST, PORT))

# app = Flask(__name__)
# CORS(app)
# scheduler = APScheduler()

# station = ephem.Observer()
# station.lat = '+31.7677'
# station.long = '-106.4351'
# station.elev = 0

# epoch = dt.datetime.utcnow()
# observer_latitude = 31.7677
# observer_longitude = -106.4351

# bluffton = wgs84.latlon(+31.7677, -106.4351)

# # Fetch TLEs and store them in a dictionary
# ts = load.timescale()
# satellites = load.tle_file('https://www.celestrak.com/NORAD/elements/active.txt')
# satellite_dict =  {sat.model.satnum: sat for sat in satellites}

# # buffer for gnuradio data
# buffer = []


# def gnuradio_receiver():
#     raw_data = TASK_SOCKET.recv()
#         # convert to an array of floats
#     float_list = array.array('f', raw_data) # struct.unpack will be faster
#         # print flowgraph data
#     for signal_val in float_list:
#         buffer.append(signal_val)
    
#     TASK_SOCKET.close()
#     return 0

# def plot_signal():
#     plt.plot(buffer)

# def update_tles():
#     global satellite_dict
#     os.remove('active.txt')
#     updated_satellites = load.tle_file('https://www.celestrak.com/NORAD/elements/active.txt')
#     satellite_dict =  {sat.model.satnum: sat for sat in updated_satellites}
#     print('Updated TLEs')

# def get_tle_by_catalog(catalog_number):
#     tle = []
#     with open('active.txt', 'r') as file:
#         lines = file.readlines()

#     for i, line in enumerate(lines):
#         if catalog_number in line:
#             tle.append((lines[i-1]))
#             tle.append((line))
#             tle.append((lines[i + 1]))
#             break
#     tle_fixed = (fix_checksum(tle[1]), fix_checksum(tle[2]))
#     return tle_fixed, tle[0]

# def passes(station, satellite, start=None, duration=7):
#     result = []
#     if start is not None:
#         station.date = ephem.date(start)
#     end = ephem.date(station.date + duration)
#     while station.date < end:
#         t_aos, azr, t_max, elt, t_los, azs = station.next_pass(satellite)
#         result.append({'aos': t_aos.datetime(), 'los': t_los.datetime(), 'duration': 0})
#         station.date = t_los + ephem.second
#     return result

# def parse_tle_file():
#     tle_data = {}
#     current_catalog_number = None
#     current_tle_lines = []

#     with open('active.txt', 'r') as file:
#         for line in file:
#             line = line.strip()
#             if line.startswith('1 '):
#                 current_tle_lines.append(line)
#             elif line.startswith('2 '):
#                 current_tle_lines.append(line)
#                 tle_data[current_catalog_number] = current_tle_lines
#                 current_catalog_number = None
#                 current_tle_lines = []

#     return tle_data

# def get_satellite_velocity(satellite):
#     t = ts.now()
#     geocentric = satellite.at(t)
#     velocity = geocentric.velocity.km_per_s  
#     speed = np.linalg.norm(velocity)
#     return speed

# def is_satellite_sunlit(satellite):
#     return satellite.at(ts.now()).is_sunlit(load("de421.bsp"))

# def get_satellite_positions(catalog_number):
#     t = ts.now()
#     num_positions = 10
#     satellite = satellite_dict[catalog_number]
#     # print(satellite)
#     difference = satellite - bluffton
#     topocentric = difference.at(t)

#     coordinates = []
#     for _ in range(num_positions):
#         t = ts.now()
#         geocentric = satellite.at(t)
#         lat, lon = wgs84.latlon_of(geocentric)
#         coordinates.append((lat.degrees, lon.degrees))  # Append as a tuple
#         # Increment the time for the next position
#         time.sleep(.2)
#         #t = t + timedelta(seconds = 3)  # Increment by 1 minute (adjust as needed)

#     return coordinates

# def calculate_pass_predictions(catalog_number, observer_location, start_time, end_time, min_elevation_deg):
    
#     satellite = satellite_dict.get(catalog_number)
#     passes = []
#     if not satellite:
#         return []

#     observer = wgs84.latlon(observer_location[0], observer_location[1])
#     t, events = satellite.find_events(observer, start_time, end_time, altitude_degrees=min_elevation_deg)
    
#     offset = len(events) % 3
#     t = t[offset:]
#     events = events[offset:]

#     for pass_times, pass_events in zip(chunked(t, 3), chunked(events, 3)):
#         full_pass = serialize_pass(satellite, pass_times, pass_events, observer)
#         start_time_dt = pass_times[0].utc_datetime()
#         end_time_dt = pass_times[-1].utc_datetime()
#         pass_duration_seconds = (end_time_dt - start_time_dt).total_seconds()
#         pass_duration_minutes = pass_duration_seconds / 60  # Convert seconds to minutes
#         full_pass["pass_duration_minutes"] = pass_duration_minutes
#         passes.append(full_pass)

#     return passes

# def serialize_pass(satellite, pass_times, pass_events, observer):
#     full_pass = {}
#     difference = satellite - bluffton
#     topocentric = difference.at(ts.now())

#     for time, event_type in zip(pass_times, pass_events):
#         geometric_sat = (satellite - observer).at(time)

#         sat_alt, sat_az, sat_d = geometric_sat.altaz()
#         is_sunlit = geometric_sat.is_sunlit(load("de421.bsp"))
#         event = ('rise', 'culmination', 'set')[event_type]

#         full_pass[event] = {
#             "alt": f"{sat_alt.degrees:.2f}",
#             "az": f"{sat_az.degrees:.2f}",
#             "utc_datetime": str(time.utc_datetime()),
#             "utc_timestamp": int(time.utc_datetime().timestamp()),
#             "is_sunlit": bool(is_sunlit)
#         }

#     return full_pass

# def serialize_pass_duration(pass_prediction):
#     pass_duration = {
#         "aos": pass_prediction['aos'],
#         "los" : pass_prediction['los'],
#         "duration" : str(pass_prediction['los'] - pass_prediction['aos'])
#     }

#     return pass_duration

# @app.route('/get_satellite_position', methods=['POST'])
# def get_satellite_position_route():
#     data = request.json
#     cat_num = data['catalog_number']
#     catalog_number = int(data['catalog_number'])  # Get the catalog number from JSON data
#     t = ts.now()
#     satellite = satellite_dict[catalog_number]
#     difference = satellite - bluffton
#     topocentric = difference.at(t)
#     el, az, distance= topocentric.altaz()

#     if el.degrees > 0:
#         print('The ISS is above the horizon')
   
#     if satellite is None:
#         return jsonify({
#             'error': 'Satellite not found'
#         })
#     geocentric = satellite.at(t)
#     lat, lon = wgs84.latlon_of(geocentric)
#     height = wgs84.height_of(geocentric)
#     speed = get_satellite_velocity(satellite)
#     sunlit = is_satellite_sunlit(satellite)
#     return jsonify({
#         'lon': lon.degrees,
#         'lat': lat.degrees,
#         'az': az.degrees,
#         'el': el.degrees,
#         'speed': speed,
#         'sunlit': bool(sunlit),
#         'name': satellite.name,
#         'catalog_number': cat_num
#     })

# @app.route('/get_pass_predictions', methods=['POST'])
# def get_pass_predictions_route():
#     data = request.json
#     catalog_number = int(data['catalog_number'])
#     min_elevation_deg = float(data['min_elevation'])
#     days = data['days']
#     start_time = ts.now()
#     end_time = start_time + timedelta(days=days)
#     observer_location = (observer_latitude, observer_longitude)
#     pass_predictions = calculate_pass_predictions(catalog_number, observer_location, start_time, end_time, min_elevation_deg)
#     print(pass_predictions)
#     return jsonify(pass_predictions)

# @app.route('/calculate_passes', methods=['POST'])
# def calculate_passes_route():
#     data = request.json
#     catalog_number = str(data['catalog_number'])
#     days = data['days']
#     full_tle = get_tle_by_catalog(catalog_number)
#     print(full_tle[0][0])
#     print(type(full_tle[1]))
#     passes_predicted = passes(station, ephem.readtle(full_tle[1], full_tle[0][0], full_tle[0][1]), epoch, 3)
#     all_passes = []
#     for i in passes_predicted:
#         all_passes.append(serialize_pass_duration(i))
#     return all_passes

# @app.route('/get_position_chunk', methods=['POST'])
# def get_position_chunk():
#     data = request.json
#     catalog_number = int(data['catalog_number'])
#     coordinates = get_satellite_positions(catalog_number)
#     return jsonify({
#         'coordinates': coordinates
#     })

# def create_app():
#     return app

# gnuradio_receiver()
# print(buffer)

# if __name__ == '__main__':
#     scheduler.add_job(id = 'TLE Update', func = update_tles, trigger="interval", hours = 23)
#     scheduler.start()
#     app.run(debug=True)
####################################################################################################################

# from flask import Flask, request, jsonify
# from flask_apscheduler import APScheduler
# from flask_cors import CORS, cross_origin
# from skyfield.api import load, wgs84
# from datetime import timedelta
# from more_itertools import chunked
# import numpy as np
# import ephem
# import time
# import datetime as dt
# from sgp4.io import fix_checksum
# import os

# app = Flask(__name__)
# cors = CORS(app)
# app.config['CORS_HEADERS'] = 'Content-Type'
# scheduler = APScheduler()

# station = ephem.Observer()
# station.lat = '+31.7677'
# station.long = '-106.4351'
# station.elev = 0

# epoch = dt.datetime.utcnow()
# observer_latitude = 31.7677
# observer_longitude = -106.4351

# bluffton = wgs84.latlon(+31.7677, -106.4351)

# # Fetch TLEs and store them in a dictionary
# ts = load.timescale()
# satellites = load.tle_file('https://www.celestrak.com/NORAD/elements/active.txt')
# satellite_dict =  {sat.model.satnum: sat for sat in satellites}

# def update_tles():
#     global satellite_dict
#     os.remove('active.txt')
#     updated_satellites = load.tle_file('https://www.celestrak.com/NORAD/elements/active.txt')
#     satellite_dict =  {sat.model.satnum: sat for sat in updated_satellites}
#     print('Updated TLEs')

# def get_tle_by_catalog(catalog_number):
#     tle = []
#     with open('active.txt', 'r') as file:
#         lines = file.readlines()

#     for i, line in enumerate(lines):
#         if catalog_number in line:
#             tle.append((lines[i-1]))
#             tle.append((line))
#             tle.append((lines[i + 1]))
#             break
#     tle_fixed = (fix_checksum(tle[1]), fix_checksum(tle[2]))
#     return tle_fixed, tle[0]

# def passes(station, satellite, start=None, duration=7):
#     result = []
#     if start is not None:
#         station.date = ephem.date(start)
#     end = ephem.date(station.date + duration)
#     while station.date < end:
#         t_aos, azr, t_max, elt, t_los, azs = station.next_pass(satellite)
#         result.append({'aos': t_aos.datetime(), 'los': t_los.datetime(), 'duration': 0})
#         station.date = t_los + ephem.second
#     return result

# def parse_tle_file():
#     tle_data = {}
#     current_catalog_number = None
#     current_tle_lines = []

#     with open('active.txt', 'r') as file:
#         for line in file:
#             line = line.strip()
#             if line.startswith('1 '):
#                 current_tle_lines.append(line)
#             elif line.startswith('2 '):
#                 current_tle_lines.append(line)
#                 tle_data[current_catalog_number] = current_tle_lines
#                 current_catalog_number = None
#                 current_tle_lines = []
#     return tle_data

# def get_satellite_velocity(satellite):
#     t = ts.now()
#     geocentric = satellite.at(t)
#     velocity = geocentric.velocity.km_per_s  
#     speed = np.linalg.norm(velocity)
#     return speed

# def is_satellite_sunlit(satellite):
#     return satellite.at(ts.now()).is_sunlit(load("de421.bsp"))

# def get_satellite_positions(catalog_number):
#     t = ts.now()
#     num_positions = 10
#     satellite = satellite_dict[catalog_number]
#     difference = satellite - bluffton
#     topocentric = difference.at(t)

#     coordinates = []
#     for _ in range(num_positions):
#         t = ts.now()
#         geocentric = satellite.at(t)
#         lat, lon = wgs84.latlon_of(geocentric)
#         coordinates.append((lat.degrees, lon.degrees))  # Append as a tuple
#         # Increment the time for the next position
#         time.sleep(.2)
#         #t = t + timedelta(seconds = 3)  # Increment by 1 minute (adjust as needed)
#     return coordinates

# def calculate_pass_predictions(catalog_number, observer_location, start_time, end_time, min_elevation_deg):
    
#     satellite = satellite_dict.get(catalog_number)
#     passes = []
#     if not satellite:
#         return []

#     observer = wgs84.latlon(observer_location[0], observer_location[1])
#     t, events = satellite.find_events(observer, start_time, end_time, altitude_degrees=min_elevation_deg)
    
#     offset = len(events) % 3
#     t = t[offset:]
#     events = events[offset:]

#     for pass_times, pass_events in zip(chunked(t, 3), chunked(events, 3)):
#         full_pass = serialize_pass(satellite, pass_times, pass_events, observer)
#         start_time_dt = pass_times[0].utc_datetime()
#         end_time_dt = pass_times[-1].utc_datetime()
#         pass_duration_seconds = (end_time_dt - start_time_dt).total_seconds()
#         pass_duration_minutes = pass_duration_seconds / 60  # Convert seconds to minutes
#         full_pass["pass_duration_minutes"] = pass_duration_minutes
#         passes.append(full_pass)

#     return passes

# def serialize_pass(satellite, pass_times, pass_events, observer):
#     full_pass = {}
#     difference = satellite - bluffton
#     topocentric = difference.at(ts.now())

#     for time, event_type in zip(pass_times, pass_events):
#         geometric_sat = (satellite - observer).at(time)

#         sat_alt, sat_az, sat_d = geometric_sat.altaz()
#         is_sunlit = geometric_sat.is_sunlit(load("de421.bsp"))
#         event = ('rise', 'culmination', 'set')[event_type]

#         full_pass[event] = {
#             "alt": f"{sat_alt.degrees:.2f}",
#             "az": f"{sat_az.degrees:.2f}",
#             "utc_datetime": str(time.utc_datetime()),
#             "utc_timestamp": int(time.utc_datetime().timestamp()),
#             "is_sunlit": bool(is_sunlit)
#         }

#     return full_pass

# def serialize_pass_duration(pass_prediction):
#     pass_duration = {
#         "aos": pass_prediction['aos'],
#         "los" : pass_prediction['los'],
#         "duration" : str(pass_prediction['los'] - pass_prediction['aos'])
#     }

#     return pass_duration

# @app.route('/get_satellite_position', methods=['POST'])
# @cross_origin()
# def get_satellite_position_route():
#     data = request.json
#     cat_num = data['catalog_number']
#     catalog_number = int(data['catalog_number'])  # Get the catalog number from JSON data
#     t = ts.now()
#     satellite = satellite_dict[catalog_number]
#     difference = satellite - bluffton
#     topocentric = difference.at(t)
#     el, az, distance= topocentric.altaz()

#     if el.degrees > 0:
#         print('The ISS is above the horizon')
   
#     if satellite is None:
#         return jsonify({
#             'error': 'Satellite not found'
#         })
#     geocentric = satellite.at(t)
#     lat, lon = wgs84.latlon_of(geocentric)
#     height = wgs84.height_of(geocentric)
#     speed = get_satellite_velocity(satellite)
#     sunlit = is_satellite_sunlit(satellite)
#     return jsonify({
#         'lon': lon.degrees,
#         'lat': lat.degrees,
#         'az': az.degrees,
#         'el': el.degrees,
#         'speed': speed,
#         'sunlit': bool(sunlit),
#         'name': satellite.name,
#         'catalog_number': cat_num
#     })

# @app.route('/get_pass_predictions', methods=['POST'])
# @cross_origin()
# def get_pass_predictions_route():
#     data = request.json
#     catalog_number = int(data['catalog_number'])
#     min_elevation_deg = float(data['min_elevation'])
#     days = data['days']
#     start_time = ts.now()
#     end_time = start_time + timedelta(days=days)
#     observer_location = (observer_latitude, observer_longitude)
#     pass_predictions = calculate_pass_predictions(catalog_number, observer_location, start_time, end_time, min_elevation_deg)
#     return jsonify(pass_predictions)

# @app.route('/calculate_passes', methods=['POST'])
# @cross_origin()
# def calculate_passes_route():
#     data = request.json
#     catalog_number = str(data['catalog_number'])
#     days = data['days']
#     full_tle = get_tle_by_catalog(catalog_number)
#     passes_predicted = passes(station, ephem.readtle(full_tle[1], full_tle[0][0], full_tle[0][1]), epoch, 3)
#     all_passes = []
#     for i in passes_predicted:
#         all_passes.append(serialize_pass_duration(i))
#     return all_passes

# @app.route('/get_position_chunk', methods=['POST'])
# @cross_origin()
# def get_position_chunk():
#     data = request.json
#     catalog_number = int(data['catalog_number'])
#     coordinates = get_satellite_positions(catalog_number)
#     return jsonify({
#         'coordinates': coordinates
#     })

# @cross_origin()
# def create_app():
#     return app

# if __name__ == '__main__':
#     scheduler.add_job(id = 'TLE Update', func = update_tles, trigger="interval", hours = 23)
#     scheduler.start()
#     app.run(debug=True) 

#############################################################################################################################################
from flask import Flask, request, jsonify
from flask_apscheduler import APScheduler
from flask_cors import CORS
from skyfield.api import load, wgs84, EarthSatellite
from datetime import timezone, timedelta, datetime
from more_itertools import chunked
import numpy as np
import ephem
import time
import datetime as dt
from sgp4.io import fix_checksum
import os

app = Flask(__name__)
CORS(app)
scheduler = APScheduler()

station = ephem.Observer()
station.lat = '+31.7677'
station.long = '-106.4351'
station.elev = 0

epoch = dt.datetime.utcnow()
observer_latitude = 31.7677
observer_longitude = -106.4351

bluffton = wgs84.latlon(+31.7677, -106.4351)


time_series = {}

# Fetch TLEs and store them in a dictionary
ts = load.timescale()
satellites = load.tle_file('https://www.celestrak.com/NORAD/elements/active.txt')
satellite_dict =  {sat.model.satnum: sat for sat in satellites}

def update_tles():
    global satellite_dict
    os.remove('active.txt')
    updated_satellites = load.tle_file('https://www.celestrak.com/NORAD/elements/active.txt')
    satellite_dict =  {sat.model.satnum: sat for sat in updated_satellites}
    print('Updated TLEs')

def orbit_propagation(catalog_number):
    tle = get_tle_by_catalog(catalog_number)
    print(tle[0][0])
    my_sat = EarthSatellite(tle[0][0], tle[0][1])
    tz = timezone(timedelta(hours=0))  # whatever your timezone offset from UTC is
    start = datetime.now(tz=tz)  # timezone-aware start time
    end = start + timedelta(hours=12)  # one day's worth of times
    delta = timedelta(seconds=10)  # your interval over which you evaluate
    difference = my_sat - bluffton
    now = start
    while now <= end:
        astrometrics = my_sat.at(ts.utc(now))
        topocentric = difference.at(ts.utc(now))
        el, az, distance = topocentric.altaz()
        lat, lon = wgs84.latlon_of(astrometrics)
        velocity = astrometrics.velocity.km_per_s
        altitude = wgs84.height_of(astrometrics)
        sunlit = astrometrics.is_sunlit(load("de421.bsp"))
        time_series[now] = [{'el':el.degrees, 'az':az.degrees, 'lat': lat.degrees, 'lon': lon.degrees, 'alt': altitude.km, 'speed': np.linalg.norm(velocity), 'sunlit': sunlit}]
        now += delta
        # print(now)
    
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
    tle_fixed = (fix_checksum(tle[1]), fix_checksum(tle[2]))
    return tle_fixed, tle[0]

def passes(station, satellite, start=None, duration=7):
    result = []
    if start is not None:
        station.date = ephem.date(start)
    end = ephem.date(station.date + duration)
    while station.date < end:
        t_aos, azr, t_max, elt, t_los, azs = station.next_pass(satellite)
        result.append({'aos': t_aos.datetime(), 'los': t_los.datetime(), 'duration': 0})
        station.date = t_los + ephem.second
    return result

def parse_tle_file():
    tle_data = {}
    current_catalog_number = None
    current_tle_lines = []

    with open('active.txt', 'r') as file:
        for line in file:
            line = line.strip()
            if line.startswith('1 '):
                current_tle_lines.append(line)
            elif line.startswith('2 '):
                current_tle_lines.append(line)
                tle_data[current_catalog_number] = current_tle_lines
                current_catalog_number = None
                current_tle_lines = []
    return tle_data

def get_satellite_velocity(satellite):
    t = ts.now()
    geocentric = satellite.at(t)
    velocity = geocentric.velocity.km_per_s  
    speed = np.linalg.norm(velocity)
    return speed

def is_satellite_sunlit(satellite):
    return satellite.at(ts.now()).is_sunlit(load("de421.bsp"))

def get_positions():
    for element in time_series:
        cur_day = datetime.now(tz=timezone(timedelta(hours=0))).day
        curr_hour = datetime.now(tz=timezone(timedelta(hours=0))).hour
        curr_min = datetime.now(tz=timezone(timedelta(hours=0))).min
        curr_sec = datetime.now(tz=timezone(timedelta(hours=0))).second
        if element.day == cur_day and element.hour == curr_hour and element.min == curr_min:
            for i in range (curr_sec - 5, curr_sec+5):
                if element.second == i:
                    return(time_series[element][0])
        

def get_satellite_positions(catalog_number):
    t = ts.now()
    num_positions = 10
    satellite = satellite_dict[catalog_number]
    difference = satellite - bluffton
    topocentric = difference.at(t)

    coordinates = []
    for _ in range(num_positions):
        t = ts.now()
        geocentric = satellite.at(t)
        lat, lon = wgs84.latlon_of(geocentric)
        coordinates.append((lat.degrees, lon.degrees))  # Append as a tuple
        # Increment the time for the next position
        time.sleep(.2)
        #t = t + timedelta(seconds = 3)  # Increment by 1 minute (adjust as needed)
    return coordinates

def calculate_pass_predictions(catalog_number, observer_location, start_time, end_time, min_elevation_deg):
    
    satellite = satellite_dict.get(catalog_number)
    passes = []
    if not satellite:
        return []

    observer = wgs84.latlon(observer_location[0], observer_location[1])
    t, events = satellite.find_events(observer, start_time, end_time, altitude_degrees=min_elevation_deg)
    
    offset = len(events) % 3
    t = t[offset:]
    events = events[offset:]

    for pass_times, pass_events in zip(chunked(t, 3), chunked(events, 3)):
        full_pass = serialize_pass(satellite, pass_times, pass_events, observer)
        start_time_dt = pass_times[0].utc_datetime()
        end_time_dt = pass_times[-1].utc_datetime()
        pass_duration_seconds = (end_time_dt - start_time_dt).total_seconds()
        pass_duration_minutes = pass_duration_seconds / 60  # Convert seconds to minutes
        full_pass["pass_duration_minutes"] = pass_duration_minutes
        passes.append(full_pass)

    return passes

def serialize_pass(satellite, pass_times, pass_events, observer):
    full_pass = {}
    difference = satellite - bluffton
    topocentric = difference.at(ts.now())

    for time, event_type in zip(pass_times, pass_events):
        geometric_sat = (satellite - observer).at(time)

        sat_alt, sat_az, sat_d = geometric_sat.altaz()
        is_sunlit = geometric_sat.is_sunlit(load("de421.bsp"))
        event = ('rise', 'culmination', 'set')[event_type]

        full_pass[event] = {
            "alt": f"{sat_alt.degrees:.2f}",
            "az": f"{sat_az.degrees:.2f}",
            "utc_datetime": str(time.utc_datetime()),
            "utc_timestamp": int(time.utc_datetime().timestamp()),
            "is_sunlit": bool(is_sunlit)
        }

    return full_pass

def serialize_pass_duration(pass_prediction):
    pass_duration = {
        "aos": pass_prediction['aos'],
        "los" : pass_prediction['los'],
        "duration" : str(pass_prediction['los'] - pass_prediction['aos'])
    }

    return pass_duration

@app.route('/get_satellite_position', methods=['POST'])
def get_satellite_position_route():
    data = request.json
    cat_num = data['catalog_number']
    catalog_number = int(data['catalog_number'])  # Get the catalog number from JSON data
    t = ts.now()
    satellite = satellite_dict[catalog_number]
    difference = satellite - bluffton
    topocentric = difference.at(t)
    el, az, distance= topocentric.altaz()

    if el.degrees > 0:
        print('The ISS is above the horizon')
   
    if satellite is None:
        return jsonify({
            'error': 'Satellite not found'
        })
    geocentric = satellite.at(t)
    lat, lon = wgs84.latlon_of(geocentric)
    height = wgs84.height_of(geocentric)
    speed = get_satellite_velocity(satellite)
    sunlit = is_satellite_sunlit(satellite)
    return jsonify({
        'lon': lon.degrees,
        'lat': lat.degrees,
        'az': az.degrees,
        'el': el.degrees,
        'speed': speed,
        'sunlit': bool(sunlit),
        'name': satellite.name,
        'catalog_number': cat_num
    })

@app.route('/get_pass_predictions', methods=['POST'])
def get_pass_predictions_route():
    data = request.json
    catalog_number = int(data['catalog_number'])
    min_elevation_deg = float(data['min_elevation'])
    days = data['days']
    start_time = ts.now()
    end_time = start_time + timedelta(days=days)
    observer_location = (observer_latitude, observer_longitude)
    pass_predictions = calculate_pass_predictions(catalog_number, observer_location, start_time, end_time, min_elevation_deg)
    return jsonify(pass_predictions)

@app.route('/calculate_passes', methods=['POST'])
def calculate_passes_route():
    data = request.json
    catalog_number = str(data['catalog_number'])
    days = data['days']
    full_tle = get_tle_by_catalog(catalog_number)
    passes_predicted = passes(station, ephem.readtle(full_tle[1], full_tle[0][0], full_tle[0][1]), epoch, 3)
    all_passes = []
    for i in passes_predicted:
        all_passes.append(serialize_pass_duration(i))
    return all_passes

@app.route('/get_position_chunk', methods=['POST'])
def get_position_chunk():
    data = request.json
    catalog_number = int(data['catalog_number'])
    coordinates = get_satellite_positions(catalog_number)
    return jsonify({
        'coordinates': coordinates
    })

def create_app():
    return app

orbit_propagation('25544')
get_positions()

if __name__ == '__main__':
    scheduler.add_job(id = 'TLE Update', func = update_tles, trigger="interval", hours = 23)
    # scheduler.add_job(id = 'Propagate Orbit', func = orbit_propagation, trigger="interval", hours = 23)
    scheduler.start()
    app.run(debug=True) 