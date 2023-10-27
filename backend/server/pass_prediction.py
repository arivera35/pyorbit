import ephem
import datetime as dt
from sgp4.earth_gravity import wgs84
from sgp4.io import twoline2rv, verify_checksum, fix_checksum, compute_checksum

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

station = ephem.Observer()
station.lat = '+31.7677'
station.long = '-106.4351'
station.elev = 0

epoch = dt.datetime.utcnow()

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

catalog_number = input("Enter the catalog number: ")
tle = get_tle_by_catalog(catalog_number)

print(fix_checksum(tle[1]))
print(fix_checksum(tle[2]))
tle1_fixed = (fix_checksum(tle[1]), fix_checksum(tle[2]))

for i in passes(station, ephem.readtle("MOONLIGHTER (GENERATED)", tle1_fixed[0], tle1_fixed[1]), epoch, 3):
    print("AOS ", i['aos'], "   LOS ", i['los'], "   DURATION ", (i['los']-i['aos']))