from flask import Flask, request, jsonify
from flask_cors import CORS
from skyfield.api import Topos, load, EarthSatellite, wgs84
from datetime import datetime, timedelta
import pytz
from skyfield.api import load as skyfield_load
from more_itertools import chunked
import numpy as np
import math
import ephem
import time
import datetime as dt

app = Flask(__name__)
CORS(app)

station = ephem.Observer()
station.lat = '+31.7677'
station.long = '-106.4351'
station.elev = 0

epoch = dt.datetime.utcnow()
observer_latitude = 31.7677
observer_longitude = -106.4351

bluffton = wgs84.latlon(+31.7677, -106.4351)

# Fetch TLEs and store them in a dictionary
ts = load.timescale()
satellites = load.tle_file('https://www.celestrak.com/NORAD/elements/active.txt')
satellite_dict =  {sat.model.satnum: sat for sat in satellites}

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

def passes(station, satellite, start=None, duration=7):
    result = []
    if start is not None:
        station.date = ephem.date(start)
    end = ephem.date(station.date + duration)
    while station.date < end:
        t_aos, azr, t_max, elt, t_los, azs = station.next_pass(satellite)
        result.append({'aos': t_aos.datetime(), 'los': t_los.datetime()})
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
    return satellite.at(ts.now()).is_sunlit(skyfield_load("de421.bsp"))


def get_satellite_positions(catalog_number):
    t = ts.now()
    num_positions = 10
    satellite = satellite_dict[catalog_number]
    # print(satellite)
    difference = satellite - bluffton
    topocentric = difference.at(t)

    coordinates = []
    for _ in range(num_positions):
        t = ts.now()
        geocentric = satellite.at(t)
        lat, lon = wgs84.latlon_of(geocentric)
        coordinates.append((lat.degrees, lon.degrees))  # Append as a tuple
        # Increment the time for the next position
        time.sleep(.3)
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
        is_sunlit = geometric_sat.is_sunlit(skyfield_load("de421.bsp"))
        event = ('rise', 'culmination', 'set')[event_type]

        full_pass[event] = {
            "alt": f"{sat_alt.degrees:.2f}",
            "az": f"{sat_az.degrees:.2f}",
            "utc_datetime": str(time.utc_datetime()),
            "utc_timestamp": int(time.utc_datetime().timestamp()),
            "is_sunlit": bool(is_sunlit)
        }

    return full_pass

@app.route('/get_satellite_position', methods=['POST'])
def get_satellite_position_route():
    data = request.json
    cat_num = data['catalog_number']
    catalog_number = int(data['catalog_number'])  # Get the catalog number from JSON data
    t = ts.now()
    satellite = satellite_dict[catalog_number]
    # print(satellite)
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
    print(pass_predictions)
    return jsonify(pass_predictions)

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

if __name__ == '__main__':
    app.run(debug=True)