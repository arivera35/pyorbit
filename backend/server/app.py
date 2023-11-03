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
import pytz

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
ts = load.timescale()
tz = pytz.timezone('UTC')  # Use UTC timezone
bsp = load("de421.bsp")

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

def get_satellite_velocity(satellite):
    t = ts.now()
    geocentric = satellite.at(t)
    velocity = geocentric.velocity.km_per_s  
    speed = np.linalg.norm(velocity)
    return speed

def is_satellite_sunlit(satellite):
    return satellite.at(ts.now()).is_sunlit(bsp)

def serialize_pass_duration(pass_prediction):
    pass_duration = {
        "aos": pass_prediction['aos'],
        "los" : pass_prediction['los'],
        "duration" : str(pass_prediction['los'] - pass_prediction['aos'])
    }

    return pass_duration

def orbit_propagation(catalog_numbers):
    start = datetime.now(tz=tz)
    end = start + timedelta(hours=1)
    delta = timedelta(seconds=60)
    time_series = {}
    now = start
    while now <= end:
        time_series[now] = {}
        for catalog_number in catalog_numbers:
            tle, satellite_name = get_tle_by_catalog(str(catalog_number))
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
                satellite_data.append({'el': el.degrees, 'az': az.degrees, 'lat': lat.degrees, 'lon': lon.degrees, 'alt': altitude.km, 'speed': np.linalg.norm(velocity), 'sunlit': str(sunlit), 'satellite_name': satellite_name})
                
                time_series[now][catalog_number] = satellite_data  # Use catalog_number as the identifier

        now += delta

    return time_series

def get_nearest_position(time_series, current_time):
    timestamps = list(time_series.keys())
    nearest_positions = {}
    for timestamp in timestamps:
        if current_time <= timestamp :
            break  # Stop searching if we've passed the current time
        nearest_positions = time_series[timestamp]

    return nearest_positions

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

@app.route('/get_access_windows', methods=['POST'])
def get_access_windows():
    data = request.json
    catalog_number = str(data['catalog_number'])
    days = data['days']
    full_tle = get_tle_by_catalog(catalog_number)
    passes_predicted = passes(station, ephem.readtle(full_tle[1], full_tle[0][0], full_tle[0][1]), epoch, 3)
    all_passes = []
    for i in passes_predicted:
        all_passes.append(serialize_pass_duration(i))
    return all_passes

@app.route('/get_satellite_orbit',  methods=['POST'])
def get_orbit():
    data = request.json
    catalog_numbers = []
    i = 0
    for catalog_number in data['catalog_numbers']:
        catalog_numbers.append(str(data['catalog_numbers'][i]))
        i = i + 1
    result = orbit_propagation(catalog_numbers)
    json_result = {str(timestamp): {catalog_number: position_data for catalog_number, position_data in satellite_data_dict.items()} for timestamp, satellite_data_dict in result.items()}
    return jsonify(json_result)

@app.route('/get_current_position_from_timeseries', methods=['POST'])
def get_current_position_from_timeseries():
    data = request.json
    catalog_numbers = []
    i = 0
    for catalog_number in data['catalog_numbers']:
        catalog_numbers.append(str(data['catalog_numbers'][i]))
        i = i + 1
    result = orbit_propagation(catalog_numbers)
    current_time = datetime.now(tz=timezone(timedelta(hours=0)))
    estimated_positions = get_nearest_position(result, current_time)
    
    return jsonify(estimated_positions)

@app.route('/get_position_from_timeseries', methods=['POST'])
def get_positions_at_specific_time():
    data = request.json
    specific_time_str = data['specific_time']
    specific_time = datetime.fromisoformat(specific_time_str)
    catalog_numbers = []
    i = 0
    for catalog_number in data['catalog_numbers']:
        catalog_numbers.append(str(data['catalog_numbers'][i]))
        i = i + 1
    result = orbit_propagation(catalog_numbers)
    estimated_positions = get_nearest_position(result, specific_time)
    return jsonify(estimated_positions)
    # if specific_time in result:
    #     positions_at_specific_time = result[specific_time]
    #     return jsonify(positions_at_specific_time)
    # else:
        # return jsonify({"error": "Positions not available for the specified time."})


def create_app():
    return app

if __name__ == '__main__':
    scheduler.add_job(id = 'TLE Update', func = update_tles, trigger="interval", hours = 12)
    scheduler.start()
    app.run(debug=True) 